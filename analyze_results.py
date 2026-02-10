"""
Performance Test Results Analyzer
Reads CSV files and generates comparison reports
"""
import csv
import os
import glob
from datetime import datetime
from collections import defaultdict


def parse_csv_stats(csv_path):
    """Parse Locust stats CSV file"""
    stats = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip aggregated row
                if row['Name'] == 'Aggregated':
                    continue
                stats.append({
                    'type': row['Type'],
                    'name': row['Name'],
                    'requests': int(row['Request Count']),
                    'failures': int(row['Failure Count']),
                    'avg_time': float(row['Average Response Time']),
                    'min_time': float(row['Min Response Time']),
                    'max_time': float(row['Max Response Time']),
                    'rps': float(row['Requests/s'])
                })
    except Exception as e:
        print(f"Error parsing {csv_path}: {e}")
        return []
    
    return stats


def find_latest_results():
    """Find the most recent test results"""
    reports_dir = "reports"
    
    # Find all stats CSV files
    csv_files = {
        '10': None,
        '50': None,
        '100': None
    }
    
    for user_count in ['10', '50', '100']:
        pattern = f"{reports_dir}/results_{user_count}users_*_stats.csv"
        files = glob.glob(pattern)
        if files:
            # Get most recent file
            csv_files[user_count] = max(files, key=os.path.getmtime)
    
    return csv_files


def analyze_endpoint_performance(all_stats):
    """Compare endpoint performance across load levels"""
    
    # Group by endpoint
    endpoints = defaultdict(lambda: {'10': None, '50': None, '100': None})
    
    for user_count, stats in all_stats.items():
        for stat in stats:
            endpoint_name = stat['name']
            endpoints[endpoint_name][user_count] = stat
    
    return endpoints


def generate_comparison_report(endpoints):
    """Generate markdown comparison report"""
    
    report = []
    report.append("# Endpoint Performance Comparison\n")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")
    
    # Sort endpoints by name
    sorted_endpoints = sorted(endpoints.keys())
    
    for endpoint in sorted_endpoints:
        data = endpoints[endpoint]
        
        report.append(f"## {endpoint}\n\n")
        report.append("| Load | Requests | Failures | Avg Time | Min | Max | RPS |\n")
        report.append("|------|----------|----------|----------|-----|-----|-----|\n")
        
        for users in ['10', '50', '100']:
            if data[users]:
                d = data[users]
                report.append(
                    f"| {users} users | {d['requests']:,} | {d['failures']} | "
                    f"{d['avg_time']:.0f}ms | {d['min_time']:.0f}ms | "
                    f"{d['max_time']:.0f}ms | {d['rps']:.2f} |\n"
                )
            else:
                report.append(f"| {users} users | - | - | - | - | - | - |\n")
        
        # Calculate degradation
        if data['10'] and data['100']:
            baseline_time = data['10']['avg_time']
            stress_time = data['100']['avg_time']
            degradation = ((stress_time - baseline_time) / baseline_time) * 100
            
            report.append(f"\n**Performance Degradation:** {degradation:+.1f}% at 100 users\n\n")
            
            if degradation > 1000:
                report.append("🔴 **CRITICAL:** Severe performance degradation\n\n")
            elif degradation > 300:
                report.append("⚠️ **WARNING:** Significant performance degradation\n\n")
            elif degradation > 100:
                report.append("⚠️ **CAUTION:** Moderate performance degradation\n\n")
            else:
                report.append("✅ **GOOD:** Acceptable performance degradation\n\n")
        
        report.append("---\n\n")
    
    return ''.join(report)


def generate_summary_table(all_stats):
    """Generate summary statistics table"""
    
    summary = []
    summary.append("# Performance Summary by Load Level\n\n")
    
    summary.append("| Load | Total Requests | Total Failures | Avg RPS | Avg Response Time |\n")
    summary.append("|------|----------------|----------------|---------|-------------------|\n")
    
    for users in ['10', '50', '100']:
        if users in all_stats and all_stats[users]:
            stats = all_stats[users]
            total_requests = sum(s['requests'] for s in stats)
            total_failures = sum(s['failures'] for s in stats)
            avg_rps = sum(s['rps'] for s in stats)
            avg_time = sum(s['avg_time'] * s['requests'] for s in stats) / total_requests if total_requests > 0 else 0
            
            summary.append(
                f"| {users} users | {total_requests:,} | {total_failures} | "
                f"{avg_rps:.2f} | {avg_time:.0f}ms |\n"
            )
    
    summary.append("\n---\n\n")
    return ''.join(summary)


def main():
    """Main analysis function"""
    print("=" * 60)
    print("PERFORMANCE TEST RESULTS ANALYZER")
    print("=" * 60)
    print()
    
    # Find latest results
    csv_files = find_latest_results()
    
    print("Found test results:")
    for users, path in csv_files.items():
        if path:
            print(f"  ✅ {users} users: {os.path.basename(path)}")
        else:
            print(f"  ❌ {users} users: Not found")
    print()
    
    # Parse all stats
    all_stats = {}
    for users, path in csv_files.items():
        if path:
            all_stats[users] = parse_csv_stats(path)
    
    if not all_stats:
        print("❌ No results found to analyze!")
        return
    
    # Analyze endpoint performance
    endpoints = analyze_endpoint_performance(all_stats)
    
    # Generate reports
    print("Generating comparison report...")
    comparison = generate_comparison_report(endpoints)
    summary = generate_summary_table(all_stats)
    
    # Write to file
    output_file = "reports/COMPARISON.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
        f.write(comparison)
    
    print(f"✅ Report generated: {output_file}")
    print()
    print("=" * 60)
    print("Key Findings:")
    print("=" * 60)
    
    # Print quick summary
    for users in ['10', '50', '100']:
        if users in all_stats and all_stats[users]:
            stats = all_stats[users]
            total_requests = sum(s['requests'] for s in stats)
            total_failures = sum(s['failures'] for s in stats)
            failure_rate = (total_failures / total_requests * 100) if total_requests > 0 else 0
            
            print(f"{users} users: {total_requests:,} requests, {total_failures} failures ({failure_rate:.2f}%)")
    
    print("=" * 60)


if __name__ == "__main__":
    main()