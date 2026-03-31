# =============================================================================
# Mismatch.py
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
# Load Flow Analysis — Power Mismatch
# =============================================================================
# DESCRIPTION:
#   This module computes the power mismatch at each iteration of the
#   Newton-Raphson load flow. It contains two functions:
#
#       form_specified_values()  — computes specified (scheduled) P and Q
#       compute_mismatch()       — computes mismatch = specified - calculated
#
# MISMATCH DEFINITION:
#       ΔP = P_specified - P_calculated      (for all buses except slack)
#       ΔQ = Q_specified - Q_calculated      (for PQ buses only)
#
# MISMATCH VECTOR (for Jacobian solve):
#       mismatch = [ ΔP_2, ΔP_3, ..., ΔP_N,      ← buses 2 to N
#                    ΔQ_2, ΔQ_3, ..., ΔQ_Npq ]    ← PQ buses only
#
# DEPENDENCIES:
#   SystemData.py   — global database
#   NetworkState.py — db.state.compute_power() provides P_calc, Q_calc
#
# WORKFLOW:
#   ... → NetworkState.py → Mismatch.py → Jacobian.py → ...
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# FUNCTION 1 — FORM SPECIFIED VALUES
# =============================================================================

def form_specified_values():
    """
    Computes the specified (scheduled) net power injection at every bus.

    The specified power is the net injection from generators and loads:
        P_spec[i] = P_gen[i] - P_load[i]     (in per unit)
        Q_spec[i] = Q_gen[i] - Q_load[i]     (in per unit)

    Since bus nodes are numbered 1 to N sequentially:
        array index = node number - 1

    Parameters: none — reads directly from db.generators and db.loads.

    Returns:
        P_spec : numpy array of size N  (index 0 = bus 1 = slack)
        Q_spec : numpy array of size N

    -----------------------------------------------------------------------
    HINT:
    -----------------------------------------------------------------------
    Start with zero arrays and accumulate contributions:

        P_spec = np.zeros(N)
        Q_spec = np.zeros(N)

        for gen in db.generators:
            i = gen.node - 1                      # node to index
            P_spec[i] += gen.P / db.base_mva

        for load in db.loads:
            i = load.node - 1
            P_spec[i] -= load.P / db.base_mva
            Q_spec[i] -= load.Q / db.base_mva
    -----------------------------------------------------------------------
    """

    N      = len(db.buses)
    P_spec = np.zeros(N)
    Q_spec = np.zeros(N)

    # YOUR CODE STARTS HERE
    # Accumulate generator and load contributions into P_spec and Q_spec.
    # Use node - 1 as the array index.
    # Remember to convert MW/MVAR to per unit by dividing by db.base_mva.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    return P_spec, Q_spec


# =============================================================================
# FUNCTION 2 — COMPUTE MISMATCH
# =============================================================================

def compute_mismatch(P_spec, Q_spec):
    """
    Computes the power mismatch vector for the current Newton-Raphson iteration.

    Parameters:
    -----------
        P_spec : numpy array — specified active power at all buses (pu)
        Q_spec : numpy array — specified reactive power at all buses (pu)

        NOTE: These are passed in rather than recomputed here because the
        constant PQ load model means they do not change between iterations.
        form_specified_values() is called once in LF.py before the loop.

    Steps:
    ------
        1. Call db.state.compute_power() to get P_calc and Q_calc
           from the current bus voltages.

        3. Compute the full mismatch across all N buses:
               dP_full = P_spec - db.state.P
               dQ_full = Q_spec - db.state.Q

        4. Extract the relevant entries:
               dP = dP_full[1:]        ← buses 2 to N (exclude slack at index 0)
               dQ = dQ_full for PQ buses only

        5. Assemble the mismatch vector:
               mismatch_vector = np.concatenate([dP, dQ])

        6. Compute convergence indicators:
               max_dP = np.max(np.abs(dP))
               max_dQ = np.max(np.abs(dQ))

    Returns:
        dP              : numpy array — ΔP at buses 2 to N
        dQ              : numpy array — ΔQ at PQ buses only
        mismatch_vector : numpy array — full [dP; dQ] for the Jacobian solve
        max_dP          : float — maximum |ΔP| for convergence check
        max_dQ          : float — maximum |ΔQ| for convergence check
    """

    # YOUR CODE STARTS HERE
    # Follow the 6 steps described above.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


# =============================================================================
# END OF Mismatch.py
# =============================================================================
