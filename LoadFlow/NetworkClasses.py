# =============================================================================
# NetworkClasses.py
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
# Power System Network — Class Definitions
# =============================================================================
# DESCRIPTION:
#   This file defines all the data classes used to represent elements of the
#   power system network. It is imported by Reading.py and all subsequent
#   analysis modules.
#
#   Classes defined here:
#       Bus              - Represents a network bus node
#       Transformer      - Represents a transformer branch
#       TransmissionLine - Represents a transmission line branch
#       ShuntReactor     - Represents a shunt reactor element
#       Load             - Represents a load at a bus
#       Generator        - Represents a generator at a bus
# =============================================================================

import cmath  # For complex number operations (used in voltage initialization)


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
        Code        : Record identifier (always 'BS')
        Zone        : Zone number (integer)
        Description : 8-character bus name/label (string)
        Node        : Bus node number (integer)
        Voltage     : Nominal voltage level in kV (float)
    """

    def __init__(self, zone, description, node, voltage):

        # YOUR CODE STARTS HERE
        # Define the attributes of the Bus class using the parameters above.
        # Each parameter corresponds to a field parsed from the data file.
        # Example: self.zone = zone

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the Bus object.
        # Example format: "Bus <node>: <description> | Zone: <zone> | Voltage: <voltage> kV"

        pass  # Remove this line once you add your return statement

        # YOUR CODE ENDS HERE

    # -------------------------------------------------------------------------

    def initialize_voltage(self, generators, slack_node):
        """
        Initializes the complex voltage at this bus for the load flow iteration.

        Bus Types in Load Flow Analysis:
        ---------------------------------
          Slack Bus (Reference Bus):
              - Voltage magnitude and angle are both fixed (|V| = 1.0, angle = 0°).
              - There is exactly ONE slack bus in the network (typically node 1).
              - It absorbs all real and reactive power mismatches in the system.

          PV Bus (Generator Bus):
              - A generator is connected to this bus.
              - Voltage MAGNITUDE is fixed (from generator's V_setpoint).
              - Voltage ANGLE is initially set to 0° (will be updated by Newton-Raphson).
              - Real power P is scheduled (known).

          PQ Bus (Load Bus):
              - No generator is connected to this bus.
              - Both P and Q are known (from load data).
              - Voltage magnitude and angle are both unknown — to be solved.
              - Initial guess: |V| = 1.0, angle = 0°  →  V = 1 + 0j (flat start).

        Parameters:
        -----------
            generators  : list of Generator objects (parsed from the data file)
            slack_node  : integer node number of the slack bus

        What this method should do:
        ----------------------------
            1. Check if this bus is the slack bus (compare self.node to slack_node).
               If yes, set self.V = 1.0 + 0j  and  self.bus_type = 'Slack'.

            2. Otherwise, check if any Generator in the generators list is connected
               to this bus (i.e., generator.node == self.node).
               If yes, this is a PV bus:
                   - Set self.V using the generator's V_setpoint as the magnitude
                     and an initial angle of 0°.
                   - Set self.bus_type = 'PV'.

            3. If neither of the above, this is a PQ bus:
               - Set self.V = 1.0 + 0j  (flat start).
               - Set self.bus_type = 'PQ'.

        Hint — Creating a complex voltage from polar form:
        ---------------------------------------------------
            V = |V| * e^(j*angle)  can be written in Python as:
            V = cmath.rect(magnitude, angle_in_radians)
            For a flat start: cmath.rect(1.0, 0.0) = (1+0j)

        Output:
        -------
            After calling this method, each Bus object should have:
                self.V         : complex voltage (initial guess)
                self.bus_type  : string — 'Slack', 'PV', or 'PQ'
        """

        # YOUR CODE STARTS HERE
        # Use the steps described above to set self.V and self.bus_type.
        # You may add helper variables as needed.

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
        Code        : Record identifier (always 'TR')
        Zone        : Zone number (integer)
        Description : 8-character transformer label (string)
        From Node   : Sending end bus node number (integer)
        To Node     : Receiving end bus node number (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
        Tap         : Tap ratio (float)
        Max Loading : Maximum loading in MVA (float)
    """

    def __init__(self, zone, description, from_node, to_node, r, x, tap, max_loading):

        # YOUR CODE STARTS HERE
        # Define the attributes of the Transformer class using the parameters above.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the Transformer object.

        pass  # Remove this line once you add your return statement

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
        Code        : Record identifier (always 'TL')
        Zone        : Zone number (integer)
        Description : 8-character line label (string)
        From Node   : Sending end bus node number (integer)
        To Node     : Receiving end bus node number (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
        B_half      : Half line charging susceptance in per unit (float)
        Max Loading : Maximum loading in MVA (float)
    """

    def __init__(self, zone, description, from_node, to_node, r, x, b_half, max_loading):

        # YOUR CODE STARTS HERE
        # Define the attributes of the TransmissionLine class using the parameters above.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the TransmissionLine object.

        pass  # Remove this line once you add your return statement

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
        Code        : Record identifier (always 'DZ')
        Zone        : Zone number (integer)
        Description : 8-character reactor label (string)
        Node        : Bus node number where reactor is connected (integer)
        R           : Resistance in per unit (float)
        X           : Reactance in per unit (float)
    """

    def __init__(self, zone, description, node, r, x):

        # YOUR CODE STARTS HERE
        # Define the attributes of the ShuntReactor class using the parameters above.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the ShuntReactor object.

        pass  # Remove this line once you add your return statement

        # YOUR CODE ENDS HERE


# =============================================================================
# LOAD CLASS
# =============================================================================

class Load:
    """
    Represents a Load connected to a bus in the power system network.

    Record Format:
        DP   <zone>  <description>  <node>  <P>  <Q>  <compensation>

    Example:
        DP   1  HYD-220    5   430.0  170.00  0.00

    Fields:
        Code         : Record identifier (always 'DP')
        Zone         : Zone number (integer)
        Description  : 8-character load label (string)
        Node         : Bus node number where load is connected (integer)
        P            : Active power demand in MW (float)
        Q            : Reactive power demand in MVAR (float)
        Compensation : Capacitive compensation in MVAR (float)
    """

    def __init__(self, zone, description, node, P, Q, compensation):

        # YOUR CODE STARTS HERE
        # Define the attributes of the Load class using the parameters above.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the Load object.

        pass  # Remove this line once you add your return statement

        # YOUR CODE ENDS HERE


# =============================================================================
# GENERATOR CLASS
# =============================================================================

class Generator:
    """
    Represents a Generator connected to a bus in the power system network.

    Record Format:
        GP   <zone>  <description>  <node>  <P>  <Q_max>  <Q_min>  <V_setpoint>

    Example:
        GP  11  RMG        1  1820.0   950.0  -150.0     1.0

    Fields:
        Code       : Record identifier (always 'GP')
        Zone       : Zone number (integer)
        Description: 8-character generator label (string)
        Node       : Bus node number where generator is connected (integer)
        P          : Scheduled active power output in MW (float)
        Q_max      : Maximum reactive power output in MVAR (float)
        Q_min      : Minimum reactive power output in MVAR (float)
        V_setpoint : Voltage set point in per unit (float)
    """

    def __init__(self, zone, description, node, P, Q_max, Q_min, V_setpoint):

        # YOUR CODE STARTS HERE
        # Define the attributes of the Generator class using the parameters above.

        pass  # Remove this line once you add your attributes

        # YOUR CODE ENDS HERE

    def __repr__(self):
        # YOUR CODE STARTS HERE
        # Return a readable string representation of the Generator object.

        pass  # Remove this line once you add your return statement

        # YOUR CODE ENDS HERE


# =============================================================================
# END OF NetworkClasses.py
# =============================================================================
