import mesa
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import Slider, Checkbox, Choice, NumberInput, StaticText


class BuildingEnvironment(Model):
    def __init__(self, N_ev_chargers, N_evs, N_breakers):
        super().__init__()
        choices = [20, 30, 40, 50, 60]
        self.breaker_capacity = [random.choice(choices) for _ in range(N_breakers)]
        self.num_agents = N_evs
        self.schedule = RandomActivation(self)

        # Initialize breakers
        self.breakers = [{'capacity': cap, 'chargers': []} for cap in self.breaker_capacity]

        # Initialize chargers and assign them to breakers
        self.chargers = []
        for i in range(N_ev_chargers):
            selected_breaker_index = random.randint(0, N_breakers - 1)
            charger = EVCharger(i, self, random.randint(6, 48), selected_breaker_index)
            self.chargers.append(charger)
            # Add charger to the selected breaker's list
            self.breakers[selected_breaker_index]['chargers'].append(charger)
            self.schedule.add(charger)

        # Initialize EVs
        self.evs = [ElectricVehicle(i, self, random.uniform(50, 100)) for i in range(N_evs)]
        for ev in self.evs:
            self.schedule.add(ev)

        self.unavailable_charger_events = 0
        self.datacollector = DataCollector(
            model_reporters={
                "Total Consumption": lambda m: sum([ev.power_consumed for ev in m.evs]),
                "Active Chargers": lambda m: sum([1 for c in m.chargers if not c.availability]),
                "Unavailable Charger Events": lambda m: m.unavailable_charger_events  # Track unavailable charger events
            }
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def register_unavailable_charger_event(self):
        self.unavailable_charger_events += 1

    def adjust_charger_power(self):
        # Loop through each breaker
        for breaker in self.breakers:
            if breaker['chargers']:  # Check if there are chargers connected to this breaker
                # Evenly divide breaker's capacity among its chargers
                amperage_per_charger = breaker['capacity'] / len(breaker['chargers'])
                for charger in breaker['chargers']:
                    charger.adjust_charging_power(amperage_per_charger)


class ElectricalPanel(Agent):
    def __init__(self, unique_id, model, num_breakers, breakers_capacity):
        super().__init__(unique_id, model)
        self.num_breakers = num_breakers
        self.breakers_capacity = breakers_capacity


class ElectricVehicle(Agent):
    def __init__(self, unique_id, model, battery_capacity):
        super().__init__(unique_id, model)
        self.power_consumed = 0
        self.battery_capacity = battery_capacity
        self.charging_status = False

        self.charge_level = random.uniform(0.2,
                                           1.0) * battery_capacity  # Initial charge level as a percentage of capacity
        self.charging_status = False

    def step(self):
        if not self.charging_status:
            self.daily_use()
        if self.needs_charging() and not self.charging_status:
            self.start_charging()

    def start_charging(self):
        # Attempt to find and start charging with an available charger
        available_charger = self.find_available_charger()
        if available_charger:
            available_charger.activate_charger(self)
            self.charging_status = True
            self.power_consumed = self.battery_capacity - self.charge_level
        else:
            self.model.register_unavailable_charger_event()

    def stop_charging(self):
        self.charging_status = False

    def daily_use(self):
        # Simulate daily consumption based on kilometers driven and efficiency

        variable = random.uniform(0, 100)

        # Assuming efficiency of 5 km/kWh
        daily_km_rand = variable / 5

        consumption = daily_km_rand
        self.charge_level -= consumption
        if self.charge_level < 0:
            self.charge_level = 0

    def needs_charging(self):
        # Assume the vehicle needs charging if below 80% capacity
        return self.charge_level < 0.7 * self.battery_capacity

    def find_available_charger(self):
        for charger in self.model.chargers:
            if charger.availability:
                return charger
        return None


class EVCharger(Agent):
    def __init__(self, unique_id, model, connected_breaker, charging_power=48):
        super().__init__(unique_id, model)
        self.availability = True
        self.connected_ev = None
        self.initial_charging_power = charging_power  # Store the initial charging power
        self.current_charging_power = charging_power  # Current charging power, to be adjusted
        self.connected_breaker_index = connected_breaker  # Store index of connected breaker

    def activate_charger(self, ev):
        if self.availability:
            self.availability = False
            self.connected_ev = ev
            self.model.adjust_charger_power()

    def adjust_charging_power(self, new_power):
        # Adjust the charger's current charging power
        self.current_charging_power = new_power

    def deactivate_charger(self):
        if self.connected_ev:
            self.connected_ev.stop_charging()
        self.availability = True
        self.connected_ev = None
        self.model.adjust_charger_power()

    def charge_ev(self):

        # Assuming a constant voltage of 240 volts for Level 2 charging
        charge_amount = self.current_charging_power * 240 / 1000  # kW
        self.connected_ev.charge_level += charge_amount
        if self.connected_ev.charge_level >= self.connected_ev.battery_capacity:
            self.connected_ev.charge_level = self.connected_ev.battery_capacity
            self.deactivate_charger()  # Correctly deactivate the charger

    def step(self):
        # if self.connected_ev and not self.availability:
        #     self.charge_ev()
        if self.connected_ev and not self.availability:
            self.charge_ev()
        elif not self.connected_ev and not self.availability:
            # If the charger is not available but no EV is connected, reset availability
            self.availability = True


from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer


def run_simulation():
    # Setup parameters

    total_consumption_chart = ChartModule(
        [{"Label": "Total Consumption", "Color": "Black"}],
        data_collector_name='datacollector'
    )

    active_chargers_chart = ChartModule(
        [{"Label": "Active Chargers", "Color": "Blue"}],
        data_collector_name='datacollector'
    )

    unavailable_charger_chart = ChartModule(
        [{"Label": "Unavailable Charger Events", "Color": "Red"}],
        data_collector_name='datacollector'
    )

    # Define model parameters for the user interface, if not already done
    model_params = {
        "N_ev_chargers": Slider("Number of EV Chargers", 10, 1, 20, 1),
        "N_evs": Slider("Number of EVs", 20, 1, 50, 1),
        "N_breakers": NumberInput("Number of Breakers", value=5),
    }

    N_ev_chargers = 10  # Example starting value
    N_evs = 20
    N_breakers = 5
    breaker_capacity = [20, 30, 30, 40, 50]  # Example capacities

    # Initialize and run the model
    model = BuildingEnvironment(N_ev_chargers, N_evs, N_breakers)
    for i in range(100):  # Run for 100 days, for example
        model.step()

    # Visualization setup
    server = ModularServer(BuildingEnvironment,
                           [total_consumption_chart, active_chargers_chart, unavailable_charger_chart],
                           "EV Charging Simulation",
                           model_params)

    server.port = 8520  # The default
    server.launch()


if __name__ == "__main__":
    run_simulation()
