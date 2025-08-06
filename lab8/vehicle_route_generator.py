from road_elements import *
from random import randint

class VehicleGenerator:
    def __init__(self, num_route_steps: int = 1) -> None:
        self.num_route_steps = num_route_steps

    def generate(self, roads_dict: dict[int, Road], nodes_dict: dict[int, CrossRoad]) -> Vehicle | None:
        nodes, roads = [], []
        start_node_id = randint(0, len(nodes_dict)-1)
        nodes.append(start_node_id)
        start_node = nodes_dict[start_node_id]
        for _ in range(self.num_route_steps):
            port_id = randint(0, 3)
            if start_node.road_id_vs_ports[port_id] == -1:
                port_id = 0
            road_tmp_id = start_node.road_id_vs_ports[port_id]
            road_tmp = roads_dict[road_tmp_id]
            next_node_id = road_tmp.node_to_id
            direct_flow = True
            if next_node_id == start_node_id:
                next_node_id = road_tmp.node_from_id
                direct_flow = False
            next_node = nodes_dict[next_node_id]
            distance = ((start_node.x - next_node.x)**2 + (start_node.y - next_node.y)**2) ** 0.5
            roads.append((road_tmp_id, direct_flow, distance))
            nodes.append(next_node_id)
            start_node_id, start_node = next_node_id, next_node
        speed = randint(5, 50)
        print(nodes, roads, speed)
        return Vehicle(nodes, roads, speed)
