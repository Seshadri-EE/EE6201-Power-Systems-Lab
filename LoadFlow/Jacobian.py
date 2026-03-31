# =============================================================================
# Jacobian.py
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
# Load Flow Analysis — Jacobian Matrix
# =============================================================================
# DESCRIPTION:
#   This module provides the function form_jacobian() which builds the
#   Jacobian matrix at every Newton-Raphson iteration from the current
#   bus voltages and the Y-bus matrix.
#
#   The Jacobian linearises the nonlinear power flow equations at the
#   current operating point, allowing the linear system J*Δx = mismatch
#   to be solved for voltage corrections.
#
# JACOBIAN STRUCTURE:
#   For a system with N buses (bus 1 = slack), Npv PV buses, Npq PQ buses:
#
#       Unknowns : [δ_2, ..., δ_N, |V|_pq1, ..., |V|_pqNpq]
#                   ← N-1 angles →  ←    Npq magnitudes    →
#
#       J = [ J1   J2 ]    size: (N-1+Npq) × (N-1+Npq)
#           [ J3   J4 ]
#
#       J1 = ∂P/∂δ      size: (N-1) × (N-1)
#       J2 = ∂P/∂|V|    size: (N-1) × Npq
#       J3 = ∂Q/∂δ      size: Npq   × (N-1)
#       J4 = ∂Q/∂|V|    size: Npq   × Npq
#
#   Note: Npq changes if PV-PQ switching has occurred. The Jacobian is
#   always rebuilt from scratch at each iteration using the current bus types.
#
# JACOBIAN ELEMENTS:
#   Let θ_ij = δ_i - δ_j,  G_ij = Re(Y_ij),  B_ij = Im(Y_ij)
#
#   J1 — ∂P/∂δ:
#       Off-diagonal (i≠j) : ∂P_i/∂δ_j   =  |V_i||V_j|(G_ij sinθ_ij - B_ij cosθ_ij)
#       Diagonal     (i=j) : ∂P_i/∂δ_i   = -Q_i - B_ii|V_i|²
#
#   J2 — ∂P/∂|V|:
#       Off-diagonal (i≠j) : ∂P_i/∂|V_j| =  |V_i|(G_ij cosθ_ij + B_ij sinθ_ij)
#       Diagonal     (i=j) : ∂P_i/∂|V_i| =  P_i/|V_i| + G_ii|V_i|
#
#   J3 — ∂Q/∂δ:
#       Off-diagonal (i≠j) : ∂Q_i/∂δ_j   = -|V_i||V_j|(G_ij cosθ_ij + B_ij sinθ_ij)
#       Diagonal     (i=j) : ∂Q_i/∂δ_i   =  P_i - G_ii|V_i|²
#
#   J4 — ∂Q/∂|V|:
#       Off-diagonal (i≠j) : ∂Q_i/∂|V_j| =  |V_i|(G_ij sinθ_ij - B_ij cosθ_ij)
#       Diagonal     (i=j) : ∂Q_i/∂|V_i| =  Q_i/|V_i| - B_ii|V_i|
#
# DEPENDENCIES:
#   SystemData.py   — global database (db.buses, db.ybus, db.state)
#   NetworkState.py — db.state.P and db.state.Q must be current
#
# WORKFLOW:
#   ... → check_pv_pq_switch() → form_jacobian() → solve → update → ...
# =============================================================================

import numpy as np
import cmath
import SystemData as db


# =============================================================================
# FUNCTION — FORM JACOBIAN
# =============================================================================

def form_jacobian():
    """
    Builds and returns the Jacobian matrix for the current iteration.

    Uses current bus voltages (db.buses[i].V), calculated powers
    (db.state.P, db.state.Q), Y-bus elements (db.ybus.Y_bus), and
    current bus types to determine which rows and columns to include.

    Returns:
    --------
        J : numpy array of shape (N-1+Npq, N-1+Npq)

    -----------------------------------------------------------------------
    SUGGESTED APPROACH:
    -----------------------------------------------------------------------
    Step 1 — Identify bus index sets:

        non_slack = [i for i, bus in enumerate(db.buses)
                     if bus.bus_type != 'Slack']    # rows/cols for δ

        pq_buses  = [i for i, bus in enumerate(db.buses)
                     if bus.bus_type == 'PQ']       # rows/cols for |V|

        n_nonsslack = len(non_slack)
        n_pq        = len(pq_buses)
        size        = n_nonslock + n_pq

    Step 2 — Extract voltage magnitudes and angles for all buses:

        V_mag   = np.array([abs(bus.V)          for bus in db.buses])
        V_ang   = np.array([cmath.phase(bus.V)  for bus in db.buses])
        G       = db.ybus.Y_bus.real
        B       = db.ybus.Y_bus.imag

    Step 3 — Initialise J as a zero matrix of the correct size:

        J = np.zeros((size, size))

    Step 4 — Fill J1 (∂P/∂δ) — rows: non_slack, cols: non_slack
    Step 5 — Fill J2 (∂P/∂|V|) — rows: non_slack, cols: pq_buses
    Step 6 — Fill J3 (∂Q/∂δ) — rows: pq_buses,  cols: non_slack
    Step 7 — Fill J4 (∂Q/∂|V|) — rows: pq_buses,  cols: pq_buses

    -----------------------------------------------------------------------
    HINT — Filling submatrices efficiently:
    -----------------------------------------------------------------------
    Use nested loops over the index sets. For example, for J1:

        for row, i in enumerate(non_slack):
            for col, j in enumerate(non_slack):
                theta_ij = V_ang[i] - V_ang[j]
                if i == j:
                    J[row, col] = -db.state.Q[i] - B[i,i] * V_mag[i]**2
                else:
                    J[row, col] = V_mag[i] * V_mag[j] * (
                                  G[i,j] * np.sin(theta_ij) -
                                  B[i,j] * np.cos(theta_ij))

    Apply the same pattern for J2, J3, J4 using the appropriate
    index sets, formulas, and column offsets in J.

    Note that J2, J3, J4 are placed with a column/row offset of
    n_nonslock since J1 occupies the first n_nonslock rows and columns.
    -----------------------------------------------------------------------
    """

    # YOUR CODE STARTS HERE
    # Follow the 7 steps described above.
    # Return the completed Jacobian matrix J.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


# =============================================================================
# END OF Jacobian.py
# =============================================================================
