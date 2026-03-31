# =============================================================================
# YBus.py
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
# Load Flow Analysis — Network Model (Y-Bus Formation)
# =============================================================================
# OBJECTIVE:
#   Build the bus admittance matrix (Y_bus) of the power system network.
#   The Y_bus is an N x N complex matrix where N is the number of buses.
#
# CONTRIBUTIONS TO Y_bus:
#
#   Transmission Line (between bus i and bus j):
#       y_ij        = 1 / (r + jx)          series admittance
#       Y_bus[i,i] +=  y_ij + j(b/2)
#       Y_bus[j,j] +=  y_ij + j(b/2)
#       Y_bus[i,j] += -y_ij
#       Y_bus[j,i] += -y_ij
#
#   Transformer (between bus i and bus j, tap ratio t):
#       y_ij        = 1 / (r + jx)
#       Y_bus[i,i] +=  y_ij / t^2
#       Y_bus[j,j] +=  y_ij
#       Y_bus[i,j] += -y_ij / t
#       Y_bus[j,i] += -y_ij / t
#
#   Shunt Reactor (at bus i):
#       y_sh        = 1 / (r + jx)
#       Y_bus[i,i] +=  y_sh
#
# DEPENDENCIES:
#   SystemData.py  — shared global database
#   Reading.py          — must be run first to populate the database
#   Initialize.py       — must be run before YBus.py
#
# WORKFLOW:
#   Reading.py  →  Initialize.py  →  YBus.py  →  (Jacobian, ...)
# =============================================================================

import numpy as np
import SystemData as db


# =============================================================================
# CLASS: YBus
# =============================================================================

class YBus:
    """
    Represents the mathematical model of the power system network.

    Core attribute:
        Y_bus : numpy complex matrix of size (N x N), where N = number of buses.
    """

    def __init__(self):
        """
        Initializes the YBus using data from the global database.
        Builds the Y_bus matrix by stamping contributions from all elements.
        """

        # Pull directly from the shared global database
        self.buses          = db.buses
        self.lines          = db.lines
        self.transformers   = db.transformers
        self.shunt_reactors = db.shunt_reactors

        # Number of buses
        self.N = len(db.buses)

        # ---------------------------------------------------------------------
        # NODE-TO-INDEX MAPPING
        # ---------------------------------------------------------------------
        # Maps each bus node number to its row/column index in Y_bus.
        # Example: nodes [1, 2, 5, 7]  →  {1:0, 2:1, 5:2, 7:3}

        self.node_index = {bus.node: idx for idx, bus in enumerate(db.buses)}

        # ---------------------------------------------------------------------
        # Y_BUS INITIALIZATION
        # ---------------------------------------------------------------------

        self.Y_bus = np.zeros((self.N, self.N), dtype=complex)

        # ---------------------------------------------------------------------
        # BUILD Y_BUS
        # ---------------------------------------------------------------------

        self._add_transmission_lines()
        self._add_transformers()
        self._add_shunt_reactors()

    # =========================================================================
    # TRANSMISSION LINE CONTRIBUTIONS
    # =========================================================================

    def _add_transmission_lines(self):
        """
        Adds the contribution of all transmission lines to Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
        Extract all parameters into numpy arrays first, then compute
        admittances in one vectorized operation:

            r   = np.array([ln.r      for ln in self.lines])
            x   = np.array([ln.x      for ln in self.lines])
            b   = np.array([ln.b_half for ln in self.lines])
            y   = 1 / (r + 1j * x)     # vectorized — no loop needed

        Then stamp into Y_bus using node_index. For diagonal stamping
        of all elements at once, explore numpy.add.at:

            np.add.at(self.Y_bus, (i_idx, i_idx), y + 1j*b)
        -----------------------------------------------------------------
        """

        # YOUR CODE STARTS HERE
        # Step 1: Extract r, x, b_half, from_node, to_node for all lines.
        # Step 2: Compute series admittance y = 1 / (r + jx).
        # Step 3: Stamp into Y_bus — diagonal and off-diagonal entries.

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    # =========================================================================
    # TRANSFORMER CONTRIBUTIONS
    # =========================================================================

    def _add_transformers(self):
        """
        Adds the contribution of all transformers to Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
            r   = np.array([tr.r   for tr in self.transformers])
            x   = np.array([tr.x   for tr in self.transformers])
            tap = np.array([tr.tap for tr in self.transformers])
            y   = 1 / (r + 1j * x)

        Note the tap ratio scaling — diagonal and off-diagonal entries
        differ from the transmission line case.
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
        Adds the contribution of all shunt reactors to Y_bus.

        -----------------------------------------------------------------
        EFFICIENCY HINT:
        -----------------------------------------------------------------
        Shunt reactors only affect the diagonal. You can stamp all of
        them in one shot using numpy.add.at:

            nodes = [self.node_index[dz.node] for dz in self.shunt_reactors]
            y_sh  = np.array([1/(dz.r + 1j*dz.x) for dz in self.shunt_reactors])
            np.add.at(self.Y_bus, (nodes, nodes), y_sh)
        -----------------------------------------------------------------
        """

        # YOUR CODE STARTS HERE
        # Step 1: Extract r, x, node for all shunt reactors.
        # Step 2: Compute shunt admittance y_sh = 1 / (r + jx).
        # Step 3: Stamp onto diagonal of Y_bus only.

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE

    # =========================================================================
    # DISPLAY
    # =========================================================================

    def print_Ybus(self):
        """
        Prints the Y_bus matrix in a readable G + jB format.
        """
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
# INSTANTIATE AND STORE IN GLOBAL DATABASE
# =============================================================================
# The YBus object is stored back into SystemData so that
# subsequent modules (Jacobian, etc.) can access Y_bus via db.ybus.

db.ybus = YBus()

print(f"  Y_bus size : {db.ybus.N} x {db.ybus.N}")
print(f"  dtype      : {db.ybus.Y_bus.dtype}")
db.ybus.print_Ybus()

# =============================================================================
# END OF YBus.py
# =============================================================================
