from city_elements import *
from vehicle_generator import VehicleGenerator
from SPB import SPB_CR, SPB_ROADS
from city_plots import plot_spb_map_with_traffic
from datetime import timedelta
from random import seed
import numpy as np
import matplotlib.pyplot as plt

"""Simulation configuration"""
seed(0)
CROSS_ROADS = SPB_CR
ROADS = SPB_ROADS
CARS = dict()
SIM_DURATION = 600  # sec
DELTA_T = 3  # sec
CAR_SPAWN_RATE = 100 * DELTA_T  # every x seconds a new car appears
CAR_ROUTE_LENGHT = 25  # num of roads in route
JAM_THRESHOLD = 35  # % from all active cars


def get_cars_coords(
    cross_roads: list[CrossRoad], roads: list[Road], cars: dict[int, Vehicle]
) -> list[list[float]]:
    out_coords = []
    offset = 10
    for car in cars.values():
        direct_flow = car.curr_road_direct_flow
        road_tmp = roads[car.curr_road_id]
        cr0 = cross_roads[road_tmp.node_from_id]
        cr1 = cross_roads[road_tmp.node_to_id]
        if not direct_flow:
            cr0, cr1 = cr1, cr0
        n_vec = np.array([cr1.y - cr0.y, cr0.x - cr1.x], dtype=np.float32)
        full_dist = np.linalg.norm(n_vec)
        n_vec = offset * n_vec / full_dist
        xr = car.remaining_dist * (cr1.x - cr0.x) / full_dist
        yr = car.remaining_dist * (cr1.y - cr0.y) / full_dist
        out_coords.append(list([cr1.x - xr + n_vec[0], cr1.y - yr + n_vec[1]]))
    return out_coords


"""Simulation variables"""
next_car_id = 0
time_vec = np.arange(0, SIM_DURATION, step=DELTA_T, dtype=np.int32)
roads_state_vec = np.empty(shape=(time_vec.shape[0], len(ROADS), 2), dtype=np.int32)
route_gen = VehicleGenerator(CAR_ROUTE_LENGHT)
# initial cars
for _ in range(20):
    CARS.update({next_car_id: route_gen.generate(ROADS, CROSS_ROADS)})
    road_id = CARS[next_car_id].curr_road_id
    direct_flow = CARS[next_car_id].curr_road_direct_flow
    ROADS[road_id].add_car_to_road(next_car_id, direct_flow)
    next_car_id += 1


"""Activating interactive city plot"""
plt.ion()
plot_spb_map_with_traffic(CROSS_ROADS, ROADS, CARS)
fig, ax = plt.gcf(), plt.gca()
sctr_plt = ax.scatter([], [], c="k", marker=".", zorder=3)  # no cars yet
jam_streets_plt = ax.plot([], [], color="red", zorder=2)  # no traffic jams yet
fig.suptitle("Saint-Petersburg")
abs_time = timedelta(hours=14, minutes=15, seconds=0)
ax.set_title("Local time: " + str(abs_time))

for i_time, global_time_s in enumerate(time_vec):
    if global_time_s % CAR_SPAWN_RATE == 0:
        CARS.update({next_car_id: route_gen.generate(ROADS, CROSS_ROADS)})
        road_id = CARS[next_car_id].curr_road_id
        direct_flow = CARS[next_car_id].curr_road_direct_flow
        ROADS[road_id].add_car_to_road(next_car_id, direct_flow)
        next_car_id += 1
    finished_cars_id = list([])
    jam_streets_for_plot = []
    for id, car in CARS.items():
        car.update(DELTA_T)
        ready_to_switch_road = car.ready_to_switch_road
        road_id = car.curr_road_id
        direct_flow = car.curr_road_direct_flow
        road = ROADS[road_id]
        if ready_to_switch_road:
            node_id = road.node_to_id if direct_flow else road.node_from_id
            port_id = road.node_to_port_id if direct_flow else road.node_from_port_id
            tr_light_state = CROSS_ROADS[node_id].get_current_state()
            if tr_light_state[port_id]:
                road.remove_car_from_road(id, direct_flow)
                car.proceed_to_next_step()
                if car.reached_destination:
                    finished_cars_id.append(id)
                else:
                    new_road_id = car.curr_road_id
                    direct_flow = car.curr_road_direct_flow
                    ROADS[new_road_id].add_car_to_road(id, direct_flow)
    for car_id in finished_cars_id:
        CARS.pop(car_id)
    for id, node in enumerate(CROSS_ROADS):
        node.update(DELTA_T)
    for id, road in enumerate(ROADS):
        roads_state_vec[i_time][id][0], roads_state_vec[i_time][id][1] = (
            road.get_road_state()
        )

    sctr_plt.set_offsets(get_cars_coords(CROSS_ROADS, ROADS, CARS))
    ax.set_title(
        "Local time: " + str(abs_time + timedelta(seconds=float(global_time_s)))
    )
    fig.canvas.draw_idle()
    plt.pause(0.2)

plt.ioff()
plt.show()
