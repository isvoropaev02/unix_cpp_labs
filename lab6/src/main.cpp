#include "quick_sort.h"
#include "cocktail_sort.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

template<typename T>
std::vector<T> get_array_from_file()
{
    size_t k{0};
    T tmp;
    std::vector<T> out;
    std::ifstream input_file ("lab6/src/input.txt");
    if (input_file.is_open())
    {
        input_file >> k;
        out.reserve(k);
        for (size_t i = 0; i < k; i++)
        {
            input_file >> tmp;
            out.push_back(tmp);
        }
        input_file.close();
    }
    return out;
}

int main() {
    auto test_vec_qs = get_array_from_file<int>();
    auto test_vec_cs{test_vec_qs};
    const auto t_qs = quick_sort(test_vec_qs);
    const auto t_cs = cocktail_sort(test_vec_cs);
    std::cout << "Quick-sort (t=" << t_qs << " us):\n";
    for (size_t i = 0; i < std::min((size_t)150, test_vec_qs.size()); i++) {
        std::cout << test_vec_qs[i] << " ";
    }
    std::cout << "\n\n";
    std::cout << "Cocktail-sort (t=" << t_cs << " us):\n";
    for (size_t i = 0; i < std::min((size_t)150, test_vec_cs.size()); i++) {
        std::cout << test_vec_cs[i] << " ";
    }
    std::cout << "\n";
    return 0;
}
