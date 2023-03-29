#include <iostream>
#include <vector>
#include "main.h"
using namespace std;


int main()
{
    setlocale(LC_ALL, "ru");
    //Демонстрация работы
    NDArray<int> emp(8); //создание пустого масcива
    cout << "Creating and outputting an empty array: ";
    emp.print();

    emp.randNum(); //заполнение пустого массива случайными элементами
    cout << "Filling an empty array with random elements: ";
    emp.print();

    //создание массивов заполненных любым значением (int)
    vector<int> s0{ 2, 3 };
    vector<int> s1{ 3, 5 };
    NDArray<int> arr0(&s0, 0); //заполнен нулями
    NDArray<int> arr1(&s1, 1); //заполнен единицами
    cout << "An array filled with zeros: " << endl;
    arr0.print();
    cout << "An array filled with the number one: " << endl;
    arr1.print();

    //создание массивов заполненных любым значением (float)
    NDArray<float> arr2(&s0, 8.9);
    NDArray<float> arr3(5, 145.9376);
    cout << "Arrays filled with any float value: " << endl;
    arr2.print();
    cout << endl;
    arr3.print();

    // Оператор поэлементного сложения
    vector<int> s{2, 2};
    NDArray<float> arr4(&s, 7.53);
    NDArray<float> arr5(&s, 1.341);
    NDArray<float> emp1(&s, 1);
    arr4 += arr5;
    emp1 = arr4 + arr5;
    cout << "\nAddition via +=: " << endl;
    arr4.print();
    cout << "Addition via +: " << endl;
    emp1.print();

    // Оператор поэлементного вычитания
    arr4 -= arr5;
    emp1 = arr4 - arr5;
    cout << "\nSubtraction by -=: " << endl;
    arr4.print();
    cout << "Subtraction by -: " << endl;
    emp1.print();

    // Оператор поэлементного умножения
    arr4 *= arr5;
    emp1 = arr4 * arr5;
    cout << "\nMultiplication by *=: " << endl;
    arr4.print();
    cout << "Multiplication by *: " << endl;
    emp1.print();

    // Оператор поэлементного деления
    arr4 /= arr5;
    emp1 = arr4 / arr5;
    cout << "\nDivision by /=: " << endl;
    arr4.print();
    cout << "Division by /: " << endl;
    emp1.print();

    //Операторы сложения, вычитания, умножения, деления на число
    NDArray<int> arr6(7, 2);
    cout << "\nAddition with 1: " << endl;
    arr6.print();
    arr6 += 1;
    arr6.print();
    cout << "Subtraction of 1: " << endl;
    arr6 = arr6 - 1;
    arr6.print();
    cout << "Multiplication by 2: " << endl;
    arr6 = arr6 * 2;
    arr6.print();
    cout << "Division by 3: " << endl;
    arr6 /= 3;
    arr6.print();

    //Матричное умножение и изменение занчения у элемента массива
    vector<int> s2{ 2, 3 };
    vector<int> s3{ 3, 5 };
    NDArray<int> arr7(&s2, 4);
    NDArray<int> arr8(&s3, 13);
    cout << "\nThe original array: " << endl;
    arr7.print();
    cout << "Changing the value of an array element arr7(0, 2) = 2: " << endl;
    arr7(0, 2) = 2;
    arr7.print();
    arr7(1, 1) = 3; arr7(1, 0) = 6;
    arr8(1, 0) = 9; arr8(2, 4) = 17; arr8(1, 3) = 34;
    cout << "\nMatrix multiplication: " << endl;
    arr7 = arr7.multMatrx(arr8);
    arr7.print();

    //Транспонирование
    cout << "\nTransposing the previous matrix: " << endl;
    arr7.transpose();
    arr7.print();

    //Операции сокращения: минимум, максимум, среднее
    cout << "\nThe minimum of the previous matrix: " << arr7.min();
    cout << "\nThe maximum of the previous matrix: " << arr7.max();
    cout << "\nThe average of the second(1) row: " << arr7.mean(1);
    return 0;
}

