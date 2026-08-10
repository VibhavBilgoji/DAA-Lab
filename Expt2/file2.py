import random
import time


def measure_quicksort_time(n):
    random_numbers = [random.randint(-100, 100) for _ in range(n)]

    global a
    a = [None] + random_numbers + [float("inf")]

    start_time = time.perf_counter()
    QuickSort(1, n)
    end_time = time.perf_counter()

    time_in_ms = (end_time - start_time) * 1000
    print(f"\nInput Size: {n:<4}\tTime taken: {time_in_ms:<6.4f} ms")

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
            if a[i] >= v:
                break

        while True:
            j = j - 1
            if a[j] <= v:
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

print("Enter elements seperated by spaces: ");
a = [None] + [int(n) for n in input().split(" ")] + [float("inf")]
n = len(a) - 2

print("\nOriginal Array:", a[1 : n + 1])
QuickSort(1, n)
print("Sorted Array:  ", a[1 : n + 1])

measure_quicksort_time(100)
measure_quicksort_time(1000)
