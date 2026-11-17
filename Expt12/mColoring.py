import matplotlib.pyplot as plt
import networkx as nx

n = 5
x = [0] * (n + 1)

SHOW_KILLED = True

G = [
    [0, 0, 0, 0, 0, 0],  # dummy row 0, no edges
    [0, 0, 1, 1, 0, 0],  # vertex 1: adj 2, 3
    [0, 1, 0, 1, 1, 0],  # vertex 2: adj 1, 3, 4
    [0, 1, 1, 0, 0, 1],  # vertex 3: adj 1, 2, 5
    [0, 0, 1, 0, 0, 1],  # vertex 4: adj 2, 5
    [0, 0, 0, 1, 1, 0],  # vertex 5: adj 3, 4
]

def colorable(k, m_try, y):
    """Return True as soon as one valid m_try-coloring of vertices k..n exists."""
    if k > n:
        return True
    for c in range(1, m_try + 1):
        if all(not (G[k][j] and y[j] == c) for j in range(1, n + 1)):
            y[k] = c
            if colorable(k + 1, m_try, y):
                return True
            y[k] = 0
    return False

m = 1
while not colorable(1, m, [0] * (n + 1)):
    m += 1

_names = "RGBYOPCMKW"
COLORS = {c: (_names[c - 1] if c <= len(_names) else str(c)) for c in range(1, m + 1)}

solution_count = 0

T = nx.DiGraph()
info = {}
_id = [0]

def add_node(label, status, parent=None):
    nid = _id[0]; _id[0] += 1
    T.add_node(nid)
    info[nid] = {"label": label, "status": status}
    if parent is not None:
        T.add_edge(parent, nid)
    return nid

def lbl(k, c):
    return COLORS[c]

def NextValue(k):
    while True:
        x[k] = (x[k] + 1) % (m + 1)
        if x[k] == 0:
            return
        j = 1
        while j <= n:
            if G[k][j] != 0 and x[k] == x[j]:
                break
            j += 1
        if j == n + 1:
            return

def mColoring(k, parent):
    global solution_count
    children = 0
    while True:
        prev = x[k]
        NextValue(k)
        c = x[k]

        if SHOW_KILLED:
            for r in range(prev + 1, c if c else m + 1):
                add_node(lbl(k, r), "bounded", parent)

        if c == 0:
            return children

        children += 1
        if k == n:
            solution_count += 1
            print(f"Solution {solution_count}: {x[1:]}")
            add_node(lbl(k, c), "solution", parent)
        else:
            node = add_node(lbl(k, c), "open", parent)
            if mColoring(k + 1, node) == 0:   # feasible but every child rejected
                info[node]["status"] = "bounded"

print(f"Chromatic number found: m = {m}")
print(f"Starting m-Coloring (Vertices: {n}, Colors: {m})")
root = add_node("Root", "open")
mColoring(1, root)
print(f"\nTotal valid colorings: {solution_count}")

pos = {}
_leaf = [0]
def layout(node, depth):
    ch = list(T.successors(node))
    if not ch:
        xx = _leaf[0]; _leaf[0] += 1
    else:
        xs = [layout(c, depth + 1) for c in ch]
        xx = sum(xs) / len(xs)
    pos[node] = (xx, -depth)
    return xx
layout(root, 0)

from matplotlib.patches import Patch

colors = {"open": "#a6cee3", "bounded": "#f1948a", "solution": "#82e0aa"}
node_colors = [colors[info[v]["status"]] for v in T.nodes]
node_sizes = [1300 if v == root else 420 for v in T.nodes]
labels = {v: info[v]["label"] for v in T.nodes}

n_leaves = _leaf[0]
fig, ax = plt.subplots(figsize=(max(14, 0.42 * n_leaves + 3), 8))
nx.draw_networkx_edges(T, pos, ax=ax, arrows=True, arrowsize=8,
                       edge_color="#888888", width=1, node_size=node_sizes)
nx.draw_networkx_nodes(T, pos, ax=ax, node_color=node_colors,
                       node_size=node_sizes, edgecolors="#444444", linewidths=0.8)
nx.draw_networkx_labels(T, pos, labels=labels, ax=ax, font_size=8, font_weight="bold")

x_left = min(p[0] for p in pos.values()) - 1.8
ax.text(x_left, 0, "Root", ha="right", va="center", fontsize=10, color="#555555")
for k in range(1, n + 1):
    ax.text(x_left, -k, f"x[{k}]", ha="right", va="center", fontsize=10, color="#555555")
    ax.axhline(-k, color="#dddddd", lw=0.6, zorder=0)

counts = {s: sum(1 for v in info.values() if v["status"] == s) for s in colors}
legend = [Patch(facecolor=colors["open"], edgecolor="#444444", label="feasible (partial)"),
          Patch(facecolor=colors["solution"], edgecolor="#444444",
                label=f"solution ({counts['solution']})")]
if counts["bounded"]:
    legend.append(Patch(facecolor=colors["bounded"], edgecolor="#444444",
                        label=f"bounded / rejected ({counts['bounded']})"))
ax.legend(handles=legend, loc="upper right", fontsize=10)

key = " ".join(f"{COLORS[c]}={c}" for c in COLORS)
ax.set_title(f"m-Coloring State-Space Tree (n={n}, m={m}, {key})   "
             f"total nodes={T.number_of_nodes()}", fontsize=13)
ax.set_xlim(x_left - 1.2, max(p[0] for p in pos.values()) + 0.8)
ax.axis("off")
plt.tight_layout()
plt.show()