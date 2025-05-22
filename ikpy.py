import numpy as np
from ikpy.chain import Chain
from ikpy.link import URDFLink

panda_chain = Chain(name='panda_arm', links=[
    URDFLink(
        name="link1",
        origin_translation=np.array([0, 0, 0.333]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([0, 0, 1]),
    ),
    URDFLink(
        name="link2",
        origin_translation=np.array([0, 0, 0]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([0, 1, 0]),
    ),
    URDFLink(
        name="link3",
        origin_translation=np.array([0, 0, 0.316]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([0, 1, 0]),
    ),
    URDFLink(
        name="link4",
        origin_translation=np.array([0, 0, 0]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([0, 1, 0]),
    ),
    URDFLink(
        name="link5",
        origin_translation=np.array([0, 0, 0.384]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([1, 0, 0]),
    ),
    URDFLink(
        name="link6",
        origin_translation=np.array([0, 0, 0]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([0, 1, 0]),
    ),
    URDFLink(
        name="link7",
        origin_translation=np.array([0, 0, 0.107]),
        origin_orientation=np.array([0, 0, 0]),
        rotation=np.array([1, 0, 0]),
    ),
])

target_position = [0.5, 0.0, 0.4]

target_frame = np.eye(4)
target_frame[:3, 3] = target_position

initial_position = [0] * 7

angles = panda_chain.inverse_kinematics_frame(target_frame, initial_position=initial_position)


min_pos = np.array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])
max_pos = np.array([ 2.8973,  1.7628,  2.8973, -0.0698,  2.8973,  3.7525,  2.8973])

# Clipping
angles_clipped = np.clip(angles, min_pos, max_pos)

print("Begrenzte Winkel:", angles_clipped)


print("Gelenkwinkel (Radiant):", angles)
print("Gelenkwinkel (Grad):", np.degrees(angles))
