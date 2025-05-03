#include "core.h"
#include "comand.h"

#include <vector>
#include <string>
#include <stdexcept>
#include <iostream>
#include <unordered_map>

Core::Core(const std::vector<std::vector<std::vector<std::string>>>& comands) : all_tasks_(comands)
{
    threads_pool_.reserve(comands.size());
}

void Core::run_task(const size_t id)
{
    const auto task = all_tasks_[id];
    std::unordered_map<std::string, Variable> variables;
    for (size_t i_func = 0; i_func < task.size(); i_func++)
    {
        auto current_comand = task[i_func][0];
        if (current_comand == "int" || current_comand == "flt")
        {
            CreateVariable new_var(task[i_func]);
            new_var.run(variables, id);
            // cout_mtx.lock();
            // std::cout << ("[THREAD " + std::to_string(id) + "] " + current_comand + "\n");
            // cout_mtx.unlock();
        }
        else if (current_comand == "print")
        {
            Print new_print(task[i_func]);
            new_print.run(variables, id);
            // cout_mtx.lock();
            // std::cout << ("[THREAD " + std::to_string(id) + "] " + current_comand + "\n");
            // cout_mtx.unlock();
        }
        else if (current_comand == "expr") continue;
        else if (current_comand == "for") continue;
        else throw std::invalid_argument("No such comand: " + current_comand + " in line " + std::to_string(id) +"\n");
    }
}

void Core::process()
{
    for (size_t id = 0; id < all_tasks_.size(); id++)
    {
        threads_pool_.emplace_back([this, id]() {
            this->run_task(id);
        });
    }
    for (auto& thread : threads_pool_) thread.join();
}