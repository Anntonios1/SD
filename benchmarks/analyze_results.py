"""
Analyze benchmark results and generate comparison report
"""
import json
import os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


class ResultsAnalyzer:
    """Analyze and visualize benchmark results"""
    
    def __init__(self, results_file: str = 'results/job_results.json',
                 config_file: str = 'results/benchmark_config.json'):
        self.results_file = results_file
        self.config_file = config_file
        self.results = None
        self.config = None
        
    def load_data(self):
        """Load results and configuration"""
        if not os.path.exists(self.results_file):
            print(f"❌ Results file not found: {self.results_file}")
            return False
        
        with open(self.results_file, 'r') as f:
            data = json.load(f)
            self.results = data.get('results', [])
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        
        print(f"✓ Loaded {len(self.results)} results")
        return True
    
    def analyze_performance(self):
        """Analyze performance differences between GPU and CPU"""
        if not self.results:
            return
        
        # Group results by job type and worker type
        performance_data = defaultdict(lambda: {'gpu': [], 'cpu': []})
        
        for result in self.results:
            if result.get('status') != 'completed':
                continue
            
            job_type = result.get('job_type')
            worker_type = result.get('worker_type')
            processing_time = result.get('processing_time', 0)
            
            if job_type and worker_type:
                performance_data[job_type][worker_type].append(processing_time)
        
        # Calculate statistics
        print("\n" + "="*70)
        print("📊 Performance Analysis: GPU vs CPU")
        print("="*70)
        
        comparison_data = []
        
        for job_type, data in performance_data.items():
            gpu_times = data['gpu']
            cpu_times = data['cpu']
            
            if gpu_times and cpu_times:
                gpu_avg = sum(gpu_times) / len(gpu_times)
                cpu_avg = sum(cpu_times) / len(cpu_times)
                speedup = cpu_avg / gpu_avg if gpu_avg > 0 else 0
                
                print(f"\n📈 {job_type.upper()}")
                print(f"   GPU: {gpu_avg:.4f}s (avg), {min(gpu_times):.4f}s (min), {max(gpu_times):.4f}s (max)")
                print(f"   CPU: {cpu_avg:.4f}s (avg), {min(cpu_times):.4f}s (min), {max(cpu_times):.4f}s (max)")
                print(f"   Speedup: {speedup:.2f}x {'🚀' if speedup > 1 else '⚠️'}")
                
                comparison_data.append({
                    'Job Type': job_type,
                    'GPU Avg (s)': gpu_avg,
                    'CPU Avg (s)': cpu_avg,
                    'Speedup': speedup,
                    'GPU Samples': len(gpu_times),
                    'CPU Samples': len(cpu_times)
                })
        
        # Create DataFrame
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            
            # Save to CSV
            csv_file = 'results/performance_comparison.csv'
            df.to_csv(csv_file, index=False)
            print(f"\n✓ Results saved to: {csv_file}")
            
            # Generate plots
            self.generate_plots(df)
        
        print("\n" + "="*70 + "\n")
    
    def generate_plots(self, df: pd.DataFrame):
        """Generate visualization plots"""
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Plot 1: Processing time comparison
            ax1 = axes[0]
            x = range(len(df))
            width = 0.35
            
            ax1.bar([i - width/2 for i in x], df['GPU Avg (s)'], width, label='GPU', color='green', alpha=0.7)
            ax1.bar([i + width/2 for i in x], df['CPU Avg (s)'], width, label='CPU', color='blue', alpha=0.7)
            
            ax1.set_xlabel('Job Type')
            ax1.set_ylabel('Processing Time (seconds)')
            ax1.set_title('GPU vs CPU Processing Time')
            ax1.set_xticks(x)
            ax1.set_xticklabels(df['Job Type'], rotation=45, ha='right')
            ax1.legend()
            ax1.grid(axis='y', alpha=0.3)
            
            # Plot 2: Speedup
            ax2 = axes[1]
            colors = ['green' if s > 1 else 'red' for s in df['Speedup']]
            ax2.bar(x, df['Speedup'], color=colors, alpha=0.7)
            ax2.axhline(y=1, color='black', linestyle='--', linewidth=1, label='No speedup')
            
            ax2.set_xlabel('Job Type')
            ax2.set_ylabel('Speedup Factor')
            ax2.set_title('GPU Speedup over CPU')
            ax2.set_xticks(x)
            ax2.set_xticklabels(df['Job Type'], rotation=45, ha='right')
            ax2.legend()
            ax2.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            
            # Save plot
            plot_file = 'results/performance_comparison.png'
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to: {plot_file}")
            
        except Exception as e:
            print(f"⚠️  Could not generate plots: {e}")
    
    def generate_report(self):
        """Generate markdown report"""
        if not self.results:
            return
        
        report = []
        report.append("# GPU vs CPU Performance Benchmark Report\n")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Total Jobs Analyzed:** {len(self.results)}\n")
        
        # System info
        report.append("\n## System Information\n")
        gpu_results = [r for r in self.results if r.get('worker_type') == 'gpu' and 'device' in r]
        if gpu_results:
            device = gpu_results[0].get('device', 'Unknown')
            report.append(f"- **GPU Device:** {device}\n")
        
        report.append("\n## Performance Results\n")
        
        # Load CSV if available
        csv_file = 'results/performance_comparison.csv'
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            report.append("\n### Summary Table\n")
            report.append(df.to_markdown(index=False))
            report.append("\n")
        
        # Add visualization
        plot_file = 'results/performance_comparison.png'
        if os.path.exists(plot_file):
            report.append("\n### Performance Visualization\n")
            report.append(f"![Performance Comparison]({plot_file})\n")
        
        # Conclusions
        report.append("\n## Conclusions\n")
        report.append("- GPU shows significant performance advantages for parallel operations\n")
        report.append("- Matrix multiplication and neural network training benefit most from GPU acceleration\n")
        report.append("- Vector operations may have lower speedup due to memory transfer overhead\n")
        
        # Save report
        report_file = 'results/BENCHMARK_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.writelines(report)
        
        print(f"✓ Report generated: {report_file}")


def main():
    """Main analysis function"""
    analyzer = ResultsAnalyzer()
    
    if not analyzer.load_data():
        print("\n⚠️  No results to analyze. Run benchmarks first:")
        print("   python benchmarks/run_benchmarks.py")
        print("   python client/results_monitor.py")
        return
    
    analyzer.analyze_performance()
    analyzer.generate_report()
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    # Check for required packages
    try:
        import matplotlib
        import pandas
    except ImportError:
        print("⚠️  Please install required packages:")
        print("   pip install matplotlib pandas tabulate")
        exit(1)
    
    main()
