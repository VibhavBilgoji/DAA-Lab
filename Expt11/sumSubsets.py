import matplotlib.pyplot as plt

n = 5
m = 276
w = [0, 23, 69, 115, 161, 184]
x = [0] * (n + 2)

total_sum = sum(w[1:n+1])
w.append(float('inf'))

tree = {}
counter = [0]
solutions = []

def SumOfSub(s, k, r, chosen=(), parent=None, decision=""):

    counter[0] += 1
    node = counter[0]

    tree[node] = {
        "state": (s, k, r),
        "children": [],
        "solution": False
    }

    if parent is not None:
        tree[parent]["children"].append((node, decision))

    if s == m:
        tree[node]["solution"] = True
        solutions.append(chosen)
        print("Subset found:", chosen)
        return node

    if k <= n and s + w[k] == m:
        x[k] = 1
        SumOfSub(
            s + w[k], k + 1, r - w[k],
            chosen + (w[k],), node, 1
        )
        return node

    if k < n and s + w[k] + w[k+1] <= m:
        x[k] = 1
        SumOfSub(
            s + w[k], k + 1, r - w[k],
            chosen + (w[k],), node, 1
        )

    if (k < n and
        s + r - w[k] >= m and
        s + w[k+1] <= m):

        x[k] = 0
        SumOfSub(
            s, k + 1, r - w[k],
            chosen, node, 0
        )

    return node


root = SumOfSub(0, 1, total_sum)

positions = {}
leaf_counter = [0]

def set_positions(node, depth=0):

    children = tree[node]["children"]

    if not children:
        xpos = leaf_counter[0]
        leaf_counter[0] += 1
    else:
        child_positions = []

        for child, decision in children:
            child_x = set_positions(child, depth + 1)
            child_positions.append(child_x)

        xpos = sum(child_positions) / len(child_positions)

    positions[node] = (xpos, -depth * 1.1)
    return xpos


set_positions(root)

fig, ax = plt.subplots(figsize=(13, 7))

for node, data in tree.items():

    px, py = positions[node]
    k = data["state"][1]

    for child, decision in data["children"]:

        cx, cy = positions[child]

        ax.plot(
            [px, cx],
            [py - 0.18, cy + 0.18],
            color="black",
            linewidth=0.8
        )

        label = rf"$x_{{{k}}}={decision}$"
        offset = -0.2 if decision == 1 else 0.2

        ax.text(
            (px + cx) / 2 + offset,
            (py + cy) / 2,
            label,
            fontsize=8,
            ha="center"
        )

for node, data in tree.items():

    xpos, ypos = positions[node]
    s, k, r = data["state"]

    color = "lightgreen" if data["solution"] else "white"

    ax.text(
        xpos, ypos,
        f"{s}, {k}, {r}",
        ha="center",
        va="center",
        fontsize=8,
        bbox=dict(
            boxstyle="square,pad=0.3",
            facecolor=color,
            edgecolor="black",
            linewidth=0.8
        )
    )

    if not data["children"] and not data["solution"]:
        tag = "bound" if s + r < m else "killed"
        ax.text(
            xpos, ypos - 0.22,
            tag,
            ha="center",
            va="top",
            fontsize=7,
            color="red"
        )

ax.set_title("State Space Tree - Sum of Subsets", fontsize=12)
ax.axis("off")
plt.tight_layout()
plt.show()

