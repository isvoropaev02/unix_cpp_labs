#pragma once

#include <utility>
#include <vector>
#include <chrono>

template <typename T>
size_t partition(std::vector<T>& in_array, size_t low, size_t high) {
    T pivot = in_array[high-1];
    size_t i = low;

    for (size_t j = low; j < high-1; ++j) {
        if (in_array[j] < pivot) {
            std::swap(in_array[i], in_array[j]);
            ++i;
        }
    }
    std::swap(in_array[i], in_array[high-1]);
    return i;
}

template <typename T>
void quick_sort_core(std::vector<T>& in_array, size_t low, size_t high) {
    if (low < high) {
        size_t pivot_idx = partition(in_array, low, high);
        quick_sort_core(in_array, low, pivot_idx);
        quick_sort_core(in_array, pivot_idx + 1, high);
    }
}

template <typename T>
int64_t quick_sort(std::vector<T>& in_array) {
    auto task_start = std::chrono::high_resolution_clock::now();
    quick_sort_core(in_array, 0, in_array.size());
    auto task_end = std::chrono::high_resolution_clock::now();
    return (std::chrono::duration_cast<std::chrono::microseconds>(task_end - task_start)).count();
}
