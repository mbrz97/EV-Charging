# Electric Vehicle Charging Simulation

This simulation models an environment where electric vehicles (EVs) interact with charging stations connected to electrical breakers. It aims to explore the dynamics of EV charging, including the consumption of electrical power and the availability of chargers under varying conditions.

## Components

### `BuildingEnvironment` (Model)

- **Purpose**: Serves as the main environment for the simulation, containing EV chargers, electric vehicles (EVs), and electrical breakers.
- **Key Features**:
  - Initializes the simulation with a specified number of EV chargers, EVs, and breakers.
  - Distributes chargers across breakers and manages the scheduling of all agents (EVs and chargers).
  - Collects data on total power consumption, active chargers, and instances where EVs cannot find an available charger.

### `ElectricVehicle` (Agent)

- **Purpose**: Represents an individual electric vehicle within the simulation.
- **Key Features**:
  - Consumes power daily, simulating daily vehicle use.
  - Seeks charging when its battery level falls below a set threshold.
  - Records the amount of power consumed when charging.

### `EVCharger` (Agent)

- **Purpose**: Represents a charging station for electric vehicles.
- **Key Features**:
  - Can be available or unavailable, depending on whether it is currently charging an EV.
  - Adjusts its charging power based on the capacity of the connected electrical breaker.
  - Charges connected EVs and tracks the charging process.

### `ElectricalPanel` (Agent)

- **Note**: This class is defined but not utilized in the provided code. It could represent a collection of electrical breakers in more complex simulations.

## Data Collection

The simulation collects and reports on the following metrics:
- **Total Consumption**: The sum of power consumed by all EVs.
- **Active Chargers**: The count of chargers currently in use.
- **Unavailable Charger Events**: The number of times an EV attempted to find a charger but none were available.

## Running the Simulation

To run the simulation, execute the `run_simulation` function, which sets up the simulation environment and launches a web server for visualization. Users can interact with the simulation through a web-based interface, adjusting parameters like the number of EVs, chargers, and breakers before running the simulation to observe different scenarios.

## Customization

Users can customize the simulation by adjusting the initial parameters and modifying the behavior of EVs and chargers. This includes changing the daily power consumption of EVs, the capacity of chargers, and how chargers are allocated among electrical breakers.
