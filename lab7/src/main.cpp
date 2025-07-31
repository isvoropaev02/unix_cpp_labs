#include "additional.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <limits>
#include <cmath>

template <typename T>
struct point_t
{
    T x;
    T y;
    T distance(const point_t<T> &other) const { return std::sqrt((x - other.x) * (x - other.x) + (y - other.y) * (y - other.y)); }
};

template <typename T>
std::vector<point_t<T>> get_coords_from_file()
{
    size_t k;
    T x_tmp, y_tmp;
    std::vector<point_t<T>> out;
    std::ifstream input_file("lab7/src/input.txt");
    if (input_file)
    {
        size_t k;
        input_file >> k;
        out.reserve(k);
        while (k-- && input_file >> x_tmp >> y_tmp)
        {
            out.push_back({x_tmp, y_tmp});
        }
    }
    return out;
}

template <typename T>
std::vector<std::vector<T>> calculate_dist_graph(const std::vector<point_t<T>> &cities)
{
    const size_t n = cities.size();
    std::vector<std::vector<T>> graph(n, std::vector<T>(n, 0));
    for (size_t j0 = 0; j0 < n; j0++)
    {
        for (size_t j1 = 0; j1 < n; j1++)
        {
            graph[j0][j1] = cities[j0].distance(cities[j1]);
        }
    }
    return graph;
}

template <typename T>
T tsp_solve(const std::vector<std::vector<T>> &dist_matr)
{
    const size_t n = dist_matr.size();
    if (n <= 1)
    {
        return (T)0;
    }
    const size_t num_masks = ((size_t)1 << n);
    std::vector<std::vector<T>> state_table(num_masks, std::vector<T>(n, std::numeric_limits<T>::max()));

    // Базовый случай: начальный город 0
    state_table[1 << 0][0] = 0;
    for (size_t mask = 1; mask < num_masks; ++mask)
    {
        // Пропускаем маски без стартового города
        if (!(mask & 1))
        {
            continue;
        }
        for (size_t last = 0; last < n; ++last)
        {
            if (!(mask & ((size_t)1 << last)))
            {
                continue;
            }

            // Маска без текущего города
            const size_t prev_mask = mask ^ ((size_t)1 << last);

            for (size_t prev = 0; prev < n; ++prev)
            {
                if (prev == last || !(prev_mask & (1 << prev)))
                {
                    continue;
                }
                const auto new_dist = state_table[prev_mask][prev] + dist_matr[prev][last];
                if (new_dist < state_table[mask][last])
                {
                    state_table[mask][last] = new_dist;
                }
            }
        }
    }
    // Находим минимальный тур (возврат в город 0)
    T min_tour = std::numeric_limits<T>::max();
    const size_t full_mask = num_masks - 1;
    for (size_t last = 1; last < n; ++last)
    {
        min_tour = std::min(min_tour, state_table[full_mask][last] + dist_matr[last][0]);
    }

    return min_tour;
}

int main()
{
    auto cities = get_coords_from_file<float>();
    // for (const auto &city : cities)
    // {
    //     std::cout << city.x << " " << city.y << "\n";
    // }
    auto graph = calculate_dist_graph(cities);
    // for (const auto &row : graph)
    // {
    //     for (const auto &val : row)
    //     {
    //         std::cout << val << " ";
    //     }
    //     std::cout << "\n";
    // }

    std::cout << "Min distance: " << tsp_solve(graph)
              << "\n";

    auto [dist, seq] = tsp_solve_with_path(graph);
    std::cout << "Min distance (1): " << tsp_solve(graph)
              << "\n";

    for (auto &&el : seq)
    {
        std::cout << el << " ";
    }
    std::cout << "\n";
    return 0;
}
