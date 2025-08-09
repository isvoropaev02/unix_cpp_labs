import cv2
import matplotlib.pyplot as plt
from road_elements import *
from SPB import *
import numpy as np


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


def plot_city_map(crossroads: dict[int, CrossRoad], roads: dict[int, Road]) -> None:
    plt.figure()
    # python >= 3.7 сохраняется порядок вставки
    cr_x, cr_y = zip(*[(cr.x, cr.y) for _, cr in crossroads.items()])
    plt.scatter(cr_x, cr_y)
    for road in roads.values():
        id0, id1 = road.node_from_id, road.node_to_id
        plt.plot([cr_x[id0], cr_x[id1]], [cr_y[id0], cr_y[id1]], color='k')
    plt.show()


def plot_spb_map(cross_roads: list[CrossRoad], roads: list[Road]) -> None:
    image = cv2.cvtColor(cv2.imread("spb_map.png", 1), cv2.COLOR_BGR2RGB)

    # Координаты, в которых будет отображаться изображение
    img_x_min, img_x_max = 0, 3820     # по X
    img_y_min, img_y_max = 0, 2970     # по Y

    offset_x, offset_y = 12, 10

    plt.figure()
    plt.imshow(image, extent=(img_x_min, img_x_max,
                              img_y_min, img_y_max), origin="upper")
    # чтобы ось Y шла сверху вниз (как в изображениях)
    for i, road in enumerate(roads):
        cr0 = cross_roads[road.node_from_id]
        cr1 = cross_roads[road.node_to_id]
        plt.plot([cr0.x, cr1.x], [cr0.y, cr1.y], color='chocolate')
        plt.text((cr0.x + cr1.x) / 2 + offset_x,
                 (cr0.y + cr1.y) / 2 + offset_y, str(i) +
                 ", {" + str(road.node_from_id) + "|" + str(road.node_from_port_id) + ", " +
                 str(road.node_to_id) + "|" + str(road.node_to_port_id) + "}",
                 fontsize=8, color='orangered')

    for i, cr in enumerate(cross_roads):
        plt.scatter([cr.x], [cr.y], c='royalblue')
        plt.text(cr.x + offset_x, cr.y + offset_y, str(i) +
                 str(cr.road_id_vs_ports), fontsize=8)

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.show()


def plot_spb_map_with_traffic(cross_roads: list[CrossRoad], roads: list[Road], cars: dict[int, Vehicle]) -> None:
    image = cv2.cvtColor(cv2.imread("spb_map.png", 1), cv2.COLOR_BGR2RGB)

    # Координаты, в которых будет отображаться изображение
    img_x_min, img_x_max = 0, 3820     # по X
    img_y_min, img_y_max = 0, 2970     # по Y

    offset = 10

    plt.figure()
    plt.imshow(image, extent=(img_x_min, img_x_max,
                              img_y_min, img_y_max), origin="upper", zorder=1)
    # чтобы ось Y шла сверху вниз (как в изображениях)
    for i, road in enumerate(roads):
        cr0 = cross_roads[road.node_from_id]
        cr1 = cross_roads[road.node_to_id]
        n_vec = np.array([cr1.y-cr0.y, cr0.x-cr1.x], dtype=np.float32)
        n_vec = offset * n_vec / np.linalg.norm(n_vec)
        plt.plot(np.array([cr0.x + n_vec[0], cr1.x + n_vec[0]], dtype=np.float32), np.array(
            [cr0.y + n_vec[1], cr1.y + n_vec[1]], dtype=np.float32), color='chocolate', zorder=2)
        plt.plot(np.array([cr0.x - n_vec[0], cr1.x - n_vec[0]], dtype=np.float32), np.array(
            [cr0.y - n_vec[1], cr1.y - n_vec[1]], dtype=np.float32), color='chocolate', linestyle='--', zorder=2)

    for i, cr in enumerate(cross_roads):
        plt.scatter([cr.x], [cr.y], c='royalblue', zorder=3)

    for car in cars.values():
        direct_flow = car.curr_road_direct_flow
        sgn = 1
        road_tmp = roads[car.curr_road_id]
        cr0 = cross_roads[road_tmp.node_from_id]
        cr1 = cross_roads[road_tmp.node_to_id]
        if not direct_flow:
            cr0, cr1 = cr1, cr0
        n_vec = np.array([cr1.y-cr0.y, cr0.x-cr1.x], dtype=np.float32)
        full_dist = np.linalg.norm(n_vec)
        n_vec = offset * n_vec / full_dist
        xr = car.remaining_dist * (cr1.x-cr0.x) / full_dist
        yr = car.remaining_dist * (cr1.y-cr0.y) / full_dist
        plt.scatter([cr1.x-xr + n_vec[0]],
                    [cr1.y-yr+n_vec[1]], c='k', marker='.', zorder=3)

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    # plot_spb_map(SPB_CR, SPB_ROADS)
    # plot_city_map(CROSS_ROADS, ROADS)
    plot_spb_map_with_traffic(SPB_CR, SPB_ROADS, {0: Vehicle(
        path_nodes=[11, 12], path_roads=[(37, False, 300)], target_speed_kmh=30)})
