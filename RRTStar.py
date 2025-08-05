from isaacsim.robot_motion.motion_generation.path_planning_interface import PathPlanner

class Planner(LulaInterfaceHelper, PathPlanner):
    def __init__(self, robot_description_path, urdf_path, rrt_config_path, end_effector_frame_name, cost_function=None):
        self.robot_description_path = robot_description_path
        self.urdf_path = urdf_path
        self.rrt_config_path = rrt_config_path
        self.end_effector_frame_name = end_effector_frame_name
        self.cost_function = cost_function if cost_function is not None else self.default_cost_function
        
    #params: ctive_joint_positions (np.array) – current positions of joints specified by get_active_joints()
    #watched_joint_positions (np.array) – current positions of joints specified by get_watched_joints()
    def compute_path(active_joint_positions, watched_joint_positions):
        # if self.target_not_defined():
        #     return None
        beispielpath = np.array([
            [0.000, 1.571, 0.050, 0.000, 0.000, 0.010, 0.2],  # Start
            [0.808, 0.570, 0.047, 0.010, 0.011, 0.009, 0.2],
            [0.805, 0.179, 0.038, 0.029, 0.030, 0.008, 0.2],
            [0.758, 0.047, 0.017, 0.054, 0.051, 0.003, 0.2],
            [0.760, 0.112, 0.053, 0.069, 0.065, 0.011, 0.2],
            [0.791, 0.195, 0.106, 0.076, 0.076, 0.021, 0.2],
            [0.784, 0.314, 0.201, 0.088, 0.087, 0.040, 0.2],
            [0.785, 0.377, 0.259, 0.093, 0.092, 0.052, 0.2],
            [0.785, 0.460, 0.350, 0.100, 0.100, 0.070, 0.2]  # Ziel
        ])
        return beispielpath

    def set_robot_base_pose(self, robot_position: array, robot_orientation: array):
        pass

    def set_max_iterations(self, max_iter: int):
         self.max_iter = max_iter

    def set_random_seed(self, random_seed: int):
        pass

    def set_param(self, param_name: str, value: array | float | int | str):
        pass

    def default_cost_function(self, from_node, to_node):
        # Standardkostenfunktion (z. B. euklidische Distanz)
        return np.linalg.norm(to_node - from_node)

    
