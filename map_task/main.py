import matplotlib.pyplot as plt
import sys
import time

data = input().split()

с_arr_n = list(map(int, data[::3]))
с_memory_size = list(map(int, data[1::3]))
с_filling_time = list(map(float, data[2::3]))

py_arr_n = []
py_memory_size = []
py_filling_time = []

counter = {}

for i in range(6):
    n = 10 ** i
    counter.clear()
    start = time.time()
    for j in range(1, n+1):
        counter[j] = j
    end = time.time()
    py_arr_n.append(n)
    py_memory_size.append(sys.getsizeof(counter))
    py_filling_time.append((end-start) * 10**6)

print(с_arr_n, с_memory_size)
print(py_arr_n, py_memory_size)

plt.figure()
a1 = plt.subplot(221)
a1.set_title('C++ memory')
a1.plot(с_arr_n, с_memory_size)
plt.xlabel("elements")
plt.ylabel("bytes")

a2 = plt.subplot(222)
a2.set_title('C++ time')
a2.plot(с_arr_n, с_filling_time)
plt.xlabel("elements")
plt.ylabel("µs")

a3 = plt.subplot(223)
a3.set_title('Python memory')
a3.plot(py_arr_n, py_memory_size)
plt.xlabel("elements")
plt.ylabel("bytes")

a4 = plt.subplot(224)
a4.set_title('Python time')
a4.plot(py_arr_n, py_filling_time)
plt.xlabel("elements")
plt.ylabel("µs")

plt.tight_layout()
plt.show()
