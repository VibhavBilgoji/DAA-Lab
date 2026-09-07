def greedyKnapsack(m, n):
    i = 0
    for i in range(1, n + 1):
        x[i] = 0.0

    u = m

    for i in range(1, n + 1):
        if w[i] > u:
            break

        x[i] = 1.0
        u = u - w[i]

    i += 1

    if i <= n:
        x[i] = u / w[i]


def main():
    global p, w, x

    n = int(input("Enter n: "))

    p = [0.0] + [float(i) for i in input("Enter profits: ").split()]
    w = [0.0] + [float(i) for i in input("Enter weights: ").split()]

    m = float(input("Enter knapsack capacity: "))

    items = sorted(
        [(p[i], w[i]) for i in range(1, n + 1)],
        key=lambda item: item[0] / item[1],
        reverse=True
    )

    p = [0.0] + [item[0] for item in items]
    w = [0.0] + [item[1] for item in items]

    x = [0.0] * (n + 1)

    greedyKnapsack(m, n)

    profit = 0

    print("\nSolution:")

    for i in range(1, n + 1):
        print(f"x[{i}] = {x[i]:.2f}")
        profit += p[i] * x[i]

    print("Maximum profit:", profit)
    print("m=",m)

if __name__ == "__main__":
    main()
