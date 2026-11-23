import heapq
from fractions import Fraction
import matplotlib.pyplot as plt

p = [41, 20, 40, 45, 25, 12]
w = [4, 2, 7, 8, 5, 6]
m = 16
n = len(p)


def Bound(cp, cw, k):
    """Lower bound on cost = -(fractional-knapsack profit) from item k onward."""
    b = Fraction(cp)
    c = cw
    for i in range(k, n):
        c += w[i]
        if c <= m:
            b += p[i]
        else:
            return -(b + (1 - Fraction(c - m, w[i])) * p[i])
    return -b


def UBound(cp, cw, k):
    """Upper bound on cost = -(profit of a greedy feasible completion)."""
    b = cp
    c = cw
    for i in range(k, n):
        if c + w[i] <= m:
            c += w[i]
            b += p[i]
    return -b


class Node:
    def __init__(self, node_id, cp, cw, k, parent, edge, x):
        self.id, self.cp, self.cw, self.k = node_id, cp, cw, k
        self.parent, self.edge, self.x = parent, edge, x
        self.children = []
        self.status = "live"  # live | killed | infeasible | optimal
        self.c_hat = self.u = None
        if cw > m:
            self.status = "infeasible"
        elif k == n:
            self.c_hat = self.u = -cp
        else:
            self.c_hat = Bound(cp, cw, k)
            self.u = UBound(cp, cw, k)


def lc_branch_and_bound():
    root = Node(1, 0, 0, 0, None, "", [0] * n)
    nodes = {1: root}
    U = root.u
    heap = [(root.c_hat, root.id)]
    answer = None

    while heap:
        c_hat, nid = heapq.heappop(heap)
        node = nodes[nid]
        if c_hat > U:  # smallest c_hat is already worse than U: kill everything left
            node.status = "killed"
            for _, rid in heap:
                nodes[rid].status = "killed"
            break
        if node.k == n:  # least-cost live node is a leaf -> optimal
            node.status = "optimal"
            answer = node
            break

        for take in (1, 0):
            nxt = len(nodes) + 1
            x = node.x.copy()
            x[node.k] = take
            child = Node(nxt, node.cp + take * p[node.k], node.cw + take * w[node.k],
                         node.k + 1, node.id, "x%d=%d" % (node.k + 1, take), x)
            nodes[nxt] = child
            node.children.append(child)
            if child.status == "infeasible":
                continue
            U = min(U, child.u)
            if child.c_hat > U:
                child.status = "killed"
            else:
                heapq.heappush(heap, (child.c_hat, child.id))

    # live nodes that were never expanded are bounded out by the answer
    for node in nodes.values():
        if node.status == "live" and not node.children:
            node.status = "bound"

    return nodes, answer


def fmt(v, digits=3):
    v = float(v)
    return str(int(v)) if v == int(v) else ("%." + str(digits) + "f") % v


nodes, answer = lc_branch_and_bound()

print("Node Calculations:")
for nid, node in sorted(nodes.items()):
    if node.status == "infeasible":
        print("Node %d (%s): Infeasible (w=%d > %d)" % (nid, node.edge, node.cw, m))
    else:
        print("Node %d (%s): c = %s, u = %s [%s]" %
              (nid, node.edge or "root", fmt(node.c_hat), fmt(node.u), node.status))

path = []
cur = answer
while cur is not None:
    path.append(cur.id)
    cur = nodes.get(cur.parent)
path.reverse()

print("\nOptimal Maximum Profit:", answer.cp)
print("X vector:", answer.x)
print("Path:", " -> ".join(map(str, path)))

# ---- Drawing ----
positions = {}
leaf_x = [0]


def layout(node, depth):
    if not node.children:
        x = leaf_x[0]
        leaf_x[0] += 1
    else:
        xs = [layout(c, depth + 1) for c in node.children]
        x = sum(xs) / len(xs)
    positions[node.id] = (x * 1.8, -depth * 1.8)
    return x


layout(nodes[1], 0)

tags = {"killed": "killed", "bound": "bound", "infeasible": "inf"}

fig, ax = plt.subplots(figsize=(16, 10))

for node in nodes.values():
    if node.parent is None:
        continue
    x, y = positions[node.id]
    px, py = positions[node.parent]
    ax.plot([px, x], [py, y], color="black", lw=1.2, zorder=1)
    ax.text((px + x) / 2, (py + y) / 2, node.edge, fontsize=8, color="black",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

for node in nodes.values():
    x, y = positions[node.id]
    ax.add_patch(plt.Circle((x, y), 0.32, fc="white", ec="black", lw=1.5, zorder=2))
    ax.text(x, y, str(node.id), fontsize=10, fontweight="bold", ha="center", va="center", zorder=3)
    if node.status == "infeasible":
        ax.text(x, y - 0.5, "w=%d > %d" % (node.cw, m), fontsize=8, color="black",
                ha="center", va="top")
        ax.text(x, y - 0.8, tags[node.status], fontsize=9, fontweight="bold",
                ha="center", va="top")
    else:
        ax.text(x, y - 0.45, r"$\hat{c}=$" + fmt(node.c_hat, 1), fontsize=8, color="black",
                ha="center", va="top")
        ax.text(x, y - 0.75, r"$u=$" + fmt(node.u, 1), fontsize=8, color="black",
                ha="center", va="top")
        if node.status in tags:
            ax.text(x, y - 1.05, tags[node.status], fontsize=9, fontweight="bold",
                    ha="center", va="top")


ax.set_aspect("equal")
ax.axis("off")
ax.autoscale_view()
plt.title("LC Branch-and-Bound State Space Tree (0/1 Knapsack)", fontsize=13)
plt.tight_layout()
plt.show()
