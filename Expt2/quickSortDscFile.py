import random
import string
import time
import timeit

a = []


def Interchange(a, i, j):
    temp = a[i]
    a[i] = a[j]
    a[j] = temp


def Partition(a, m, p):
    v = a[m]
    i = m
    j = p

    while True:
        while True:
            i = i + 1
            if a[i] <= v:
                break

        while True:
            j = j - 1
            if a[j] >= v:
                break

        if i < j:
            Interchange(a, i, j)

        if i >= j:
            break

    a[m] = a[j]
    a[j] = v
    return j


def QuickSort(p, q):
    if p < q:
        j = Partition(a, p, q + 1)
        QuickSort(p, j - 1)
        QuickSort(j + 1, q)


def get_data(data_type, size):
    if data_type == "Integer":
        return [random.randint(1, 100000) for _ in range(size)]
    elif data_type == "Float":
        return [random.uniform(1.0, 100000.0) for _ in range(size)]
    elif data_type == "Character":
        return [random.choice(string.ascii_letters) for _ in range(size)]
    elif data_type == "String":
        return [
            "".join(random.choices(string.ascii_letters, k=8))
            for _ in range(size)
        ]


def run_sort(data):
    global a
    n = len(data)
    if isinstance(data[0], str) and len(data[0]) == 1:
        sentinel = "\x00"
    elif isinstance(data[0], str):
        sentinel = ""
    else:
        sentinel = float('-inf')
    a = [None] + list(data) + [sentinel]
    QuickSort(1, n)


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


print_table("Quick Sort Benchmarking using time.perf_counter (time in seconds)", perf_times)
print_table("Quick Sort Benchmarking using timeit (time in seconds)", timeit_times)
