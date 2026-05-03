# =============================================================================
# NetworkClasses.py
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
# Short Circuit Analysis — Class Definitions
# =============================================================================
# DESCRIPTION:
#   Defines all data classes used to represent power system network elements.
#   Imported by Reading.py and all subsequent analysis modules.
#
#   Classes:
#       Bus              — network bus node
#       Transformer      — transformer branch
#       TransmissionLine — transmission line branch
#       ShuntReactor     — shunt reactor element
#       Load             — load at a bus
#       Generator        — generator at a bus
#
# NOTE ON SEQUENCE IMPEDANCES:
#   For this assignment, positive, negative, and zero sequence impedances
#   are assumed equal and taken directly from the data file.
#   In a full implementation, each element would carry separate sequence
#   impedance attributes (r1/x1, r2/x2, r0/x0). The class definitions
#   here leave room for students to extend them later.
# =============================================================================

import cmath


# =============================================================================
# BUS CLASS
# =============================================================================

class Bus:
    """
    Represents a Bus in the power system network.

    Record Format:
        BS   <zone>  <description>  <node>  <voltage_level>

    Example:
        BS   1  RAMG-GEN   1    15.0

    Fields:
        Zone        : Zone number (integer)
        Description : 8-character bus name/label (string)
        Node        : Bus node number (integer)
        Voltage     : Nominal voltage level in kV (float)
    """

    def __init__(self, zone, description, node, voltage):

        # YOUR CODE STARTS HERE
        # Define the attributes of the Bus class.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def initialize_voltage(self):
        """
        Sets the pre-fault bus voltage to the flat start value: 1∠0° pu.

        In short circuit analysis the pre-fault voltage at every bus is
        assumed to be 1∠0° pu unless load flow results are available.

        For a more accurate analysis:
            - Run the load flow solver (Assignment 10 / LF.py) first.
            - Use the converged complex voltages as pre-fault conditions.
            - This accounts for the actual loading of the network before
              the fault occurs and gives more accurate fault currents.

        For this assignment, flat start is sufficient.
        """

        # YOUR CODE STARTS HERE
        # Set self.V = 1 + 0j  (complex flat start voltage)

        pass  # Remove this line once you add your code

        # YOUR CODE ENDS HERE


# =============================================================================
# TRANSFORMER CLASS
# =============================================================================

class Transformer:
    """
    Represents a Transformer in the power system network.

    Record Format:
        TR   <zone>  <description>  <from_node>  <to_node>  <r>  <x>  <tap>  <max_loading>

    Example:
        TR   1  2*315MVA  16   5  0.00099  0.01984  1.00  630.00

    Fields:
        Zone        : Zone number (integer)
        Description : 8-character label (string)
        From Node   : Sending end bus node number (integer)
        To Node     : Receiving end bus node number (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
        Tap         : Tap ratio (float)
        Max Loading : Maximum loading in MVA (float)

    NOTE ON ZERO SEQUENCE:
        The zero sequence model of a transformer depends on its winding
        connection (Y-grounded, Y-ungrounded, Delta). For this assignment,
        the same impedance is used for all three sequences. In a full
        implementation, the winding connection type would be read from the
        data file and used to determine the zero sequence equivalent circuit.
    """

    def __init__(self, zone, description, from_node, to_node, r, x, tap, max_loading):

        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


# =============================================================================
# TRANSMISSION LINE CLASS
# =============================================================================

class TransmissionLine:
    """
    Represents a Transmission Line in the power system network.

    Record Format:
        TL   <zone>  <description>  <from_node>  <to_node>  <r>  <x>  <b_half>  <max_loading>

    Example:
        TL   1  S*220KMS  22  25  0.00215  0.02385  0.3185  500.00

    Fields:
        Zone        : Zone number (integer)
        Description : 8-character label (string)
        From Node   : Sending end bus node number (integer)
        To Node     : Receiving end bus node number (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
        B_half      : Half line charging susceptance in per unit (float)
        Max Loading : Maximum loading in MVA (float)

    NOTE ON ZERO SEQUENCE:
        The zero sequence impedance of a transmission line is typically
        2 to 3.5 times the positive sequence impedance, depending on the
        earth return path and tower geometry. For this assignment, the same
        impedance is used for all three sequences. Students may extend this
        by adding r0, x0, b0_half attributes and reading them from the data
        file in a future version.
    """

    def __init__(self, zone, description, from_node, to_node, r, x, b_half, max_loading):

        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


# =============================================================================
# SHUNT REACTOR CLASS
# =============================================================================

class ShuntReactor:
    """
    Represents a Shunt Reactor in the power system network.

    Record Format:
        DZ   <zone>  <description>  <node>  <r>  <x>

    Example:
        DZ   0  SALEM400  19  .0000  2.20500

    Fields:
        Zone        : Zone number (integer)
        Description : 8-character label (string)
        Node        : Bus node number (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
    """

    def __init__(self, zone, description, node, r, x):

        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


# =============================================================================
# LOAD CLASS
# =============================================================================

class Load:
    """
    Represents a Load connected to a bus.

    Record Format:
        DP   <zone>  <description>  <node>  <P>  <Q>  <compensation>

    Example:
        DP   1  HYD-220    5   430.0  170.00  0.00

    Fields:
        Zone         : Zone number (integer)
        Description  : 8-character label (string)
        Node         : Bus node number (integer)
        P            : Active power demand in MW (float)
        Q            : Reactive power demand in MVAR (float)
        Compensation : Capacitive compensation in MVAR (float)

    NOTE:
        Loads are not modeled in the sequence networks for fault analysis.
        They are included here for completeness and potential future use
        (e.g., computing pre-fault loading for more accurate initial voltages
        if the load flow is run before the fault analysis).
    """

    def __init__(self, zone, description, node, P, Q, compensation):

        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


# =============================================================================
# GENERATOR CLASS
# =============================================================================

class Generator:
    """
    Represents a Generator connected to a bus.

    Record Format:
        GP   <zone>  <description>  <node>  <P>  <Q_max>  <Q_min>  <V_setpoint>

    Example:
        GP  11  RMG        1  1820.0   950.0  -150.0     1.0

    Fields:
        Zone       : Zone number (integer)
        Description: 8-character label (string)
        Node       : Bus node number (integer)
        P          : Scheduled active power in MW (float)
        Q_max      : Maximum reactive power in MVAR (float)
        Q_min      : Minimum reactive power in MVAR (float)
        V_setpoint : Voltage set point in per unit (float)

    NOTE ON FAULT ANALYSIS:
        For accurate fault analysis, the generator subtransient reactance
        Xd'' should be used to model the generator's contribution to fault
        current. In this assignment, generators are modeled as voltage
        sources behind their subtransient reactance — but since Xd'' is
        not available in the data file, the generator is not explicitly
        modeled as a shunt element in the sequence networks.

        Students may extend this by:
            1. Adding an Xd'' field to this class
            2. Reading it from the data file
            3. Adding a shunt admittance of 1/jXd'' at the generator bus
               in the positive sequence network
    """

    def __init__(self, zone, description, node, P, Q_max, Q_min, V_setpoint):

        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        pass
        # YOUR CODE ENDS HERE


# =============================================================================
# END OF NetworkClasses.py
# =============================================================================
