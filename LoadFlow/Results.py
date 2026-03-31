# =============================================================================
# Results.py
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
# Load Flow Analysis — Results
# =============================================================================
# DESCRIPTION:
#   This module prints the final load flow results after convergence.
#   It contains three functions:
#
#       print_bus_results()   — final voltage profile and bus power injections
#       print_line_flows()    — active and reactive power flows on all branches
#       print_summary()       — generation, load, and loss totals
#
# NOTE:
#   All results are computed from the converged voltage solution stored in
#   db.buses. Line flows require a separate calculation from branch data —
#   they are NOT directly available from the Y-bus or the mismatch vector.
#
# DEPENDENCIES:
#   SystemData.py   — db.buses, db.lines, db.transformers, db.state
#
# WORKFLOW:
#   LF.py (after convergence) → Results.py
# =============================================================================

import numpy as np
import cmath
import SystemData as db


# =============================================================================
# FUNCTION 1 — BUS RESULTS
# =============================================================================

def print_bus_results():
    """
    Prints the final voltage profile and net power injection at each bus.

    Columns:
        Node  | Name | Type | |V| (pu) | Angle (deg) | P_calc (MW) | Q_calc (MVAR)

    P_calc and Q_calc are taken from db.state after the final
    compute_power() call. Convert from per unit to MW/MVAR by
    multiplying by db.base_mva.

    -----------------------------------------------------------------------
    HINT:
    -----------------------------------------------------------------------
        for i, bus in enumerate(db.buses):
            mag   = abs(bus.V)
            angle = math.degrees(cmath.phase(bus.V))
            P_MW  = db.state.P[i] * db.base_mva
            Q_MW  = db.state.Q[i] * db.base_mva
    -----------------------------------------------------------------------
    """

    print("\n" + "=" * 75)
    print("  BUS RESULTS")
    print("=" * 75)
    print(f"  {'Node':<6} {'Name':<12} {'Type':<6} {'|V| (pu)':<10} "
          f"{'Angle (deg)':<14} {'P (MW)':<12} {'Q (MVAR)'}")
    print("  " + "-" * 70)

    # YOUR CODE STARTS HERE
    # Loop over db.buses and print each row.
    # Use abs(bus.V) for magnitude and cmath.phase() for angle.
    # Multiply db.state.P[i] and db.state.Q[i] by db.base_mva for MW/MVAR.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print("  " + "-" * 70)


# =============================================================================
# FUNCTION 2 — LINE AND TRANSFORMER FLOWS
# =============================================================================

def print_line_flows():
    """
    Computes and prints the power flow on each transmission line
    and transformer.

    For a branch between bus i and bus j with series admittance y = g + jb
    and half-line charging y_sh = 0 + j(b/2):

    Current from i to j:
        I_ij = y * (V_i - V_j) + y_sh * V_i

    Power flow from i to j:
        S_ij = V_i * conj(I_ij)
        P_ij = Re(S_ij) * base_mva     (MW)
        Q_ij = Im(S_ij) * base_mva     (MVAR)

    Power flow from j to i:
        I_ji = y * (V_j - V_i) + y_sh * V_j
        S_ji = V_j * conj(I_ji)

    Branch loss:
        P_loss = P_ij + P_ji           (MW)

    For transformers, use the tap-corrected admittance:
        y = 1 / (r + jx)
        I_ij = (y / tap) * (V_i / tap - V_j)

    -----------------------------------------------------------------------
    HINT — Getting bus voltages by node number:
    -----------------------------------------------------------------------
    Build a voltage lookup dictionary once:

        V = {bus.node: bus.V for bus in db.buses}

    Then for any branch:
        Vi = V[line.from_node]
        Vj = V[line.to_node]
    -----------------------------------------------------------------------
    """

    print("\n" + "=" * 75)
    print("  BRANCH FLOWS")
    print("=" * 75)
    print(f"  {'From':<6} {'To':<6} {'Type':<6} {'P_from (MW)':<14} "
          f"{'Q_from (MVAR)':<16} {'P_to (MW)':<14} {'Q_to (MVAR)':<14} {'Loss (MW)'}")
    print("  " + "-" * 88)

    # YOUR CODE STARTS HERE
    # Loop over db.lines and db.transformers.
    # Compute S_ij and S_ji for each branch using the formulas above.
    # Print one row per branch.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print("  " + "-" * 88)


# =============================================================================
# FUNCTION 3 — SYSTEM SUMMARY
# =============================================================================

def print_summary():
    """
    Prints total generation, total load, and total system losses.

    Total generation P and Q: sum over all generator buses.
    Total load P and Q      : sum over all load buses.
    Total losses            : Total generation - Total load.

    -----------------------------------------------------------------------
    HINT:
    -----------------------------------------------------------------------
    You can sum directly from db.generators and db.loads:

        total_P_gen  = sum(g.P for g in db.generators)
        total_Q_gen  = sum(g.Q_max for g in db.generators)   # scheduled
        total_P_load = sum(l.P for l in db.loads)
        total_Q_load = sum(l.Q for l in db.loads)

    OR compute from db.state after convergence (more accurate, includes
    the slack bus generation which is not explicitly in db.generators):

        total_P_gen  = sum(db.state.P[i] * db.base_mva
                           for i, bus in enumerate(db.buses)
                           if bus.bus_type in ['Slack', 'PV'])
    -----------------------------------------------------------------------
    """

    print("\n" + "=" * 75)
    print("  SYSTEM SUMMARY")
    print("=" * 75)

    # YOUR CODE STARTS HERE
    # Compute and print total generation, total load, and total losses.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print("=" * 75 + "\n")


# =============================================================================
# END OF Results.py
# =============================================================================
