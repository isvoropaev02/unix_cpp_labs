from road_elements import *
from vehicle_route_generator import VehicleGenerator

'''Simulation configuration'''
CROSS_ROADS = {0: CrossRoad(coords=(0, 0), road_id_vs_ports=[0, 1, -1, -1], tr_light_duration_s=20.),
               1: CrossRoad(coords=(0., 300.), road_id_vs_ports=[0, 2, -1, -1], tr_light_duration_s=15),
               2: CrossRoad(coords=(400., 300.), road_id_vs_ports=[1, 2, 3, 4], tr_light_duration_s=22),
               3: CrossRoad(coords=(450., 500.), road_id_vs_ports=[3, 5, -1, -1], tr_light_duration_s=18),
               4: CrossRoad(coords=(600., 300.), road_id_vs_ports=[5, 4, -1, -1], tr_light_duration_s=27)}
ROADS = {0: Road((0, 0), (1, 0)),
         1: Road((0, 1), (2, 0)),
         2: Road((1, 1), (2, 1)),
         3: Road((2, 2), (3, 0)),
         4: Road((2, 3), (4, 1)),
         5: Road((3, 1), (4, 0))}
CARS = dict()
CAR_SPAWN_RATE = 20     # every x seconds a new car appears
CAR_ROUTE_LENGHT = 4    # num of roads in route
SIM_DURATION = 120      # sec
DELTA_T = 1             # sec

'''Simulation variables'''
global_time_s = 0
next_car_id = 0

route_gen = VehicleGenerator(CAR_ROUTE_LENGHT)

while global_time_s < SIM_DURATION:
    print(f"GLOBAL TIME: {global_time_s} sec")
    if global_time_s % CAR_SPAWN_RATE == 0:
        CARS.update({next_car_id: route_gen.generate(ROADS, CROSS_ROADS)})
        road_id = CARS[next_car_id].curr_road_id
        direct_flow = CARS[next_car_id].curr_road_direct_flow
        ROADS[road_id].add_car_to_road(next_car_id, direct_flow)
        next_car_id += 1
    finished_cars_id = list([])
    for id, car in CARS.items():
        print(f"car id: {id}  |  step_id: {car.path_step_id}  |  remaining dist: {car.remaining_dist}")
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
    for id, node in CROSS_ROADS.items():
        print(f"node id: {id}  |  state: {node.get_current_state()}")
        node.update(DELTA_T)
    for id, road in ROADS.items():
        print(f"road id: {id}  |  state: {road.get_road_state()}")
    print()
    global_time_s += DELTA_T
