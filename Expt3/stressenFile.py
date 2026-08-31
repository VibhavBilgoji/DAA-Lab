import random
import time


def add(A:list[list[int]], B:list[list[int]]):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A:list[list[int]], B:list[list[int]]):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def splitMatrix(A:list[list[int]]):
    n = len(A)
    mid = n // 2
    A11 = [[A[i][j] for j in range(mid)] for i in range(mid)]
    A12 = [[A[i][j] for j in range(mid, n)] for i in range(mid)]
    A21 = [[A[i][j] for j in range(mid)] for i in range(mid, n)]
    A22 = [[A[i][j] for j in range(mid, n)] for i in range(mid, n)]
    return A11, A12, A21, A22

def mergeMatrix(C11:list[list[int]], C12:list[list[int]], C21:list[list[int]], C22:list[list[int]]):
    n = len(C11) * 2
    mid = len(C11)
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
    return C

def divideAndConquerMult(A:list[list[int]], B:list[list[int]]):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = splitMatrix(A)
    B11, B12, B21, B22 = splitMatrix(B)

    C11 = add(divideAndConquerMult(A11, B11), divideAndConquerMult(A12, B21))
    C12 = add(divideAndConquerMult(A11, B12), divideAndConquerMult(A12, B22))
    C21 = add(divideAndConquerMult(A21, B11), divideAndConquerMult(A22, B21))
    C22 = add(divideAndConquerMult(A21, B12), divideAndConquerMult(A22, B22))

    return mergeMatrix(C11, C12, C21, C22)

def strassenMult(A:list[list[int]], B:list[list[int]]):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = splitMatrix(A)
    B11, B12, B21, B22 = splitMatrix(B)

    P = strassenMult(add(A11, A22), add(B11, B22))
    Q = strassenMult(add(A21, A22), B11)
    R = strassenMult(A11, sub(B12, B22))
    S = strassenMult(A22, sub(B21, B11))
    T = strassenMult(add(A11, A12), B22)
    U = strassenMult(sub(A21, A11), add(B11, B12))
    V = strassenMult(sub(A12, A22), add(B21, B22))

    C11 = add(sub(add(P, S), T), V)
    C12 = add(R, T)
    C21 = add(Q, S)
    C22 = add(sub(add(P, R), Q), U)

    return mergeMatrix(C11, C12, C21, C22)

def generateRandomMatrix(n):
    return [[random.randint(1, 1000) for _ in range(n)] for _ in range(n)]

sizes = [32, 64, 128, 256, 512]

print("_________________________________________________________________")
print("|   n   |  Divide and conquer | Strassen's Algorithm |")
print("_________________________________________________________________")

for n in sizes:
    A = generateRandomMatrix(n)
    B = generateRandomMatrix(n)

    startTime = time.perf_counter()
    divideAndConquerMult(A, B)
    dcTime = time.perf_counter() - startTime

    startTime = time.perf_counter()
    strassenMult(A, B)
    strassenTime = time.perf_counter() - startTime

    print(f"|  {n:<4} | {dcTime:18.4f}s | {strassenTime:19.4f}s |")

print("_________________________________________________________________")
