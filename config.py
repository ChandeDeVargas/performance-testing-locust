"""
Performance Testing Configuration
Centralized settings for Locust tests
"""

# API Configuration
API_BASE_URL = "https://jsonplaceholder.typicode.com"

# SLA Thresholds (Response Time Limits)
SLA_THRESHOLDS = {
    "GET": {
        "/posts": 500,              # Max 500ms for browsing posts
        "/posts/1": 300,            # Max 300ms for single post
        "/comments": 400,           # Max 400ms for comments
        "/users": 500,              # Max 500ms for browsing users
        "/users/1": 300,            # Max 300ms for single user
        "/albums": 500,             # Max 500ms for browsing albums
        "/posts?userId=1": 600,     # Max 600ms for filtered posts
    },
    "POST": {
        "/posts": 1000,             # Max 1000ms for creating post
    },
    "PUT": {
        "/posts/1": 800,            # Max 800ms for updating post
    }
}
# Performance Percentiles to Track
PERCENTILES = [0.50, 0.75, 0.90, 0.95, 0.99]

# Test Scenarios Configuration
SCENARIOS = {
    "baseline": {
        "users": 10,
        "spawn_rate": 2,
        "duration": "60s"
    },
    "medium": {
        "users": 50,
        "spawn_rate": 5,
        "duration": "60s"
    },
    "stress": {
        "users": 100,
        "spawn_rate": 10,
        "duration": "60s"
    }
}

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Feature Flags
ENABLE_ASSERTIONS = True       # Fail tests if SLA violated
ENABLE_DETAILED_LOGGING = True # Log each request details
ENABLE_PERCENTILE_TRACKING = True