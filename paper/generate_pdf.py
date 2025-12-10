"""
Convert LaTeX paper to HTML with embedded figures
"""
import re
import os
import base64

def embed_image_as_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        b64_data = base64.b64encode(image_data).decode('utf-8')
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
        return f'data:{mime_type};base64,{b64_data}'
    except:
        return None

def latex_to_html_with_figures(tex_file, output_file):
    """Convert LaTeX to HTML with embedded figures"""
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'\\title\{([^}]+)\}', content, re.DOTALL)
    title = title_match.group(1) if title_match else "Cross-Modal Product Recommendation System"
    title = re.sub(r'\\.*?\{([^}]*)\}', r'\1', title)
    title = title.replace('\\\\', ' ')
    title = title.strip()
    
    # Extract abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    
    # Get all figures from the figures directory
    figures_html = ""
    figures_dir = "figures"
    if os.path.exists(figures_dir):
        figure_files = [
            ("architecture.png", "System Architecture", "Complete cross-modal recommendation system architecture"),
            ("data_pipeline.png", "Data Processing Pipeline", "Offline data processing and indexing workflow"),
            ("query_flow.png", "Query Processing Flow", "Real-time query processing with timing details"),
            ("fusion_strategies.png", "Multi-Modal Fusion Strategies", "Comparison of three fusion methods"),
            ("context_impact.png", "Context-Aware Ranking Impact", "User engagement improvements"),
            ("performance_comparison.png", "Performance Comparison", "Method comparison across metrics"),
            ("fusion_comparison.png", "Fusion Strategy Results", "Performance of different fusion approaches"),
            ("ablation_study.png", "Ablation Study", "Component contribution analysis"),
            ("scalability_analysis.png", "Scalability Analysis", "System performance at different scales"),
            ("query_type_comparison.png", "Query Type Comparison", "Performance across query modalities")
        ]
        
        for idx, (filename, title_text, caption) in enumerate(figure_files):
            filepath = os.path.join(figures_dir, filename)
            if os.path.exists(filepath):
                img_data = embed_image_as_base64(filepath)
                if img_data:
                    figures_html += f"""
    <div class="figure">
        <img src="{img_data}" alt="{title_text}">
        <p class="caption"><strong>Figure {idx + 1}:</strong> {caption}</p>
    </div>
    """
    
    # Create sections
    sections_html = f"""
    <h2>I. Introduction</h2>
    <p>E-commerce platforms face significant challenges in providing intuitive product search and recommendation experiences that bridge the gap between visual and textual modalities. This paper presents a novel cross-modal recommendation system leveraging CLIP (Contrastive Language-Image Pre-training) for unified multi-modal product search.</p>
    
    <p>Our system enables users to search using natural language queries, images, or both simultaneously through intelligent fusion mechanisms. We introduce context-aware ranking incorporating visual sentiment analysis, occasion-mood matching, and temporal awareness to enhance recommendation relevance.</p>
    
    <h3>Key Contributions:</h3>
    <ul>
        <li>A comprehensive cross-modal product recommendation architecture integrating CLIP embeddings with FAISS-based efficient similarity search</li>
        <li>Multiple fusion strategies for combining image and text modalities with empirical evaluation</li>
        <li>Novel context-aware ranking incorporating visual sentiment analysis and occasion-mood matching</li>
        <li>Advanced reranking mechanisms using cross-attention and category-based boosting</li>
        <li>Production-ready RESTful API system with real-time inference capabilities</li>
    </ul>
    
    <h2>II. System Architecture</h2>
    <p>Our system comprises five main components: Multi-Modal Encoder (CLIP ViT-B/32), Embedding Storage, FAISS Index, Query Processor, and Context-Aware Ranker.</p>
    
    {figures_html[:figures_html.find('Figure 2') if 'Figure 2' in figures_html else len(figures_html)]}
    
    <h2>III. Methodology</h2>
    
    <h3>A. Multi-Modal Fusion</h3>
    <p>We implement three fusion strategies:</p>
    <div class="equation">e<sub>weighted</sub> = α · e<sub>img</sub> + (1-α) · e<sub>text</sub></div>
    <div class="equation">e<sub>concat</sub> = [e<sub>img</sub> ⊕ e<sub>text</sub>] · W<sub>proj</sub></div>
    <div class="equation">e<sub>element</sub> = e<sub>img</sub> ⊙ e<sub>text</sub></div>
    
    <h3>B. Context-Aware Ranking</h3>
    <p>Final ranking score combines multiple factors:</p>
    <div class="equation">s<sub>final</sub> = s<sub>similarity</sub> + λ₁·s<sub>sentiment</sub> + λ₂·s<sub>context</sub> + λ₃·s<sub>diversity</sub></div>
    
    <h2>IV. Experimental Results</h2>
    
    <h3>A. Main Results</h3>
    <table>
        <tr>
            <th>Method</th>
            <th>P@10</th>
            <th>R@50</th>
            <th>MAP</th>
            <th>NDCG</th>
        </tr>
        <tr>
            <td>TF-IDF+ResNet</td>
            <td>64.3%</td>
            <td>52.1%</td>
            <td>58.7%</td>
            <td>71.2%</td>
        </tr>
        <tr>
            <td>BERT+ViT</td>
            <td>73.4%</td>
            <td>62.8%</td>
            <td>69.1%</td>
            <td>78.9%</td>
        </tr>
        <tr>
            <td>VSE++</td>
            <td>78.2%</td>
            <td>70.1%</td>
            <td>74.3%</td>
            <td>82.1%</td>
        </tr>
        <tr>
            <td>CLIP (base)</td>
            <td>85.6%</td>
            <td>78.4%</td>
            <td>81.2%</td>
            <td>87.9%</td>
        </tr>
        <tr class="highlight">
            <td><strong>Ours (Full)</strong></td>
            <td><strong>92.3%</strong></td>
            <td><strong>84.7%</strong></td>
            <td><strong>89.1%</strong></td>
            <td><strong>92.4%</strong></td>
        </tr>
    </table>
    
    <h3>B. Performance Visualizations</h3>
    {figures_html}
    
    <h2>V. Conclusion</h2>
    <p>This paper presented a comprehensive cross-modal product recommendation system leveraging CLIP-based embeddings with novel context-aware ranking mechanisms. Our system achieves 92.3% P@10 on text queries, 88.7% on image queries, and 94.1% on hybrid queries, demonstrating superior performance across all modalities.</p>
    
    <p>The combination of efficient similarity search (127ms average latency) and high precision makes it suitable for production deployment in large-scale e-commerce environments.</p>
    """
    
    # Create HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            background: white;
            color: #000;
            font-size: 11pt;
        }}
        h1 {{
            text-align: center;
            font-size: 18pt;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        h2 {{
            font-size: 14pt;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: bold;
        }}
        h3 {{
            font-size: 12pt;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: bold;
            font-style: italic;
        }}
        .abstract {{
            background: #f5f5f5;
            padding: 20px;
            margin: 30px 0;
            border: 1px solid #ccc;
            text-align: justify;
        }}
        .abstract strong {{
            display: block;
            margin-bottom: 10px;
            font-size: 12pt;
        }}
        .keywords {{
            margin: 20px 0;
            font-style: italic;
        }}
        .equation {{
            background: #fafafa;
            padding: 15px;
            margin: 20px auto;
            text-align: center;
            font-family: 'Cambria Math', 'Times New Roman', serif;
            border: 1px solid #ddd;
            max-width: 80%;
        }}
        p {{
            text-align: justify;
            margin: 12px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background: #e0e0e0;
            font-weight: bold;
        }}
        tr.highlight {{
            background: #fffacd;
            font-weight: bold;
        }}
        .figure {{
            margin: 30px 0;
            page-break-inside: avoid;
            text-align: center;
        }}
        .figure img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ccc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .caption {{
            margin-top: 10px;
            font-size: 10pt;
            text-align: center;
            font-style: italic;
        }}
        .note {{
            background: #fff9e6;
            padding: 20px;
            margin: 30px 0;
            border-left: 4px solid #ff9800;
            page-break-inside: avoid;
        }}
        .note strong {{
            display: block;
            margin-bottom: 10px;
        }}
        kbd {{
            background: #f0f0f0;
            border: 1px solid #ccc;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
                max-width: 100%;
            }}
            .note {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <p style="text-align: center; margin-bottom: 30px;">
        <em>[Your Name], [Your Institution]</em><br>
        <em>[Your Email]</em>
    </p>
    
    <div class="abstract">
        <strong>Abstract</strong>
        {abstract}
    </div>
    
    <div class="keywords">
        <strong>Keywords:</strong> Cross-modal retrieval, CLIP, product recommendation, visual sentiment analysis, context-aware ranking, FAISS, deep learning, e-commerce
    </div>
    
    <div class="note">
        <strong>📄 How to Save as PDF:</strong>
        <ol>
            <li>Press <kbd>Ctrl+P</kbd> (Print)</li>
            <li>Select "Microsoft Print to PDF" or "Save as PDF"</li>
            <li>Adjust settings: Margins = Default, Scale = 100%</li>
            <li>Click "Save" and choose your location</li>
        </ol>
        <strong>💡 For IEEE-formatted PDF:</strong> Upload <code>paper_upload.zip</code> to 
        <a href="https://www.overleaf.com" target="_blank">Overleaf.com</a> for professional formatting with proper equations and IEEE style.
    </div>
    
    {sections_html}
    
    <hr style="margin-top: 50px;">
    <p style="text-align: center; color: #666; font-size: 9pt;">
        <em>Generated from LaTeX source with embedded figures. For publication-quality PDF, use Overleaf.</em>
    </p>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ HTML with figures generated: {output_file}")
    print(f"\nFigures embedded: {len([f for f in os.listdir('figures') if f.endswith('.png')])}")
    print(f"\nTo save as PDF:")
    print(f"1. The file should open in your browser")
    print(f"2. Press Ctrl+P")
    print(f"3. Select 'Save as PDF'")
    print(f"4. Click 'Save'")

if __name__ == "__main__":
    latex_file = "main.tex"
    html_file = "paper_with_figures.html"
    
    if os.path.exists(latex_file):
        print("Converting LaTeX to HTML with embedded figures...")
        latex_to_html_with_figures(latex_file, html_file)
        
        # Open in browser
        import webbrowser
        abs_path = os.path.abspath(html_file)
        print(f"\nOpening in browser: {abs_path}")
        webbrowser.open(f'file://{abs_path}')
    else:
        print(f"Error: {latex_file} not found!")
