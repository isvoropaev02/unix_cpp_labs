import numpy as np
import matplotlib.pyplot as plt


class PostProcessor:
    def __init__(
        self, timestamps: np.ndarray, road_states: np.ndarray, threshold: float = 25
    ) -> None:
        assert timestamps.shape[0] == road_states.shape[0]
        self.__times = timestamps.copy()
        self.__state = road_states.copy()
        self.__threshold = threshold

    def calculate_mean_load(self, en_plot: bool = False) -> np.ndarray:
        mean_data = np.round(np.mean(np.sum(self.__state, axis=2), axis=0), 1)
        if en_plot:
            color_cycle = plt.cm.get_cmap("tab20", 20)
            fig3 = plt.figure(figsize=(12, 5))
            fig3.add_subplot(1, 1, 1)
            plt.bar(
                np.arange(len(mean_data)),
                mean_data,
                color=[color_cycle(i % 20) for i in range(len(mean_data))],
            )
            plt.xlabel("Road ID")
            plt.ylabel("Mean number of cars")
            plt.grid()
            fig3.savefig("lab8/doc/mean_load.png", transparent=False)
        return mean_data

    def get_roads_with_most_load_at_the_start(self) -> np.ndarray:
        return np.argsort(np.sum(self.__state[0], axis=1))[-10:][::-1]

    def plot_report(self) -> None:
        most_load_ids = self.get_roads_with_most_load_at_the_start()
        combined_states = np.sum(self.__state, axis=2)
        fig1 = plt.figure(figsize=(14, 12))
        fig1.suptitle("Road's load evolution")

        for j_plot, j_road in enumerate(most_load_ids):
            plt.subplot(len(most_load_ids), 1, j_plot + 1)
            plt.plot(
                self.__times,
                combined_states[:, j_road],
                label="Sequential",
                color="C" + str(j_plot),
            )
            plt.ylabel(f"Road ID:\n{j_road}", rotation=0)
            plt.grid()
            plt.gca().yaxis.set_label_coords(-0.10, 0.5)
            if j_plot == len(most_load_ids) - 1:
                plt.xlabel("Time [sec]")

        fig1.savefig("lab8/doc/load_evolution_plot.png", transparent=False)

        # getting traffic jam erasure time
        initial_top_load_roads_percentage_evolution = (
            100
            * np.sum(combined_states[:, most_load_ids], axis=1)
            / np.sum(combined_states, axis=1)
        )
        indices = np.where(
            initial_top_load_roads_percentage_evolution < self.__threshold
        )[0]
        er_time = float(self.__times[-1])
        if len(indices) > 0:
            er_time = self.__times[indices[0]]

        fig2 = plt.figure(figsize=(12, 5))
        fig2.suptitle("Load percentage")
        plt.subplot(1, 1, 1)
        plt.plot(
            self.__times,
            initial_top_load_roads_percentage_evolution,
            label="percent of all cars on roads",
        )
        plt.axvline(
            x=er_time,
            color="r",
            linestyle="--",
            label=f"jam erasure time: {er_time} sec",
        )
        plt.grid()
        plt.ylabel("Load [%]")
        plt.xlabel("Time [sec]")
        plt.legend()
        fig2.savefig("lab8/doc/load_percentqage_plot.png", transparent=False)
