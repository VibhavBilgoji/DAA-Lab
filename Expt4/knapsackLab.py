from fractions import Fraction


def greedyKnapsack(m, items):
    u = m
    total = 0
    included = {}

    for idx, p, w in items:
        if w > u:
            frac = u / w
            total += p * frac
            included[idx] = w * frac
            break

        total += p
        u -= w
        included[idx] = w

    return total, included


def format_ratio(r):
    r = Fraction(r)
    return str(r.numerator) if r.denominator == 1 else f"{r.numerator}/{r.denominator}"


def main():
    # n = int(input("Enter n: "))
    n = 11

    # profits = [float(i) for i in input("Enter profits: ").split()]
    profits = [Fraction(x) for x in [387, 281, 357, 456, 570, 768, 408, 26, 254, 62, 464]]
    # weights = [float(i) for i in input("Enter weights: ").split()]
    weights = [Fraction(x) for x in [23, 84, 69, 47, 95, 85, 61, 96, 75, 51, 94]]

    # m = float(input("Enter knapsack capacity: "))
    m = Fraction(768)

    # elements as (profit, weight), kept in their original index order 1..n
    elements = list(zip(profits[:n], weights[:n]))

    # tag every element with its original 1-based index so we can always
    # map results back to the original (unmodified) input order
    indexed_elements = list(enumerate(elements, start=1))  # (idx, (p, w))
    original_weight = {idx: w for idx, (p, w) in indexed_elements}

    # case 1: element number j (from 1) has both its profit and weight
    # divided by i = j + 1, i.e. the ratio 1 / i starts from i = 2.
    # The original order is kept.
    scaled_indexed = [
        (idx, (p / (idx + 1), w / (idx + 1))) for idx, (p, w) in indexed_elements
    ]

    cases = [
        ("1 / i Ratio", scaled_indexed),
        ("Maximum Profits", sorted(indexed_elements, key=lambda ie: ie[1][0], reverse=True)),
        ("Minimum Weights", sorted(indexed_elements, key=lambda ie: ie[1][1])),
        (
            "Maximum profit/weight",
            sorted(indexed_elements, key=lambda ie: ie[1][0] / ie[1][1], reverse=True),
        ),
    ]

    print("\nelements :", [(f"{float(p):g}", f"{float(w):g}") for p, w in elements], "(profit, weight)")
    print("capacity :", f"{float(m):g}\n")

    # for each case, run the greedy fill and, per element (in ORIGINAL
    # index order), work out what fraction of its ORIGINAL weight actually
    # ended up in the sack: 1 if fully taken, a fraction if it's the one
    # element that got cut off when capacity ran out, 0 if never reached
    rows = []
    for label, case_items in cases:
        items_for_algo = [(idx, p, w) for idx, (p, w) in case_items]
        profit, included = greedyKnapsack(m, items_for_algo)

        ratios = [
            included.get(idx, Fraction(0)) / original_weight[idx] for idx in range(1, n + 1)
        ]
        ratio_str = "[" + ", ".join(format_ratio(r) for r in ratios) + "]"
        rows.append((label, float(profit), ratio_str))

    ratio_col_width = max(24, max(len(ratio_str) for _, _, ratio_str in rows) + 2)

    header = (
        f"| {'case':<4} | {'ratios of elements':<24} | {'maximum profit':>14} "
        f"| {'weight ratios (original order)':<{ratio_col_width}} |"
    )
    line = (
        "|" + "-" * 6 + "|" + "-" * 26 + "|" + "-" * 16 + "|" + "-" * (ratio_col_width + 2) + "|"
    )

    print(line)
    print(header)
    print(line)

    for k, (label, profit, ratio_str) in enumerate(rows, start=1):
        print(
            f"| {k:<4} | {label:<24} | {profit:>14.2f} "
            f"| {ratio_str:<{ratio_col_width}} |"
        )

    print(line)


if __name__ == "__main__":
    main()