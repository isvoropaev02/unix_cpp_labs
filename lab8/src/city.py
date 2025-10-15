from city_elements import *
from city_plots import plot_spb_map_with_traffic
from vehicle_generator import VehicleGenerator
from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple, List, Dict
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class SimParams:
    sim_duration: int = 600  # sec
    delta_t: int = 3  # sec
    car_spawn_rate: int = 100  # every (x * delta_t) seconds a new car appears
    car_route_length: int = 25  # num of roads in route
    num_initial_cars: int = 20  # num of cars at the start of simulation
    en_city_plot: bool = False  # enable/disable city plot with moving traffic


class City:
    def __init__(
        self,
        nodes: List[CrossRoad],
        roads: List[Road],
        cars: Dict[int, Vehicle],
        sim_params: SimParams,
        offset: int = 10,
    ) -> None:
        self.cars = cars
        self.nodes = deepcopy(nodes)
        self.roads = deepcopy(roads)
        self.road_offset = offset
        self.sim_params = sim_params
        self.next_car_id = 0
        self.route_gen = VehicleGenerator(self.sim_params.car_route_length)
        self.__init_simulation()

    def get_cars_coords(self) -> List[List[float]]:
        out_coords = []
        offset = 10
        for car in self.cars.values():
            direct_flow = car.curr_road_direct_flow
            road_tmp = self.roads[car.curr_road_id]
            cr0 = self.nodes[road_tmp.node_from_id]
            cr1 = self.nodes[road_tmp.node_to_id]
            if not direct_flow:
                cr0, cr1 = cr1, cr0
            n_vec = np.array([cr1.y - cr0.y, cr0.x - cr1.x], dtype=np.float32)
            full_dist = np.linalg.norm(n_vec)
            n_vec = offset * n_vec / full_dist
            xr = car.remaining_dist * (cr1.x - cr0.x) / full_dist
            yr = car.remaining_dist * (cr1.y - cr0.y) / full_dist
            out_coords.append(list([cr1.x - xr + n_vec[0], cr1.y - yr + n_vec[1]]))
        return out_coords

    # legacy
    def __get_road_load_percentage(self) -> List[List[float]]:
        road_load_percentage = len(self.roads) * [[0.0, 0.0]]
        total_active_cars = len(self.cars)
        for i, road in enumerate(self.roads):
            dir_num_cars, inv_num_cars = road.get_road_state()
            road_load_percentage[i] = [
                dir_num_cars / total_active_cars * 100,
                inv_num_cars / total_active_cars * 100,
            ]
        return road_load_percentage

    def __get_road_cars_num(self) -> List[List[int]]:
        road_cars_num = len(self.roads) * [[0, 0]]
        for i, road in enumerate(self.roads):
            road_cars_num[i] = list(road.get_road_state())
        return road_cars_num

    def __update_cars(self, new_car: Vehicle) -> None:
        self.cars.update({self.next_car_id: new_car})
        road_id = self.cars[self.next_car_id].curr_road_id
        direct_flow = self.cars[self.next_car_id].curr_road_direct_flow
        self.roads[road_id].add_car_to_road(self.next_car_id, direct_flow)
        self.next_car_id += 1

    def __init_simulation(self) -> None:
        # initial cars
        for _ in range(self.sim_params.num_initial_cars):
            self.__update_cars(self.route_gen.generate(self.roads, self.nodes))

    def customize_nodes_traffic_lights(self, dur_array: np.ndarray) -> None:
        for j_node, dur_s in enumerate(dur_array):
            self.nodes[j_node].reset_traffic_light(dur_s=dur_s)

    def run_simulation(self) -> Tuple[np.ndarray, np.ndarray]:
        time_vec = np.arange(
            0,
            self.sim_params.sim_duration,
            step=self.sim_params.delta_t,
            dtype=np.int32,
        )
        roads_state_vec = np.empty(
            shape=(time_vec.shape[0], len(self.roads), 2), dtype=np.int32
        )
        en_plot = self.sim_params.en_city_plot
        abs_time = timedelta(hours=14, minutes=15, seconds=0)
        fig, ax, sctr_plt = None, None, None
        if en_plot:
            plt.ion()
            plot_spb_map_with_traffic(self.nodes, self.roads, {})
            fig, ax = plt.gcf(), plt.gca()
            sctr_plt = ax.scatter([], [], c="k", marker=".", zorder=3)  # no cars yet
            fig.suptitle("Saint-Petersburg")
            ax.set_title("Local time: " + str(abs_time))

        for i_time, global_time_s in enumerate(time_vec):
            if (
                global_time_s
                % (self.sim_params.delta_t * self.sim_params.car_spawn_rate)
                == 0
            ):
                self.__update_cars(self.route_gen.generate(self.roads, self.nodes))
            finished_cars_id = list([])
            for id, car in self.cars.items():
                car.update(self.sim_params.delta_t)
                ready_to_switch_road = car.ready_to_switch_road
                road_id = car.curr_road_id
                direct_flow = car.curr_road_direct_flow
                road = self.roads[road_id]
                if ready_to_switch_road:
                    node_id = road.node_to_id if direct_flow else road.node_from_id
                    port_id = (
                        road.node_to_port_id if direct_flow else road.node_from_port_id
                    )
                    tr_light_state = self.nodes[node_id].get_current_state()
                    if tr_light_state[port_id]:
                        road.remove_car_from_road(id, direct_flow)
                        car.proceed_to_next_step()
                        if car.reached_destination:
                            finished_cars_id.append(id)
                        else:
                            new_road_id = car.curr_road_id
                            direct_flow = car.curr_road_direct_flow
                            self.roads[new_road_id].add_car_to_road(id, direct_flow)
            for car_id in finished_cars_id:
                self.cars.pop(car_id)
            for id, node in enumerate(self.nodes):
                node.update(self.sim_params.delta_t)
            for id, road in enumerate(self.roads):
                # roads_state_vec[i_time][id][0], roads_state_vec[i_time][id][1] = road.get_road_state()
                # roads_state_vec[i_time] = self.__get_road_load_percentage()
                roads_state_vec[i_time] = self.__get_road_cars_num()

            if en_plot:
                sctr_plt.set_offsets(self.get_cars_coords())
                ax.set_title(
                    "Local time: "
                    + str(abs_time + timedelta(seconds=float(global_time_s)))
                )
                fig.canvas.draw_idle()
                plt.pause(0.2)
        if en_plot:
            plt.ioff()
            plt.show()

        return (time_vec, roads_state_vec)
