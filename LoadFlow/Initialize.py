# =============================================================================
# Initialize.py
# =============================================================================
#
# Course    : EE6201 - Power Systems Lab
# Institute : Indian Institute of Technology Hyderabad (IIT Hyderabad)
# Semester  : Spring 2026
# Assignment: Assignment 10
# Instructor: V. Seshadri Sravan Kumar, Dept. of Electrical Engineering
#
# Note      : The concepts, structure, and pedagogical ideas in this assignment
#             are original. The assignment template was developed with partial
#             assistance from an AI language model (Claude, Anthropic) for
#             formatting and scaffolding purposes.
#
# =============================================================================
# Load Flow Analysis — Network Initialization
# =============================================================================
# OBJECTIVE:
#   Set up the initial complex voltage at every bus for the Newton-Raphson
#   load flow iteration (flat start with PV bus corrections).
#
# DEPENDENCIES:
#   SystemData.py  — shared global database
#   NetworkClasses.py   — Bus.initialize_voltage() method (your implementation)
#   Reading.py          — must be run first to populate the database
#
# WORKFLOW:
#   Reading.py  →  Initialize.py  →  NetworkModel.py  →  (Jacobian, ...)
# =============================================================================

import cmath
import SystemData as db


# =============================================================================
# INITIALIZE VOLTAGES AT ALL BUSES
# =============================================================================
# Calls initialize_voltage() on each Bus object.
# After this loop every bus will have:
#   bus.V         — complex initial voltage
#   bus.bus_type  — 'Slack', 'PV', or 'PQ'

for bus in db.buses:
    bus.initialize_voltage(db.generators, db.slack_node)


# =============================================================================
# SUMMARY OUTPUT
# =============================================================================

print("\n--- Initial Voltage Profile ---")
print(f"  {'Node':<6} {'Name':<12} {'Type':<6} {'|V| (pu)':<12} {'Angle (deg)'}")
print("  " + "-" * 52)

for bus in db.buses:

    # YOUR CODE STARTS HERE
    # Compute magnitude and angle (degrees) of bus.V and print a formatted row.
    #
    # HINT:
    #   magnitude = abs(bus.V)
    #   angle_deg = math.degrees(cmath.phase(bus.V))

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

print("  " + "-" * 52 + "\n")

# =============================================================================
# END OF Initialize.py
# =============================================================================
