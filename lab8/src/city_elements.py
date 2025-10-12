from typing import List, Tuple


class TrafficLight:
    def __init__(
        self, coords: Tuple[float, float] = (0.0, 0.0), state_duration_s: float = 20.0
    ) -> None:
        self.x, self.y = coords
        self.signal_cycle = [(True, False), (False, True)]
        self.state_duration_s = state_duration_s
        self.local_time = 0.0
        self.current_state_id = 0

    def update(self, dt_s: float = 1.0) -> None:
        self.local_time += dt_s
        if self.local_time > self.state_duration_s:
            self.current_state_id = (self.current_state_id + 1) % 2
            self.local_time = 0.0

    def get_current_state(self) -> Tuple[bool, bool]:
        return self.signal_cycle[self.current_state_id]


class CrossRoad:
    def __init__(
        self,
        coords: Tuple[float, float] = (0.0, 0.0),
        road_id_vs_ports: List[int] = [0, -1, -1, -1],
        tr_light_duration_s: float = 20.0,
    ) -> None:
        self.x, self.y = coords
        self.road_id_vs_ports = road_id_vs_ports
        self.tr_light = TrafficLight(coords, tr_light_duration_s)
        self.port_green = [True, False, True, False]

    def update(self, dt_s: float = 1.0) -> None:
        self.tr_light.update(dt_s)
        green02, green13 = self.tr_light.get_current_state()
        self.port_green = [green02, green13, green02, green13]

    def get_current_state(self) -> List[bool]:
        return self.port_green


class Road:
    def __init__(
        self, node_from: Tuple[int, int] = (0, 0), node_to: Tuple[int, int] = (1, 0)
    ) -> None:
        self.node_from_id, self.node_from_port_id = node_from
        self.node_to_id, self.node_to_port_id = node_to
        self.direct_flow_car_ids = set()
        self.inverse_flow_car_ids = set()

    def get_road_state(self) -> Tuple[int, int]:
        return (len(self.direct_flow_car_ids), len(self.inverse_flow_car_ids))

    def remove_car_from_road(self, id: int = 0, direct_flow: bool = True) -> None:
        if direct_flow:
            self.direct_flow_car_ids.remove(id)
        else:
            self.inverse_flow_car_ids.remove(id)

    def add_car_to_road(self, id: int = 0, direct_flow: bool = True) -> None:
        if direct_flow:
            self.direct_flow_car_ids.add(id)
        else:
            self.inverse_flow_car_ids.add(id)


class Vehicle:
    def __init__(
        self,
        path_nodes: List[int],
        path_roads: List[Tuple[int, bool, float]],
        target_speed_kmh: float = 20.0,
    ) -> None:
        # [id of crossroad]
        self.path_nodes = path_nodes
        # [(id of road, is_direct_flow, length), ...]
        self.path_roads = path_roads
        self.path_step_id = 0
        self.curr_node_id = path_nodes[self.path_step_id + 1]
        self.curr_road_id, self.curr_road_direct_flow, self.remaining_dist = path_roads[
            self.path_step_id
        ]
        # m/s - speed of car if there is no obstacles
        self.target_speed_m_per_s = target_speed_kmh * 10 / 36
        self.ready_to_switch_road = False
        self.reached_destination = False

    def update(self, dt_s: float = 1.0) -> None:
        dist_per_dt = dt_s * self.target_speed_m_per_s
        self.remaining_dist -= dist_per_dt
        if self.remaining_dist <= 0:
            self.remaining_dist = 0
            self.ready_to_switch_road = True

    def proceed_to_next_step(self) -> None:
        self.path_step_id += 1
        if self.path_step_id == len(self.path_roads):
            self.reached_destination = True
        else:
            self.curr_node_id = self.path_nodes[self.path_step_id + 1]
            self.curr_road_id, self.curr_road_direct_flow, self.remaining_dist = (
                self.path_roads[self.path_step_id]
            )
            self.ready_to_switch_road = False
