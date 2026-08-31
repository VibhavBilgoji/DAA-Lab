import random
import string
import time
import timeit

# Global arrays as specified in the algorithm notes
a = []
b = []


# -------------------------------------------------------------------
# Algorithm Implementation (Directly mapped from handwritten notes)
# -------------------------------------------------------------------
def merge(low, mid, high):
    global a, b
    h = low
    i = low
    j = mid + 1

    # Merge elements from both halves into auxiliary array b
    while h <= mid and j <= high:
        if a[h] <= a[j]:
            b[i] = a[h]
            h += 1
        else:
            b[i] = a[j]
            j += 1
        i += 1

    # Copy remaining elements from right sub-array
    if h > mid:
        for k in range(j, high + 1):
            b[i] = a[k]
            i += 1
    # Copy remaining elements from left sub-array
    else:
        for k in range(h, mid + 1):
            b[i] = a[k]
            i += 1

    # Copy sorted elements back into global array a
    for k in range(low, high + 1):
        a[k] = b[k]


def merge_sort(low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(low, mid)
        merge_sort(mid + 1, high)
        merge(low, mid, high)


# -------------------------------------------------------------------
# Data Generator Functions
# -------------------------------------------------------------------
def generate_data(data_type, size):
    if data_type == "Integer":
        return [random.randint(1, 100000) for _ in range(size)]
    elif data_type == "Float":
        return [random.uniform(1.0, 100000.0) for _ in range(size)]
    elif data_type == "Alphabet":
        return [random.choice(string.ascii_letters) for _ in range(size)]
    elif data_type == "Strings":
        return [
            "".join(random.choices(string.ascii_letters, k=8))
            for _ in range(size)
        ]


def run_sort(data):
    global a, b
    a = list(data)  # Populate global array 'a'
    b = [None] * len(data)  # Allocate global auxiliary array 'b'
    merge_sort(0, len(a) - 1)


# -------------------------------------------------------------------
# Execution & Table Output
# -------------------------------------------------------------------
sizes = [1000, 2500, 5000, 7500, 10000]
datatypes = ["Integer", "Float", "Alphabet", "Strings"]

perf_results = {dt: [] for dt in datatypes}
timeit_results = {dt: [] for dt in datatypes}

# Benchmark execution
for dt in datatypes:
    for size in sizes:
        dataset = generate_data(dt, size)

        # 1. Timing with time.perf_counter
        start_time = time.perf_counter()
        run_sort(dataset)
        end_time = time.perf_counter()
        perf_results[dt].append(end_time - start_time)

        # 2. Timing with timeit module
        t = timeit.Timer(lambda: run_sort(dataset))
        timeit_results[dt].append(t.timeit(number=1))


def print_table(title, results):
    print(title)
    # Header format matching sample output spacing
    print(f"{'Datatype':<12}" + "".join([f"{size:>14}" for size in sizes]))
    print("-" * 82)
    for dt in datatypes:
        row = f"{dt:<12}"
        for timing in results[dt]:
            row += f"{timing:>14.6f}"
        print(row)
    print("Time is shown in seconds.\n")


# Display final outputs
print_table("Merge Sort Timing using time.perf_counter", perf_results)
print_table("Merge Sort Timing using timeit", timeit_results)
