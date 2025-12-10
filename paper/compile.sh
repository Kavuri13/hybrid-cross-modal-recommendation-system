#!/bin/bash
# Compile IEEE Paper - Unix/Linux/macOS Script
# Requires LaTeX distribution installed

echo "========================================"
echo "Compiling IEEE Paper"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/5] First LaTeX pass..."
pdflatex -interaction=nonstopmode main.tex
if [ $? -ne 0 ]; then
    echo "Error: First LaTeX pass failed!"
    exit 1
fi

echo ""
echo "[2/5] Running BibTeX..."
bibtex main
if [ $? -ne 0 ]; then
    echo "Warning: BibTeX encountered issues"
fi

echo ""
echo "[3/5] Second LaTeX pass..."
pdflatex -interaction=nonstopmode main.tex

echo ""
echo "[4/5] Third LaTeX pass..."
pdflatex -interaction=nonstopmode main.tex

echo ""
echo "[5/5] Cleaning auxiliary files..."
rm -f main.aux main.bbl main.blg main.log main.out main.synctex.gz

echo ""
echo "========================================"
echo "Compilation Complete!"
echo "========================================"
echo "Output file: main.pdf"
echo ""

if [ -f main.pdf ]; then
    # Try to open PDF with system default viewer
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open main.pdf
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open main.pdf 2>/dev/null || echo "Please open main.pdf manually"
    fi
else
    echo "Error: PDF not generated!"
    exit 1
fi
