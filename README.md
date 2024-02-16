# EV Charging Simulation Documentation

## Overview

This code represents a simulation of an electric vehicle (EV) charging environment using the Mesa framework for Python. It models a building environment with a specified number of electric vehicle chargers, electric vehicles (EVs), and electrical breakers with varying capacities. The simulation's main objectives are to manage the charging process, allocate power efficiently among chargers, and track power consumption and charger availability.

![Charts](/chart/figure.png "Example Charts")


## Key Components

### `BuildingEnvironment` (Model)

#### Purpose
Represents the main simulation model, integrating all components (EVs, chargers, and breakers) and managing their interactions.

#### Key Attributes
- `breaker_capacity`: A list containing the capacity (in amperes) for each breaker.
- `num_agents`: The number of EVs in the simulation.
- `schedule`: A Mesa `RandomActivation` scheduler to activate agents in a random order each step.
- `breakers`: A list of dictionaries, each representing a breaker with a specific capacity and associated chargers.
- `chargers`: A list of `EVCharger` agents.
- `evs`: A list of `ElectricVehicle` agents.
- `unavailable_charger_events`: A counter for tracking how often EVs cannot find an available charger.
- `datacollector`: A Mesa `DataCollector` for gathering and storing simulation data.

#### Key Methods
- `__init__`: Initializes the model, creating breakers, chargers, and EVs based on input parameters.
- `step`: Advances the model by one step, collecting data and updating the state of all agents.
- `register_unavailable_charger_event`: Increments the counter for unavailable charger events.
- `adjust_charger_power`: Adjusts the power allocated to each charger based on the capacity of its connected breaker.

### `ElectricVehicle` (Agent)

#### Purpose
Represents an electric vehicle within the simulation, with its own battery capacity and charging needs.

#### Key Attributes
- `battery_capacity`: The total battery capacity of the EV.
- `power_consumed`: The amount of power consumed by the EV.
- `charging_status`: A boolean indicating whether the EV is currently charging.
- `charge_level`: The current charge level of the EV's battery.

#### Key Methods
- `__init__`: Initializes the EV with a specified battery capacity.
- `step`: Defines the behavior of the EV in each simulation step, including daily use and starting or stopping charging.
- `needs_charging`: Determines whether the EV needs to be charged.
- `start_charging`: Attempts to find an available charger and start charging.
- `stop_charging`: Stops the charging process for the EV.
- `find_available_charger`: Finds an available charger for the EV to use.

### `EVCharger` (Agent)

#### Purpose
Represents an individual charger for electric vehicles.

#### Key Attributes
- `availability`: A boolean indicating whether the charger is currently available.
- `connected_ev`: The `ElectricVehicle` agent (if any) currently connected to the charger.
- `initial_charging_power`: The initial power output of the charger.
- `current_charging_power`: The current power output of the charger, which can be adjusted.
- `connected_breaker_index`: The index of the breaker to which the charger is connected.

#### Key Methods
- `__init__`: Initializes the charger with a specified connected breaker and charging power.
- `activate_charger`: Connects an EV to the charger and starts the charging process.
- `adjust_charging_power`: Adjusts the charger's power output.
- `deactivate_charger`: Disconnects the EV from the charger and makes it available again.
- `charge_ev`: Charges the connected EV based on the current power output.
- `step`: Defines the behavior of the charger in each simulation step.

## Data Collection

### Purpose
Tracks and records simulation data for analysis.

### Collected Metrics
- `Total Consumption`: The sum of the power consumed by all EVs.
- `Active Chargers`: The number of chargers currently in use.
- `Unavailable Charger Events`: The total number of times an EV has attempted to charge but could not find an available charger.

## Visualization

Utilizes Mesa's `ModularServer` and `ChartModule` to provide a web-based visualization of the simulation.

### Charts
- `Total Consumption`: Displays the total electricity consumption over time.
- `Active Chargers`: Shows the number of chargers in use over time.
- `Unavailable Charger Events`: Tracks the occurrences of EVs unable to find an available charger.

## Running the Simulation

### Function: `run_simulation`

#### Purpose
Sets up and launches the Mesa simulation server with specified model parameters and visualization modules.

#### Parameters
Uses sliders and input fields to allow users to adjust the number of EV chargers, EVs, and breakers, as well as the capacities of the breakers.

## Usage

To run the simulation, ensure Mesa is installed in your Python environment, then execute the script. The simulation parameters can be adjusted through the web interface launched by Mesa's server.

## Conclusion

This code provides a comprehensive framework for simulating and visualizing the dynamics of EV charging in a controlled environment. It allows for the exploration of various configurations and their impact on power consumption, charger utilization, and the frequency of unavailable charging opportunities.
