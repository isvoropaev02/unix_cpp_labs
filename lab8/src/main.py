from SPB import SPB_CR, SPB_ROADS
from city import City, SimParams
from random import seed
import numpy as np

seed(1)

sim_params = SimParams(
    sim_duration=600,
    delta_t=3,
    car_spawn_rate=6,
    car_route_length=25,
    num_initial_cars=400,
    en_city_plot=False,
)
city_model = City(nodes=SPB_CR, roads=SPB_ROADS, cars={}, sim_params=sim_params)

time_vec, road_states = city_model.run_simulation()


def calculate_mean_load(road_load_sample: np.ndarray) -> np.ndarray:
    return np.round(np.mean(np.sum(road_load_sample, axis=2), axis=0), 1)


def get_roads_with_most_load_at_the_start(road_load_sample: np.ndarray) -> np.ndarray:
    return np.argsort(np.sum(road_load_sample[0], axis=1))[-10:][::-1]


print("most start load ids:\n", get_roads_with_most_load_at_the_start(road_states))
print("mean load:\n", calculate_mean_load(road_states))
