from isaacsim.robot_motion.motion_generation.path_planning_interface import PathPlanner
import numpy as np
import csv
import ast
#import pandas as pd
class RRTStar(PathPlanner):
    def __init__(self, robot_description_path, urdf_path, rrt_config_path, end_effector_frame_name, cost_function=None):
        self.robot_description_path = robot_description_path
        self.urdf_path = urdf_path
        self.rrt_config_path = rrt_config_path
        self.end_effector_frame_name = end_effector_frame_name
        self.cost_function = cost_function if cost_function is not None else self.default_cost_function
        
    #params: ctive_joint_positions (np.array) – current positions of joints specified by get_active_joints()
    #watched_joint_positions (np.array) – current positions of joints specified by get_watched_joints()
    def compute_path(self, active_joint_positions, watched_joint_positions):
        # Beispielhafte Ladepfade (kannst du anpassen)
        path = np.load("C:\\Users\\volle\\Downloads\\joint_angles.npy") 
        ompl = np.load("C:\\Users\\volle\\Downloads\\ompl_angles.npy") 
        first = np.load("C:\\Users\\volle\\Downloads\\first_sol.npy")
        bp = np.array([[0.0423, 0.3303, -0.5652, -2.2751, -0.5282, 1.8924, -2.8707],
                    [0.1423, 0.3303, -0.5652, -2.2751, -0.5282, 1.8924, -2.8707],
                    [0.0423, 0.3303, -0.5652, -2.2751, -0.5282, 1.8924, -2.8707]])
        path_env3 = np.array([...])  # hier deinen langen Array weiterführen
        
        # CSV lesen und letzten Pfad extrahieren
        with open("C:\\Users\\volle\\Downloads\\ompl_results_env4\\run_summary_RRTstar.csv", "r") as f:
            reader = csv.DictReader(f)
            last_path_str = None
            for row in reader:
                if row["path"]:
                    last_path_str = row["path"]
        
        path_rrt = ast.literal_eval(last_path_str)  # String zu Liste/Array umwandeln
        path_rrt = np.array(path_rrt)
        return path_rrt

    def get_active_joints(self):
        return ["panda_joint1", "panda_joint2", "panda_joint3", "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"]

    def set_robot_base_pose(self, robot_position, robot_orientation):
        pass

    def set_max_iterations(self, max_iter: int):
        pass

    def set_random_seed(self, random_seed: int):
        pass

    def set_param(self, param_name: str, value):
        pass

    def default_cost_function(self, from_node, to_node):
        # Standardkostenfunktion (z. B. euklidische Distanz)
        return np.linalg.norm(to_node - from_node)

    
