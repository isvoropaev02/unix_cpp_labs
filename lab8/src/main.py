from SPB import SPB_CR, SPB_ROADS
from city import City, SimParams
from random import seed
from typing import List
import numpy as np

seed(0)

sim_params = SimParams(
    sim_duration=600,
    delta_t=3,
    car_spawn_rate=6,
    car_route_length=25,
    num_initial_cars=100,
    en_city_plot=False,
)
city_model = City(nodes=SPB_CR, roads=SPB_ROADS, cars={}, sim_params=sim_params)

time_vec, road_states = city_model.run_simulation()


def calculate_inhomogenity_metric(road_load_sample: np.ndarray) -> float:
    most_loads = np.sort(road_load_sample.flatten())[-5:][::-1]
    return most_loads[-1] / most_loads[0] if most_loads[0] != 0 else 0.0


inhomogenity_metric_vec = np.array(
    [calculate_inhomogenity_metric(road_states[i]) for i in range(road_states.shape[0])]
)
print(inhomogenity_metric_vec)
