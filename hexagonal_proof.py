"""
Proof: For hexagonal cellular geometry, D = R√(3N), where N = i² + ij + j².

This follows the assignment derivation using the law of cosines on the
(i, j) reuse vector with adjacent cell spacing 2Rp and Rp = (√3/2)R.
"""

from __future__ import annotations

import argparse
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import RegularPolygon


def cluster_size(i: int, j: int) -> int:
    return i * i + i * j + j * j


def adjacent_center_distance(radius: float) -> float:
    """Center-to-center distance between two adjacent hexagonal cells."""
    rp = (math.sqrt(3) / 2) * radius
    return 2 * rp


def axial_to_cartesian(q: int, r: int, radius: float) -> tuple[float, float]:
    """Convert axial hex coordinates to Cartesian (pointy-top layout)."""
    x = 1.5 * radius * q
    y = math.sqrt(3) * radius * (r + q / 2)
    return x, y


def reuse_distance_formula(radius: float, n: int) -> float:
    return radius * math.sqrt(3 * n)


def reuse_ratio(n: int) -> float:
    return math.sqrt(3 * n)


def print_proof(i: int, j: int, radius: float = 1.0) -> None:
    """Print the full step-by-step proof from the assignment."""
    n = cluster_size(i, j)
    rp = (math.sqrt(3) / 2) * radius
    two_rp = 2 * rp
    cos_120 = math.cos(math.radians(120))
    d_squared = (i * two_rp) ** 2 + (j * two_rp) ** 2 - 2 * (i * two_rp) * (j * two_rp) * cos_120
    d_from_steps = math.sqrt(d_squared)
    d_from_formula = reuse_distance_formula(radius, n)
    q_ratio = reuse_ratio(n)

    bar = "=" * 72

    print(bar)
    print("PROOF: Co-channel reuse distance in hexagonal geometry")
    print(bar)
    print()
    print("To prove:")
    print("    D = R√(3N)     and     Q = D/R = √(3N)")
    print("where")
    print("    R = radius of a regular hexagonal cell")
    print("    N = i² + ij + j²   (cluster size)")
    print("    i, j = non-negative integers along two 120° reuse directions")
    print("    D = distance between centers of two co-channel cells")
    print()
    print("-" * 72)
    print("STEP 1 — Geometry of the reuse vector")
    print("-" * 72)
    print()
    print("Refer to the diagram: move i hex steps from A to B, then j steps")
    print("from B to C along a direction 120° to AB. The co-channel distance is AC = D.")
    print()
    print("Let Rp = center-to-center distance of adjacent hexagonal cells / 2")
    print("     (half the spacing between neighboring cell centers).")
    print()
    print("Each step spans 2Rp, so:")
    print(f"    AB = i · 2Rp = {i} × {two_rp:.4f} = {i * two_rp:.4f}")
    print(f"    BC = j · 2Rp = {j} × {two_rp:.4f} = {j * two_rp:.4f}")
    print(f"    ∠ABC = 120°     (cos 120° = {cos_120:.1f})")
    print()
    print("-" * 72)
    print("STEP 2 — Law of cosines")
    print("-" * 72)
    print()
    print("Applying the law of cosines in triangle ABC (interior angle at B = 120°):")
    print()
    print("    D² = (i·2Rp)² + (j·2Rp)² − 2(i·2Rp)(j·2Rp) cos(120°)")
    print()
    print(f"Substituting cos(120°) = {cos_120:.1f}:")
    print()
    print("    D² = 4Rp²i² + 4Rp²j² − 2·4Rp²ij·(−½)")
    print("    D² = 4Rp² (i² + ij + j²)")
    print()
    print(f"Numerical check with i={i}, j={j}, R={radius}:")
    print(f"    D² = {d_squared:.6f}  →  D = {d_from_steps:.6f}")
    print()
    print("-" * 72)
    print("STEP 3 — Relating Rp to cell radius R")
    print("-" * 72)
    print()
    print("For a regular hexagon of radius R (center to vertex):")
    print()
    print("    Rp = (√3 / 2) · R")
    print()
    print(f"With R = {radius}:")
    print(f"    Rp = {rp:.6f}")
    print(f"    2Rp = √3 · R = {two_rp:.6f}")
    print()
    print("Substituting Rp into D²:")
    print()
    print("    D² = 4 · (3R²/4) · (i² + ij + j²)")
    print("    D² = 3R² · (i² + ij + j²)")
    print()
    print("-" * 72)
    print("STEP 4 — Cluster size N")
    print("-" * 72)
    print()
    print("By definition of cluster size in hexagonal reuse:")
    print()
    print(f"    N = i² + ij + j² = {i}² + {i}×{j} + {j}² = {n}")
    print()
    print("Therefore:")
    print()
    print("    D² = 3R²N")
    print("    D  = R√(3N)")
    print()
    print("Co-channel reuse ratio:")
    print()
    print("    Q = D/R = √(3N)")
    print()
    print("-" * 72)
    print("STEP 5 — Numerical verification")
    print("-" * 72)
    print()
    print(f"Given: i = {i}, j = {j}, R = {radius}")
    print(f"    N = {n}")
    print(f"    D (from law of cosines)  = {d_from_steps:.6f}")
    print(f"    D (from formula R√(3N))  = {d_from_formula:.6f}")
    print(f"    Q = D/R                  = {q_ratio:.6f}")
    print(f"    √(3N)                    = {q_ratio:.6f}")
    print()

    if math.isclose(d_from_steps, d_from_formula, rel_tol=1e-9):
        print("✓ Both methods agree — proof verified numerically.")
    else:
        print("✗ Numerical mismatch — check parameters.")

    print()
    print("∴  D = R√(3N)  proved.")
    print(bar)


def draw_hex_at(ax, q: int, r: int, radius: float, **kwargs) -> tuple[float, float]:
    x, y = axial_to_cartesian(q, r, radius)
    defaults = dict(
        numVertices=6,
        radius=radius,
        orientation=np.radians(30),
        edgecolor="black",
        linewidth=1.2,
        facecolor="#e8f4fc",
        alpha=0.9,
    )
    defaults.update(kwargs)
    ax.add_patch(RegularPolygon((x, y), **defaults))
    return x, y


def plot_proof_diagram(
    i: int,
    j: int,
    radius: float = 1.0,
    output_path: str | None = None,
    show: bool = True,
) -> None:
    """Draw the A–B–C reuse-vector diagram from the assignment."""
    n = cluster_size(i, j)
    d_formula = reuse_distance_formula(radius, n)

    ax_x, ax_y = axial_to_cartesian(0, 0, radius)
    bx, by = axial_to_cartesian(i, 0, radius)
    cx, cy = axial_to_cartesian(i, j, radius)

    # Draw hex cells along the path A → B → C and at endpoints.
    cells = {(0, 0), (i, 0), (i, j)}
    for step in range(1, i):
        cells.add((step, 0))
    for step in range(1, j):
        cells.add((i, step))

    fig, ax = plt.subplots(figsize=(10, 8))

    for q, r in cells:
        draw_hex_at(ax, q, r, radius)

    # Highlight centers A, B, C.
    for label, (x, y) in zip("ABC", [(ax_x, ax_y), (bx, by), (cx, cy)]):
        ax.plot(x, y, "ko", markersize=7)
        ax.text(x, y - 0.35 * radius, label, ha="center", va="top", fontsize=14, fontweight="bold")

    # Vectors i and j along AB and BC.
    ax.annotate(
        "",
        xy=(bx, by),
        xytext=(ax_x, ax_y),
        arrowprops=dict(arrowstyle="->", color="#1a5276", lw=2.5),
    )
    ax.text((ax_x + bx) / 2, (ax_y + by) / 2 + 0.25 * radius, f"i = {i}", ha="center", fontsize=12, color="#1a5276")

    ax.annotate(
        "",
        xy=(cx, cy),
        xytext=(bx, by),
        arrowprops=dict(arrowstyle="->", color="#922b21", lw=2.5),
    )
    ax.text((bx + cx) / 2 + 0.2 * radius, (by + cy) / 2, f"j = {j}", ha="center", fontsize=12, color="#922b21")

    # Co-channel distance D (dashed).
    ax.plot([ax_x, cx], [ax_y, cy], "k--", lw=2)
    ax.text((ax_x + cx) / 2 - 0.3 * radius, (ax_y + cy) / 2, f"D = {d_formula:.3f}", ha="center", fontsize=12)

    # 120° angle arc at B.
    v1 = np.array([ax_x - bx, ax_y - by])
    v2 = np.array([cx - bx, cy - by])
    angle1 = math.degrees(math.atan2(v1[1], v1[0]))
    angle2 = math.degrees(math.atan2(v2[1], v2[0]))
    arc = plt.matplotlib.patches.Arc(
        (bx, by),
        width=1.2 * radius,
        height=1.2 * radius,
        angle=0,
        theta1=min(angle1, angle2),
        theta2=max(angle1, angle2),
        color="green",
        lw=1.5,
    )
    ax.add_patch(arc)
    ax.text(bx + 0.55 * radius, by + 0.15 * radius, "120°", fontsize=11, color="green")

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.set_title(
        f"Hexagonal Reuse Geometry — N = {i}² + {i}×{j} + {j}² = {n},  "
        f"D = R√(3N) = {radius}×√(3×{n}) = {d_formula:.3f}",
        fontsize=12,
    )
    plt.axis("off")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Saved proof diagram to: {output_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prove and verify D = R√(3N) for hexagonal cellular geometry."
    )
    parser.add_argument("-i", "--i-param", type=int, dest="i", default=2, help="Reuse parameter i")
    parser.add_argument("-j", "--j-param", type=int, dest="j", default=1, help="Reuse parameter j")
    parser.add_argument("--radius", type=float, default=1.0, help="Cell radius R")
    parser.add_argument(
        "--diagram",
        type=str,
        default=None,
        help="Save the A-B-C geometry diagram to this path",
    )
    parser.add_argument("--no-show", action="store_true", help="Do not open plot window")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.i == 0 and args.j == 0:
        print("Error: i and j cannot both be zero.")
        return 1

    print_proof(args.i, args.j, args.radius)
    plot_proof_diagram(
        args.i,
        args.j,
        args.radius,
        output_path=args.diagram,
        show=not args.no_show,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
