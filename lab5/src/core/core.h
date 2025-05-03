#include <string>
#include <vector>
#include <thread>
#include <mutex>

class Core
{
private:
    std::vector<std::vector<std::vector<std::string>>> all_tasks_;
    void run_task(const size_t id);
    void run_subtask(const std::vector<std::vector<std::string>>& subtask, const size_t id);
    std::vector<std::thread> threads_pool_;
public:
    Core(const std::vector<std::vector<std::vector<std::string>>>& comands);
    ~Core() = default;
    void process();
};

