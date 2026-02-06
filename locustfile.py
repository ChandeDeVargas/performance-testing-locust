"""
Performance Testing - JSONPlaceholder API
Purpose: Load test public REST API to identify performance bottlenecks
"""
from locust import HttpUser, task, between

class JSONPlaceholderUser(HttpUser):
    """
    Simulates a user interacting with JSONPlaceholder API.
    
    Wait time: 1-3 seconds between requests (realistic user behavior)
    """
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"

    @task(3) # Weight: 3x more frequent than other tasks
    def get_all_posts(self):
        """
        Test: GET /posts
        Expected: 200 OK, response time < 500ms
        Simulates: User browsing all posts
        """
        with self.client.get("/posts", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")



    @task(2) # Weight: 2x
    def get_single_post(self):
        """
        Test: GET /posts/1
        Expected: 200 OK, response time < 300ms
        Simulates: User viewing a specific post
        """
        with self.client.get("/posts/1", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Got status code {response.status_code}")
            

    @task(1) # Weight: 1x (less frequent)
    def create_post(self):
        """
        Test: POST /posts
        Expected: 201 Created, response time < 1000ms
        Simulates: User creating a new post
        """
        payload = {
            "title": "Performance Test Post",
            "body": "This is a test post created during load testing",
            "userId": 1
        }

        with self.client.post("/posts", json=payload, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Expected 201, got {response.status_code}")