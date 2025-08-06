import cv2
import matplotlib.pyplot as plt
from road_elements import *
from SPB import *


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


def plot_spb_map_debug() -> None:
    image = cv2.cvtColor(cv2.imread("spb_map.png", 1), cv2.COLOR_BGR2RGB)

    # Координаты, в которых будет отображаться изображение
    img_x_min, img_x_max = 0, 3820     # по X
    img_y_min, img_y_max = 0, 2970     # по Y

    plt.figure()
    plt.imshow(image, extent=(img_x_min, img_x_max,
                              img_y_min, img_y_max), origin="upper")
    # чтобы ось Y шла сверху вниз (как в изображениях)

    plt.scatter([5], [1705], c='royalblue')
    plt.scatter([3795], [2830], c='royalblue')
    plt.scatter([241], [455], c='royalblue')
    plt.scatter([401], [103], c='royalblue')
    plt.scatter([593], [647], c='royalblue')
    plt.scatter([1080], [1390], c='royalblue')
    plt.scatter([1239], [1101], c='royalblue')
    plt.scatter([376], [2218], c='royalblue')
    plt.scatter([675], [2038], c='royalblue')
    plt.scatter([949], [451], c='royalblue')
    plt.scatter([1440], [840], c='royalblue')
    plt.scatter([1125], [226], c='royalblue')
    plt.scatter([1603], [561], c='royalblue')
    plt.scatter([2818], [226], c='royalblue')
    plt.scatter([2106], [386], c='royalblue')
    plt.scatter([2241], [958], c='royalblue')
    plt.scatter([2822], [991], c='royalblue')
    plt.scatter([2049], [1285], c='royalblue')
    plt.scatter([2519], [1547], c='royalblue')
    plt.scatter([2286], [2104], c='royalblue')
    plt.scatter([3517], [46], c='royalblue')
    plt.scatter([2896], [516], c='royalblue')
    plt.scatter([3530], [643], c='royalblue')
    plt.scatter([3550], [1163], c='royalblue')
    plt.scatter([3620], [2361], c='royalblue')
    plt.scatter([3076], [2836], c='royalblue')
    plt.scatter([2802], [2815], c='royalblue')
    plt.scatter([842], [2807], c='royalblue')
    plt.scatter([1321], [2504], c='royalblue')
    plt.scatter([2025], [2648], c='royalblue')
    plt.scatter([2200], [2308], c='royalblue')
    plt.scatter([1096], [1883], c='royalblue')
    plt.scatter([2961], [2418], c='royalblue')
    plt.scatter([3583], [1944], c='royalblue')

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.show()


plot_city_map(CROSS_ROADS, ROADS)
plot_spb_map_debug()


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
        plt.plot([cr0.x, cr1.x], [cr0.y, cr1.y], color='grey')
        plt.text((cr0.x + cr1.x) / 2 + offset_x,
                 (cr0.y + cr1.y) / 2 + offset_y, str(i), fontsize=8, color='orangered')

    for i, cr in enumerate(cross_roads):
        plt.scatter([cr.x], [cr.y], c='royalblue')
        plt.text(cr.x + offset_x, cr.y + offset_y, str(i), fontsize=8)

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.show()


plot_spb_map(SPB_CR, SPB_ROADS)
