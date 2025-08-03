from road_elements import Vehicle
from random import randint

class VehicleGenerator:
    def __init__(self, rate: float, num_route_steps: int = 1) -> None:
        self.rate = rate
        self.local_time = 0
        self.num_route_steps = num_route_steps

    def generate(self, roads_dict) -> Vehicle | None:
        if self.local_time % self.rate == 1:
            nodes, roads = [], []
            initial_road_id = randint(0, len(roads_dict)-1)
            initial_direct_flow = bool(randint(0, 1))
            if initial_direct_flow:
                pass
            return None
        else:
            return None