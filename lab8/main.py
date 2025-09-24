from city_elements import *
from vehicle_route_generator import VehicleGenerator
from SPB import SPB_CR, SPB_ROADS
from city_plots import plot_spb_map_with_traffic

import numpy as np
import matplotlib.pyplot as plt


'''Simulation configuration'''
CROSS_ROADS = SPB_CR
ROADS = SPB_ROADS
CARS = dict()
SIM_DURATION = 600      # sec
DELTA_T = 4             # sec
CAR_SPAWN_RATE = 1 * DELTA_T  # every x seconds a new car appears
CAR_ROUTE_LENGHT = 14    # num of roads in route


'''Simulation variables'''
global_time_s = 0
next_car_id = 0
time_vec = np.arange(0, SIM_DURATION, step=DELTA_T, dtype=np.int32)
roads_state_vec = np.empty(
    shape=(time_vec.shape[0], len(ROADS), 2), dtype=np.int32)

route_gen = VehicleGenerator(CAR_ROUTE_LENGHT)

for i_time, global_time_s in enumerate(time_vec):
    print(f"GLOBAL TIME: {global_time_s} sec")
    if global_time_s % CAR_SPAWN_RATE == 0:
        CARS.update({next_car_id: route_gen.generate(ROADS, CROSS_ROADS)})
        road_id = CARS[next_car_id].curr_road_id
        direct_flow = CARS[next_car_id].curr_road_direct_flow
        ROADS[road_id].add_car_to_road(next_car_id, direct_flow)
        next_car_id += 1
    finished_cars_id = list([])
    for id, car in CARS.items():
        print(
            f"car id: {id}  |  step_id: {car.path_step_id}  |  remaining dist: {car.remaining_dist}")
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
        print(f"node id: {id}  |  state: {node.get_current_state()}")
        node.update(DELTA_T)
    for id, road in enumerate(ROADS):
        print(f"road id: {id}  |  state: {road.get_road_state()}")
        roads_state_vec[i_time][id][0], roads_state_vec[i_time][id][1] = road.get_road_state()
    print()


plot_spb_map_with_traffic(CROSS_ROADS, ROADS, CARS)
