from city_elements import *
import numpy as np
from dataclasses import dataclass

@dataclass
class SimParams:
    sim_duration: int = 600      # sec
    delta_t: int = 3             # sec
    car_spawn_rate: int = 100    # every x seconds a new car appears
    car_route_length: int = 25   # num of roads in route
    num_initial_cars: int = 20   # num of cars at the start of simulation
    en_city_plot: bool = False   # enable/disable city plot with moving traffic


class City:
    def __init__(self, nodes: list[CrossRoad], roads: list[Road], cars: dict[int, Vehicle], offset: int = 10) -> None:
        self.cars = cars
        self.nodes = nodes
        self.roads = roads
        self.road_offset = offset

    def get_cars_coords(self) -> list[list[float]]:
        out_coords = []
        offset = 10
        for car in self.cars.values():
            direct_flow = car.curr_road_direct_flow
            road_tmp = self.roads[car.curr_road_id]
            cr0 = self.nodes[road_tmp.node_from_id]
            cr1 = self.nodes[road_tmp.node_to_id]
            if not direct_flow:
                cr0, cr1 = cr1, cr0
            n_vec = np.array([cr1.y-cr0.y, cr0.x-cr1.x], dtype=np.float32)
            full_dist = np.linalg.norm(n_vec)
            n_vec = offset * n_vec / full_dist
            xr = car.remaining_dist * (cr1.x-cr0.x) / full_dist
            yr = car.remaining_dist * (cr1.y-cr0.y) / full_dist
            out_coords.append(list([cr1.x-xr + n_vec[0], cr1.y-yr+n_vec[1]]))
        return out_coords

    def get_road_load_percentage(self) -> list[list[float]]:
        road_load_percentage = len(self.roads)*[[0.0, 0.0]]
        total_active_cars = len(self.cars)
        for i, road in enumerate(self.roads):
            dir_num_cars, inv_num_cars = road.get_road_state()
            road_load_percentage[i] = [dir_num_cars/total_active_cars*100, inv_num_cars/total_active_cars*100]
        return road_load_percentage
        
    def init_simulation(self) -> None:
        return
    
    def run_simulation(self):
        return
