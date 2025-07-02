#include "quick_sort.h"
#include "cocktail_sort.h"

#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {10, 9, 8, 7, 6, 3, 1, 4, 6, 7, 3, 8, 7, 2, 4, 9, 6, 1, 4, 9, 3, 6, 8, 8, 5, 1, 2};
    std::vector<int> numbers1 = {2, 3, 1, 1, 1, 4, 5, 10, 2, 2, 2, 22, 3, 6, 8, 9, 9, 7, 8};
    std::vector<int> numbers2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11, 11, 12, 13, 14, 15, 16, 17, 17, 18, 19, 20, 20, 21, 22};
    auto t0 = cocktail_sort(numbers);
    auto t1 = cocktail_sort(numbers1);
    auto t2 = cocktail_sort(numbers2);

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

    std::cout << "Отсортированный массив (t=" << t2 << " us):";
    for (int num : numbers2) {
        std::cout << num << " ";
    }
    std::cout << "\n";
    return 0;
}
