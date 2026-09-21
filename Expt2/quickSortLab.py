a = []


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

    print(show(a, m, p - 1, len(a) - 2))
    return j


def QuickSort(p, q):
    if p < q:
        j = Partition(a, p, q + 1)
        QuickSort(p, j - 1)
        QuickSort(j + 1, q)


data = [505, 209, 800, 880, 430, 199, 800, 673, 595, 985, 266]
n = len(data)

# 1-indexed array (index 0 unused) with +infinity sentinel at a[n + 1]
a = [None] + data + [float('inf')]

print("Initial array:")
print(" ".join(str(x) for x in data))
print()
print("Quick Sort steps:")

QuickSort(1, n)

print()
print("Sorted array:")
print(" ".join(str(x) for x in a[1:n + 1]))
