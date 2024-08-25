import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow, QLabel, QSizePolicy, QPushButton, QVBoxLayout
from qtmodern import styles
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from Widgets.custom_combo_box import custom_combo_box
from Widgets.custom_slider import custom_slider_bar
from particle import Particle


class ParticleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Pocket physics V1.0')
        self.resize(800, 600) 

        """Widgets of the application"""
        self.slider_bodies = custom_slider_bar(min=1, max=5, default_value=3, tickInterval=1)               # slider for the number of particles
        self.slider_bodies.valueChanged.connect(self.on_slider_value_changed)                               # connect the signal to the slot
        self.label_bodies = QLabel(str(self.slider_bodies.value()))                                         # label for the number of particles

        self.slider_time_scale =custom_slider_bar(min=1, max=100, default_value=1, tickInterval=1)          # slider for the time scale
        self.slider_time_scale.valueChanged.connect(self.on_slider_time_scale_changed)                      # connect the signal to the slot
        self.label_time_scale = QLabel(str(self.slider_time_scale.value()))                                 # label for the time sc
        menu_scenarios = ["None", "3-bodies problem", "Stable orbit", "Black hole", "Comet perturbation"]   # menu for the scenarios

        self.combo_scenarios = custom_combo_box(menu_scenarios)                                             # combo box for the scenarios
        self.combo_scenarios.currentIndexChanged.connect(self.set_scenario)                                 # connect the signal to the slot

        self.button_start = QPushButton("Start simulation")                                                 # button to start the simulation
        self.button_start.clicked.connect(self.play_simulation)                                             # connect the signal to the slot

        self.button_stop = QPushButton("Stop simulation")                                                   # button to stop the simulation
        self.button_stop.clicked.connect(self.stop_simulation)                                              # connect the signal to the slot
        
        self.spacer = QWidget()                                                                             # spacer for the top bar
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        """Layouts of the application"""
        self.widget_top_bar = QWidget()
        self.layout_top_bar = QGridLayout(self.widget_top_bar)
        self.layout_top_bar.setContentsMargins(0, 0, 0, 0)
        self.layout_top_bar.addWidget(QLabel("Bodies:"),        0, 0, 1, 1)
        self.layout_top_bar.addWidget(self.slider_bodies,       0, 1, 1, 1)
        self.layout_top_bar.addWidget(self.label_bodies,        0, 2, 1, 1)

        self.layout_top_bar.addWidget(QLabel("Time scale:"),    1, 0, 1, 1)
        self.layout_top_bar.addWidget(self.slider_time_scale,   1, 1, 1, 1)
        self.layout_top_bar.addWidget(self.label_time_scale,    1, 2, 1, 1)

        self.layout_top_bar.addWidget(QLabel("Scenario:"),      2, 0, 1, 1)
        self.layout_top_bar.addWidget(self.combo_scenarios,     2, 1, 1, 1)
        
        self.layout_top_bar.addWidget(self.button_start,        0, 3, 1, 1)
        self.layout_top_bar.addWidget(self.button_stop,         1, 3, 1, 1)

        self.layout_top_bar.addWidget(self.spacer,              3, 0, 1, 4)

        # Simulation area
        self.widget_simulation = QWidget()
        self.widget_simulation.setStyleSheet("background-color: darkgrey; border-radius: 5px;")
        self.layout_simulation = QVBoxLayout(self.widget_simulation)
        self.layout_simulation.setContentsMargins(0, 0, 0, 0)

        # Main Layout of the application
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        lay = QGridLayout(main_widget)

        lay.addWidget(self.widget_top_bar, 0, 0, 1, 1)
        lay.addWidget(self.widget_simulation, 1, 0, 1, 1)


    def on_slider_value_changed(self):
        """ Slot for the slider value changed signal """
        self.label_bodies.setText(str(self.slider_bodies.value()))

    def on_slider_time_scale_changed(self):
        """ Slot for the slider time scale changed signal """
        self.label_time_scale.setText(str(self.slider_time_scale.value()))

    def stop_simulation(self):
        """ Stop the simulation """
        # if animation is running, stop it
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
            # clear the simulation area
            for i in reversed(range(self.layout_simulation.count())):
                widget_to_remove = self.layout_simulation.itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)

    def set_scenario(self):
        """ Set the scenario of the simulation """
        time_scale = self.slider_time_scale.value()                                                                     # get the time scale
        n_particles = self.slider_bodies.value()                                                                        # get the number of particles
        # check for the selected scenario
        scenario = self.combo_scenarios.currentText()
        if scenario == "None":
            particles = []                                                                                                  # Reset particles
            cmap = cm.get_cmap('winter')
            for i in range(n_particles):
                x = np.random.randint(-10, 10)
                y = np.random.randint(-10, 10)
                vx = np.random.uniform(-0.5, 0.5)
                vy = np.random.uniform(-0.5, 0.5)
                m = np.random.randint(100000000, 500000000)
                p = Particle(x, y, vx, vy, m, time_scale)
                particles.append(p)
            self.slider_bodies.setEnabled(True)
            self.slider_time_scale.setEnabled(True)
            return particles, cmap

        elif scenario == "3-bodies problem":
            self.slider_bodies.setValue(3)
            self.slider_time_scale.setValue(10)
            self.label_bodies.setText(str(3))
            self.slider_bodies.setEnabled(False)
            self.slider_time_scale.setEnabled(False)
            cmap = cm.get_cmap('winter')
            particles = [Particle(0, 2, 0, -0.15, 2000000, time_scale),
                            Particle(2, 0, -0.02, -0.25, 3000000, time_scale),
                            Particle(-2, 0, 0.06, -0.18, 2500000, time_scale)]
            return particles, cmap

        elif scenario == "Stable orbit":
            self.slider_bodies.setValue(2)
            self.label_bodies.setText(str(2))
            self.slider_time_scale.setValue(23)
            self.label_time_scale.setText(str(23))
            cmap = cm.get_cmap('winter')
            particles = [Particle(0, 0, 0, 0, 100000000, time_scale),
                         Particle(2.5, 0, -0.01, -0.35, 200, time_scale)]
            self.slider_bodies.setEnabled(False)
            self.slider_time_scale.setEnabled(False)
            return particles, cmap

        elif scenario == "Black hole":
            self.slider_bodies.setValue(2)
            self.label_bodies.setText(str(2))
            self.slider_time_scale.setValue(25)
            self.label_time_scale.setText(str(25))
            cmap = cm.get_cmap('plasma_r')
            particles = [Particle(0, 0, 0, 0, 100000000, time_scale),
                         Particle(3, 3, 0.1, -0.1, 200, time_scale)]
            self.slider_bodies.setEnabled(False)
            self.slider_time_scale.setEnabled(False)
            return particles, cmap

        elif scenario == "Comet perturbation":
            self.slider_bodies.setValue(2)
            self.label_bodies.setText(str(2))
            self.slider_time_scale.setValue(25)
            self.label_time_scale.setText(str(25))
            cmap = cm.get_cmap('winter')
            particles = [Particle(0, 0, 0, 0, 100000000, time_scale),
                         Particle(2.5, 0, -0.01, -0.35, 2000, time_scale),
                         Particle(25, 25, -0.15, -0.1, 20, time_scale)]
            self.slider_bodies.setEnabled(False)
            self.slider_time_scale.setEnabled(False)           
            return particles, cmap

    def play_simulation(self):
        """ Play the simulation """
        self.stop_simulation()                                                                                          # reset the simulation
        particles, cmap = self.set_scenario()                                                                           # get the particles and colormap

        fig, ax = plt.subplots()                                                                                        # Create the figure and axis 
        fig.patch.set_facecolor((45/255, 45/255, 45/255))
        ax.set_facecolor((10/255, 11/255, 17/255))

        canvas = FigureCanvas(fig)                                                                                      # Create the canvas for the figure
        self.layout_simulation.addWidget(canvas)
        
        masses = np.array([p.m for p in particles])                                                                     # Extract the masses of the particles for the colormap
        norm = mcolors.Normalize(vmin=masses.min(), vmax=masses.max())
        
        
        particle_trajectories = {i: {'x': [], 'y': []} for i in range(len(particles))}                                  # Store the previous positions of the particles

        def update(frame, particles):                                                                                         
            temp_particles = []                                                                                         # Compute the new position of the particles
            for idx, p in enumerate(particles):
                p.compute_new_position(particles)
                temp_particles.append(Particle(p.x, p.y, p.vx, p.vy, p.m, p.time_scale))
                particle_trajectories[idx]['x'].append(p.x)                                                             # Save the new positions to plot the trajectory
                particle_trajectories[idx]['y'].append(p.y)
            particles[:] = temp_particles

            ax.clear()                                                                                                  # Erase the previous frame
            ax.set_facecolor((10/255, 11/255, 17/255))
            
            all_x = [p.x for p in particles]                                                                            # Adjust the limits of the plot
            all_y = [p.y for p in particles]
            ax.set_xlim(min(all_x) - 10, max(all_x) + 10)
            ax.set_ylim(min(all_y) - 10, max(all_y) + 10)

            masses = np.array([p.m for p in particles])                                                                 # Extract the masses of the particles for the colormap
            colors = cmap(norm(masses))

            ax.scatter([p.x for p in particles], [p.y for p in particles], c=colors, s=40, edgecolor='none')            # Replot the particles

            for idx in range(len(particles)):                                                                           # Plot the trajectories
                ax.plot(particle_trajectories[idx]['x'], particle_trajectories[idx]['y'], color=colors[idx], alpha=0.3)

            ax.grid(True, color=((17/255, 32/255, 30/255)), linewidth=0.3)                                              # Add grid to the plot
            return ax,

        self.ani = FuncAnimation(fig, update, frames=5000, fargs=(particles,), interval=10, blit=False)                 # Store the animation object as an instance attribute to prevent garbage collection
        canvas.draw()







if __name__ == "__main__":
    app = QApplication(sys.argv)
    styles.dark(app)
    window = ParticleEditor()
    window.show()
    sys.exit(app.exec_())
