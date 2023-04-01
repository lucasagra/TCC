const express = require("express");
const fs = require("fs");
const bodyParser = require("body-parser");
const path = require('path');

const app = express();
app.use(bodyParser.json());

const documentsFile = "./documents.json";

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/style.css', (req, res) => {
res.sendFile(path.join(__dirname, 'style.css'));
});

app.get('/script.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'script.js'));
});

app.get('/documents.json', (req, res) => {
    res.sendFile(path.join(__dirname, documentsFile));
});

app.get('/entities.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'entities.json'));
});

// Define route to retrieve a specific document.
app.get('/documents/:id', async (req, res) => {
    const id = req.params.id;
    const documents = JSON.parse(await fs.readFileSync(documentsFile));
    const document = documents.find(doc => doc.id === id);
  
    if (!document) {
      return res.status(404).send('Document not found');
    }
  
    res.json(document);
  });

// Define route to check if a document is done.
app.post("/check", async (req, res) => {
    const { documentIndex, isChecked } = req.body;
    try {
        const documents = JSON.parse(fs.readFileSync(documentsFile));
        const doc = documents[documentIndex];
        doc.isDone = isChecked;
        fs.writeFileSync(documentsFile, JSON.stringify(documents, null, 2), { flag: 'w' });
        res.status(200).send("Document checked.");
    } catch (error) {
        console.error(error);
        res.status(500).send("Error checking document.");
    }
});

// Define a route to save changes on a document.
app.post("/save", async (req, res) => {
    const { documentIndex, report } = req.body;
    try {
        const documents = JSON.parse(fs.readFileSync(documentsFile));
        const doc = documents[documentIndex];
        doc.report = report;
        fs.writeFileSync(documentsFile, JSON.stringify(documents, null, 2));
        res.status(200).send("Annotation saved.");
    } catch (error) {
        console.error(error);
        res.status(500).send("Error saving annotation.");
    }
});

app.listen(3000, () => {
    console.log("Server listening on port 3000");
});
