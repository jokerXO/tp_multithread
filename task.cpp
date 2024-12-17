#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <nlohmann/json.hpp>
#include <Eigen/Dense>

using json = nlohmann::json;
using namespace Eigen;
using namespace std;

class Task {
private:
    int identifier;
    int size;
    MatrixXd a;
    VectorXd b;
    VectorXd x;
    double elapsed_time;

public:
    Task(int id = 0, int sz = -1) : identifier(id), size(sz) {
        if (size == -1) {
            random_device rd;
            mt19937 gen(rd());
            uniform_int_distribution<> dist(300, 3000);
            size = dist(gen);
        }
        a = MatrixXd::Random(size, size);
        b = VectorXd::Random(size);
        x = VectorXd::Zero(size);
        elapsed_time = 0.0;
    }

    void work() {
        auto start = chrono::high_resolution_clock::now();
        x = a.colPivHouseholderQr().solve(b);
        auto end = chrono::high_resolution_clock::now();
        elapsed_time = chrono::duration<double>(end - start).count();
    }

    string to_json() const {
        json info;
        info["identifier"] = identifier;
        info["size"] = size;
        info["a"] = vector<vector<double>>(a.rows(), vector<double>(a.cols()));
        info["b"] = vector<double>(b.data(), b.data() + b.size());
        info["x"] = vector<double>(x.data(), x.data() + x.size());
        info["time"] = elapsed_time;

        for (int i = 0; i < a.rows(); ++i)
            for (int j = 0; j < a.cols(); ++j)
                info["a"][i][j] = a(i, j);

        return info.dump();
    }

    static Task from_json(const string &text) {
        json data = json::parse(text);
        Task task(data["identifier"], data["size"]);
        task.elapsed_time = data["time"];

        for (int i = 0; i < task.size; ++i) {
            for (int j = 0; j < task.size; ++j) {
                task.a(i, j) = data["a"][i][j];
            }
            task.b(i) = data["b"][i];
            task.x(i) = data["x"][i];
        }
        return task;
    }

    bool operator==(const Task &other) const {
        return identifier == other.identifier && a.isApprox(other.a) &&
               b.isApprox(other.b) && x.isApprox(other.x) &&
               elapsed_time == other.elapsed_time;
    }

    friend ostream &operator<<(ostream &os, const Task &task) {
        os << "Task " << task.identifier;
        return os;
    }
};

int main() {
    Task task(1);
    task.work();
    string json_text = task.to_json();
    Task new_task = Task::from_json(json_text);

    cout << new_task << endl;
    return 0;
}
