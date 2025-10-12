from city_elements import CrossRoad, Road

SPB_CR = [
    CrossRoad(
        coords=(10, 1705), road_id_vs_ports=[0, 1, 2, -1], tr_light_duration_s=25.0
    ),
    CrossRoad(
        coords=(241, 455), road_id_vs_ports=[45, 46, -1, -1], tr_light_duration_s=28.0
    ),
    CrossRoad(
        coords=(401, 103), road_id_vs_ports=[44, 45, -1, -1], tr_light_duration_s=25.0
    ),
    CrossRoad(
        coords=(593, 647), road_id_vs_ports=[46, 0, 47, -1], tr_light_duration_s=23.0
    ),
    CrossRoad(
        coords=(1080, 1390), road_id_vs_ports=[1, 5, 6, -1], tr_light_duration_s=22.0
    ),
    CrossRoad(
        coords=(1239, 1101), road_id_vs_ports=[6, 47, 41, -1], tr_light_duration_s=31.0
    ),
    CrossRoad(
        coords=(376, 2218), road_id_vs_ports=[2, 3, 4, -1], tr_light_duration_s=29.0
    ),
    CrossRoad(
        coords=(949, 451), road_id_vs_ports=[42, 43, 44, -1], tr_light_duration_s=34.0
    ),
    CrossRoad(
        coords=(1440, 840), road_id_vs_ports=[41, 34, 40, 42], tr_light_duration_s=24.0
    ),
    CrossRoad(
        coords=(1125, 226), road_id_vs_ports=[39, 43, -1, -1], tr_light_duration_s=36.0
    ),
    CrossRoad(
        coords=(1603, 561), road_id_vs_ports=[38, 39, 40, -1], tr_light_duration_s=30.0
    ),
    CrossRoad(
        coords=(2818, 226), road_id_vs_ports=[37, 30, 32, -1], tr_light_duration_s=20.0
    ),
    CrossRoad(
        coords=(2106, 386), road_id_vs_ports=[37, 36, 38, -1], tr_light_duration_s=22.0
    ),
    CrossRoad(
        coords=(2241, 958), road_id_vs_ports=[33, 35, 36, -1], tr_light_duration_s=31.0
    ),
    CrossRoad(
        coords=(2822, 991), road_id_vs_ports=[24, 35, 27, -1], tr_light_duration_s=33.0
    ),
    CrossRoad(
        coords=(2049, 1285), road_id_vs_ports=[28, 33, 34, -1], tr_light_duration_s=29.0
    ),
    CrossRoad(
        coords=(2519, 1547), road_id_vs_ports=[16, 22, 24, 28], tr_light_duration_s=27.0
    ),
    CrossRoad(
        coords=(2286, 2104), road_id_vs_ports=[12, 15, 16, -1], tr_light_duration_s=29.0
    ),
    CrossRoad(
        coords=(3517, 46), road_id_vs_ports=[31, 32, -1, -1], tr_light_duration_s=21.0
    ),
    CrossRoad(
        coords=(2896, 516), road_id_vs_ports=[27, 29, 30, -1], tr_light_duration_s=25.0
    ),
    CrossRoad(
        coords=(3530, 643), road_id_vs_ports=[26, 29, 31, -1], tr_light_duration_s=28.0
    ),
    CrossRoad(
        coords=(3550, 1163), road_id_vs_ports=[23, 25, 26, -1], tr_light_duration_s=30.0
    ),
    CrossRoad(
        coords=(3620, 2361), road_id_vs_ports=[20, 19, 21, -1], tr_light_duration_s=29.0
    ),
    CrossRoad(
        coords=(3076, 2836), road_id_vs_ports=[17, 19, 18, -1], tr_light_duration_s=38.0
    ),
    CrossRoad(
        coords=(2802, 2815), road_id_vs_ports=[13, 14, 17, -1], tr_light_duration_s=33.0
    ),
    CrossRoad(
        coords=(842, 2807), road_id_vs_ports=[4, 7, -1, -1], tr_light_duration_s=24.0
    ),
    CrossRoad(
        coords=(1321, 2504), road_id_vs_ports=[8, 7, 9, -1], tr_light_duration_s=32.0
    ),
    CrossRoad(
        coords=(2025, 2648), road_id_vs_ports=[9, 10, -1, -1], tr_light_duration_s=19.0
    ),
    CrossRoad(
        coords=(2200, 2308), road_id_vs_ports=[10, 11, 12, 13], tr_light_duration_s=35.0
    ),
    CrossRoad(
        coords=(1096, 1883), road_id_vs_ports=[3, 8, 11, 5], tr_light_duration_s=33.0
    ),
    CrossRoad(
        coords=(2961, 2418), road_id_vs_ports=[14, 15, -1, -1], tr_light_duration_s=30.0
    ),
    CrossRoad(
        coords=(3583, 1944), road_id_vs_ports=[21, 22, 23, -1], tr_light_duration_s=26.0
    ),
    CrossRoad(
        coords=(3795, 2830), road_id_vs_ports=[18, 20, -1, -1], tr_light_duration_s=27.0
    ),
]

SPB_ROADS = [
    Road(node_from=(0, 0), node_to=(3, 1)),
    Road(node_from=(0, 1), node_to=(4, 0)),
    Road(node_from=(0, 2), node_to=(6, 0)),
    Road(node_from=(6, 1), node_to=(29, 0)),
    Road(node_from=(6, 2), node_to=(25, 0)),
    Road(node_from=(4, 1), node_to=(29, 3)),
    Road(node_from=(4, 2), node_to=(5, 0)),
    Road(node_from=(25, 1), node_to=(26, 1)),
    Road(node_from=(29, 1), node_to=(26, 0)),
    Road(node_from=(26, 2), node_to=(27, 0)),
    Road(node_from=(27, 1), node_to=(28, 0)),
    Road(node_from=(29, 2), node_to=(28, 1)),
    Road(node_from=(28, 2), node_to=(17, 0)),
    Road(node_from=(28, 3), node_to=(24, 0)),
    Road(node_from=(24, 1), node_to=(30, 0)),
    Road(node_from=(17, 1), node_to=(30, 1)),
    Road(node_from=(17, 2), node_to=(16, 0)),
    Road(node_from=(24, 2), node_to=(23, 0)),
    Road(node_from=(23, 2), node_to=(32, 0)),
    Road(node_from=(23, 1), node_to=(22, 1)),
    Road(node_from=(32, 1), node_to=(22, 0)),
    Road(node_from=(22, 2), node_to=(31, 0)),
    Road(node_from=(31, 1), node_to=(16, 1)),
    Road(node_from=(31, 2), node_to=(21, 0)),
    Road(node_from=(16, 2), node_to=(14, 0)),
    Road(node_from=(14, 1), node_to=(21, 1)),
    Road(node_from=(21, 2), node_to=(20, 0)),
    Road(node_from=(14, 2), node_to=(19, 0)),
    Road(node_from=(16, 3), node_to=(15, 0)),
    Road(node_from=(19, 1), node_to=(20, 1)),
    Road(node_from=(19, 2), node_to=(11, 1)),
    Road(node_from=(20, 2), node_to=(18, 0)),
    Road(node_from=(11, 2), node_to=(18, 1)),
    Road(node_from=(15, 1), node_to=(13, 0)),
    Road(node_from=(15, 2), node_to=(8, 1)),
    Road(node_from=(13, 1), node_to=(14, 1)),
    Road(node_from=(13, 2), node_to=(12, 1)),
    Road(node_from=(12, 0), node_to=(11, 0)),
    Road(node_from=(12, 2), node_to=(10, 0)),
    Road(node_from=(10, 1), node_to=(9, 0)),
    Road(node_from=(10, 2), node_to=(8, 2)),
    Road(node_from=(5, 2), node_to=(8, 0)),
    Road(node_from=(8, 3), node_to=(7, 0)),
    Road(node_from=(7, 1), node_to=(9, 1)),
    Road(node_from=(7, 2), node_to=(2, 0)),
    Road(node_from=(2, 1), node_to=(1, 0)),
    Road(node_from=(1, 1), node_to=(3, 0)),
    Road(node_from=(3, 2), node_to=(5, 1)),
]


# debug
# for i_cr, node in enumerate(SPB_CR):
#     p = [-1, -1, -1, -1]
#     for i_r, road in enumerate(SPB_ROADS):
#         if road.node_from_id == i_cr:
#             p[road.node_from_port_id] = i_r
#         elif road.node_to_id == i_cr:
#             p[road.node_to_port_id] = i_r
#         else:
#             continue
#     print(f"{i_cr}: {p}")
