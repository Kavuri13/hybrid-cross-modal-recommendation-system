@echo off
REM Compile IEEE Paper - Windows Batch Script
REM Requires MiKTeX or TeX Live installed

echo ========================================
echo Compiling IEEE Paper
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] First LaTeX pass...
pdflatex -interaction=nonstopmode main.tex
if %ERRORLEVEL% NEQ 0 (
    echo Error: First LaTeX pass failed!
    pause
    exit /b 1
)

echo.
echo [2/5] Running BibTeX...
bibtex main
if %ERRORLEVEL% NEQ 0 (
    echo Warning: BibTeX encountered issues
)

echo.
echo [3/5] Second LaTeX pass...
pdflatex -interaction=nonstopmode main.tex

echo.
echo [4/5] Third LaTeX pass...
pdflatex -interaction=nonstopmode main.tex

echo.
echo [5/5] Cleaning auxiliary files...
del main.aux main.bbl main.blg main.log main.out main.synctex.gz 2>nul

echo.
echo ========================================
echo Compilation Complete!
echo ========================================
echo Output file: main.pdf
echo.

if exist main.pdf (
    echo Opening PDF...
    start main.pdf
) else (
    echo Error: PDF not generated!
    pause
    exit /b 1
)

pause
