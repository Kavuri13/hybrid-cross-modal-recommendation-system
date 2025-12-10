"""
Generate Architecture and Flow Diagrams for IEEE Paper
Creates publication-quality system architecture, data flow, and pipeline diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import matplotlib.lines as mlines
import numpy as np

# Set publication style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 9
plt.rcParams['figure.dpi'] = 300

def create_system_architecture():
    """Create comprehensive system architecture diagram"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(6, 9.5, 'Cross-Modal Recommendation System Architecture', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Color scheme
    input_color = '#3498db'
    encoder_color = '#2ecc71'
    storage_color = '#f39c12'
    search_color = '#9b59b6'
    rank_color = '#e74c3c'
    output_color = '#1abc9c'
    
    # ============ INPUT LAYER ============
    # Text Input
    text_box = FancyBboxPatch((0.5, 7.5), 2, 1, boxstyle="round,pad=0.1",
                              edgecolor=input_color, facecolor=input_color, alpha=0.3, linewidth=2)
    ax.add_patch(text_box)
    ax.text(1.5, 8, 'Text Query', ha='center', va='center', fontweight='bold')
    ax.text(1.5, 7.7, '"red dress for party"', ha='center', va='center', fontsize=7, style='italic')
    
    # Image Input
    img_box = FancyBboxPatch((3, 7.5), 2, 1, boxstyle="round,pad=0.1",
                             edgecolor=input_color, facecolor=input_color, alpha=0.3, linewidth=2)
    ax.add_patch(img_box)
    ax.text(4, 8, 'Image Query', ha='center', va='center', fontweight='bold')
    ax.text(4, 7.7, 'User uploaded', ha='center', va='center', fontsize=7, style='italic')
    
    # Context Input
    ctx_box = FancyBboxPatch((5.5, 7.5), 2.5, 1, boxstyle="round,pad=0.1",
                             edgecolor=input_color, facecolor=input_color, alpha=0.3, linewidth=2)
    ax.add_patch(ctx_box)
    ax.text(6.75, 8.2, 'Context Profile', ha='center', va='center', fontweight='bold', fontsize=8)
    ax.text(6.75, 7.9, 'Occasion: Wedding', ha='center', va='center', fontsize=6)
    ax.text(6.75, 7.6, 'Mood: Elegant', ha='center', va='center', fontsize=6)
    
    # ============ CLIP ENCODER ============
    clip_box = FancyBboxPatch((1, 5.8), 6, 1.2, boxstyle="round,pad=0.15",
                              edgecolor=encoder_color, facecolor=encoder_color, alpha=0.2, linewidth=2)
    ax.add_patch(clip_box)
    ax.text(4, 6.7, 'CLIP Encoder (ViT-B/32)', ha='center', va='center', 
            fontweight='bold', fontsize=11)
    ax.text(4, 6.3, 'Shared Embedding Space: 512-dim', ha='center', va='center', fontsize=7)
    
    # Image Encoder branch
    ax.text(2, 5.95, 'Image Encoder', ha='center', va='center', fontsize=7, fontweight='bold')
    ax.text(2, 5.7, '224×224 → ViT', ha='center', va='center', fontsize=6)
    
    # Text Encoder branch
    ax.text(4, 5.95, 'Text Encoder', ha='center', va='center', fontsize=7, fontweight='bold')
    ax.text(4, 5.7, 'Tokenize → Transformer', ha='center', va='center', fontsize=6)
    
    # ============ FUSION LAYER ============
    fusion_box = FancyBboxPatch((1.5, 4.3), 5, 1, boxstyle="round,pad=0.1",
                                edgecolor='#34495e', facecolor='#34495e', alpha=0.2, linewidth=2)
    ax.add_patch(fusion_box)
    ax.text(4, 5, 'Multi-Modal Fusion', ha='center', va='center', fontweight='bold')
    
    # Fusion strategies
    ax.text(2.2, 4.6, '① Weighted Avg', ha='center', fontsize=6)
    ax.text(4, 4.6, '② Concatenation', ha='center', fontsize=6)
    ax.text(5.8, 4.6, '③ Element-wise', ha='center', fontsize=6)
    
    # ============ PRODUCT DATABASE ============
    db_box = FancyBboxPatch((8.5, 5.5), 3, 2, boxstyle="round,pad=0.15",
                            edgecolor=storage_color, facecolor=storage_color, alpha=0.2, linewidth=2)
    ax.add_patch(db_box)
    ax.text(10, 7.2, 'Product Database', ha='center', va='center', fontweight='bold', fontsize=10)
    ax.text(10, 6.8, '50,000+ Products', ha='center', va='center', fontsize=7)
    ax.text(10, 6.5, '━━━━━━━━━', ha='center', va='center', fontsize=7, color=storage_color)
    ax.text(10, 6.2, 'Pre-computed', ha='center', fontsize=6)
    ax.text(10, 5.95, 'Embeddings', ha='center', fontsize=6)
    
    # ============ FAISS INDEX ============
    faiss_box = FancyBboxPatch((8.5, 3.5), 3, 1.5, boxstyle="round,pad=0.15",
                               edgecolor=search_color, facecolor=search_color, alpha=0.2, linewidth=2)
    ax.add_patch(faiss_box)
    ax.text(10, 4.7, 'FAISS Index', ha='center', va='center', fontweight='bold', fontsize=10)
    ax.text(10, 4.35, 'HNSW Algorithm', ha='center', va='center', fontsize=7)
    ax.text(10, 4.05, 'M=32, efSearch=100', ha='center', va='center', fontsize=6)
    ax.text(10, 3.75, 'ANN Search < 127ms', ha='center', va='center', fontsize=6, style='italic')
    
    # ============ SIMILARITY SEARCH ============
    search_box = FancyBboxPatch((1.5, 2.8), 5, 0.8, boxstyle="round,pad=0.1",
                                edgecolor=search_color, facecolor=search_color, alpha=0.2, linewidth=2)
    ax.add_patch(search_box)
    ax.text(4, 3.4, 'Cosine Similarity Search', ha='center', va='center', fontweight='bold')
    ax.text(4, 3, 'Top-K Products (K=10-100)', ha='center', va='center', fontsize=7)
    
    # ============ CONTEXT-AWARE RANKING ============
    rank_box = FancyBboxPatch((1.5, 1.2), 5, 1.3, boxstyle="round,pad=0.1",
                              edgecolor=rank_color, facecolor=rank_color, alpha=0.2, linewidth=2)
    ax.add_patch(rank_box)
    ax.text(4, 2.3, 'Context-Aware Reranking', ha='center', va='center', 
            fontweight='bold', fontsize=10)
    
    # Ranking components
    ax.text(2.2, 1.9, '⭐ Sentiment', ha='center', fontsize=6)
    ax.text(3.3, 1.9, '🎯 Occasion', ha='center', fontsize=6)
    ax.text(4.4, 1.9, '🔄 Cross-Attn', ha='center', fontsize=6)
    ax.text(5.5, 1.9, '🎲 Diversity', ha='center', fontsize=6)
    
    # Formula
    ax.text(4, 1.5, 'Score = ', ha='center', fontsize=7)
    ax.text(4, 1.25, 's_sim + λ₁·s_sent + λ₂·s_ctx + λ₃·s_div', 
            ha='center', fontsize=6, family='monospace')
    
    # ============ OUTPUT ============
    output_box = FancyBboxPatch((2.5, 0.1), 3, 0.8, boxstyle="round,pad=0.1",
                                edgecolor=output_color, facecolor=output_color, alpha=0.3, linewidth=2)
    ax.add_patch(output_box)
    ax.text(4, 0.7, 'Ranked Results', ha='center', va='center', fontweight='bold')
    ax.text(4, 0.35, 'Top-10 Products with Scores', ha='center', va='center', fontsize=7)
    
    # ============ ARROWS ============
    arrow_props = dict(arrowstyle='->', lw=2, color='#2c3e50')
    
    # Input to CLIP
    ax.annotate('', xy=(2, 5.8), xytext=(1.5, 7.5), arrowprops=arrow_props)
    ax.annotate('', xy=(4, 5.8), xytext=(4, 7.5), arrowprops=arrow_props)
    
    # CLIP to Fusion
    ax.annotate('', xy=(3, 5.3), xytext=(3, 5.8), arrowprops=arrow_props)
    
    # Fusion to Search
    ax.annotate('', xy=(3.5, 3.6), xytext=(3.5, 4.3), arrowprops=arrow_props)
    
    # Database to FAISS
    ax.annotate('', xy=(10, 5), xytext=(10, 5.5), arrowprops=dict(arrowstyle='->', lw=1.5, color=storage_color))
    
    # FAISS to Search
    ax.annotate('', xy=(6.5, 3.2), xytext=(8.5, 4), arrowprops=arrow_props)
    
    # Search to Ranking
    ax.annotate('', xy=(4, 2.5), xytext=(4, 2.8), arrowprops=arrow_props)
    
    # Context to Ranking
    ax.annotate('', xy=(6.5, 2), xytext=(6.75, 7.5), 
                arrowprops=dict(arrowstyle='->', lw=1.5, color=input_color, linestyle='--'))
    
    # Ranking to Output
    ax.annotate('', xy=(4, 0.9), xytext=(4, 1.2), arrowprops=arrow_props)
    
    # Add legend
    legend_elements = [
        patches.Patch(facecolor=input_color, alpha=0.3, label='Input Layer'),
        patches.Patch(facecolor=encoder_color, alpha=0.3, label='Encoding'),
        patches.Patch(facecolor=storage_color, alpha=0.3, label='Storage'),
        patches.Patch(facecolor=search_color, alpha=0.3, label='Search'),
        patches.Patch(facecolor=rank_color, alpha=0.3, label='Ranking'),
        patches.Patch(facecolor=output_color, alpha=0.3, label='Output')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=7, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('figures/architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created architecture.png")
    plt.close()


def create_data_flow_pipeline():
    """Create data processing pipeline diagram"""
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(7, 5.5, 'Data Processing Pipeline', ha='center', fontsize=14, fontweight='bold')
    
    # Pipeline stages
    stages = [
        {"x": 0.5, "title": "Data\nCollection", "content": "• E-commerce APIs\n• 50K+ products\n• Multi-category"},
        {"x": 2.5, "title": "Image\nDownload", "content": "• Parallel fetch\n• Retry logic\n• Validation"},
        {"x": 4.5, "title": "Pre-\nprocessing", "content": "• Resize 224×224\n• Normalization\n• Augmentation"},
        {"x": 6.5, "title": "CLIP\nEncoding", "content": "• Batch process\n• GPU accel.\n• 512-dim embed"},
        {"x": 8.5, "title": "Embedding\nStorage", "content": "• NumPy arrays\n• 200MB total\n• Fast loading"},
        {"x": 10.5, "title": "FAISS\nIndexing", "content": "• HNSW build\n• ~58s for 50K\n• Optimized"},
        {"x": 12.5, "title": "Production\nReady", "content": "• REST API\n• 127ms latency\n• Scalable"}
    ]
    
    colors = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c', '#1abc9c', '#34495e']
    
    for i, stage in enumerate(stages):
        # Box
        box = FancyBboxPatch((stage["x"], 2), 1.5, 2.5, boxstyle="round,pad=0.1",
                            edgecolor=colors[i], facecolor=colors[i], alpha=0.2, linewidth=2)
        ax.add_patch(box)
        
        # Title
        ax.text(stage["x"] + 0.75, 4.2, stage["title"], ha='center', va='top', 
                fontweight='bold', fontsize=8)
        
        # Content
        for j, line in enumerate(stage["content"].split('\n')):
            ax.text(stage["x"] + 0.75, 3.6 - j*0.3, line, ha='center', va='top', fontsize=6)
        
        # Arrow to next stage
        if i < len(stages) - 1:
            ax.annotate('', xy=(stage["x"] + 2, 3.25), xytext=(stage["x"] + 1.6, 3.25),
                       arrowprops=dict(arrowstyle='->', lw=2, color='#2c3e50'))
    
    # Offline/Online marker
    ax.axhline(y=1.5, xmin=0.04, xmax=0.68, color='red', linewidth=2, linestyle='--', alpha=0.5)
    ax.text(4.5, 1.2, 'OFFLINE PROCESSING', ha='center', fontsize=8, 
            color='red', fontweight='bold')
    
    ax.axhline(y=1.5, xmin=0.72, xmax=0.96, color='green', linewidth=2, linestyle='--', alpha=0.5)
    ax.text(11.5, 1.2, 'ONLINE', ha='center', fontsize=8, 
            color='green', fontweight='bold')
    
    # Metrics
    ax.text(7, 0.5, 'Total Processing Time: ~15 min (50K products) | Query Time: <127ms | Memory: 200MB',
            ha='center', fontsize=7, style='italic', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('figures/data_pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created data_pipeline.png")
    plt.close()


def create_query_flow():
    """Create query processing flow diagram"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    ax.text(5, 7.5, 'Query Processing Flow', ha='center', fontsize=14, fontweight='bold')
    
    # User Query
    query_box = FancyBboxPatch((3.5, 6.5), 3, 0.6, boxstyle="round,pad=0.05",
                               edgecolor='#3498db', facecolor='#3498db', alpha=0.3, linewidth=2)
    ax.add_patch(query_box)
    ax.text(5, 6.8, 'User Query (Text/Image/Both)', ha='center', fontweight='bold', fontsize=9)
    
    # Encoding
    encode_box = FancyBboxPatch((3.5, 5.5), 3, 0.6, boxstyle="round,pad=0.05",
                                edgecolor='#2ecc71', facecolor='#2ecc71', alpha=0.3, linewidth=2)
    ax.add_patch(encode_box)
    ax.text(5, 5.8, 'CLIP Encoding → 512-dim vector', ha='center', fontweight='bold', fontsize=9)
    
    # Decision diamond for modality
    diamond_points = np.array([[5, 4.8], [5.7, 4.3], [5, 3.8], [4.3, 4.3], [5, 4.8]])
    diamond = patches.Polygon(diamond_points, closed=True, edgecolor='#f39c12', 
                             facecolor='#f39c12', alpha=0.3, linewidth=2)
    ax.add_patch(diamond)
    ax.text(5, 4.3, 'Multi-\nModal?', ha='center', va='center', fontsize=7, fontweight='bold')
    
    # Fusion path (Yes)
    fusion_box = FancyBboxPatch((6.5, 3.2), 2.5, 0.8, boxstyle="round,pad=0.05",
                                edgecolor='#9b59b6', facecolor='#9b59b6', alpha=0.3, linewidth=2)
    ax.add_patch(fusion_box)
    ax.text(7.75, 3.8, 'Fusion Layer', ha='center', fontweight='bold', fontsize=8)
    ax.text(7.75, 3.4, 'α·e_img + (1-α)·e_text', ha='center', fontsize=6, family='monospace')
    
    # Direct path (No)
    direct_box = FancyBboxPatch((1, 3.2), 2.5, 0.8, boxstyle="round,pad=0.05",
                                edgecolor='#95a5a6', facecolor='#95a5a6', alpha=0.3, linewidth=2)
    ax.add_patch(direct_box)
    ax.text(2.25, 3.6, 'Single Modality', ha='center', fontweight='bold', fontsize=8)
    
    # FAISS Search
    faiss_box = FancyBboxPatch((3.5, 2), 3, 0.6, boxstyle="round,pad=0.05",
                               edgecolor='#e74c3c', facecolor='#e74c3c', alpha=0.3, linewidth=2)
    ax.add_patch(faiss_box)
    ax.text(5, 2.3, 'FAISS ANN Search (Top-K)', ha='center', fontweight='bold', fontsize=9)
    
    # Context-aware ranking
    rank_box = FancyBboxPatch((3, 0.8), 4, 0.8, boxstyle="round,pad=0.05",
                              edgecolor='#1abc9c', facecolor='#1abc9c', alpha=0.3, linewidth=2)
    ax.add_patch(rank_box)
    ax.text(5, 1.4, 'Context-Aware Reranking', ha='center', fontweight='bold', fontsize=9)
    ax.text(5, 1, 'Sentiment + Occasion + Cross-Attention + Diversity', ha='center', fontsize=7)
    
    # Final results
    result_box = FancyBboxPatch((3.5, 0), 3, 0.5, boxstyle="round,pad=0.05",
                                edgecolor='#34495e', facecolor='#34495e', alpha=0.3, linewidth=2)
    ax.add_patch(result_box)
    ax.text(5, 0.25, 'Ranked Product Results', ha='center', fontweight='bold', fontsize=9)
    
    # Arrows
    arrow_style = dict(arrowstyle='->', lw=2, color='#2c3e50')
    
    ax.annotate('', xy=(5, 6.5), xytext=(5, 6.1), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 5.5), xytext=(5, 4.8), arrowprops=arrow_style)
    
    # Yes/No paths
    ax.annotate('', xy=(6.5, 3.6), xytext=(5.5, 4.15), arrowprops=arrow_style)
    ax.text(6, 4, 'Yes', fontsize=7, fontweight='bold')
    
    ax.annotate('', xy=(3.5, 3.6), xytext=(4.5, 4.15), arrowprops=arrow_style)
    ax.text(4, 4, 'No', fontsize=7, fontweight='bold')
    
    # Merge to FAISS
    ax.annotate('', xy=(6.5, 2.5), xytext=(7.75, 3.2), arrowprops=arrow_style)
    ax.annotate('', xy=(3.5, 2.5), xytext=(2.25, 3.2), arrowprops=arrow_style)
    
    ax.annotate('', xy=(5, 2), xytext=(5, 1.6), arrowprops=arrow_style)
    ax.annotate('', xy=(5, 0.8), xytext=(5, 0.5), arrowprops=arrow_style)
    
    # Timing annotations
    ax.text(8.5, 6.8, '~20ms', fontsize=6, style='italic', color='gray')
    ax.text(8.5, 5.8, '~35ms', fontsize=6, style='italic', color='gray')
    ax.text(8.5, 2.3, '~50ms', fontsize=6, style='italic', color='gray')
    ax.text(8.5, 1.2, '~22ms', fontsize=6, style='italic', color='gray')
    
    ax.text(9.2, 4, 'Total:\n127ms\navg', ha='center', fontsize=7, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('figures/query_flow.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created query_flow.png")
    plt.close()


def create_fusion_strategies():
    """Visualize different fusion strategies"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    methods = [
        'Weighted Averaging',
        'Concatenation',
        'Element-wise Multiplication'
    ]
    
    for idx, (ax, method) in enumerate(zip(axes, methods)):
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.axis('off')
        ax.set_title(method, fontsize=11, fontweight='bold', pad=10)
        
        # Input embeddings
        img_box = Rectangle((0.5, 3.5), 1.5, 0.8, edgecolor='#3498db', 
                           facecolor='#3498db', alpha=0.3, linewidth=2)
        ax.add_patch(img_box)
        ax.text(1.25, 3.9, 'Image\nEmbed', ha='center', fontsize=8, fontweight='bold')
        
        text_box = Rectangle((0.5, 2), 1.5, 0.8, edgecolor='#2ecc71', 
                            facecolor='#2ecc71', alpha=0.3, linewidth=2)
        ax.add_patch(text_box)
        ax.text(1.25, 2.4, 'Text\nEmbed', ha='center', fontsize=8, fontweight='bold')
        
        # Operation
        if idx == 0:  # Weighted averaging
            op_box = Circle((2.5, 2.9), 0.4, edgecolor='#e74c3c', 
                           facecolor='#e74c3c', alpha=0.3, linewidth=2)
            ax.add_patch(op_box)
            ax.text(2.5, 2.9, '⊕', ha='center', va='center', fontsize=16, fontweight='bold')
            ax.text(2.5, 1.5, 'α·e₁ + (1-α)·e₂', ha='center', fontsize=7, family='monospace')
            ax.text(2.5, 1.1, 'α = 0.7 (default)', ha='center', fontsize=6, style='italic')
            
        elif idx == 1:  # Concatenation
            op_box = Circle((2.5, 2.9), 0.4, edgecolor='#e74c3c', 
                           facecolor='#e74c3c', alpha=0.3, linewidth=2)
            ax.add_patch(op_box)
            ax.text(2.5, 2.9, '||', ha='center', va='center', fontsize=16, fontweight='bold')
            ax.text(2.5, 1.5, '[e₁ ⊕ e₂] · W', ha='center', fontsize=7, family='monospace')
            ax.text(2.5, 1.1, '1024→512 projection', ha='center', fontsize=6, style='italic')
            
        else:  # Element-wise
            op_box = Circle((2.5, 2.9), 0.4, edgecolor='#e74c3c', 
                           facecolor='#e74c3c', alpha=0.3, linewidth=2)
            ax.add_patch(op_box)
            ax.text(2.5, 2.9, '⊙', ha='center', va='center', fontsize=16, fontweight='bold')
            ax.text(2.5, 1.5, 'e₁ ⊙ e₂', ha='center', fontsize=7, family='monospace')
            ax.text(2.5, 1.1, 'Hadamard product', ha='center', fontsize=6, style='italic')
        
        # Output
        out_box = Rectangle((3.5, 2.5), 1.5, 0.8, edgecolor='#9b59b6', 
                           facecolor='#9b59b6', alpha=0.3, linewidth=2)
        ax.add_patch(out_box)
        ax.text(4.25, 2.9, 'Fused\nEmbed', ha='center', fontsize=8, fontweight='bold')
        
        # Arrows
        ax.annotate('', xy=(2.1, 3.2), xytext=(2, 3.7), 
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'))
        ax.annotate('', xy=(2.1, 2.7), xytext=(2, 2.6), 
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'))
        ax.annotate('', xy=(3.5, 2.9), xytext=(2.9, 2.9), 
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'))
        
        # Performance indicator
        perf = ['94.1%', '92.8%', '91.9%']
        ax.text(4.25, 1.8, f'P@10: {perf[idx]}', ha='center', fontsize=7, 
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('figures/fusion_strategies.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created fusion_strategies.png")
    plt.close()


if __name__ == "__main__":
    print("Generating architecture and flow diagrams...")
    print("-" * 50)
    
    create_system_architecture()
    create_data_flow_pipeline()
    create_query_flow()
    create_fusion_strategies()
    
    print("-" * 50)
    print("✅ All diagrams generated successfully!")
    print("\nCreated files:")
    print("  • architecture.png - Complete system architecture")
    print("  • data_pipeline.png - Data processing pipeline")
    print("  • query_flow.png - Real-time query flow")
    print("  • fusion_strategies.png - Multi-modal fusion methods")
