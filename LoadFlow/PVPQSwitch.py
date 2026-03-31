# =============================================================================
# PVPQSwitch.py
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
# Load Flow Analysis — PV-PQ Bus Type Switching
# =============================================================================
# DESCRIPTION:
#   At each Newton-Raphson iteration, generator buses (PV buses) are checked
#   against their reactive power limits. If a PV bus violates its Q limits,
#   it is converted to a PQ bus for that iteration. If a previously switched
#   bus recovers within limits, it is restored to PV.
#
# WHY THIS MATTERS:
#   A PV bus has a fixed voltage magnitude maintained by the generator's
#   automatic voltage regulator (AVR). However, the generator can only
#   supply reactive power within its capability limits [Q_min, Q_max].
#   If the required Q exceeds these limits, the AVR can no longer hold
#   the voltage — the bus effectively becomes a PQ bus with Q fixed at
#   the violated limit.
#
# SWITCHING RULES:
#   For each PV bus i, after computing Q_calc:
#
#       If Q_calc > Q_max :
#           Switch to PQ  →  bus.bus_type = 'PQ'
#                            Q_spec[i]   = Q_max  (in per unit)
#                            Release voltage magnitude constraint
#
#       If Q_calc < Q_min :
#           Switch to PQ  →  bus.bus_type = 'PQ'
#                            Q_spec[i]   = Q_min  (in per unit)
#                            Release voltage magnitude constraint
#
#       If previously switched and Q_calc is within [Q_min, Q_max]:
#           Restore to PV →  bus.bus_type = 'PV'
#                            Restore voltage magnitude from generator data
#
# EFFECT ON MISMATCH AND JACOBIAN:
#   Every switch changes Npq — the number of PQ buses. This affects:
#       - The length of dQ in the mismatch vector
#       - The size of the Jacobian matrix (J3, J4 submatrices)
#   The mismatch and Jacobian must therefore be recomputed after any switch.
#
# EFFECT ON Q_spec:
#   Unlike P_spec (which is truly constant for constant PQ loads),
#   Q_spec for PV buses is NOT fixed — it is updated by this function
#   whenever a switch occurs. Q_spec is therefore passed in and returned
#   as a modified array.
#
# DEPENDENCIES:
#   SystemData.py   — global database (db.buses, db.generators, db.state)
#
# WORKFLOW:
#   ... → compute_mismatch() → check_pv_pq_switch() → form_jacobian() → ...
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# FUNCTION — CHECK AND PERFORM PV-PQ SWITCHING
# =============================================================================

def check_pv_pq_switch(Q_spec):
    """
    Checks all PV buses against their reactive power limits and performs
    bus type switching where necessary.

    Parameters:
    -----------
        Q_spec : numpy array of size N — current specified Q at all buses (pu)
                 This array is modified in-place where switching occurs.

    Returns:
    --------
        Q_spec      : numpy array — updated Q_spec after switching
        switched    : bool — True if any bus changed type this iteration,
                             False if no changes occurred

    Steps:
    ------
        1. Build a lookup dictionary mapping node number to Generator object
           so you can quickly find Q_max and Q_min for any PV bus:

               gen_map = {g.node: g for g in db.generators}

        2. Loop over all buses. For each bus:

           a. If bus.bus_type == 'PV':
                  i   = bus.node - 1               (array index)
                  gen = gen_map[bus.node]
                  Q_calc = db.state.Q[i]            (in per unit)
                  Q_max  = gen.Q_max / db.base_mva
                  Q_min  = gen.Q_min / db.base_mva

                  If Q_calc > Q_max:
                      bus.bus_type = 'PQ'
                      Q_spec[i]   = Q_max
                      switched    = True
                      print a message indicating the switch

                  elif Q_calc < Q_min:
                      bus.bus_type = 'PQ'
                      Q_spec[i]   = Q_min
                      switched    = True
                      print a message indicating the switch

           b. If bus.bus_type == 'PQ' and bus was originally a PV bus
              (i.e., its node appears in gen_map):
                  Check if Q_calc is now within [Q_min, Q_max].
                  If yes, restore bus.bus_type = 'PV'
                  Restore voltage magnitude from generator's V_setpoint.
                  switched = True

    -----------------------------------------------------------------------
    HINT — Tracking original bus types:
    -----------------------------------------------------------------------
    To know whether a PQ bus was originally a PV bus, simply check if its
    node number exists in gen_map (the generator lookup dictionary).
    Generators are only connected to PV buses, so:

        if bus.node in gen_map:
            # this bus was originally a PV bus
    -----------------------------------------------------------------------

    -----------------------------------------------------------------------
    HINT — Restoring voltage magnitude:
    -----------------------------------------------------------------------
    When restoring a switched bus back to PV, reset the voltage magnitude
    to the generator's setpoint while keeping the current angle:

        import cmath
        angle = cmath.phase(bus.V)
        bus.V = cmath.rect(gen.V_setpoint, angle)
    -----------------------------------------------------------------------
    """

    switched = False

    # YOUR CODE STARTS HERE
    # Follow the steps described above.
    # Modify bus.bus_type and Q_spec in-place where switching occurs.
    # Set switched = True if any bus changes type.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    return Q_spec, switched


# =============================================================================
# END OF PVPQSwitch.py
# =============================================================================
