def parse_number(text):
    try:
        return int(text)
    except ValueError:
        return float(text)


def read_matrix(name):
    print(f"\nEnter matrix {name} (2 rows, 2 space-separated numbers each):")
    matrix = []
    for i in range(2):
        while True:
            try:
                row = [parse_number(x) for x in input(f"  Row {i + 1}: ").split()]
                if len(row) != 2:
                    raise ValueError
                break
            except ValueError:
                print("  Invalid input. Please enter exactly 2 numbers.")
        matrix.append(row)
    return matrix


def print_matrix(name, M):
    print(f"{name} =")
    for row in M:
        print("  [" + "  ".join(f"{x:>6}" for x in row) + " ]")


def strassen_2x2(A, B):
    # Step 1: "split" the matrices into individual elements
    A11, A12 = A[0]
    A21, A22 = A[1]
    B11, B12 = B[0]
    B21, B22 = B[1]

    print("\nSTEP 1: Split the matrices into elements")
    print(f"A11 = {A11}, A12 = {A12}, A21 = {A21}, A22 = {A22}")
    print(f"B11 = {B11}, B12 = {B12}, B21 = {B21}, B22 = {B22}")

    # Step 2: the seven Strassen products
    P = (A11 + A22) * (B11 + B22)
    Q = (A21 + A22) * B11
    R = A11 * (B12 - B22)
    S = A22 * (B21 - B11)
    T = (A11 + A12) * B22
    U = (A21 - A11) * (B11 + B12)
    V = (A12 - A22) * (B21 + B22)

    print("\nSTEP 2: Compute the 7 products")
    print(f"P = (A11 + A22) * (B11 + B22) = ({A11} + {A22}) * ({B11} + {B22}) = {P}")
    print(f"Q = (A21 + A22) * B11         = ({A21} + {A22}) * {B11} = {Q}")
    print(f"R = A11 * (B12 - B22)         = {A11} * ({B12} - {B22}) = {R}")
    print(f"S = A22 * (B21 - B11)         = {A22} * ({B21} - {B11}) = {S}")
    print(f"T = (A11 + A12) * B22         = ({A11} + {A12}) * {B22} = {T}")
    print(f"U = (A21 - A11) * (B11 + B12) = ({A21} - {A11}) * ({B11} + {B12}) = {U}")
    print(f"V = (A12 - A22) * (B21 + B22) = ({A12} - {A22}) * ({B21} + {B22}) = {V}")

    # Step 3: combine the products into the result elements
    C11 = P + S - T + V
    C12 = R + T
    C21 = Q + S
    C22 = P + R - Q + U

    print("\nSTEP 3: Combine the products into the result")
    print(f"C11 = P + S - T + V = {P} + {S} - {T} + {V} = {C11}")
    print(f"C12 = R + T         = {R} + {T} = {C12}")
    print(f"C21 = Q + S         = {Q} + {S} = {C21}")
    print(f"C22 = P + R - Q + U = {P} + {R} - {Q} + {U} = {C22}")

    # Step 4: merge the elements back into a matrix
    return [[C11, C12], [C21, C22]]


def main():
    print("Strassen's Algorithm for 2x2 Matrix Multiplication")

    A = read_matrix("A")
    B = read_matrix("B")

    print("\nInput matrices:")
    print_matrix("A", A)
    print_matrix("B", B)

    C = strassen_2x2(A, B)

    print("\nSTEP 4: Merge into the final matrix C = A x B")
    print_matrix("C", C)


if __name__ == "__main__":
    main()
