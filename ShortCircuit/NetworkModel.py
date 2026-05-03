# =============================================================================
# NetworkModel.py
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
# Short Circuit Analysis — Sequence Network Y-Bus Formation
# =============================================================================
# DESCRIPTION:
#   Builds the three sequence Y-bus matrices required for fault analysis:
#       Y_bus_pos  — positive sequence network
#       Y_bus_neg  — negative sequence network
#       Y_bus_zero — zero sequence network
#
#   For this assignment all three sequence networks use the same impedance
#   data. See the ASSUMPTIONS section in SC.py for full details.
#
# Y-BUS FORMATION (same rules as load flow):
#
#   Transmission Line (between bus i and bus j):
#       y_ij        = 1 / (r + jx)
#       Y[i,i] +=  y_ij + j(b/2)
#       Y[j,j] +=  y_ij + j(b/2)
#       Y[i,j] += -y_ij
#       Y[j,i] += -y_ij
#
#   Transformer (between bus i and bus j, tap t):
#       y_ij        = 1 / (r + jx)
#       Y[i,i] +=  y_ij / t^2
#       Y[j,j] +=  y_ij
#       Y[i,j] += -y_ij / t
#       Y[j,i] += -y_ij / t
#
#   Shunt Reactor (at bus i):
#       y_sh        = 1 / (r + jx)
#       Y[i,i] +=  y_sh
#
# DEPENDENCIES:
#   SystemData.py  — global database
#   Reading.py     — must be run first
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# CLASS: YBus
# =============================================================================

class YBus:
    """
    Builds and stores a Y-bus matrix for one sequence network.

    The same class is instantiated three times — once for each sequence.
    For this assignment all three receive identical impedance data.
    """

    def __init__(self):

        self.N          = len(db.buses)
        self.node_index = {bus.node: idx for idx, bus in enumerate(db.buses)}
        self.Y_bus      = np.zeros((self.N, self.N), dtype=complex)

        self._add_transmission_lines()
        self._add_transformers()
        self._add_shunt_reactors()

    # =========================================================================
    # TRANSMISSION LINE CONTRIBUTIONS
    # =========================================================================

    def _add_transmission_lines(self):
        """
        Stamps transmission line contributions into Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
        Extract parameters into arrays first, then vectorize:

            r   = np.array([ln.r      for ln in db.lines])
            x   = np.array([ln.x      for ln in db.lines])
            b   = np.array([ln.b_half for ln in db.lines])
            y   = 1 / (r + 1j * x)

        Then use np.add.at for efficient diagonal stamping.
        -----------------------------------------------------------------
        """

        # YOUR CODE STARTS HERE
        # Step 1: Extract r, x, b_half, from_node, to_node for all lines.
        # Step 2: Compute series admittance y = 1 / (r + jx).
        # Step 3: Stamp into Y_bus — diagonal and off-diagonal entries.
        # REMINDER: Use self.node_index[node] to get the matrix index.

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    # =========================================================================
    # TRANSFORMER CONTRIBUTIONS
    # =========================================================================

    def _add_transformers(self):
        """
        Stamps transformer contributions into Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
            r   = np.array([tr.r   for tr in db.transformers])
            x   = np.array([tr.x   for tr in db.transformers])
            tap = np.array([tr.tap for tr in db.transformers])
            y   = 1 / (r + 1j * x)
        -----------------------------------------------------------------
        """

        # YOUR CODE STARTS HERE
        # Step 1: Extract r, x, tap, from_node, to_node for all transformers.
        # Step 2: Compute series admittance y = 1 / (r + jx).
        # Step 3: Stamp into Y_bus with correct tap ratio scaling.

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    # =========================================================================
    # SHUNT REACTOR CONTRIBUTIONS
    # =========================================================================

    def _add_shunt_reactors(self):
        """
        Stamps shunt reactor contributions into the diagonal of Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
            nodes = [self.node_index[dz.node] for dz in db.shunt_reactors]
            y_sh  = np.array([1/(dz.r + 1j*dz.x) for dz in db.shunt_reactors])
            np.add.at(self.Y_bus, (nodes, nodes), y_sh)
        -----------------------------------------------------------------
        """

        # YOUR CODE STARTS HERE
        # Step 1: Extract r, x, node for all shunt reactors.
        # Step 2: Compute shunt admittance y_sh = 1 / (r + jx).
        # Step 3: Stamp onto diagonal of Y_bus only.

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    def print_Ybus(self):
        print("\n--- Y-Bus Matrix (G + jB) ---")
        for i in range(self.N):
            row = ""
            for j in range(self.N):
                g = self.Y_bus[i, j].real
                b = self.Y_bus[i, j].imag
                row += f"  ({g:+.4f}{b:+.4f}j)"
            print(row)
        print()


# =============================================================================
# FUNCTION: build_sequence_networks
# =============================================================================

def build_sequence_networks():
    """
    Builds Y-bus matrices for all three sequence networks and stores them
    in the global database.

    For this assignment:
        Positive = Negative = Zero sequence  (same impedance data)

    In a full implementation, each sequence would use different data:
        Positive sequence  — standard network impedances (same as load flow)
        Negative sequence  — same as positive for passive elements
        Zero sequence      — depends on transformer winding connections
                             and line zero-sequence impedances (~3x positive)

    -----------------------------------------------------------------------
    YOUR TASK:
    -----------------------------------------------------------------------
    Instantiate the YBus class three times and assign to db:
        db.ybus_pos  = YBus()
        db.ybus_neg  = YBus()
        db.ybus_zero = YBus()

    Since all three use the same impedance data for this assignment,
    this simply creates three identical copies.

    In a future extension, you would pass a 'sequence' parameter to YBus
    and use different impedance values for each sequence network.
    -----------------------------------------------------------------------
    """

    # YOUR CODE STARTS HERE
    # Instantiate YBus three times and assign to db.ybus_pos,
    # db.ybus_neg, and db.ybus_zero.

    pass  # Remove this line once you add your code

    # YOUR CODE ENDS HERE

    print(f"  Sequence Y-Bus size : {db.ybus_pos.N} x {db.ybus_pos.N}")
    print(f"  Positive = Negative = Zero (same impedance data)\n")


# =============================================================================
# BUILD SEQUENCE NETWORKS
# =============================================================================

build_sequence_networks()

# =============================================================================
# END OF NetworkModel.py
# =============================================================================
