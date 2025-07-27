#include <iostream>
#include <fstream>
#include <vector>

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

int main()
{
    auto cities = get_coords_from_file<float>();
    for (const auto &city : cities)
    {
        std::cout << city.x << " " << city.y << "\n";
    }
    auto graph = calculate_dist_graph(cities);
    for (const auto &row : graph)
    {
        for (const auto &val : row)
        {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }
    return 0;
}
