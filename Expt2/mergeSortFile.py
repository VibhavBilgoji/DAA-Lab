import math
import random
import string
import time
import timeit

a = []
b = []


def MergeSort(low, high):
    if low < high:
        mid = math.floor((low + high) / 2)
        MergeSort(low, mid)
        MergeSort(mid + 1, high)
        Merge(low, mid, high)


def Merge(low, mid, high):
    global a, b
    h = low
    i = low
    j = mid + 1
    while (h <= mid) and (j <= high):
        if a[h] <= a[j]:
            b[i] = a[h]
            h = h + 1
        else:
            b[i] = a[j]
            j = j + 1
        i = i + 1
    if h > mid:
        for k in range(j, high + 1):
            b[i] = a[k]
            i = i + 1
    else:
        for k in range(h, mid + 1):
            b[i] = a[k]
            i = i + 1
    for k in range(low, high + 1):
        a[k] = b[k]


def get_data(data_type, size):
    if data_type == "Integer":
        return [random.randint(1, 100000) for _ in range(size)]
    elif data_type == "Float":
        return [random.uniform(1.0, 100000.0) for _ in range(size)]
    elif data_type == "Character":
        return [random.choice(string.ascii_letters) for _ in range(size)]
    elif data_type == "String":
        return [
            "".join(random.choices(string.ascii_uppercase, k=8))
            for _ in range(size)
        ]


def run_sort(data):
    global a, b
    a = [None] + list(data)
    b = [None] * len(a)
    n = len(data)
    MergeSort(1, n)


sizes = [1000, 2500, 5000, 7500, 10000]
datatypes = ["Integer", "Float", "Character", "String"]

perf_times = {dt: [] for dt in datatypes}
timeit_times = {dt: [] for dt in datatypes}

for dt in datatypes:
    for size in sizes:
        dataset = get_data(dt, size)
        start_time = time.perf_counter()
        run_sort(dataset)
        end_time = time.perf_counter()
        perf_times[dt].append(end_time - start_time)

        elapsed_time = timeit.timeit(lambda: run_sort(dataset), number=1)
        timeit_times[dt].append(elapsed_time)


def print_table(title, results):
    print(title)
    print(f"{'Datatype':<12}" + "".join([f"{size:>14}" for size in sizes]))
    print("-" * 82)
    for dt in datatypes:
        row = f"{dt:<12}"
        for timing in results[dt]:
            row += f"{timing:>14.6f}"
        print(row)
    print()


print_table("Merge Sort Benchmarking using time.perf_counter (time in seconds)", perf_times)
print_table("Merge Sort Benchmarking using timeit (time in seconds)", timeit_times)
