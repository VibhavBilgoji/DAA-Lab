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
    return f"x{k}={c}"

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

labels = {v: str(v + 1) for v in T.nodes}
edge_labels = {(p, c): info[c]["label"] for p, c in T.edges}
node_sizes = [600 if v == root else 600 for v in T.nodes]

n_leaves = _leaf[0]
fig, ax = plt.subplots(figsize=(max(14, 0.3 * n_leaves + 3), 8))
nx.draw_networkx_edges(T, pos, ax=ax, arrows=False, edge_color="black", width=1)
nx.draw_networkx_nodes(T, pos, ax=ax, node_color="white", node_size=node_sizes,
                       edgecolors="black", linewidths=1)
nx.draw_networkx_labels(T, pos, labels=labels, ax=ax, font_size=8, font_color="black")
nx.draw_networkx_edge_labels(T, pos, edge_labels=edge_labels, ax=ax, font_size=6,
                             font_color="black", label_pos=0.5, rotate=False,
                             bbox=dict(boxstyle="square,pad=0", fc="none", ec="none"))

for v in T.nodes:
    if info[v]["status"] == "bounded":
        ax.text(pos[v][0], pos[v][1] - 0.25, "B", ha="center", va="center",
                fontsize=9, color="black")

ax.set_title(f"m-Coloring State Space Tree (m = {m})", fontsize=12, color="black")
ax.axis("off")
plt.tight_layout()
plt.show()
