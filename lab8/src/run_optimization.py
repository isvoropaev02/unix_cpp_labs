from SPB import SPB_CR, SPB_ROADS
from city import City, SimParams
from post_processing import PostProcessor
from random import seed
import numpy as np

MIN_LIGHT_DUR_S = 16
MAX_LIGHT_DUR_S = 41

seed(1)

sim_params = SimParams(
    sim_duration=600,
    delta_t=3,
    car_spawn_rate=6,
    car_route_length=25,
    num_initial_cars=400,
    en_city_plot=False,
)


def rand_search_duration(
    sim_params: SimParams, num_iter: int = 20
) -> tuple[float, np.ndarray]:
    city_model = City(nodes=SPB_CR, roads=SPB_ROADS, cars={}, sim_params=sim_params)
    out_durations = np.zeros(shape=(len(SPB_CR),), dtype=np.int32)
    min_t_erasure = sim_params.sim_duration
    for _ in range(num_iter):
        city_model.reset_cars()
        durations_s = np.random.randint(
            low=MIN_LIGHT_DUR_S,
            high=(MAX_LIGHT_DUR_S + 1),
            size=len(SPB_CR),
            dtype=np.int32,
        )
        city_model.customize_nodes_traffic_lights(durations_s)
        time_vec, road_states = city_model.run_simulation()
        post_proc = PostProcessor(time_vec, road_states, threshold=25)
        t_erasure = post_proc.get_t_erasure(en_plot=False)
        if t_erasure < min_t_erasure:
            min_t_erasure = t_erasure
            out_durations = durations_s
    return min_t_erasure, out_durations
