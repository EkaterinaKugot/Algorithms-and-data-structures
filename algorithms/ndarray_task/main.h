#include <iostream>
#include <vector>
#include <time.h>
#include <cassert>
#include <climits>
using namespace std;

template <typename T> class NDArray {
private:
    vector<int> shape;
    int size;
    vector<T> vec;
public:
    NDArray(int sh, T val = INT_MAX) { //создание одномерного массива заполненого каким-либо значением
        shape.push_back(sh);
        size = sh;
        if (val != INT_MAX)
            for (int i = 0; i < size; i++) vec.push_back(val);
    };

    NDArray(vector<int>* sh, T val = INT_MAX) { //создание много-мерного массива заполненого каким-либо значением
        int prod = 1;
        for (auto value : *sh) {
            prod *= value;
            shape.push_back(value);
        }
        size = prod;
        if (val != INT_MAX)
            for (int i = 0; i < size; i++) vec.push_back(val);
    };

    void randNum() {
        srand(time(NULL));
        vec.clear();
        for (int i = 0; i < size; i++) {
            T num = rand();
            int sign = rand() % 2;
            if (sign == 0) num *= -1;
            vec.push_back(num);   
        }
    }

    T& operator() (int i) {
        assert((i < size));
        return vec[i];
    };

    T& operator() (int i, int j) {
        assert(i < shape[0]);
        assert(j < shape[1]);
        return vec[i * shape[1] + j];
    };

    NDArray<T>& operator = (const NDArray<T>& v) { 
        vec.clear();
        size = v.size;
        shape = v.shape;
        if (v.vec.empty()) return *this;
        for (int i = 0; i < size; i++) vec.push_back(v.vec[i]);
        return *this;
    };

    NDArray<T>& operator += (const NDArray<T>& v) {//поэлементное сложение
        assert(shape == v.shape);
        for (int i = 0; i < size; i++) vec[i] += v.vec[i];
        return *this;
    }
    NDArray<T> operator + (const NDArray<T>& v) const{
        NDArray<T> res(*this);
        return res += v;
    }
    NDArray<T>& operator += (T n) {//сложение с числом всех элементов
        for (int i = 0; i < size; i++) vec[i] += n;
        return *this;
    }
    NDArray<T> operator + (T n) const {
        NDArray<T> res(*this);
        return res += n;
    }

    NDArray<T>& operator *= (const NDArray<T>& v) {//поэлементное умножение
        assert(shape == v.shape);
        for (int i = 0; i < size; i++) vec[i] *= v.vec[i];
        return *this;
    }
    NDArray<T> operator * (const NDArray<T>& v) const {
        NDArray<T> res(*this);
        return res *= v;
    }
    NDArray<T>& operator *= (T n) {//умножение на число всех элементов
        for (int i = 0; i < size; i++) vec[i] *= n;
        return *this;
    }
    NDArray<T> operator * (T n) const {
        NDArray<T> res(*this);
        return res *= n;
    }

    NDArray<T> operator -() const {//сделать отрицательным
        NDArray<T> res(*this);
        return res *= -1;
    }

    NDArray<T>& operator -= (const NDArray<T>& v) {//поэлементное вычитание
        return (*this += (-v));
    }
    NDArray<T> operator - (const NDArray<T>& v) const {
        NDArray<T> res(*this);
        return res -= v;
    }
    NDArray<T>& operator -= (T n) {//вычитание числа из всех элементов
        return (*this += (-n));
    }
    NDArray<T> operator - (T n) const {
        NDArray<T> res(*this);
        return res -= n;
    }

    NDArray<T>& operator /= (const NDArray<T>& v) {//поэлементное деление
        assert(shape == v.shape);
        for (int i = 0; i < size; i++) vec[i] /= v.vec[i];
        return *this;
    }
    NDArray<T> operator / (const NDArray<T>& v) const {
        NDArray<T> res(*this);
        return res /= v;
    }
    NDArray<T>& operator /= (T n) {//деление на число всех элементов
        for (int i = 0; i < size; i++) vec[i] /= n;
        return *this;
    }
    NDArray<T> operator / (T n) const {
        NDArray<T> res(*this);
        return res /= n;
    }

    NDArray<T>& filling(T val) {
        vec.clear();
        for (int i = 0; i < size; i++) vec.push_back(val);
        return *this;
    }

    NDArray<T>& transpose() {
        vector<int> s{ shape[1], shape[0] };
        NDArray<T> res(&s, 0);
        for (int i = 0; i < shape[0]; i++) {
            for (int j = 0; j < shape[1]; j++) {
                res(j, i) = (*this)(i, j);
            }
        }
        *this = res;
        return *this;
    }

    NDArray<T> multMatrx(NDArray<T>& v1) {
        assert(shape[1] == v1.shape[0]);
        vector<int> s{ shape[0], v1.shape[1] };
        NDArray<T> res(&s, 0);
        NDArray<T> v(1);
        v = v1;
        v.transpose();
        for (int k = 0; k < shape[0]; k++) {
            for (int i = 0; i < v.shape[0]; i++) {
                int n = 0;
                for (int j = 0; j < shape[1]; j++) {
                    n += (*this)(k, j) * v(i, j);
                }
                res(k, i) = n;
            }
        }
        return res;
    }

    T min(T n = -1) {
        assert(n < shape[0]);
        T imin = vec[0];
        if (n == -1) {
            for (auto val : vec)
                if (val < imin)
                    imin = val;
        }
        else {
            imin = vec[n * shape[1]];
            for (int i = n * shape[1]; i < n * shape[1] + shape[1]; i++) {
                if (vec[i] < imin)
                    imin = vec[i];
            }
        }
        return imin;
    }

    T max(T n = -1) {
        assert(n < shape[0]);
        T imax = vec[0];
        if (n == -1) {
            for (auto val : vec)
                if (val > imax)
                    imax = val;
        }
        else {
            imax = vec[n * shape[1]];
            for (int i = n * shape[1]; i < n * shape[1] + shape[1]; i++) {
                if (vec[i] > imax)
                    imax = vec[i];
            }
        }
        return imax;
        
    }

    T mean(T n = -1) {
        assert(n < shape[0]);
        T imean = 0;
        if (n == -1) {
            for (auto val : vec)
                imean += val;
            imean = imean / size;
        }
        else {
            for (int i = n * shape[1]; i < n * shape[1] + shape[1]; i++) {
                imean += vec[i];
            }
            imean = imean / shape[1];
        }
        return imean;
    }

    void print() { //вывод в консоль
        if (shape.size() == 1) {
            if (!vec.empty())
                for (int i = 0; i < size; i++)
                    cout << vec[i] << " ";  
            cout << endl;
        }
        else {
            for (int i = 0; i < shape[0]; i++) {
                for (int j = 0; j < shape[1]; j++)
                    cout << (*this)(i, j) << " ";
                cout << endl;
            }
        }
    };
};