from road_elements import *

'''Simulation configuration'''
CROSS_ROADS = {0: CrossRoad(coords=(0, 0), tr_light_duration_s=20.),
               1: CrossRoad(coords=(300., 0.), tr_light_duration_s=15)}
ROADS = {0: Road((0, 0), (1, 0))}
CARS = dict()
CAR_SPAWN_RATE = 10      # every x seconds a new car appears
SIM_DURATION = 120      # sec
DELTA_T = 1             # sec

'''Simulation variables'''
global_time_s = 0
next_car_id = 0

while global_time_s < SIM_DURATION:
    print(f"GLOBAL TIME: {global_time_s} sec")
    if global_time_s % CAR_SPAWN_RATE == 0:
        if bool(next_car_id%2):
            CARS.update({next_car_id: Vehicle([1, 0], [(0, False, 300.)], 20)})
        else:
            CARS.update({next_car_id: Vehicle([0, 1], [(0, True, 300.)], 25)})
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
                    road_id = car.curr_road_id
                    direct_flow = car.curr_road_direct_flow
                    road.add_car_to_road(id, direct_flow)
    for car_id in finished_cars_id:
        CARS.pop(car_id)
    for id, node in CROSS_ROADS.items():
        print(f"node id: {id}  |  state: {node.get_current_state()}")
        node.update(DELTA_T)
    for id, road in ROADS.items():
        print(f"road id: {id}  |  state: {road.get_road_state()}")
    print()
    global_time_s += DELTA_T
