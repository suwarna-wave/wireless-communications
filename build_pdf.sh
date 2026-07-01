#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Generating cluster and proof figures..."
.venv/bin/python hexagonal_cluster.py -i 1 -j 1 --no-show --output cluster_1_1.png
.venv/bin/python hexagonal_cluster.py -i 2 -j 1 --no-show --output cluster_2_1.png
.venv/bin/python hexagonal_cluster.py -i 3 -j 2 --no-show --output cluster_3_2.png
.venv/bin/python hexagonal_proof.py -i 2 -j 1 --no-show --diagram proof_2_1.png

echo "Compiling LaTeX document..."
lualatex -interaction=nonstopmode assignment.tex
lualatex -interaction=nonstopmode assignment.tex

echo "Done: assignment.pdf"
