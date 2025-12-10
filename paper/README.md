# IEEE Journal Paper - Cross-Modal Recommendation System

This directory contains the IEEE journal paper manuscript for the Cross-Modal Product Recommendation System.

## 📄 Files

- **main.tex** - Main LaTeX document following IEEE conference template format
- **references.bib** - BibTeX bibliography with all cited references
- **figures/** - Directory for paper figures and diagrams

## 🔧 Prerequisites

To compile the paper, you need:

1. **LaTeX Distribution**:
   - Windows: [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
   - macOS: [MacTeX](https://www.tug.org/mactex/)
   - Linux: `sudo apt-get install texlive-full`

2. **Required LaTeX Packages**:
   - IEEEtran
   - cite
   - amsmath, amssymb, amsfonts
   - algorithmic
   - graphicx
   - textcomp
   - xcolor
   - hyperref
   - booktabs
   - multirow
   - array

Most distributions include these by default, but they may auto-install on first compilation.

## 📊 Preparing Figures

Before compiling, create the `figures/` directory and add the following images:

1. **architecture.png** - System architecture diagram showing:
   - Multi-modal encoder (CLIP)
   - Embedding storage
   - FAISS index
   - Query processor
   - Context-aware ranker

2. **context_impact.png** - Bar chart showing:
   - Click-through rate with/without context-aware ranking
   - Conversion rate comparison
   - User satisfaction scores

You can create these figures using:
- **Draw.io / Diagrams.net** - For architecture diagrams
- **Python (matplotlib/seaborn)** - For result visualizations
- **PowerPoint/Keynote** - For conceptual diagrams
- **TikZ** - For LaTeX-native diagrams

### Example Python Script for Results Figure

```python
import matplotlib.pyplot as plt
import numpy as np

# Context impact data
categories = ['Click-Through\nRate', 'Conversion\nRate', 'User\nSatisfaction']
without_context = [0.62, 0.34, 0.71]
with_context = [0.83, 0.48, 0.92]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, without_context, width, label='Without Context-Aware', color='#3498db')
bars2 = ax.bar(x + width/2, with_context, width, label='With Context-Aware', color='#e74c3c')

ax.set_ylabel('Score', fontsize=12)
ax.set_title('Impact of Context-Aware Ranking on User Engagement', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('figures/context_impact.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 🔨 Compilation Instructions

### Method 1: Using pdflatex (Recommended)

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The multiple runs are necessary to resolve references and citations.

### Method 2: Using latexmk (Automated)

```bash
cd paper
latexmk -pdf main.tex
```

This automatically handles all compilation passes.

### Method 3: Using Overleaf

1. Create a new project on [Overleaf](https://www.overleaf.com/)
2. Upload `main.tex` and `references.bib`
3. Create a `figures/` folder and upload images
4. The document will compile automatically

## 📋 Customization Checklist

Before submission, update the following sections:

- [ ] **Author Information** (Lines 23-28 in main.tex)
  - Your name(s)
  - Department/affiliation
  - Institution name
  - City, country
  - Email address(es)

- [ ] **Acknowledgments** (Line 683)
  - Add funding sources
  - Thank advisors/collaborators
  - Acknowledge resources used

- [ ] **Abstract** (Lines 32-35)
  - Review and refine based on actual results
  - Update performance numbers if needed

- [ ] **Experimental Results** (Section IV)
  - Replace placeholder numbers with actual evaluation results
  - Add your dataset statistics
  - Update query latency measurements

- [ ] **Figures**
  - Create and add architecture.png
  - Generate context_impact.png from your data
  - Consider adding more figures (confusion matrix, latency graphs, etc.)

## 📐 IEEE Submission Guidelines

### For IEEE Transactions/Journals:

1. **Length**: Typically 10-15 pages for full papers
2. **Format**: Two-column IEEE format (already configured)
3. **Figures**: 
   - Minimum 300 DPI for raster images
   - Vector formats (PDF, EPS) preferred
   - Clear, readable text even when scaled
4. **References**: IEEE style (already configured in IEEEtran.bst)
5. **Copyright**: Prepare IEEE copyright form after acceptance

### For IEEE Conferences:

If targeting a conference instead of a journal:
- Change document class: `\documentclass[conference]{IEEEtran}` (already set)
- Typical length: 6-8 pages
- Add conference name and dates in title/footnote

## 🎯 Suggested Target Journals

Based on your topic, consider these IEEE journals:

1. **IEEE Transactions on Multimedia** (Impact Factor: 8.4)
   - Focus: Multimedia systems, cross-modal learning
   - Scope: Perfect fit for your work

2. **IEEE Transactions on Neural Networks and Learning Systems** (IF: 14.3)
   - Focus: Deep learning, neural architectures
   - Scope: CLIP-based learning, context-aware AI

3. **IEEE Transactions on Knowledge and Data Engineering** (IF: 8.9)
   - Focus: Data mining, recommendation systems
   - Scope: E-commerce applications, retrieval systems

4. **IEEE Access** (IF: 3.9)
   - Focus: Open access, broad CS topics
   - Scope: Practical systems, applications
   - Advantage: Faster review, lower cost

5. **IEEE Internet of Things Journal** (IF: 10.6)
   - If emphasizing mobile/edge deployment
   - Smart retail applications

## 📝 Additional Tips

1. **Proofread Carefully**: Use Grammarly or similar tools
2. **Check Math**: Verify all equations render correctly
3. **Validate References**: Ensure all citations have complete information
4. **Consistent Terminology**: Use same terms throughout (e.g., "cross-modal" vs "multimodal")
5. **Figure Captions**: Make them self-explanatory
6. **Revision Tracking**: Use Git to track changes during revision

## 🔍 Common Compilation Issues

**Issue**: Missing .sty files
**Solution**: Install missing packages via MiKTeX Package Manager or `tlmgr install <package>`

**Issue**: Figures not found
**Solution**: Ensure figures/ directory exists and paths are correct

**Issue**: Bibliography not showing
**Solution**: Run bibtex step, then pdflatex twice more

**Issue**: Overfull/underfull hbox warnings
**Solution**: Adjust text or add `\sloppy` command (use sparingly)

## 📧 Contact

For questions about the paper content or compilation, contact:
[Your Email]

## 📄 License

This research paper and LaTeX source are part of the Cross-Modal Recommendation System project.

---

**Last Updated**: December 2025
