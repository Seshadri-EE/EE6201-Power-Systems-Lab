# =============================================================================
# Update.py
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
# Load Flow Analysis — Linear System Solve and Voltage Update
# =============================================================================
# DESCRIPTION:
#   This module provides two functions that form the final steps of each
#   Newton-Raphson iteration:
#
#       solve_linear_system()  — solves J * Δx = mismatch for corrections Δx
#       update_voltages()      — applies Δx to bus voltages
#
# CORRECTION VECTOR STRUCTURE:
#   The solution vector Δx is ordered consistently with the mismatch vector
#   and the Jacobian:
#
#       Δx = [ Δδ_2,   Δδ_3,   ..., Δδ_N,          ← N-1 angle corrections
#              Δ|V|_pq1, ...,  Δ|V|_pqNpq ]         ← Npq magnitude corrections
#
#   Angles    are updated at ALL non-slack buses (PQ and PV).
#   Magnitudes are updated at PQ buses ONLY.
#   PV bus magnitudes are held fixed (voltage controlled by generator AVR).
#   Slack bus voltage (magnitude and angle) is never updated.
#
# NOTE ON PV-PQ SWITCHING:
#   If a PV bus has been switched to PQ by PVPQSwitch.py, its index will
#   appear in the pq_buses list and its magnitude will be corrected.
#   This is handled automatically since bus types are read fresh from
#   db.buses at every call.
#
# DEPENDENCIES:
#   SystemData.py  — global database (db.buses)
#   Jacobian.py    — J must be formed before calling solve_linear_system()
#   Mismatch.py    — mismatch_vector must be current before solving
#
# WORKFLOW:
#   ... → form_jacobian() → solve_linear_system() → update_voltages() → ...
# =============================================================================

import numpy as np
import cmath
import SystemData as db


# =============================================================================
# FUNCTION 1 — SOLVE LINEAR SYSTEM
# =============================================================================

def solve_linear_system(J, mismatch_vector):
    """
    Solves the linear system J * Δx = mismatch_vector for the correction
    vector Δx using numpy's direct solver.

    Parameters:
    -----------
        J                : numpy array (N-1+Npq, N-1+Npq) — Jacobian matrix
        mismatch_vector  : numpy array (N-1+Npq,) — current mismatch [dP; dQ]

    Returns:
    --------
        dx : numpy array (N-1+Npq,) — correction vector [Δδ; Δ|V|]

    -----------------------------------------------------------------------
    HINT:
    -----------------------------------------------------------------------
    Use numpy's built-in direct solver:

        dx = np.linalg.solve(J, mismatch_vector)

    This solves J * dx = mismatch_vector efficiently using LU decomposition.

    You may also check the condition number of J as a diagnostic:

        cond = np.linalg.cond(J)
        if cond > 1e10:
            print(f"  [WARNING] Jacobian is ill-conditioned (cond = {cond:.2e})")

    A very large condition number suggests the network may be close to
    voltage collapse or the data has an error.
    -----------------------------------------------------------------------
    """

    # YOUR CODE STARTS HERE
    # Solve the linear system and return dx.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


# =============================================================================
# FUNCTION 2 — UPDATE VOLTAGES
# =============================================================================

def update_voltages(dx):
    """
    Applies the correction vector Δx to the bus voltages in db.buses.

    The correction vector is structured as:
        dx[:N-1]   — angle corrections Δδ for buses 2 to N  (non-slack)
        dx[N-1:]   — magnitude corrections Δ|V| for PQ buses only

    Update rules:
    -------------
        Non-slack buses (PQ and PV):
            δ_new  = δ_old  + Δδ

        PQ buses only:
            |V|_new = |V|_old + Δ|V|

        PV buses:
            |V| unchanged  (magnitude held fixed by AVR)

        Slack bus:
            Nothing updated  (reference bus, fixed V and δ)

    After updating magnitude and angle separately, reconstruct the
    complex voltage:
        bus.V = cmath.rect(|V|_new, δ_new)

    Parameters:
    -----------
        dx : numpy array — correction vector [Δδ; Δ|V|] from solve_linear_system()

    -----------------------------------------------------------------------
    HINT — Splitting dx:
    -----------------------------------------------------------------------
    Identify bus index sets fresh from db.buses (bus types may have changed
    due to PV-PQ switching):

        non_slack = [i for i, bus in enumerate(db.buses)
                     if bus.bus_type != 'Slack']

        pq_buses  = [i for i, bus in enumerate(db.buses)
                     if bus.bus_type == 'PQ']

    Split dx accordingly:
        d_delta = dx[:len(non_slack)]      # angle corrections
        d_Vmag  = dx[len(non_slack):]      # magnitude corrections

    Then update each bus:
        for k, i in enumerate(non_slack):
            mag   = abs(db.buses[i].V)
            angle = cmath.phase(db.buses[i].V) + d_delta[k]
            # magnitude update for PQ buses handled separately below
            db.buses[i].V = cmath.rect(mag, angle)

        for k, i in enumerate(pq_buses):
            mag   = abs(db.buses[i].V) + d_Vmag[k]
            angle = cmath.phase(db.buses[i].V)
            db.buses[i].V = cmath.rect(mag, angle)
    -----------------------------------------------------------------------
    """

    # YOUR CODE STARTS HERE
    # Split dx, update angles for non-slack buses, update magnitudes
    # for PQ buses, and reconstruct complex voltages using cmath.rect().

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE


# =============================================================================
# END OF Update.py
# =============================================================================
