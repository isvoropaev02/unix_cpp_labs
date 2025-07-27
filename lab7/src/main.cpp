#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>

template <typename T>
struct point_t
{
    T x;
    T y;
    T distance(const point_t<T> &other) const { return ((x - other.x) * (x - other.x) + (y - other.y) * (y - other.y)); }
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

int main()
{
    auto cities = get_coords_from_file<float>();
    for (const auto &city : cities)
    {
        std::cout << city.x << " " << city.y << "\n";
        std::cout << city.distance(cities[0]) << "\n";
    }
    return 0;
}
