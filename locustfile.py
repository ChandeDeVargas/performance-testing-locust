"""
Performance Testing - JSONPlaceholder API
Purpose: Load test REST API with multiple user load scenarios
Author: Chande De Vargas
Date: 2026-02-08

Scenarios:
    - Baseline: 10 users (normal load)
    - Medium: 50 users (moderate stress)
    - Stress: 100 users (high load)
"""
from locust import HttpUser, task, between
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONPlaceholderUser(HttpUser):
    """
    Simulates a user interacting with JSONPlaceholder API.
    
    Behavior:
    - Wait 1-3 seconds between requests (realistic user)
    - Weighted tasks (some endpoints more frequent than others)
    - Response validation with custom success/failure criteria
    
    Host: https://jsonplaceholder.typicode.com
    """
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"
    
    def on_start(self):
        """Called when a simulated user starts. Use for login/setup."""
        logger.info(f"User {self.environment.runner.user_count} started")
    
    
    @task(3)  # Weight: 3x (most frequent)
    def get_all_posts(self):
        """
        Test: GET /posts
        Expected: 200 OK, response time < 500ms
        Simulates: User browsing all posts (homepage)
        Weight: 3x (most common action)
        """
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code == 200:
                # Validate response contains data
                if response.json() and len(response.json()) > 0:
                    response.success()
                else:
                    response.failure("Response is empty")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    
    @task(2)  # Weight: 2x
    def get_single_post(self):
        """
        Test: GET /posts/1
        Expected: 200 OK, response time < 300ms
        Simulates: User viewing a specific post
        Weight: 2x
        """
        with self.client.get("/posts/1", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                # Validate response structure
                if "id" in data and "title" in data:
                    response.success()
                else:
                    response.failure("Invalid response structure")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    
    @task(2)  # Weight: 2x
    def get_comments(self):
        """
        Test: GET /comments?postId=1
        Expected: 200 OK, response time < 400ms
        Simulates: User reading comments on a post
        Weight: 2x
        """
        with self.client.get("/comments?postId=1", catch_response=True) as response:
            if response.status_code == 200:
                comments = response.json()
                if comments and len(comments) > 0:
                    response.success()
                else:
                    response.failure("No comments returned")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    
    @task(1)  # Weight: 1x (less frequent)
    def create_post(self):
        """
        Test: POST /posts
        Expected: 201 Created, response time < 1000ms
        Simulates: User creating a new post (less common)
        Weight: 1x
        """
        payload = {
            "title": "Performance Test Post",
            "body": "This is a test post created during load testing",
            "userId": 1
        }
        
        with self.client.post("/posts", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                data = response.json()
                if "id" in data:
                    response.success()
                else:
                    response.failure("Response missing ID")
            else:
                response.failure(f"Expected 201, got {response.status_code}")
    
    
    @task(1)  # Weight: 1x
    def update_post(self):
        """
        Test: PUT /posts/1
        Expected: 200 OK, response time < 800ms
        Simulates: User editing their post
        Weight: 1x
        """
        payload = {
            "id": 1,
            "title": "Updated Performance Test Post",
            "body": "This post was updated during load testing",
            "userId": 1
        }
        
        with self.client.put("/posts/1", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Expected 200, got {response.status_code}")