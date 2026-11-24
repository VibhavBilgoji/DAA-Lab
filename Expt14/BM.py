def compute_last(P):
    last = {}
    for idx in range(len(P)):
        last[P[idx]] = idx
    return last

def BMMatch(T, P):
    n = len(T)
    m = len(P)
    last = compute_last(P)

    print(f"{'i':<4} | {'j':<4} | {'last(T[i])':<10}")
    print("-" * 24)

    i = m - 1
    j = m - 1
    comp = 1
    alignments = []
    current_align_start = i - j
    current_comps = {}

    while i <= n - 1:
        l = last.get(T[i], -1)
        print(f"{i:<4} | {j:<4} | {l:<10}")

        if P[j] == T[i]:
            current_comps[j] = comp
            if j == 0:
                alignments.append((current_align_start, current_comps))
                break
            else:
                i -= 1
                j -= 1
        else:
            current_comps[j] = comp
            alignments.append((current_align_start, current_comps))
            i = i + m - min(j, 1 + l)
            j = m - 1
            current_align_start = i - j
            current_comps = {}
        comp += 1
    else:
        if current_comps:
            alignments.append((current_align_start, current_comps))
        i = -1

    print("\nAlignment Diagram:")
    idx_str = "Index:  " + " ".join(f"{k:<2}" for k in range(n))
    txt_str = "Text:   " + " ".join(f"{ch:<2}" for ch in T)
    print(idx_str)
    print(txt_str)
    print("        " + "-" * (n * 3 - 1))

    for start, comps in alignments:
        prefix = "        " + "   " * start
        comp_line = prefix + " ".join(f"{comps[k]:<2}" if k in comps else "  " for k in range(m))
        pat_line = prefix + " ".join(f"{ch:<2}" for ch in P)
        print(comp_line)
        print(pat_line)

    if i != -1:
        print(f"\nStarting Index of Match: {i}")
        print(f"Total Comparisons: {comp}")
    else:
        print("\nThere is no substring of T matching P.")

T = "vvbbbhhhbhvbhvvhvvbvbvbvh"
P = "vbvbvh"
BMMatch(T, P)