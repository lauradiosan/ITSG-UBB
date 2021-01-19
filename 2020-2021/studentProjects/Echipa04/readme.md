# Pinguinii Galactici

# Automated Assistant for Bladder Tumor Segmentation

This repository contains the our proposed solution for the Automated Medical Assistant application.

## Backend

The Backend folder contains most of the files needed to run the server. The technologies used are Python (Flask) and SQL Server. 

### Run server locally

**Environment**

Install anaconda and Python3.8

Create a conda environment with the following packages installed: flask, libpng, numpy, opencv, pillow, pynrrd, pyodbc, pypng, scikit-image

Activate the conda environment

    conda activate {env-name}
	
If running the server gives you errors about missing libraries, run the commands

    pip install {missing-library}

**For the intelligent models to work:**

1. Download the Output zip from the following link https://we.tl/t-kCWuCmxl9x
2. Extract the folder in the Backend folder of the project
3. Download the detectron2 zip from the following link https://we.tl/t-n8N1P1up2t
4. Extract the 2 folders in the zip and copy them into the folder Backend/Models/Detectron2

**Database**

The Database folder contains files for creating the database tables, inserting some values, and dropping the tables, if need be. We used SQL Server and SQL Management Studio to create and handle the database.

You also need to modify the app/init.py file to connect to your specific SQL server.

**Start the server**

To start the server, in the Backend folder, run the commands

	set FLASK_APP=app.py

    flask run --host={your-ip}
	
## Frontend

### Project
This project was generated with Angular CLI version 9.1.4. Before starting the project, a `npm install` command is required. 

### Development server
Run `ng serve` for a dev server. Navigate to http://localhost:4200/. The app will automatically reload if you change any of the source files.

### Build
Run `ng build --aot --build-optimizer` to build the project. The build artifacts will be stored in the dist/ directory. Use the --prod flag for a production build.

### Project Structure 

All the components can be found in the `components` folder, each having its own scss, ts and html file. 
Pipes, services, models and images are located in the `shared` folder.
Server url can be changed from `environments`.
