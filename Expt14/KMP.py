def kmp_failure_function(P):
    m = len(P)
    f = [0] * m
    i = 1
    j = 0
    while i < m:
        if P[j] == P[i]:
            f[i] = j + 1
            i += 1
            j += 1
        elif j > 0:
            j = f[j - 1]
        else:
            f[i] = 0
            i += 1
    return f

def kmp_match_with_trace(T, P):
    n = len(T)
    m = len(P)
    f = kmp_failure_function(P)

    print("Failure Function Table:")
    print("j:    " + " ".join(f"{k:<2}" for k in range(m)))
    print("P[j]: " + " ".join(f"{ch:<2}" for ch in P))
    print("f(j): " + " ".join(f"{val:<2}" for val in f))
    print()

    print(f"{'i':<4} | {'j':<4} | {'f(j-1)':<8}")
    print("-" * 22)

    i = 0
    j = 0
    comp = 1
    alignments = []
    current_align_start = i - j
    current_comps = {}
    match_idx = -1

    while i < n:
        f_val = f[j - 1] if j > 0 else "-"
        print(f"{i:<4} | {j:<4} | {str(f_val):<8}")

        if P[j] == T[i]:
            current_comps[j] = comp
            if j == m - 1:
                alignments.append((current_align_start, current_comps))
                match_idx = i - m + 1
                break
            i += 1
            j += 1
        elif j > 0:
            current_comps[j] = comp
            alignments.append((current_align_start, current_comps))
            j = f[j - 1]
            current_align_start = i - j
            current_comps = {}
        else:
            current_comps[j] = comp
            alignments.append((current_align_start, current_comps))
            i += 1
            current_align_start = i - j
            current_comps = {}
        comp += 1
    else:
        if current_comps:
            alignments.append((current_align_start, current_comps))

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

    if match_idx != -1:
        print(f"\nStarting Index of Match: {match_idx}")
        print(f"Total Comparisons: {comp}")
    else:
        print("\nThere is no substring of T matching P.")

T = "sssscsqqsqccsssqsqqsssscq"
P = "sssscq"
kmp_match_with_trace(T, P)
