import numpy as np

def splitMatrix(A):
    mid = A.shape[0] // 2
    return A[:mid, :mid], A[:mid, mid:], A[mid:, :mid], A[mid:, mid:]

def mergeMatrix(C11, C12, C21, C22):
    return np.block([[C11, C12], [C21, C22]])

def divideAndConquerMult(A, B):
    if len(A) == 1:
        return A * B

    A11, A12, A21, A22 = splitMatrix(A)
    B11, B12, B21, B22 = splitMatrix(B)

    C11 = divideAndConquerMult(A11, B11) + divideAndConquerMult(A12, B21)
    C12 = divideAndConquerMult(A11, B12) + divideAndConquerMult(A12, B22)
    C21 = divideAndConquerMult(A21, B11) + divideAndConquerMult(A22, B21)
    C22 = divideAndConquerMult(A21, B12) + divideAndConquerMult(A22, B22)

    return mergeMatrix(C11, C12, C21, C22)

def strassenMult(A, B):
    if len(A) == 1:
        return A * B

    A11, A12, A21, A22 = splitMatrix(A)
    B11, B12, B21, B22 = splitMatrix(B)

    P = strassenMult(A11 + A22, B11 + B22)
    Q = strassenMult(A21 + A22, B11)
    R = strassenMult(A11, B12 - B22)
    S = strassenMult(A22, B21 - B11)
    T = strassenMult(A11 + A12, B22)
    U = strassenMult(A21 - A11, B11 + B12)
    V = strassenMult(A12 - A22, B21 + B22)

    C11 = P + S - T + V
    C12 = R + T
    C21 = Q + S
    C22 = P + R - Q + U

    return mergeMatrix(C11, C12, C21, C22)

sizes = [32, 64, 128, 256, 512]

for n in sizes:
    A = np.random.randint(1, 1001, size=(n, n))
    B = np.random.randint(1, 1001, size=(n, n))

    dcResult = divideAndConquerMult(A, B)
    strassenResult = strassenMult(A, B)
