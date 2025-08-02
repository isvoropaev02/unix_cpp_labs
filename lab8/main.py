from road_elements import *

'''Simulation configuration'''
CROSS_ROADS = {0: CrossRoad(coords=(0, 0), tr_light_duration_s=20.),
               1: CrossRoad(coords=(300., 0.), tr_light_duration_s=15)}
ROADS = {0: Road((0, 0), (1, 0))}
CARS = dict()
CAR_SPAWN_RATE = 6      # every x seconds a new car appears
SIM_DURATION = 120      # sec
DELTA_T = 1             # sec

'''Simulation variables'''
global_time_s = 0
car_id = 0

while global_time_s < SIM_DURATION:
    if global_time_s % CAR_SPAWN_RATE == 0:
        CARS.update({car_id: Vehicle([0, 1], [(0, True, 300.)], 20)})
        car_id += 1
    for id, car in CARS.items():
        car.update(DELTA_T)
        ROADS[car.curr_road_id].add_car_to_road
