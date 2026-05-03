# =============================================================================
# Initialize.py
# =============================================================================
#
# Course    : EE6201 - Power Systems Lab
# Institute : Indian Institute of Technology Hyderabad (IIT Hyderabad)
# Semester  : Spring 2026
# Assignment: Assignment 11
# Instructor: V. Seshadri Sravan Kumar, Dept. of Electrical Engineering
#
# Note      : The concepts, structure, and pedagogical ideas in this assignment
#             are original. The assignment template was developed with partial
#             assistance from an AI language model (Claude, Anthropic) for
#             formatting and scaffolding purposes.
#
# =============================================================================
# Short Circuit Analysis — Pre-Fault Voltage Initialisation
# =============================================================================
# DESCRIPTION:
#   Sets the pre-fault voltage at every bus. These voltages serve as the
#   Thevenin source voltages in the fault analysis (the open-circuit voltage
#   at each bus before the fault is applied).
#
# TWO APPROACHES:
#
#   1. FLAT START (used in this assignment):
#      All bus voltages are set to 1∠0° pu.
#      This is the standard assumption for hand calculations and is
#      adequate when the network is lightly loaded.
#
#   2. LOAD FLOW SOLUTION (recommended for accuracy):
#      Run the load flow solver (Assignment 10 — LF.py) on the same
#      network first and use the converged complex bus voltages as the
#      pre-fault conditions.
#      This is more accurate because it accounts for:
#          - Actual voltage magnitude variations due to loading
#          - Voltage angle differences between buses
#          - The effect of reactive power compensation
#      For this assignment, flat start is sufficient. Students may
#      extend this by importing and running LF.py before SC.py.
#
# DEPENDENCIES:
#   SystemData.py    — db.buses, db.V0
#   Reading.py       — must be run first
# =============================================================================

import numpy as np
import cmath
import SystemData as db


# =============================================================================
# INITIALISE PRE-FAULT VOLTAGES
# =============================================================================

for bus in db.buses:
    bus.initialize_voltage()    # sets bus.V = 1 + 0j (flat start)

# Store pre-fault voltages as a numpy array in db.V0
# Array index = node number - 1  (bus 1 → index 0)

# YOUR CODE STARTS HERE
# Assemble db.V0 as a numpy array of complex voltages from db.buses.
# HINT: db.V0 = np.array([bus.V for bus in db.buses])

pass  # Remove this line once you add your code

# YOUR CODE ENDS HERE


# =============================================================================
# SUMMARY OUTPUT
# =============================================================================

print("\n--- Pre-Fault Voltage Profile (Flat Start) ---")
print(f"  {'Node':<6} {'Name':<12} {'|V| (pu)':<12} {'Angle (deg)'}")
print("  " + "-" * 42)

for bus in db.buses:
    mag   = abs(bus.V)
    angle = cmath.phase(bus.V) * (180 / 3.141592653589793)
    print(f"  {bus.node:<6} {bus.description:<12} {mag:<12.4f} {angle:.4f}")

print("  " + "-" * 42 + "\n")

# =============================================================================
# END OF Initialize.py
# =============================================================================
