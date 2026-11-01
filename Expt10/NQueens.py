n = int(input("Enter the value of n: "))
x = [0] * (n + 1)
solutions = []

def Place(k, i):
    for j in range(1, k):
        if (x[j] == i) or (abs(x[j] - i) == abs(j - k)):
            return False
    return True

def NQueens(k, n):
    for i in range(1, n + 1):
        if Place(k, i):
            x[k] = i
            if k == n:
                solutions.append(x[1:n + 1].copy())
            else:
                NQueens(k + 1, n)
            x[k] = 0

NQueens(1, n)

print(f"Total no. of possible solns: {len(solutions)}\n")

for idx, sol in enumerate(solutions, 1):
    print(f"Soln {idx}:")
    for r in range(1, n + 1):
        row = ["-"] * n
        row[sol[r - 1] - 1] = "Q"
        print("  [ " + " ".join(row) + " ]")
    print(f"  Array: {sol}\n")