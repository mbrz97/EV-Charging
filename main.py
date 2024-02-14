import mesa
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random


class BuildingEnvironment(Model):
    def __init__(self, N_ev_chargers, N_evs, growth_rate, initial_ev_owners, N_breakers, breaker_capacity):
        super().__init__()
        self.num_agents = N_evs
        self.schedule = RandomActivation(self)
        self.growth_rate = growth_rate
        # Initialize breakers
        self.breakers = [{'capacity': cap, 'connected_load': 0} for cap in breaker_capacity]
        # Initialize chargers and assign them to breakers in a round-robin fashion
        self.chargers = [EVCharger(i, self, random.randint(6, 48), self.breakers[i % N_breakers]['capacity']) for i in
                         range(N_ev_chargers)]
        for charger in self.chargers:
            self.schedule.add(charger)
        # Initialize EVs
        self.evs = [ElectricVehicle(i, self, random.uniform(50, 100), random.uniform(0.2, 0.4)) for i in range(N_evs)]
        for ev in self.evs:
            self.schedule.add(ev)
        self.datacollector = DataCollector(
            agent_reporters={"Charge Level": "charge_level"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def adjust_load_balancing(self):
        for breaker in self.breakers:
            # Find all chargers connected to this breaker
            connected_chargers = [c for c in self.chargers if c.connected_breaker == breaker and not c.availability]
            if not connected_chargers:
                continue
            # Calculate available amperage for this breaker
            total_available_amperage = breaker['capacity'] - sum(c.current_charging_power for c in connected_chargers)
            if total_available_amperage < 0:
                total_available_amperage = 0
            # Evenly distribute available amperage among active chargers
            if len(connected_chargers) > 0:
                allocated_amperage = total_available_amperage / len(connected_chargers)
                for charger in connected_chargers:
                    charger.current_charging_power = min(charger.initial_charging_power, allocated_amperage)


class ElectricalPanel(Agent):
    def __init__(self, unique_id, model, num_breakers, breakers_capacity):
        super().__init__(unique_id, model)
        self.num_breakers = num_breakers
        self.breakers_capacity = breakers_capacity


class ElectricVehicle(Agent):
    def __init__(self, unique_id, model, battery_capacity, daily_km):
        super().__init__(unique_id, model)
        self.battery_capacity = battery_capacity
        # Assume a fixed consumption rate per km
        self.consumption_rate = 0.2  # kWh per km
        self.daily_km = daily_km
        self.charge_level = random.uniform(0.2, 1.0) * battery_capacity  # Initial charge level as a percentage of capacity
        self.charging_status = False

    def step(self):
        self.daily_use()
        if self.needs_charging():
            self.start_charging()

    def start_charging(self):
        if not self.charging_status:
            self.charging_status = True
            # Find an available charger and initiate charging
            for charger in self.model.chargers:
                if charger.availability:
                    charger.activate_charger(self)
                    break

    def stop_charging(self):
        self.charging_status = False

    def daily_use(self):
        # Simulate daily consumption
        consumption = self.daily_km * self.consumption_rate
        self.charge_level -= consumption
        if self.charge_level < 0:
            self.charge_level = 0

    def needs_charging(self):
        # Assume the vehicle needs charging if below 20% capacity
        return self.charge_level < 0.2 * self.battery_capacity

class EVCharger(Agent):
    def __init__(self, unique_id, model, charging_power, connected_breaker):
        super().__init__(unique_id, model)
        self.availability = True
        self.initial_charging_power = charging_power
        self.current_charging_power = charging_power  # This may change due to dynamic load balancing
        self.connected_breaker = connected_breaker
        self.connected_ev = None

    def activate_charger(self, ev):
        if self.availability:
            self.availability = False
            self.connected_ev = ev
            self.model.adjust_load_balancing()

    def deactivate_charger(self):
        self.availability = True
        self.connected_ev = None
        self.model.adjust_load_balancing()

    def charge_ev(self):
        # Assuming a constant voltage of 240 volts for Level 2 charging
        charge_amount = self.current_charging_power * 240 / 1000  # kW
        self.connected_ev.charge_level += charge_amount
        if self.connected_ev.charge_level > self.connected_ev.battery_capacity:
            self.connected_ev.charge_level = self.connected_ev.battery_capacity
            self.deactivate_charger()

    def step(self):
        if self.connected_ev and not self.availability:
            self.charge_ev()



from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer

def run_simulation():
    # Setup parameters
    N_ev_chargers = 10  # Example starting value
    N_evs = 20
    growth_rate = 0.05
    initial_ev_owners = 5
    N_breakers = 5
    breaker_capacity = [20, 30, 30, 40, 50]  # Example capacities

    # Initialize and run the model
    model = BuildingEnvironment(N_ev_chargers, N_evs, growth_rate, initial_ev_owners, N_breakers, breaker_capacity)
    for i in range(100):  # Run for 100 days, for example
        model.step()

    # Visualization setup here (e.g., using ChartModule for daily consumption and bottleneck visualization)

if __name__ == "__main__":
    run_simulation()

    def __init__(self, N_ev_chargers, N_evs, growth_rate, initial_ev_owners, N_breakers, breaker_capacity):
        # Previous initialization code
        self.datacollector = DataCollector(
            model_reporters={
                "Total Consumption": lambda m: sum([ev.charge_level for ev in m.evs]),
                "Active Chargers": lambda m: sum([1 for c in m.chargers if not c.availability])
            }
        )


    total_consumption_chart = ChartModule(
        [{"Label": "Total Consumption", "Color": "Black"}],
        data_collector_name='datacollector'
    )

    active_chargers_chart = ChartModule(
        [{"Label": "Active Chargers", "Color": "Blue"}],
        data_collector_name='datacollector'
    )


    from mesa.visualization.ModularVisualization import ModularServer

    def run_simulation():
        # Setup parameters as before

        # Initialize and run the model as before

        # Visualization setup
        server = ModularServer(
            BuildingEnvironment,
            [total_consumption_chart, active_chargers_chart],
            "EV Charging Simulation",
            {"N_ev_chargers": 10, "N_evs": 20, "growth_rate": 0.05, "initial_ev_owners": 5, "N_breakers": 5, "breaker_capacity": [20, 30, 30, 40, 50]}
        )
        server.port = 8521  # The default
        server.launch()
