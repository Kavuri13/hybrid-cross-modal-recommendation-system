"""
Generate publication-quality table images for IEEE journal paper
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np

# Set publication-quality parameters
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

def create_table_image(data, col_labels, row_labels, title, filename, highlight_last_row=True):
    """Create a professional table image"""
    fig, ax = plt.subplots(figsize=(10, len(row_labels) * 0.5 + 1.5))
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=data, colLabels=col_labels, rowLabels=row_labels,
                     cellLoc='center', loc='center',
                     colWidths=[0.15] * len(col_labels))
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.0)
    
    # Header row styling
    for i in range(len(col_labels)):
        cell = table[(0, i)]
        cell.set_facecolor('#4472C4')
        cell.set_text_props(weight='bold', color='white')
    
    # Row label styling
    for i in range(1, len(row_labels) + 1):
        cell = table[(i, -1)]
        cell.set_facecolor('#E7E6E6')
        cell.set_text_props(weight='bold')
    
    # Highlight last row (our method)
    if highlight_last_row:
        for j in range(len(col_labels)):
            cell = table[(len(row_labels), j)]
            cell.set_facecolor('#FFE699')
            cell.set_text_props(weight='bold')
    
    # Alternate row colors
    for i in range(1, len(row_labels)):
        for j in range(len(col_labels)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F2F2F2')
            else:
                table[(i, j)].set_facecolor('white')
    
    # Add title
    plt.title(title, fontsize=12, fontweight='bold', pad=20)
    
    plt.savefig(f'figures/{filename}', bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()
    print(f"✓ Generated {filename}")


# Table I: Performance Comparison - Text Queries
data1 = [
    ['64.3%', '52.1%', '58.7%', '71.2%'],
    ['73.4%', '62.8%', '69.1%', '78.9%'],
    ['78.2%', '70.1%', '74.3%', '82.1%'],
    ['85.6%', '78.4%', '81.2%', '87.9%'],
    ['92.3%', '84.7%', '89.1%', '92.4%']
]
col_labels1 = ['P@10', 'R@50', 'MAP', 'NDCG']
row_labels1 = ['TF-IDF+ResNet', 'BERT+ViT', 'VSE++', 'CLIP (base)', 'Ours (Full)']
create_table_image(data1, col_labels1, row_labels1, 
                   'Table I: Performance Comparison - Text Queries',
                   'table1_text_queries.png')

# Table II: Performance Comparison - Image Queries
data2 = [
    ['61.2%', '49.8%', '55.6%', '68.7%'],
    ['70.1%', '61.4%', '67.3%', '76.1%'],
    ['75.8%', '68.2%', '72.4%', '79.8%'],
    ['83.4%', '76.2%', '79.6%', '86.2%'],
    ['88.7%', '82.1%', '86.3%', '90.1%']
]
create_table_image(data2, col_labels1, row_labels1,
                   'Table II: Performance Comparison - Image Queries',
                   'table2_image_queries.png')

# Table III: Performance Comparison - Hybrid Queries
data3 = [
    ['68.9%', '56.7%', '62.3%', '73.4%'],
    ['77.6%', '69.1%', '74.1%', '81.2%'],
    ['82.1%', '74.3%', '78.9%', '85.4%'],
    ['89.1%', '82.3%', '85.7%', '90.3%'],
    ['94.1%', '87.9%', '91.2%', '94.7%']
]
create_table_image(data3, col_labels1, row_labels1,
                   'Table III: Performance Comparison - Hybrid Queries',
                   'table3_hybrid_queries.png')

# Table IV: Contribution of Each Component
data4 = [
    ['85.6%', '81.2%', '98ms'],
    ['89.1%', '84.7%', '114ms'],
    ['90.8%', '87.1%', '119ms'],
    ['91.7%', '88.6%', '123ms'],
    ['92.3%', '89.1%', '127ms']
]
col_labels4 = ['P@10', 'MAP', 'Latency']
row_labels4 = ['Base (CLIP only)', '+ Sentiment Analysis', '+ Occasion Matching', 
               '+ Cross-Attention', 'Full System']
create_table_image(data4, col_labels4, row_labels4,
                   'Table IV: Contribution of Each Component (Ablation Study)',
                   'table4_ablation.png')

# Table V: Fusion Strategy Comparison
data5 = [
    ['94.1%', '91.2%', '94.7%', '127ms'],
    ['92.8%', '89.7%', '93.4%', '139ms'],
    ['91.9%', '88.3%', '92.6%', '124ms']
]
col_labels5 = ['P@10', 'MAP', 'NDCG', 'Latency']
row_labels5 = ['Weighted Avg (α=0.7)', 'Concatenation', 'Element-wise']
create_table_image(data5, col_labels5, row_labels5,
                   'Table V: Performance of Different Fusion Strategies',
                   'table5_fusion.png', highlight_last_row=False)

# Table VI: Scalability Analysis
data6 = [
    ['12s', '45ms', '80MB', '98.2%'],
    ['58s', '127ms', '200MB', '97.8%'],
    ['124s', '189ms', '410MB', '97.5%'],
    ['682s', '347ms', '2.1GB', '96.9%'],
    ['1456s', '521ms', '4.3GB', '96.4%']
]
col_labels6 = ['Index Build', 'Query Time', 'Memory', 'Accuracy (P@10)']
row_labels6 = ['10K products', '50K products', '100K products', '500K products', '1M products']
create_table_image(data6, col_labels6, row_labels6,
                   'Table VI: System Performance at Different Scales',
                   'table6_scalability.png', highlight_last_row=False)

# Table VII: Query Processing Time Breakdown
data7 = [
    ['35', '27.6%'],
    ['5', '3.9%'],
    ['50', '39.4%'],
    ['15', '11.8%'],
    ['12', '9.4%'],
    ['10', '7.9%'],
    ['127', '100%']
]
col_labels7 = ['Time (ms)', 'Percentage']
row_labels7 = ['Text/Image Encoding', 'Fusion (if hybrid)', 'FAISS Search', 
               'Context Scoring', 'Reranking', 'Response Formatting', 'Total']
create_table_image(data7, col_labels7, row_labels7,
                   'Table VII: Component-wise Latency Analysis (50K Products)',
                   'table7_latency.png', highlight_last_row=False)

print("\n✅ All 7 table images generated successfully!")
print("📁 Saved in: paper/figures/")
print("\nGenerated files:")
print("  - table1_text_queries.png")
print("  - table2_image_queries.png")
print("  - table3_hybrid_queries.png")
print("  - table4_ablation.png")
print("  - table5_fusion.png")
print("  - table6_scalability.png")
print("  - table7_latency.png")
