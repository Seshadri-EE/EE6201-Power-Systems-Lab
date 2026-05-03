# =============================================================================
# ZBus.py
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
# Short Circuit Analysis — Z-Bus Formation
# =============================================================================
# DESCRIPTION:
#   Computes the bus impedance matrix (Z-bus) for each sequence network
#   by inverting the corresponding Y-bus matrix:
#
#       Z_bus = Y_bus^(-1)
#
#   The Z-bus is the key matrix for fault analysis. Its diagonal element
#   Z_bus[k,k] is the Thevenin impedance seen from bus k into the network,
#   and its off-diagonal element Z_bus[i,k] gives the transfer impedance
#   between buses i and k.
#
# METHOD — DIRECT INVERSION:
#   Z_bus = np.linalg.inv(Y_bus)
#
#   This is used here for simplicity and clarity. For large networks,
#   direct inversion is computationally expensive (O(N^3)).
#
#   More efficient alternatives for production codes:
#
#   1. Z-Bus Building Algorithm (Kron Reduction):
#      Builds Z_bus element by element as branches are added to the
#      network. Avoids forming Y_bus altogether. Efficient for networks
#      where only specific Z_bus elements are needed.
#
#   2. Sparse LU Factorisation:
#      Factor Y_bus = L * U once, then solve Y_bus * Z_col = I for each
#      column of Z_bus using forward/backward substitution. Much faster
#      than full inversion for large sparse networks.
#
#   3. Partial Z-Bus:
#      If only fault currents at a specific bus are needed, only the
#      k-th column (or diagonal element) of Z_bus is required. This
#      can be obtained by solving Y_bus * z = e_k (unit vector) without
#      forming the full Z_bus.
#
# DEPENDENCIES:
#   SystemData.py    — db.ybus_pos, db.ybus_neg, db.ybus_zero
#   NetworkModel.py  — must be run first
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# FUNCTION: compute_zbus
# =============================================================================

def compute_zbus():
    """
    Computes Z-bus matrices for all three sequence networks by direct
    inversion of the corresponding Y-bus matrices.

    Stores results in:
        db.zbus_pos   — positive sequence Z-bus (numpy complex matrix)
        db.zbus_neg   — negative sequence Z-bus (numpy complex matrix)
        db.zbus_zero  — zero sequence Z-bus     (numpy complex matrix)

    -----------------------------------------------------------------------
    HINT:
    -----------------------------------------------------------------------
    Use numpy's matrix inverse:

        db.zbus_pos  = np.linalg.inv(db.ybus_pos.Y_bus)
        db.zbus_neg  = np.linalg.inv(db.ybus_neg.Y_bus)
        db.zbus_zero = np.linalg.inv(db.ybus_zero.Y_bus)

    After inversion, verify by checking that Y * Z ≈ I:
        residual = np.max(np.abs(db.ybus_pos.Y_bus @ db.zbus_pos
                                 - np.eye(db.ybus_pos.N)))
        print(f"  Inversion residual : {residual:.2e}  (should be ~1e-12)")

    A large residual indicates the Y-bus may be singular — check for
    isolated buses or disconnected network components.
    -----------------------------------------------------------------------
    """

    # YOUR CODE STARTS HERE
    # Invert all three sequence Y-bus matrices and store in db.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print(f"  Z-Bus computed for all three sequence networks.")
    print(f"  Size : {db.zbus_pos.shape[0]} x {db.zbus_pos.shape[1]}\n")


# =============================================================================
# COMPUTE Z-BUS
# =============================================================================

compute_zbus()

# =============================================================================
# END OF ZBus.py
# =============================================================================
