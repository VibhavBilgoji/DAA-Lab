def greedyKnapsack(m, items):
    u = m
    total = 0.0

    for p, w in items:
        if w > u:
            total += p * (u / w)
            break

        total += p
        u -= w

    return total


def main():
    n = int(input("Enter n: "))

    profits = [float(i) for i in input("Enter profits: ").split()]
    weights = [float(i) for i in input("Enter weights: ").split()]

    m = float(input("Enter knapsack capacity: "))

    # elements as (profit, weight), kept in their original index order 1..n
    elements = list(zip(profits[:n], weights[:n]))

    # case 1: element number j (from 1) has both its profit and weight
    # divided by i = j + 1, i.e. the ratio 1 / i starts from i = 2.
    # The original order is kept.
    scaled = [(p / (j + 1), w / (j + 1)) for j, (p, w) in enumerate(elements, start=1)]

    cases = [
        ("ratio 1 / i", scaled),
        ("decreasing profits", sorted(elements, key=lambda e: e[0], reverse=True)),
        ("increasing weights", sorted(elements, key=lambda e: e[1])),
        ("decreasing profit/weight", sorted(elements, key=lambda e: e[0] / e[1], reverse=True)),
    ]

    print("\nelements :", [(f"{p:g}", f"{w:g}") for p, w in elements], "(profit, weight)")
    print("capacity :", f"{m:g}\n")

    header = f"| {'case':<4} | {'ratios of elements':<24} | {'maximum profit':>14} |"
    line = "|" + "-" * 6 + "|" + "-" * 26 + "|" + "-" * 16 + "|"

    print(line)
    print(header)
    print(line)

    for k, (label, ordered) in enumerate(cases, start=1):
        profit = greedyKnapsack(m, ordered)
        print(f"| {k:<4} | {label:<24} | {profit:>14.2f} |")

    print(line)


if __name__ == "__main__":
    main()
