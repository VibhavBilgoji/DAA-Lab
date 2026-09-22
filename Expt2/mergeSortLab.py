import math

a = []
b = []


def show(arr, low, high, last):
    """Return arr[1..last] as text, with arr[low..high] wrapped in [ ]."""
    out = []
    for k in range(1, last + 1):
        s = str(arr[k])
        if k == low:
            s = "[" + s
        if k == high:
            s = s + "]"
        out.append(s)
    return " ".join(out)


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

    print(show(a, low, high, len(a) - 1))


data = ["Q", "L", "R", "W", "O", "X", "Q", "N", "E", "Y"]

a = [None] + data          # 1-indexed array (index 0 unused)
b = [None] * len(a)        # auxiliary array
n = len(data)

print("Initial array:")
print(" ".join(data))
print()
print("Merge Sort steps:")

MergeSort(1, n)

print()
print("Sorted array:")
print(" ".join(a[1:]))
