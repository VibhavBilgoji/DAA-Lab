import heapq
from collections import Counter
import matplotlib.pyplot as plt

TEXT = ("a spanning tree of a connected undirected graph is a subgraph that is a tree containing all vertices.").replace(".", "")

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
        self.code = ""
        self.x = 0.0
        self.y = 0.0

    @property
    def is_leaf(self):
        return self.char is not None


def build_huffman_tree(text, verbose=True):
    freq = Counter(text)
    heap, counter = [], 0
    # Counter keeps first-occurrence order and sorted() is stable, so ties
    # on frequency are broken by first appearance in the text.
    for ch, f in sorted(freq.items(), key=lambda kv: kv[1]):
        heapq.heappush(heap, (f, 0, counter, Node(f, char=ch)))
        counter += 1

    step = 0
    while len(heap) > 1:
        f1, _, _, t1 = heapq.heappop(heap)
        f2, _, _, t2 = heapq.heappop(heap)
        parent = Node(f1 + f2, left=t1, right=t2)
        heapq.heappush(heap, (f1 + f2, 1, counter, parent))
        counter += 1
        step += 1
        if verbose:
            print(f"Pass {step:2d}: {label(t1):>4}({f1:>2}) + {label(t2):>4}({f2:>2})"
                  f" -> new tree ({f1 + f2})")
    return heap[0][3], freq


def label(node):
    if node.is_leaf:
        return "SP" if node.char == " " else node.char
    return "T"


def assign_codes(node, code=""):
    node.code = code
    if node.is_leaf:
        return
    assign_codes(node.left, code + "0")
    assign_codes(node.right, code + "1")


def collect_leaves(node, out):
    if node.is_leaf:
        out.append(node)
    else:
        collect_leaves(node.left, out)
        collect_leaves(node.right, out)
    return out


def print_code_table(root, freq):
    leaves = collect_leaves(root, [])
    leaves.sort(key=lambda n: (-n.freq, len(n.code), n.code))
    print("\n" + "=" * 52)
    print(f"{'Char':<8}{'Freq':>6}{'Huffman code':>16}{'Len':>6}{'Freq*Len':>10}")
    print("-" * 52)
    total_bits = 0
    for n in leaves:
        name = "SPACE" if n.char == " " else n.char
        bits = n.freq * len(n.code)
        total_bits += bits
        print(f"{name:<8}{n.freq:>6}{n.code:>16}{len(n.code):>6}{bits:>10}")
    print("-" * 52)
    n_chars = sum(freq.values())
    print(f"{'Total':<8}{n_chars:>6}{'':>16}{'':>6}{total_bits:>10}")
    print("=" * 52)
    print(f"Distinct characters (d)  : {len(freq)}")
    print(f"Fixed 8-bit ASCII        : {8 * n_chars} bits")
    print(f"Huffman encoded          : {total_bits} bits")
    print(f"Average code length      : {total_bits / n_chars:.2f} bits/char")
    print(f"Space saved vs ASCII     : {100 * (1 - total_bits / (8 * n_chars)):.1f}%")


def layout(node, depth, counter):
    node.y = -depth
    if node.is_leaf:
        node.x = counter[0]
        counter[0] += 1
        return
    layout(node.left, depth + 1, counter)
    layout(node.right, depth + 1, counter)
    node.x = (node.left.x + node.right.x) / 2


def draw_edges(ax, node):
    if node.is_leaf:
        return
    for child, bit in ((node.left, "0"), (node.right, "1")):
        ax.plot([node.x, child.x], [node.y, child.y], color="black", lw=1, zorder=1)
        mx = node.x + (child.x - node.x) * 0.45
        my = node.y + (child.y - node.y) * 0.45
        off = -0.28 if bit == "0" else 0.28
        ax.text(mx + off, my, bit, ha="center", va="center", fontsize=9,
                color="crimson", zorder=4)
        draw_edges(ax, child)


def draw_nodes(ax, node):
    if node.is_leaf:
        ch = "\u2423" if node.char == " " else node.char
        ax.scatter(node.x, node.y, s=420, marker="s", facecolor="white",
                   edgecolor="black", lw=1.2, zorder=2)
        ax.text(node.x, node.y, ch, ha="center", va="center",
                fontsize=11, fontweight="bold", zorder=3)
        ax.text(node.x, node.y - 0.42, str(node.freq), ha="center", va="center",
                fontsize=9, zorder=3)
        return
    ax.scatter(node.x, node.y, s=520, marker="o", facecolor="#eaf1fb",
               edgecolor="black", lw=1.2, zorder=2)
    ax.text(node.x, node.y, str(node.freq), ha="center", va="center",
            fontsize=9, zorder=3)
    draw_nodes(ax, node.left)
    draw_nodes(ax, node.right)


def plot_tree(root, freq, text, filename="huffman_tree.png"):
    layout(root, 0, [0])
    fig = plt.figure(figsize=(17, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 9], hspace=0.05)

    ax_tab = fig.add_subplot(gs[0])
    ax_tab.axis("off")
    items = sorted(freq.items(), key=lambda kv: kv[1])
    chars = ["\u2423" if c == " " else c for c, _ in items]
    freqs = [str(f) for _, f in items]
    table = ax_tab.table(cellText=[chars, freqs],
                         rowLabels=["Character", "Frequency"],
                         loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)
    ax_tab.set_title("(a) Frequency of each character of X", loc="left", fontsize=11)

    ax = fig.add_subplot(gs[1])
    draw_edges(ax, root)
    draw_nodes(ax, root)
    ax.set_title("(b) Huffman tree T for string X  "
                 "(left edge = 0, right edge = 1)", loc="left", fontsize=11)
    ax.set_xlim(-1, len(freq))
    ax.set_ylim(min(n.y for n in collect_leaves(root, [])) - 1, 0.8)
    ax.axis("off")

    fig.suptitle(f'Huffman coding of: "{text}"', fontsize=11, y=0.97)
    plt.show()


if __name__ == "__main__":
    root, freq = build_huffman_tree(TEXT)
    assign_codes(root)
    print_code_table(root, freq)
    plot_tree(root, freq, TEXT)