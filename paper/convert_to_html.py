"""
Convert LaTeX paper to HTML which can be opened in browser and saved as PDF
"""
import re
import os

def latex_to_html(tex_file, output_file):
    """Simple LaTeX to HTML converter for viewing"""
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'\\title\{([^}]+)\}', content, re.DOTALL)
    title = title_match.group(1) if title_match else "Research Paper"
    title = re.sub(r'\\.*?\{([^}]*)\}', r'\1', title)  # Remove LaTeX commands
    title = title.replace('\\\\', ' ')
    
    # Extract abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    
    # Extract main content between begin{document} and end{document}
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
    if doc_match:
        main_content = doc_match.group(1)
    else:
        main_content = content
    
    # Clean up LaTeX commands
    def clean_latex(text):
        # Remove comments
        text = re.sub(r'%.*?\n', '\n', text)
        
        # Sections
        text = re.sub(r'\\section\*?\{([^}]+)\}', r'<h2>\1</h2>', text)
        text = re.sub(r'\\subsection\*?\{([^}]+)\}', r'<h3>\1</h3>', text)
        text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'<h4>\1</h4>', text)
        
        # Text formatting
        text = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', text)
        text = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', text)
        text = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', text)
        
        # Lists
        text = re.sub(r'\\begin\{itemize\}', '<ul>', text)
        text = re.sub(r'\\end\{itemize\}', '</ul>', text)
        text = re.sub(r'\\begin\{enumerate\}', '<ol>', text)
        text = re.sub(r'\\end\{enumerate\}', '</ol>', text)
        text = re.sub(r'\\item\s+', '<li>', text)
        
        # Equations (inline and display)
        text = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'<div class="equation">\1</div>', text, flags=re.DOTALL)
        text = re.sub(r'\$\$(.*?)\$\$', r'<div class="equation">\1</div>', text, flags=re.DOTALL)
        text = re.sub(r'\$([^\$]+)\$', r'<span class="math">\1</span>', text)
        
        # Tables and figures (simplified)
        text = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '[Table]', text, flags=re.DOTALL)
        text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '[Figure]', text, flags=re.DOTALL)
        
        # Remove bibliography for now
        text = re.sub(r'\\bibliographystyle.*?\n', '', text)
        text = re.sub(r'\\bibliography.*?\n', '', text)
        
        # Remove other common LaTeX commands
        text = re.sub(r'\\maketitle', '', text)
        text = re.sub(r'\\IEEEoverridecommandlockouts', '', text)
        text = re.sub(r'\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}', 
                     r'<p><strong>Keywords:</strong> \1</p>', text, flags=re.DOTALL)
        
        # Clean up remaining LaTeX commands (simple ones)
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\\\', '<br>', text)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\n+', '</p><p>', text)
        
        return text
    
    cleaned_content = clean_latex(main_content)
    cleaned_abstract = clean_latex(abstract)
    
    # Create HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Times New Roman', Times, serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            background: white;
            color: #333;
        }}
        h1 {{
            text-align: center;
            font-size: 24px;
            margin-bottom: 30px;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{
            font-size: 18px;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 1px solid #666;
            padding-bottom: 5px;
        }}
        h3 {{
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        h4 {{
            font-size: 14px;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        .abstract {{
            background: #f5f5f5;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #333;
            font-style: italic;
        }}
        .equation {{
            background: #f9f9f9;
            padding: 10px;
            margin: 15px 0;
            text-align: center;
            font-family: 'Courier New', monospace;
            border: 1px solid #ddd;
        }}
        .math {{
            font-family: 'Courier New', monospace;
            font-style: italic;
        }}
        p {{
            text-align: justify;
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 40px;
        }}
        li {{
            margin: 8px 0;
        }}
        strong {{
            font-weight: bold;
        }}
        em {{
            font-style: italic;
        }}
        .note {{
            background: #fff3cd;
            padding: 15px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }}
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <div class="abstract">
        <strong>Abstract:</strong><br>
        {cleaned_abstract}
    </div>
    
    <div class="note">
        <strong>📄 How to Save as PDF:</strong><br>
        1. Press <kbd>Ctrl+P</kbd> (Print)<br>
        2. Select "Microsoft Print to PDF" or "Save as PDF"<br>
        3. Click "Save"<br>
        <br>
        <strong>Note:</strong> For the full LaTeX-formatted version with proper equations and tables, 
        upload <code>paper_upload.zip</code> to <a href="https://www.overleaf.com" target="_blank">Overleaf.com</a>
    </div>
    
    <div class="content">
        <p>{cleaned_content}</p>
    </div>
    
    <hr>
    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 40px;">
        Generated from LaTeX source. For best quality, compile with LaTeX or upload to Overleaf.
    </p>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ HTML generated: {output_file}")
    print(f"\nTo convert to PDF:")
    print(f"1. Open {output_file} in your browser")
    print(f"2. Press Ctrl+P (Print)")
    print(f"3. Select 'Save as PDF'")
    print(f"4. Click 'Save'")

if __name__ == "__main__":
    latex_file = "main.tex"
    html_file = "paper_preview.html"
    
    if os.path.exists(latex_file):
        print("Converting LaTeX to HTML...")
        latex_to_html(latex_file, html_file)
        
        # Try to open in browser
        import webbrowser
        import os
        abs_path = os.path.abspath(html_file)
        print(f"\nOpening in browser: {abs_path}")
        webbrowser.open(f'file://{abs_path}')
    else:
        print(f"Error: {latex_file} not found!")
