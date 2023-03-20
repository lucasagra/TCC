# Demo
![gif](https://github.com/lucasagra/TCC/blob/main/entity_annotator_app/website-annotator.gif)

# Instructions
1 - Create a new directory for your project and navigate to it in the terminal.

2 - Create a new Python virtual environment by running the following command:

```
python -m venv env
```

This command will create a new directory called env in your project directory that will contain the Python virtual environment.

3 - Activate the virtual environment by running the following command:

```
source env/bin/activate
```

4 - Install Node.js and npm inside the virtual environment by running the following command:
```
sudo npm install -g n
n latest 
```

The n package is a Node.js version manager that allows you to easily switch between different Node.js versions. The n latest command installs the latest version of Node.js.

5 - Verify that Node.js and npm are installed by running the following commands:

```
node -v
npm -v
```

6 - Create a new Node.js project by following the steps in my previous answer.

7 - Install the required Node.js dependencies for your project by running the following command:

```
sudo npm install express body-parser fs --save
```

This command will install the Express web framework, the Body Parser middleware for parsing JSON data, and the fs module for reading and writing files, and add them as dependencies to your package.json file.

8 - Run the server using the following command:

```
node app.js
```

3.1 - Command to leave the virtual environment.

```
deactivate
```