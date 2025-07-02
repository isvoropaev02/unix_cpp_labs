#include "quick_sort.h"

#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {10, 9, 8, 7, 6, 3, 1, 4, 6, 7, 3, 8, 7, 2, 4, 9, 6, 1, 4, 9, 3, 6, 8, 8, 5, 1, 2};
    std::vector<int> numbers1 = {2, 3, 1, 1, 1, 4, 5, 10, 2, 2, 2, 22, 3, 6, 8, 9, 9, 7, 8};
    auto t0 = quick_sort(numbers);
    auto t1 = quick_sort(numbers1);

    std::cout << "Отсортированный массив (t=" << t0 << " us):";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << "\n";

    std::cout << "Отсортированный массив (t=" << t1 << " us):";
    for (int num : numbers1) {
        std::cout << num << " ";
    }
    std::cout << "\n";
    return 0;
}
