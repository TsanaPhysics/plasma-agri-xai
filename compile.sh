#!/bin/bash
set -e

echo "========================================================"
echo "Compiling RBRU Academic Textbook: Plasma Physics"
echo "========================================================"

# Pass 1: Initial compilation
/Library/TeX/texbin/xelatex -interaction=nonstopmode main.tex

# Pass 2: Generate index
if [ -f main.idx ]; then
    makeindex main.idx
fi

# Pass 3: Resolve cross-references, TOC, and index
/Library/TeX/texbin/xelatex -interaction=nonstopmode main.tex

echo "========================================================"
echo "Build Successful: main.pdf is ready!"
echo "========================================================"
