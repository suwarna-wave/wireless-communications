
import argparse
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon


def hex_to_axial(col: int, row: int) -> tuple[int, int]:
    """Convert odd-q vertical offset coordinates to axial (q, r)."""
    q = col
    r = row - (col - (col & 1)) // 2
    return q, r


def get_cluster_id(q: int, r: int, i: int, j: int, n: int) -> int:
    """Assign a cluster index in [0, N-1] using the (i, j) reuse vector."""
    c = (q * (i + j) - r * j) % n
    d = (-q * j + r * i) % n
    return (c + d) % n


def cluster_size(i: int, j: int) -> int:
    return i * i + i * j + j * j


def reuse_distance(radius: float, n: int) -> float:
    """Co-channel reuse distance: D = R√(3N)."""
    return radius * np.sqrt(3 * n)


def build_hex_grid(
    i: int,
    j: int,
    rows: int = 12,
    cols: int = 12,
    radius: float = 1.0,
):
    """Return hex centers and cluster IDs for each cell in the grid."""
    n = cluster_size(i, j)
    cells = []

    for col in range(cols):
        for row in range(rows):
            x = col * 1.5 * radius
            y = np.sqrt(3) * radius * (row + 0.5 * (col % 2))
            q, r = hex_to_axial(col, row)
            cluster = get_cluster_id(q, r, i, j, n)
            cells.append(
                {
                    "col": col,
                    "row": row,
                    "x": x,
                    "y": y,
                    "q": q,
                    "r": r,
                    "cluster": cluster,
                }
            )

    return cells, n


def plot_hexagonal_layout(
    i: int,
    j: int,
    rows: int = 12,
    cols: int = 12,
    radius: float = 1.0,
    output_path: str | None = None,
    show: bool = True,
) -> None:
    n = cluster_size(i, j)
    d = reuse_distance(radius, n)
    q_ratio = d / radius

    print(f"Cluster parameters: i = {i}, j = {j}")
    print(f"Cluster size (N)     = i² + ij + j² = {i}² + {i}×{j} + {j}² = {n}")
    print(f"Cell radius (R)      = {radius}")
    print(f"Reuse distance (D)   = R√(3N) = {d:.4f}")
    print(f"Reuse ratio (Q=D/R)  = √(3N) = {q_ratio:.4f}")

    cells, _ = build_hex_grid(i, j, rows, cols, radius)

    # Distinct color per cluster (1-based labels in the plot).
    cmap = plt.colormaps["tab20"].resampled(max(n, 1))

    fig, ax = plt.subplots(figsize=(12, 11))

    for cell in cells:
        cluster = cell["cluster"]
        color = cmap(cluster % cmap.N)

        hexagon = RegularPolygon(
            (cell["x"], cell["y"]),
            numVertices=6,
            radius=radius,
            orientation=np.radians(30),
            edgecolor="black",
            linewidth=1.0,
            facecolor=color,
            alpha=0.85,
        )
        ax.add_patch(hexagon)
        ax.text(
            cell["x"],
            cell["y"],
            str(cluster + 1),
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="black",
        )

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.set_title(
        f"Hexagonal Cellular Layout — N = i² + ij + j² = "
        f"{i}² + {i}×{j} + {j}² = {n}\n"
        f"D = R√(3N) = {radius}×√(3×{n}) = {d:.3f}",
        fontsize=13,
    )
    plt.axis("off")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved plot to: {output_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hexagonal workspace with cluster allocation (N = i² + ij + j²)."
    )
    parser.add_argument("-i", "--i-param", type=int, dest="i", help="Reuse parameter i")
    parser.add_argument("-j", "--j-param", type=int, dest="j", help="Reuse parameter j")
    parser.add_argument("--rows", type=int, default=12, help="Number of hex rows")
    parser.add_argument("--cols", type=int, default=12, help="Number of hex columns")
    parser.add_argument("--radius", type=float, default=1.0, help="Hexagon radius R")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save figure to this path instead of only displaying",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open an interactive plot window",
    )
    parser.add_argument(
        "--proof",
        action="store_true",
        help="Also print the D = R√(3N) proof and draw the geometry diagram",
    )
    parser.add_argument(
        "--proof-output",
        type=str,
        default=None,
        help="Save proof diagram to this path (used with --proof)",
    )
    return parser.parse_args(argv)


def prompt_positive_int(name: str) -> int:
    while True:
        raw = input(f"Enter {name}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"  Please enter a valid integer for {name}.")
            continue
        if value < 0:
            print(f"  {name} must be non-negative.")
            continue
        return value


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.i is not None and args.j is not None:
        i, j = args.i, args.j
    elif args.i is None and args.j is None:
        i = prompt_positive_int("i")
        j = prompt_positive_int("j")
    else:
        print("Error: provide both -i and -j, or neither for interactive input.")
        return 1

    if i == 0 and j == 0:
        print("Error: i and j cannot both be zero (N would be 0).")
        return 1

    gcd_ij = math.gcd(i, j)
    if gcd_ij > 1:
        print(
            f"Note: gcd(i, j) = {gcd_ij}. For a full N-cell reuse pattern, "
            "i and j are usually coprime (e.g. i=2, j=1)."
        )

    if args.proof:
        from hexagonal_proof import plot_proof_diagram, print_proof

        print()
        print_proof(i, j, args.radius)
        plot_proof_diagram(
            i,
            j,
            args.radius,
            output_path=args.proof_output,
            show=not args.no_show,
        )

    plot_hexagonal_layout(
        i=i,
        j=j,
        rows=args.rows,
        cols=args.cols,
        radius=args.radius,
        output_path=args.output,
        show=not args.no_show,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
