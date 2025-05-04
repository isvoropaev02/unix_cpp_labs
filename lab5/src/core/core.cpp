#include "core.h"
#include "core_entities/comand.h"

#include <stdexcept>
#include <iostream>

Core::Core(const std::vector<std::vector<std::vector<std::string>>>& comands) : all_tasks_(comands)
{
    threads_pool_.reserve(comands.size());
    threads_time_.resize(comands.size());
}

void Core::run_task(const size_t id)
{
    auto task_start = std::chrono::high_resolution_clock::now();
    const auto task = all_tasks_[id];
    std::unordered_map<std::string, Variable> variables;
    run_subtask(task, id, variables);
    auto task_end = std::chrono::high_resolution_clock::now();
    threads_time_[id] = std::chrono::duration_cast<std::chrono::microseconds>(task_end - task_start);
}

void Core::run_subtask(const std::vector<std::vector<std::string>>& subtask, const size_t id,
                       std::unordered_map<std::string, Variable>& variables)
{
    for (size_t i_func = 0; i_func < subtask.size(); i_func++)
    {
        auto current_comand = subtask[i_func][0];
        if (current_comand == "int" || current_comand == "flt")
        {
            CreateVariable new_var(subtask[i_func]);
            new_var.run(variables, id);
        }
        else if (current_comand == "print")
        {
            Print new_print(subtask[i_func]);
            new_print.run(variables, id);
        }
        else if (current_comand == "expr")
        {
            Expression new_expr(subtask[i_func]);
            new_expr.run(variables, id);
        }
        else if (current_comand == "for")
        {
            if (subtask[i_func].size() != 4) throw std::invalid_argument("Incorrect comand: " + current_comand + " ... in line " + std::to_string(id) +"\n");
            size_t n_loops = std::stoi(subtask[i_func][3]);
            const std::vector<std::vector<std::string>> subsubtask(subtask.cbegin() + 1 + i_func, subtask.cend());
            for (size_t i = 0; i < n_loops; i++)
            {
                CreateVariable n_count(std::vector<std::string> {"int", subtask[i_func][1], subtask[i_func][2], std::to_string(i)});
                n_count.run(variables, id);
                run_subtask(subsubtask, id, variables);
            }
            break;
        }
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
    std::cout << "\nThreads working time:\n";
    for (size_t i = 0; i < threads_time_.size(); i++) std::cout << "Time [THREAD " << i << "]: " << threads_time_[i].count() << " usec\n";
    std::cout << "\n";
}