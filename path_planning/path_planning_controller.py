# Copyright (c) 2020-2024, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

import os
from typing import Optional

import carb
import isaacsim.core.api.objects
import isaacsim.robot_motion.motion_generation.interface_config_loader as interface_config_loader
import numpy as np
import omni.kit
from isaacsim.core.api.controllers.base_controller import BaseController
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.types import ArticulationAction
from isaacsim.robot_motion.motion_generation import ArticulationTrajectory
from isaacsim.robot_motion.motion_generation.lula import RRT
from isaacsim.robot_motion.motion_generation.lula.trajectory_generator import LulaCSpaceTrajectoryGenerator
from isaacsim.robot_motion.motion_generation.path_planner_visualizer import PathPlannerVisualizer
from isaacsim.robot_motion.motion_generation.path_planning_interface import PathPlanner

from isaacsim.examples.interactive.path_planning.rrt_star import RRTStar

class PathPlannerController(BaseController):
    def __init__(
        self,
        name: str,
        path_planner_visualizer: PathPlannerVisualizer,
        cspace_trajectory_generator: LulaCSpaceTrajectoryGenerator,
        physics_dt=1 / 60.0,
        rrt_interpolation_max_dist=0.01,
    ):
        BaseController.__init__(self, name)

        self._robot = path_planner_visualizer.get_robot_articulation()

        self._cspace_trajectory_generator = cspace_trajectory_generator
        self._path_planner = path_planner_visualizer.get_path_planner()
        self._path_planner_visualizer = path_planner_visualizer

        self._last_solution = None
        self._action_sequence = None

        self._physics_dt = physics_dt
        self._rrt_interpolation_max_dist = rrt_interpolation_max_dist
      
        



    def _convert_rrt_plan_to_trajectory(self, rrt_plan):
        if rrt_plan is None or len(rrt_plan) <= 1:
            carb.log_warn("[PathPlannerController] RRT plan is invalid or too short.")
            return []

        interpolated_path = self._path_planner_visualizer.interpolate_path(rrt_plan, self._rrt_interpolation_max_dist)
        print("[Interpolated Path]", interpolated_path)

        trajectory = self._cspace_trajectory_generator.compute_c_space_trajectory(interpolated_path)
        print("[Trajectory]", trajectory)

        if trajectory is None:
            carb.log_warn("[PathPlannerController] Failed to generate trajectory from interpolated path.")
            return []

        art_trajectory = ArticulationTrajectory(self._robot, trajectory, self._physics_dt)
        return art_trajectory.get_action_sequence()


    def _make_new_plan(
        self, target_end_effector_position: np.ndarray, target_end_effector_orientation: Optional[np.ndarray] = None
    ) -> None:
        self._path_planner.set_end_effector_target(target_end_effector_position, target_end_effector_orientation)
        self._path_planner.update_world()

        path_planner_visualizer = PathPlannerVisualizer(self._robot, self._path_planner)
        active_joints = path_planner_visualizer.get_active_joints_subset()
        if self._last_solution is None:
            start_pos = active_joints.get_joint_positions()
        else:
            start_pos = self._last_solution

        self._path_planner.set_max_iterations(5000)
        self._rrt_plan = self._path_planner.compute_path(start_pos, np.array([]))
        print(self._rrt_plan)
        if self._rrt_plan is None or len(self._rrt_plan) <= 1:
            carb.log_warn("No plan could be generated to target pose: " + str(target_end_effector_position))
            self._action_sequence = []
            return

        print(len(self._rrt_plan))

        self._action_sequence = self._convert_rrt_plan_to_trajectory(self._rrt_plan)
        self._last_solution = self._action_sequence[-1].joint_positions

    def forward(
        self, target_end_effector_position: np.ndarray, target_end_effector_orientation: Optional[np.ndarray] = None
    ) -> ArticulationAction:
        if self._action_sequence is None:
            if not hasattr(self, "_gripper_opened") or not self._gripper_opened:
                self._gripper_opened = True
                return self.open_gripper_action()
            # This will only happen the first time the forward function is used
            self._make_new_plan(target_end_effector_position, target_end_effector_orientation)

        if len(self._action_sequence) == 0:
            # The plan is completed; return null action to remain in place 
            return ArticulationAction()

        if len(self._action_sequence) == 1:
            return self.close_gripper_action()
            

        return self._action_sequence.pop(0)
    
    def open_gripper_action(self):
        # Gripper ganz öffnen (Standard bei Franka: max ca. 0.04)
        gripper_opening = 0.04
        finger_positions = np.array([gripper_opening, gripper_opening])
        finger_velocities = np.zeros(2)
        finger_indices = [self._robot.get_dof_index("panda_finger_joint1"),
                        self._robot.get_dof_index("panda_finger_joint2")]

        return ArticulationAction(
            joint_positions=finger_positions,
            joint_velocities=finger_velocities,
            joint_indices=finger_indices
        )
    
    def close_gripper_action(self):
        gripper_closing = 0.02  # Zielposition (geschlossen)
        finger_positions = np.array([gripper_closing, gripper_closing])
        finger_velocities = np.zeros(2)
        finger_indices = [
            self._robot.get_dof_index("panda_finger_joint1"),
            self._robot.get_dof_index("panda_finger_joint2"),
        ]

        # Maximal zulässige Kraft in N
        max_efforts = np.array([100.0, 100.0])

        return ArticulationAction(
            joint_positions=finger_positions,
            joint_velocities=finger_velocities,
            joint_indices=finger_indices,
            #joint_efforts=max_efforts
        )


    def add_obstacle(self, obstacle: isaacsim.core.api.objects, static: bool = False) -> None:
        self._path_planner.add_obstacle(obstacle, static)

    def remove_obstacle(self, obstacle: isaacsim.core.api.objects) -> None:
        self._path_planner.remove_obstacle(obstacle)

    def reset(self) -> None:
        # PathPlannerController will make one plan per reset
        self._path_planner.reset()
        self._action_sequence = None
        self._last_solution = None

    def get_path_planner(self) -> PathPlanner:
        return self._path_planner


class FrankaRrtController(PathPlannerController):
    def __init__(
        self,
        name,
        robot_articulation: SingleArticulation,
    ):
        ext_manager = omni.kit.app.get_app().get_extension_manager()
        ext_id = ext_manager.get_enabled_extension_id("isaacsim.examples.interactive")
        examples_extension_path = ext_manager.get_extension_path(ext_id)

        # Load default RRT config files stored in the isaacsim.robot_motion.motion_generation extension
        rrt_config = interface_config_loader.load_supported_path_planner_config("Franka", "RRT")

        # Replace the default robot description file with a copy that has inflated collision spheres
        rrt_config["robot_description_path"] = os.path.join(
            examples_extension_path,
            "isaacsim",
            "examples",
            "interactive",
            "path_planning",
            "path_planning_example_assets",
            "franka_conservative_spheres_robot_description.yaml",
        )
        rrt = RRTStar(**rrt_config)
        #rrt = RRT(**rrt_config)
        # Create a trajectory generator to convert RRT cspace waypoints to trajectories
        cspace_trajectory_generator = LulaCSpaceTrajectoryGenerator(
            rrt_config["robot_description_path"], rrt_config["urdf_path"]
        )

        # It is important that the Robot Description File includes optional Jerk and Acceleration limits so that the generated trajectory
        # can be followed closely by the simulated robot Articulation
        
        for i in range(len(rrt.get_active_joints())):
            assert cspace_trajectory_generator._lula_kinematics.has_c_space_acceleration_limit(i)
            assert cspace_trajectory_generator._lula_kinematics.has_c_space_jerk_limit(i)

        visualizer = PathPlannerVisualizer(robot_articulation, rrt)

        PathPlannerController.__init__(self, name, visualizer, cspace_trajectory_generator)

    
