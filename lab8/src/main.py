from SPB import SPB_CR, SPB_ROADS
from city import City, SimParams
from post_processing import PostProcessor
from random import seed
import numpy as np
import matplotlib.pyplot as plt

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

post_proc = PostProcessor(time_vec, road_states, threshold=25)
post_proc.plot_report()
post_proc.calculate_mean_load(en_plot=True)
