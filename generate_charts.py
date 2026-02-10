"""
Generate performance comparison charts
Creates HTML visualizations from test results
"""
import csv
import glob
import os
from collections import defaultdict


def parse_csv_stats(csv_path):
    """Parse Locust stats CSV file"""
    stats = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'Aggregated':
                    continue
                stats.append({
                    'name': row['Name'],
                    'requests': int(row['Request Count']),
                    'avg_time': float(row['Average Response Time']),
                    'rps': float(row['Requests/s'])
                })
    except Exception as e:
        print(f"Error parsing {csv_path}: {e}")
        return []
    
    return stats


def find_latest_results():
    """Find the most recent test results"""
    reports_dir = "reports"
    
    csv_files = {}
    for user_count in ['10', '50', '100']:
        pattern = f"{reports_dir}/results_{user_count}users_*_stats.csv"
        files = glob.glob(pattern)
        if files:
            csv_files[user_count] = max(files, key=os.path.getmtime)
    
    return csv_files


def generate_chart_html(all_stats):
    """Generate interactive HTML chart"""
    
    # Collect data per endpoint
    endpoints_data = defaultdict(lambda: {'10': 0, '50': 0, '100': 0})
    
    for users, stats in all_stats.items():
        for stat in stats:
            endpoints_data[stat['name']][users] = stat['avg_time']
    
    # Generate Chart.js HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Test Results - Visual Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .chart-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .legend {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Performance Test Dashboard</h1>
        
        <div class="stats-grid">
"""
    
    # Calculate summary stats
    for users in ['10', '50', '100']:
        if users in all_stats:
            total_requests = sum(s['requests'] for s in all_stats[users])
            avg_rps = sum(s['rps'] for s in all_stats[users])
            
            html += f"""
            <div class="stat-card">
                <div class="stat-label">{users} Users Load</div>
                <div class="stat-value">{total_requests:,}</div>
                <div class="stat-label">Total Requests</div>
                <div class="stat-value" style="font-size: 1.5em; margin-top: 10px;">{avg_rps:.1f}</div>
                <div class="stat-label">RPS</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="dashboard">
            <div class="chart-container">
                <h2 class="chart-title">Response Time by Load Level</h2>
                <canvas id="responseTimeChart"></canvas>
            </div>
            
            <div class="chart-container">
                <h2 class="chart-title">Endpoint Comparison</h2>
                <canvas id="endpointChart"></canvas>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #667eea;"></div>
                <span>10 Users (Baseline)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f093fb;"></div>
                <span>50 Users (Medium)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #ff6b6b;"></div>
                <span>100 Users (Stress)</span>
            </div>
        </div>
    </div>
    
    <script>
"""
    
    # Prepare data for Chart.js
    endpoints = sorted(endpoints_data.keys())
    data_10 = [endpoints_data[ep]['10'] for ep in endpoints]
    data_50 = [endpoints_data[ep]['50'] for ep in endpoints]
    data_100 = [endpoints_data[ep]['100'] for ep in endpoints]
    
    html += f"""
        // Response Time Chart
        const ctx1 = document.getElementById('responseTimeChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'bar',
            data: {{
                labels: {endpoints},
                datasets: [
                    {{
                        label: '10 Users',
                        data: {data_10},
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: 'rgba(102, 126, 234, 1)',
                        borderWidth: 2
                    }},
                    {{
                        label: '50 Users',
                        data: {data_50},
                        backgroundColor: 'rgba(240, 147, 251, 0.8)',
                        borderColor: 'rgba(240, 147, 251, 1)',
                        borderWidth: 2
                    }},
                    {{
                        label: '100 Users',
                        data: {data_100},
                        backgroundColor: 'rgba(255, 107, 107, 0.8)',
                        borderColor: 'rgba(255, 107, 107, 1)',
                        borderWidth: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{
                            font: {{
                                size: 14
                            }}
                        }}
                    }},
                    title: {{
                        display: true,
                        text: 'Average Response Time (ms)',
                        font: {{
                            size: 16
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Response Time (ms)'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            autoSkip: false,
                            maxRotation: 45,
                            minRotation: 45
                        }}
                    }}
                }}
            }}
        }});
        
        // Endpoint Comparison Chart
        const ctx2 = document.getElementById('endpointChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'line',
            data: {{
                labels: ['10 Users', '50 Users', '100 Users'],
                datasets: {[
                    {
                        'label': f"'{ep}'",
                        'data': [endpoints_data[ep]['10'], endpoints_data[ep]['50'], endpoints_data[ep]['100']],
                        'borderWidth': 3,
                        'tension': 0.4
                    } for ep in endpoints[:5]  # Top 5 endpoints only
                ]}
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: 'Performance Degradation Trends',
                        font: {{
                            size: 16
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Response Time (ms)'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html


def main():
    """Main chart generation function"""
    print("=" * 60)
    print("PERFORMANCE CHARTS GENERATOR")
    print("=" * 60)
    print()
    
    # Find latest results
    csv_files = find_latest_results()
    
    # Parse all stats
    all_stats = {}
    for users, path in csv_files.items():
        if path:
            all_stats[users] = parse_csv_stats(path)
            print(f"✅ Parsed {users} users results")
    
    if not all_stats:
        print("❌ No results found!")
        return
    
    # Generate HTML chart
    print("\nGenerating interactive dashboard...")
    html = generate_chart_html(all_stats)
    
    # Write to file
    output_file = "reports/dashboard.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_file}")
    print()
    print("Open in browser:")
    print(f"  file:///{os.path.abspath(output_file)}")
    print()
    print("Or use Python server:")
    print("  cd reports")
    print("  python -m http.server 8000")
    print("  http://localhost:8000/dashboard.html")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()