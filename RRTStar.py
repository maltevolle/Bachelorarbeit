from isaacsim.robot_motion.motion_generation.path_planning_interface import PathPlanner

class RRTStar(LulaInterfaceHelper, PathPlanner):
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
            [ 0.0, -0.5,  0.3, -1.0, 0.5,  1.2, 0.0],  # Start
            [ 0.1, -0.4,  0.4, -0.9, 0.6,  1.1, 0.1],
            [ 0.2, -0.3,  0.5, -0.8, 0.7,  1.0, 0.2],
            [ 0.3, -0.2,  0.6, -0.7, 0.8,  0.9, 0.3],
            [ 0.4, -0.1,  0.7, -0.6, 0.9,  0.8, 0.4],  # Ziel
        ])
        return beispielpath

    def set_robot_base_pose(robot_position: array, robot_orientation: array):
        pass

    def set_max_iterations(max_iter: int):
        pass

    def set_random_seed(random_seed: int):
        pass

    def set_param(param_name: str, value: array | float | int | str):
        pass

    def default_cost_function(self, from_node, to_node):
        # Standardkostenfunktion (z. B. euklidische Distanz)
        return np.linalg.norm(to_node - from_node)

    
