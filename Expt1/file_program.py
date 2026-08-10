import math

# a = [None, -72, -31, 71, -95, -68, -4, -55, 85, -93, 51]

def MinMax(i, j, max, min):
    if i == j:
        max[0] = min[0] = a[i]
    elif i == j-1:
        if a[i] > a[j]:
            max[0] = a[i]
            min[0] = a[j]
        else:
            max[0] = a[j]
            min[0] = a[i]
    else:
        mid = math.floor((i+j) / 2)
        MinMax(i, mid, max, min)
        max1, min1 = [None], [None]
        MinMax(mid+1, j, max1, min1)

        if max1[0] > max[0]:
            max[0] = max1[0]
        if min1[0] < min[0]:
            min[0] = min1[0]

a = [0]
n  = int(input("Enter number of elements: "))
for i in range(n):
    a.append(int(input()))

max, min = [None], [None]
MinMax(1, 10, max, min)

print("Final Max:", max[0])
print("Final Min:", min[0])
