# pocket_physics
A small project for visualizing orbital trajectories based on Newtonian mechanics. Currently under development, it could become educational one day?
The project is licensed under the GNU GPL V3 open source license, so feel free to modify and distribute your own version of this little tool, provided you also publish it under the GNU GPL V3 and mention me as the original author!
The GUI and widgets of this app are based on the PyQt5 library (see requirements.txt).


# Project architecture
The architecture of the project is pretty simple:

- Widgets/ folder contains the description of the different widgets (buttons, slide bars, etc...) used in the application.
- main.py is the main program, executing the GUI of the application and the animations.
- particle.py contains the particle class as well as its properties.
- requirements.txt contains the versions of the libraries used for running the application.

# Run the project
The project has been developped using python 3.11.1.
For running the project, you have to install the different libraries in requirements.txt with the following command:
```bash
pip install -r .\requirements.txt
```
Once the requirements are installed, just run main.py for using the application!
