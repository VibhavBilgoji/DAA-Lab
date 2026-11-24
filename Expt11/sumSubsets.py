import matplotlib.pyplot as plt

n = 5
m = 243
w = [0, 27, 81, 108, 135, 162]
x = [0] * (n + 2)

total_sum = sum(w[1:n + 1])
w.append(float("inf"))

tree = {}
counter = [0]
solutions = []


def add_node(state, parent=None, decision="", is_solution=False, is_bound=False):
    counter[0] += 1
    node = counter[0]
    tree[node] = {
        "state": state,
        "children": [],
        "solution": is_solution,
        "bound": is_bound,
    }
    if parent is not None:
        tree[parent]["children"].append((node, decision))
    return node


def SumOfSub(s, k, r, chosen=(), parent=None, decision=""):
    node = add_node((s, k, r), parent=parent, decision=decision, is_solution=(s == m))

    if s == m:
        solutions.append(chosen)
        print("Subset found:", chosen)
        return node

    if k <= n:
        next_r = r - w[k]

        if s + w[k] == m or (k < n and s + w[k] + w[k + 1] <= m):
            x[k] = 1
            SumOfSub(s + w[k], k + 1, next_r, chosen + (w[k],), node, 1)
        else:
            add_node((s + w[k], k + 1, next_r), parent=node, decision=1, is_bound=True)

        if k < n and (s + r - w[k] >= m) and (s + w[k + 1] <= m):
            x[k] = 0
            SumOfSub(s, k + 1, next_r, chosen, node, 0)
        else:
            add_node((s, k + 1, next_r), parent=node, decision=0, is_bound=True)

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
        child_positions = [set_positions(child, depth + 1) for child, _ in children]
        xpos = sum(child_positions) / len(child_positions)

    positions[node] = (xpos, -depth * 1.45)
    return xpos


set_positions(root)

fig, ax = plt.subplots(figsize=(15, 8))

for node, data in tree.items():
    px, py = positions[node]
    k = data["state"][1]

    for child, decision in data["children"]:
        cx, cy = positions[child]

        ax.plot(
            [px, cx],
            [py - 0.18, cy + 0.18],
            color="black",
            linewidth=0.8,
        )

        label = rf"$x_{{{k}}}={decision}$"
        offset = -0.22 if decision == 1 else 0.22

        ax.text(
            (px + cx) / 2 + offset,
            (py + cy) / 2,
            label,
            fontsize=8,
            ha="center",
            color="black",
        )

for node, data in tree.items():
    xpos, ypos = positions[node]
    s, k, r = data["state"]

    ax.text(
        xpos,
        ypos,
        f"{s}, {k}, {r}",
        ha="center",
        va="center",
        fontsize=8,
        color="black",
        bbox=dict(
            boxstyle="square,pad=0.3",
            facecolor="white",
            edgecolor="black",
            linewidth=0.9,
        ),
    )

    if data["bound"]:
        ax.text(
            xpos,
            ypos - 0.34,
            "Bound",
            ha="center",
            va="top",
            fontsize=7.5,
            color="black",
        )

ax.set_title("State Space Tree - Sum of Subsets", fontsize=12)
ax.axis("off")
plt.tight_layout()
plt.show()