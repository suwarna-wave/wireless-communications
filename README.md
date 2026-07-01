# Wireless Communications Assignment

Python and LaTeX source for the hexagonal cellular cluster allocation assignment.

## Requirements

- Python 3.12 or compatible
- `lualatex`
- Python packages from `requirements.txt`

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Build

```bash
./build_pdf.sh
```

The build script regenerates the cluster/proof figures and compiles `assignment.tex`
into `assignment.pdf`.

## Useful Commands

Generate one cluster figure:

```bash
.venv/bin/python hexagonal_cluster.py -i 2 -j 1 --no-show --output cluster_2_1.png
```

Generate a proof diagram:

```bash
.venv/bin/python hexagonal_proof.py -i 2 -j 1 --no-show --diagram proof_2_1.png
```
