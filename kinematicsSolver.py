
from omni.isaac.motion_generation import KinematicsSolver


import numpy as np

stage = omni.usd.get_context().get_stage()

# 3. KinematicsSolver erstellen
ik_solver = KinematicsSolver()

# 4. Beispiel-TCP-Pose
target_pos = np.array([0.5, 0.0, 0.5])
target_quat = np.array([0.0, 0.0, 0.0, 1.0])

# 5. IK anwenden
success, joint_positions = ik_solver.compute_inverse_kinematics(
    frame_name="panda_hand",  # <- oder was dein TCP ist
    target_positions=np.array([0.5, 0.0, 0.5]),  # Muss ein NumPy-Array sein!
    target_orientation=np.array([0.0, 0.0, 0.0, 1.0]),  # Quaternion
    warm_start=None,
    position_tolerance= None,
    orientation_tolerance= None
)

if success:
    print(f" IK erfolgreich. Gelenkwinkel: {joint_positions}")
    
else:
    print("IK fehlgeschlagen")
