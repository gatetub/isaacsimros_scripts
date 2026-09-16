"""Retune every revolute joint drive on the loaded stage.

Run inside Isaac Sim: Window -> Script Editor, paste this file's contents (or
exec it), then press Play. Drive gains are latched when the simulation starts,
so press Stop first if the timeline is already running.

The USD ships with force-mode drives around stiffness 5 N-m/rad, which cannot
hold an 11.6 kg arm against gravity (that needs ~23 N-m), let alone track a
command. Switching to acceleration mode normalises the gain by each joint's
effective inertia, so a single pair of values works for both a 2.5 kg upper arm
link and a 0.02 kg finger.

These are SIMULATION tuning values. They are not properties of the real robot
and must not be carried over to hardware.
"""

from collections import Counter

import omni.usd
from pxr import UsdPhysics

DRIVE_TYPE = "acceleration"
STIFFNESS = 1000.0
DAMPING = 100.0

# Only touch the robot the ActionGraph actually commands. A stray URDF import
# lands at /north_poc2_2_with_double_continental_grip_description and must be
# deleted, not retuned -- it interpenetrates the real robot and jams it.
ROBOT_ROOT = "/North_Poc2_2_V3_1"


def main() -> None:
    stage = omni.usd.get_context().get_stage()

    roots = [p.GetPath().pathString for p in stage.GetPseudoRoot().GetChildren()]
    print(f"stage roots: {roots}")
    if any("continental_grip_description" in r for r in roots):
        print("WARNING: a duplicate URDF robot is in the stage -- delete it first:")
        print('  stage.RemovePrim("/north_poc2_2_with_double_continental_grip_description")')

    retuned = 0
    skipped = Counter()
    for prim in stage.Traverse():
        if not prim.IsA(UsdPhysics.RevoluteJoint):
            continue
        path = prim.GetPath().pathString
        if not path.startswith(ROBOT_ROOT + "/"):
            skipped[path.split("/")[1]] += 1
            continue
        drive = UsdPhysics.DriveAPI.Get(prim, "angular")
        if not drive:
            continue
        drive.CreateTypeAttr().Set(DRIVE_TYPE)
        drive.CreateStiffnessAttr().Set(STIFFNESS)
        drive.CreateDampingAttr().Set(DAMPING)
        retuned += 1

    print(f"retuned {retuned} drives under {ROBOT_ROOT} "
          f"(type={DRIVE_TYPE} stiffness={STIFFNESS} damping={DAMPING})")
    for root, n in skipped.items():
        print(f"  skipped {n} joints under /{root}")
    if retuned != 65:
        print(f"NOTE: expected 65, got {retuned} -- check the stage tree")


main()
