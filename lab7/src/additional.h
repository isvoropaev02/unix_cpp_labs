#pragma once

#include <vector>
#include <algorithm>
#include <limits>

template <typename T>
std::pair<T, std::vector<size_t>> tsp_solve_with_path(const std::vector<std::vector<T>> &dist_matr)
{
    const size_t n = dist_matr.size();
    if (n <= 1)
    {
        return {(T)0, {0}};
    }

    const size_t num_masks = ((size_t)1 << n);
    std::vector<std::vector<std::pair<T, size_t>>> state_table(
        num_masks,
        std::vector<std::pair<T, size_t>>(n, {std::numeric_limits<T>::max(), 0}));

    // Базовый случай: начальный город 0
    state_table[1 << 0][0] = {0, 0};
    for (size_t mask = 1; mask < num_masks; ++mask)
    {
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

            const size_t prev_mask = mask ^ (1 << last);
            for (size_t prev = 0; prev < n; ++prev)
            {
                if (prev == last || !(prev_mask & (1 << prev)))
                {
                    continue;
                }

                const auto new_dist = state_table[prev_mask][prev].first + dist_matr[prev][last];
                if (new_dist < state_table[mask][last].first)
                {
                    state_table[mask][last] = {new_dist, prev};
                }
            }
        }
    }

    // Восстановление пути
    std::vector<size_t> path;
    path.reserve(n + 1);
    size_t current_mask = num_masks - 1;
    size_t current_city = 0;
    T min_tour = std::numeric_limits<T>::max();

    // Находим последний город перед возвратом в 0
    for (size_t last = 1; last < n; ++last)
    {
        T total_dist = state_table[current_mask][last].first + dist_matr[last][0];
        if (total_dist < min_tour)
        {
            min_tour = total_dist;
            current_city = last;
        }
    }

    // Восстанавливаем путь в обратном порядке
    while (true)
    {
        path.push_back(current_city);
        const size_t prev_city = state_table[current_mask][current_city].second;
        current_mask ^= ((size_t)1 << current_city);
        current_city = prev_city;
        if (current_city == 0)
        {
            break;
        }
    }
    path.push_back(0);
    std::reverse(path.begin(), path.end());
    path.push_back(0); // Добавляем стартовый город
    return {min_tour, path};
}