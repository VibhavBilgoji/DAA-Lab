# Problem instance settngs
n = 6
m = 30
w = [5, 10, 12, 13, 15, 18]

# x array to keep track of the subset (1 if included, 0 if excluded)
x = [0] * n

def SumOfSub(s, k, r):
    """
    Algorithm 7.6: Recursive backtracking algorithm for sum of subsets problem.
    s: current sum of included elements
    k: current index being considered
    r: sum of remaining elements
    """
    # Step visualization
    print(f"Evaluating Node: s={s}, k={k}, r={r}")

    # Generate left child (Include w[k])
    x[k] = 1
    print(f" -> Try including w[{k}]={w[k]} => subset path: {x[:k+1]}")

    # Check if a valid subset is found
    if s + w[k] == m:
        # Output matches the formats (1, 1, 0, 0, 1), etc.
        print(f"\n*** SUBSET FOUND: {tuple(x[:k+1])} ***\n")
        # No recursive call here as w[j] > 0 for all j

    # Check if we can still include the next element without exceeding m
    elif k + 1 < n and s + w[k] + w[k+1] <= m:
        SumOfSub(s + w[k], k + 1, r - w[k])

    # Generate right child and evaluate Bk (Exclude w[k])
    # Bounding condition:
    # 1. (s + r - w[k] >= m): Remaining sum is enough to reach target m
    # 2. (s + w[k+1] <= m): Adding the NEXT element doesn't exceed target m
    if k + 1 < n and (s + r - w[k] >= m) and (s + w[k+1] <= m):
        x[k] = 0
        print(f" -> Try excluding w[{k}]={w[k]} => subset path: {x[:k+1]}")
        SumOfSub(s, k + 1, r - w[k])

# Execution
print(f"Target sum (m) = {m}")
print(f"Weights (w) = {w}")
print(f"Initial sum of all elements = {sum(w)}\n")

# Start at the root: current sum = 0, index = 0, remaining sum = sum(w)
SumOfSub(0, 0, sum(w))