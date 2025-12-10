"""
Generate figures for the IEEE paper
Run this script to create publication-quality figures for the research paper
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

def create_context_impact_figure():
    """Create figure showing impact of context-aware ranking"""
    categories = ['Click-Through\nRate (%)', 'Conversion\nRate (%)', 'User\nSatisfaction']
    without_context = [62, 34, 71]
    with_context = [83, 48, 92]
    improvement = [34, 41, 30]  # percentage improvement
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(x - width/2, without_context, width, 
                   label='Without Context-Aware', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, with_context, width, 
                   label='With Context-Aware', color='#e74c3c', alpha=0.8)
    
    ax.set_ylabel('Score (%)', fontsize=11, fontweight='bold')
    ax.set_title('Impact of Context-Aware Ranking on User Engagement Metrics', 
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=10, loc='upper left', framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Add improvement percentages
    for i, imp in enumerate(improvement):
        ax.text(i, 95, f'+{imp}%', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/context_impact.png', dpi=300, bbox_inches='tight')
    print("✓ Created context_impact.png")
    plt.close()


def create_performance_comparison():
    """Create performance comparison across methods"""
    methods = ['TF-IDF+\nResNet', 'BERT+\nViT', 'VSE++', 'CLIP\n(base)', 'Ours']
    precision = [64.3, 73.4, 78.2, 85.6, 92.3]
    recall = [52.1, 62.8, 70.1, 78.4, 84.7]
    map_scores = [58.7, 69.1, 74.3, 81.2, 89.1]
    
    x = np.arange(len(methods))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width, precision, width, label='Precision@10', 
                   color='#3498db', alpha=0.8)
    bars2 = ax.bar(x, recall, width, label='Recall@50', 
                   color='#2ecc71', alpha=0.8)
    bars3 = ax.bar(x + width, map_scores, width, label='MAP', 
                   color='#e74c3c', alpha=0.8)
    
    ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('Performance Comparison Across Different Methods (Text Queries)', 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=10)
    ax.legend(fontsize=11, loc='upper left', framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('figures/performance_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created performance_comparison.png")
    plt.close()


def create_fusion_comparison():
    """Compare different fusion strategies"""
    fusion_methods = ['Weighted\nAveraging', 'Concatenation', 'Element-wise\nMultiplication']
    hybrid_performance = [94.1, 92.8, 91.9]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(fusion_methods, hybrid_performance, color=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.8)
    
    ax.set_ylabel('Precision@10 (%)', fontsize=11, fontweight='bold')
    ax.set_title('Performance of Different Fusion Strategies (Hybrid Queries)', 
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_ylim(85, 100)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/fusion_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created fusion_comparison.png")
    plt.close()


def create_ablation_study():
    """Ablation study showing contribution of each component"""
    configurations = ['Base\n(CLIP only)', '+ Sentiment\nAnalysis', 
                      '+ Occasion\nMatching', '+ Cross-\nAttention', 'Full\nSystem']
    precision = [85.6, 89.1, 90.8, 91.7, 92.3]
    latency = [98, 114, 119, 123, 127]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Precision subplot
    bars1 = ax1.bar(configurations, precision, color='#3498db', alpha=0.8)
    ax1.set_ylabel('Precision@10 (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Ablation Study: Precision Impact', fontsize=12, fontweight='bold')
    ax1.set_ylim(80, 100)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Latency subplot
    bars2 = ax2.bar(configurations, latency, color='#e74c3c', alpha=0.8)
    ax2.set_ylabel('Query Latency (ms)', fontsize=11, fontweight='bold')
    ax2.set_title('Ablation Study: Latency Impact', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 150)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/ablation_study.png', dpi=300, bbox_inches='tight')
    print("✓ Created ablation_study.png")
    plt.close()


def create_scalability_analysis():
    """Scalability analysis across different dataset sizes"""
    dataset_sizes = ['10K', '50K', '100K', '500K', '1M']
    query_times = [45, 127, 189, 347, 521]
    memory_usage = [80, 200, 410, 2100, 4300]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Query time subplot
    ax1.plot(dataset_sizes, query_times, marker='o', linewidth=2, 
             markersize=8, color='#3498db', label='Query Time')
    ax1.fill_between(range(len(dataset_sizes)), query_times, alpha=0.3, color='#3498db')
    ax1.set_xlabel('Dataset Size', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Query Latency (ms)', fontsize=11, fontweight='bold')
    ax1.set_title('Scalability: Query Performance', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.axhline(y=1000, color='r', linestyle='--', label='1 second threshold', alpha=0.5)
    ax1.legend(fontsize=10)
    
    for i, (size, time) in enumerate(zip(dataset_sizes, query_times)):
        ax1.text(i, time + 30, f'{time}ms', ha='center', fontsize=9, fontweight='bold')
    
    # Memory usage subplot
    ax2.plot(dataset_sizes, memory_usage, marker='s', linewidth=2, 
             markersize=8, color='#2ecc71', label='Memory Usage')
    ax2.fill_between(range(len(dataset_sizes)), memory_usage, alpha=0.3, color='#2ecc71')
    ax2.set_xlabel('Dataset Size', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Memory Usage (MB)', fontsize=11, fontweight='bold')
    ax2.set_title('Scalability: Memory Consumption', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(fontsize=10)
    
    for i, (size, mem) in enumerate(zip(dataset_sizes, memory_usage)):
        label = f'{mem}MB' if mem < 1000 else f'{mem/1000:.1f}GB'
        ax2.text(i, mem + 200, label, ha='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/scalability_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Created scalability_analysis.png")
    plt.close()


def create_query_type_comparison():
    """Compare performance across query types"""
    query_types = ['Text Only', 'Image Only', 'Hybrid\n(Text + Image)']
    our_method = [92.3, 88.7, 94.1]
    clip_base = [85.6, 83.4, 89.1]
    vse_plus = [78.2, 75.8, 82.1]
    
    x = np.arange(len(query_types))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width, vse_plus, width, label='VSE++', color='#95a5a6', alpha=0.8)
    bars2 = ax.bar(x, clip_base, width, label='CLIP (base)', color='#3498db', alpha=0.8)
    bars3 = ax.bar(x + width, our_method, width, label='Ours (Full System)', color='#e74c3c', alpha=0.8)
    
    ax.set_ylabel('Precision@10 (%)', fontsize=12, fontweight='bold')
    ax.set_title('Performance Comparison Across Query Types', fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(query_types, fontsize=11)
    ax.legend(fontsize=11, loc='lower right', framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('figures/query_type_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created query_type_comparison.png")
    plt.close()


if __name__ == "__main__":
    print("Generating figures for IEEE paper...")
    print("-" * 50)
    
    create_context_impact_figure()
    create_performance_comparison()
    create_fusion_comparison()
    create_ablation_study()
    create_scalability_analysis()
    create_query_type_comparison()
    
    print("-" * 50)
    print("✅ All figures generated successfully!")
    print("\nFigures saved in: paper/figures/")
    print("\nGenerated files:")
    print("  • context_impact.png")
    print("  • performance_comparison.png")
    print("  • fusion_comparison.png")
    print("  • ablation_study.png")
    print("  • scalability_analysis.png")
    print("  • query_type_comparison.png")
    print("\nYou can now compile the LaTeX document!")
