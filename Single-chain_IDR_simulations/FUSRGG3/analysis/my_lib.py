import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

# What i want to do is, you put you MDAnalysis universe and the frame of you need conatct map

# in cross grained model each residue is represented by its alpha carbon

class Analysis:

    def __init__(self, universe) -> None:
        self.universe = universe
        self.current_frame = None
        self.num_beads = self.universe.atoms.n_atoms

    def set_frame(self, frame) -> bool:

        if frame == None:
            self.current_frame = frame

            return True

        self.universe.trajectory[frame]

        self.current_frame = frame

        return True

    def _calc_distance(self, bead_i, bead_j) -> float:
    
        positioni = bead_i.position
        positionj = bead_j.position

        diff = positioni - positionj

        dist = np.linalg.norm(diff)
        
        return float(dist)

    def genrate_contact_map(self) -> None:
        
        if self.current_frame != None:
            dist_matrix = np.zeros((self.num_beads, self.num_beads))

            for i in range(self.num_beads):
                for j in range(self.num_beads):
                    bead_i = self.universe.atoms[i]
                    bead_j = self.universe.atoms[j]

                    dist = self._calc_distance(bead_i, bead_j)

                    dist_matrix[i, j] = dist/10 # to convert Ang to nm
            
            plt.imshow(dist_matrix, cmap='viridis', interpolation='nearest')
            plt.colorbar()
            plt.gca().invert_yaxis()
            plt.xlabel("Residue")
            plt.ylabel("Residue")
            plt.title(f"Distance between residues (nm). frame: {self.current_frame}/{len(self.universe.trajectory)}")
            plt.show()

        else:
            fig, ax = plt.subplots(figsize=(8,6))

            dist_matrix = np.zeros((self.num_beads, self.num_beads))

            for i in range(self.num_beads):
                for j in range(self.num_beads):
                    bead_i = self.universe.atoms[i]
                    bead_j = self.universe.atoms[j]

                    dist = self._calc_distance(bead_i, bead_j)

                    dist_matrix[i, j] = dist/10 # to convert Ang to nm

            contact_map = plt.imshow(dist_matrix, cmap='viridis', interpolation='nearest')
            plt.gca().invert_yaxis()
            plt.xlabel("Residue")
            plt.ylabel("Residue")


            def update(frame):
                self.universe.trajectory[frame]

                dist_matrix = np.zeros((self.num_beads, self.num_beads))

                for i in range(self.num_beads):
                    for j in range(self.num_beads):
                        bead_i = self.universe.atoms[i]
                        bead_j = self.universe.atoms[j]

                        dist = self._calc_distance(bead_i, bead_j)

                        dist_matrix[i, j] = dist/10 # to convert Ang to nm

                time = self.universe.trajectory.time
                ax.clear()
                plt.imshow(dist_matrix, cmap='viridis', interpolation='nearest')
                plt.gca().invert_yaxis()
                plt.xlabel("Residue")
                plt.ylabel("Residue")
                ax.set_title(f"frame {frame}")
                return ax.collections
            
            ani = FuncAnimation(fig, update, frames=len(self.universe.trajectory[1:]), interval=100)
            ani.save("contact_map.mp4")
            plt.show()    
    
    def plot_radius_of_gyration(self) -> None:

        time = []
        rgyr = []
        
        for ts in self.universe.trajectory:
            time.append(self.universe.trajectory.time)
            rgyr.append(self.universe.atoms.radius_of_gyration())

        plt.plot(time, np.array(rgyr)/10)
        plt.xlabel(f"time (ps)")
        plt.ylabel("Radius of Gyration (nm)")
        plt.show()

    def probability_rgyr(self) ->  None:
        rgyr = []
        
        for ts in self.universe.trajectory:
            rgyr.append(self.universe.atoms.radius_of_gyration())
        
        sns.kdeplot(np.array(rgyr)/10)
        plt.ylabel("p(r)")
        plt.xlabel("radius of gyration (nm)")
        plt.show()

