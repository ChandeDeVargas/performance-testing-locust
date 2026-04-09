"""
Performance Testing - JSONPlaceholder API
Advanced features: Custom metrics, SLA assertions, event hooks
Author: Your Name
Date: 2024-02-07
"""
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import logging
import time
import random
from config import (
    API_BASE_URL, 
    SLA_THRESHOLDS, 
    ENABLE_ASSERTIONS,
    ENABLE_DETAILED_LOGGING,
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_DATE_FORMAT
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT
)
logger = logging.getLogger(__name__)

# Global metrics storage
custom_metrics = {
    "sla_violations": 0,
    "slow_requests": []
}


# Event Hooks - Lifecycle Management
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts - setup phase"""
    logger.info("=" * 60)
    logger.info("PERFORMANCE TEST STARTED")
    logger.info("=" * 60)
    logger.info(f"Target: {API_BASE_URL}")
    logger.info(f"SLA Assertions: {'ENABLED' if ENABLE_ASSERTIONS else 'DISABLED'}")
    logger.info("=" * 60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops - cleanup phase"""
    logger.info("=" * 60)
    logger.info("PERFORMANCE TEST COMPLETED")
    logger.info("=" * 60)
    logger.info(f"Total SLA Violations: {custom_metrics['sla_violations']}")
    
    if custom_metrics['slow_requests']:
        logger.warning(f"Slow Requests Detected: {len(custom_metrics['slow_requests'])}")
        logger.warning("Top 5 slowest requests:")
        for req in sorted(custom_metrics['slow_requests'], key=lambda x: x['time'], reverse=True)[:5]:
            logger.warning(f"  - {req['method']} {req['name']}: {req['time']:.2f}ms")
    
    logger.info("=" * 60)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Called after each request - custom metrics tracking"""
    
    # Track slow requests (> 2 seconds)
    if response_time > 2000:
        custom_metrics['slow_requests'].append({
            'method': request_type,
            'name': name,
            'time': response_time
        })
        if ENABLE_DETAILED_LOGGING:
            logger.warning(f"SLOW REQUEST: {request_type} {name} took {response_time:.2f}ms")
    
    # SLA Validation
    if ENABLE_ASSERTIONS and not exception:
        sla_limit = None
        
        # Check if this endpoint has an SLA threshold
        if request_type in SLA_THRESHOLDS:
            for endpoint, limit in SLA_THRESHOLDS[request_type].items():
                if endpoint in name:
                    sla_limit = limit
                    break
        
        # Validate against SLA
        if sla_limit and response_time > sla_limit:
            custom_metrics['sla_violations'] += 1
            logger.error(
                f"SLA VIOLATION: {request_type} {name} "
                f"took {response_time:.2f}ms (limit: {sla_limit}ms)"
            )


class JSONPlaceholderUser(HttpUser):
    """
    Advanced Locust user with SLA validation and custom metrics.
    
    Features:
    - Response time assertions
    - Detailed logging
    - Custom metrics tracking
    - Event hooks
    """
    wait_time = between(1, 3)
    host = API_BASE_URL
    
    def on_start(self):
        """Called when a user starts"""
        if ENABLE_DETAILED_LOGGING:
            logger.info(f"User started (total active: {self.environment.runner.user_count})")
    
    
    def validate_response(self, response, endpoint, method, expected_status=200, required_keys=None):
        """
        Centralized response validation with SLA checking.
        
        Args:
            response: Response object
            endpoint: Endpoint name (for SLA lookup)
            method: HTTP method
            expected_status: Expected status code
            required_keys: List of keys expected in the JSON response
            
        Returns:
            bool: True if validation passed
        """
        # Status code validation
        if response.status_code != expected_status:
            response.failure(f"Expected {expected_status}, got {response.status_code}")
            return False
            
        if required_keys is not None:
            try:
                data = response.json()
                if not data:
                    response.failure("Empty or null JSON response")
                    return False
                    
                if isinstance(data, list):
                    if len(data) == 0:
                        response.failure("Empty array response")
                        return False
                    item = data[0]
                else:
                    item = data
                    
                missing_keys = [k for k in required_keys if k not in item]
                if missing_keys:
                    response.failure(f"Missing required fields: {missing_keys}")
                    return False
            except Exception as e:
                response.failure(f"Invalid JSON: {str(e)}")
                return False

        # Mark success here
        response.success()
        return True
    
    
    @task(3)
    def get_all_posts(self):
        """
        GET /posts - Browse all posts
        SLA: < 500ms
        """
        endpoint = "/posts"
        with self.client.get(endpoint, catch_response=True, name="GET /posts") as response:
            self.validate_response(response, endpoint, "GET", required_keys=["id", "title"])
    
    
    @task(2)
    def get_single_post(self):
        """
        GET /posts/{id} - View specific post
        SLA: < 300ms
        """
        post_id = random.randint(1, 100)
        endpoint = f"/posts/{post_id}"
        with self.client.get(endpoint, catch_response=True, name="GET /posts/1") as response:
            self.validate_response(response, "/posts/1", "GET", required_keys=["id", "title", "body", "userId"])
    
    
    @task(2)
    def get_comments(self):
        """
        GET /comments?postId={id} - Read comments
        SLA: < 400ms
        """
        post_id = random.randint(1, 100)
        endpoint = "/comments"
        with self.client.get(
            f"{endpoint}?postId={post_id}", 
            catch_response=True, 
            name="GET /comments"
        ) as response:
            self.validate_response(response, endpoint, "GET", required_keys=["id", "postId", "name", "email", "body"])
    
    
    @task(1)
    def create_post(self):
        """
        POST /posts - Create new post
        SLA: < 1000ms
        """
        endpoint = "/posts"
        user_id = random.randint(1, 10)
        payload = {
            "title": "Performance Test Post",
            "body": "This is a test post created during load testing",
            "userId": user_id
        }
        
        with self.client.post(
            endpoint, 
            json=payload, 
            catch_response=True,
            name="POST /posts"
        ) as response:
            self.validate_response(response, endpoint, "POST", expected_status=201, required_keys=["id"])
    
    
    @task(1)
    def update_post(self):
        """
        PUT /posts/{id} - Update existing post
        SLA: < 800ms
        """
        post_id = random.randint(1, 100)
        endpoint = f"/posts/{post_id}"
        payload = {
            "id": post_id,
            "title": "Updated Performance Test Post",
            "body": "This post was updated during load testing",
            "userId": random.randint(1, 10)
        }
        
        with self.client.put(
            endpoint,
            json=payload,
            catch_response=True,
            name="PUT /posts/1"
        ) as response:
            self.validate_response(response, "/posts/1", "PUT", required_keys=["id"])

    @task(2)
    def get_users(self):
        """
        GET /users - Browse all users
        SLA: < 500ms
        """
        endpoint = "/users"
        with self.client.get(endpoint, catch_response=True, name="GET /users") as response:
            self.validate_response(response, endpoint, "GET", required_keys=["id", "email"])
    
    
    @task(1)
    def get_user_detail(self):
        """
        GET /users/{id} - View specific user
        SLA: < 300ms
        """
        user_id = random.randint(1, 10)
        endpoint = f"/users/{user_id}"
        with self.client.get(endpoint, catch_response=True, name="GET /users/1") as response:
            self.validate_response(response, "/users/1", "GET", required_keys=["id", "name", "email", "address", "company"])
    
    
    @task(1)
    def get_albums(self):
        """
        GET /albums - Browse all albums
        SLA: < 500ms
        """
        endpoint = "/albums"
        with self.client.get(endpoint, catch_response=True, name="GET /albums") as response:
            self.validate_response(response, endpoint, "GET", required_keys=["id", "userId"])
    
    
    @task(1)
    def get_user_posts(self):
        """
        GET /posts?userId={id} - Get posts by specific user
        SLA: < 600ms
        """
        user_id = random.randint(1, 10)
        endpoint = f"/posts?userId={user_id}"
        with self.client.get(
            endpoint, 
            catch_response=True, 
            name="GET /posts?userId=1"
        ) as response:
            if self.validate_response(response, "/posts?userId=1", "GET", required_keys=["id", "userId", "title"]):
                # Validate all posts belong to user_id (not hardcoded 1)
                try:
                    data = response.json()
                    for post in data:
                        if post.get("userId") != user_id:
                            response.failure(f"Posts contain wrong userId (expected {user_id})")
                            break
                except Exception:
                    pass  # JSON already validated in validate_response