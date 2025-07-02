#pragma once

#include <utility>
#include <vector>
#include <chrono>


template <typename T>
int64_t cocktail_sort(std::vector<T>& in_array) {
    auto task_start = std::chrono::high_resolution_clock::now();

    bool swapped = true;
    size_t start = 0;
    size_t end = in_array.size() - 1;

    while (swapped) {
        swapped = false;

        // direct flow
        for (size_t i = start; i < end; ++i) {
            if (in_array[i] > in_array[i + 1]) {
                std::swap(in_array[i], in_array[i + 1]);
                swapped = true;
            }
        }

        if (!swapped) break;

        swapped = false;
        --end;

        // reverse flow
        for (size_t i = end - 1; i-- > start; ) {
            if (in_array[i] > in_array[i + 1]) {
                std::swap(in_array[i], in_array[i + 1]);
                swapped = true;
            }
        }

        ++start;
    }
    auto task_end = std::chrono::high_resolution_clock::now();
    return (std::chrono::duration_cast<std::chrono::microseconds>(task_end - task_start)).count();
}
