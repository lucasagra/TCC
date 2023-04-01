let currentDoc = null;
let selectedEntity = null;
let statefulStack = {}
let selectedListItem = null;


function configureCheckbox(doc, index) {
	const checkbox = document.createElement("input");
	checkbox.type = "checkbox";
	checkbox.style.float = "right"; // move checkbox to the right side
	checkbox.checked = (doc.isDone === true || doc.isDone === 'true');
	checkbox.addEventListener("change", function() {
		return new Promise((resolve, reject) => {
			fetch('/check', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					documentIndex : index,
					isChecked: this.checked
				})
			}) 
			.then(response => {
				if (response.ok) {
					if (this.checked) console.log("Successfully checked.");
					else console.log("Successfully unchecked.");
					resolve(); // resolve the promise
				} else {
					console.log("Something went wrong.");
					reject(); // reject the promise
				}
			})
			.catch(error => {
				console.log(error);
				reject(error); // reject the promise
			});
		});
	});
		
	return checkbox;
}


function configureListItem(doc, index) {
	const listItem = document.createElement("li");
	listItem.innerText = `Report ${doc.id}`;
	const checkbox = configureCheckbox(doc, index);
	listItem.appendChild(checkbox);
	listItem.addEventListener("click", () => {
		fetch(`/documents/${doc.id}`)
			.then(response => {
				if (response.ok) {
					return response.json();
				}
				throw new Error('Network response was not ok');
			})
			.then(response => {
				documentViewer.innerText = response.report;
				currentDoc = {...response, index: index};
				if (selectedListItem != null) {
					selectedListItem.classList.remove("selected");
				}
				listItem.classList.add("selected");
				selectedListItem = listItem;
				if (currentDoc != null && statefulStack[currentDoc.id].length > 0) {
					undoButton.disabled = false;
				} else {
					undoButton.disabled = true;
				}
			})
			.catch(error => {
				console.error('Error:', error);
			});
	});
	return listItem;
}

// Load documents from json file.
fetch("documents.json")
	.then(response => response.json())
	.then(data => {
		const documentList = document.getElementById("documentList");
		data.forEach((doc, index) => {
			statefulStack[doc.id] = []
			const listItem = configureListItem(doc, index);
			documentList.appendChild(listItem);
		});
	});

// Load entities from json file.
fetch("./entities.json")
	.then(response => response.json())
	.then(data => {
		const entitySelector = document.getElementById("entities");
		selectedEntity = data[0];
		data.forEach(entity => {
			const option = document.createElement("option");
			option.value = entity;
			option.innerText = entity;
			entitySelector.appendChild(option);
		});
	});

// Listen for Entity selection.
const entitySelector = document.getElementById("entities");
entitySelector.addEventListener("change", () => {
	selectedEntity = entitySelector.value;
});

let selectedRange = null;
// listen for text selection.
documentViewer.addEventListener("mouseup", () => {
	selectedRange = window.getSelection().getRangeAt(0);
	// Enable button if there's something highlighted.
	if (selectedRange.endOffset - selectedRange.startOffset > 0) {
		submitButton.disabled = false;
	} else {
		submitButton.disabled = true;
	}
});

// Listen for submit button click.
const submitButton = document.getElementById("submitButton");
submitButton.addEventListener("click", () => {
	if (!submitButton.disabled) {
		// Save last state.
		statefulStack[currentDoc.id].push(currentDoc.report);

		// Update HTML.
		const selectedText = selectedRange.toString();
		const entityText = `[${selectedEntity}](${selectedText})`;
		selectedRange.deleteContents();
		selectedRange.insertNode(document.createTextNode(entityText));
		selectedRange.collapse();
		selectedRange = null;

		// Update current state with HTML text.
		currentDoc.report = document.getElementById("documentViewer").textContent;	

		submitButton.disabled = true
		
		new Promise((resolve, reject) => {
			fetch('/save', {
				method: 'POST',
				headers: {
				  'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					documentIndex: currentDoc.index,
					report: currentDoc.report
				})
			  }) 
			  .then(response => {
				if (response.ok) {			
					if (statefulStack[currentDoc.id].length > 0) { 
						undoButton.disabled = false; 
					}	
					console.log("Successfully saved doc.")
					resolve()
				} else {
					const lastState = statefulStack[currentDoc.id].pop();	
					// Undo html changes replacing with last saved state.
					document.getElementById("documentViewer").textContent = lastState;
					// Replace current state with last saved state.
					currentDoc.report = lastState;
					console.log("Something went wrong.")
					reject()
				}
			  })
			  .catch(error => {
				console.log(error)
				reject(error)
			  });
		});
	}
});

// Listen for undo button click.
const undoButton = document.getElementById("undoButton");
undoButton.addEventListener("click", () => {
	// Update current state with last state.
	currentDoc.report = statefulStack[currentDoc.id].pop()
	new Promise((resolve, reject) => {
		fetch('/save', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				documentIndex: currentDoc.index,
				report: currentDoc.report
			})
		}) 
		.then(response => {
			if (response.ok) {
				// Update html with last state.
				document.getElementById("documentViewer").textContent = currentDoc.report;
				console.log("Successfully saved doc.")
				resolve()
			} else {
				// Save last state back into the stack.
				statefulStack[currentDoc.id].push(currentDoc.report)
				console.log("Something went wrong.")
				reject()
			}
		})
		.catch(error => {
			console.log(error)
			reject(error)
		});
	});
	// Disable undo button if there isn't any saved state.
	if (statefulStack[currentDoc.id].length <= 0) undoButton.disabled = true;
});