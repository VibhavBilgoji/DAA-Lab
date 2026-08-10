import math
import random
import time


def measure_time(n):
    random_chars = [chr(random.randint(97, 122)) for _ in range(n)]

    global a
    a = ['\0'] + random_chars

    start_time = time.perf_counter()
    MergeSortDsc(1, n)
    end_time = time.perf_counter()

    time_in_ms = (end_time - start_time) * 1000
    print(f"\nInput Size: {n:<4}\tTime taken: {time_in_ms:<6.4f} ms")


def MergeSortDsc(low, high):
    if low < high:
        mid = math.floor((low + high) / 2)
        MergeSortDsc(low, mid)
        MergeSortDsc(mid + 1, high)
        MergeDsc(low, mid, high)


def MergeDsc(low, mid, high):
    h = low
    i = low
    j = mid + 1

    b = ['\0'] * (high + 1)

    while (h <= mid) and (j <= high):
        if a[h] >= a[j]:
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


print("Enter elements seperated by spaces: ")
a = ['\0'] + [str(n) for n in input().split(" ")]
n = len(a) - 1

print("\nOriginal Array:", a[1 : n + 1])
MergeSortDsc(1, n)
print("Sorted Array:  ", a[1 : n + 1])

measure_time(100)
measure_time(1000)
