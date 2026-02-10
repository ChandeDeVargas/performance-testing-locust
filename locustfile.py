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
    
    
    def validate_response(self, response, endpoint, method, expected_status=200):
        """
        Centralized response validation with SLA checking.
        
        Args:
            response: Response object
            endpoint: Endpoint name (for SLA lookup)
            method: HTTP method
            expected_status: Expected status code
            
        Returns:
            bool: True if validation passed
        """
        # Status code validation
        if response.status_code != expected_status:
            response.failure(f"Expected {expected_status}, got {response.status_code}")
            return False
        
        # Response time SLA validation (already tracked in event hook)
        # Just mark success here
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
            if self.validate_response(response, endpoint, "GET"):
                # Additional validation: check response structure
                try:
                    data = response.json()
                    if not data or len(data) == 0:
                        response.failure("Empty response")
                        logger.error("GET /posts returned empty array")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(2)
    def get_single_post(self):
        """
        GET /posts/1 - View specific post
        SLA: < 300ms
        """
        endpoint = "/posts/1"
        with self.client.get(endpoint, catch_response=True, name="GET /posts/1") as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    required_fields = ["id", "title", "body", "userId"]
                    if not all(field in data for field in required_fields):
                        response.failure("Missing required fields")
                        logger.error(f"GET /posts/1 missing fields: {required_fields}")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(2)
    def get_comments(self):
        """
        GET /comments?postId=1 - Read comments
        SLA: < 400ms
        """
        endpoint = "/comments"
        with self.client.get(
            f"{endpoint}?postId=1", 
            catch_response=True, 
            name="GET /comments"
        ) as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    if not data or len(data) == 0:
                        response.failure("No comments returned")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(1)
    def create_post(self):
        """
        POST /posts - Create new post
        SLA: < 1000ms
        """
        endpoint = "/posts"
        payload = {
            "title": "Performance Test Post",
            "body": "This is a test post created during load testing",
            "userId": 1
        }
        
        with self.client.post(
            endpoint, 
            json=payload, 
            catch_response=True,
            name="POST /posts"
        ) as response:
            if self.validate_response(response, endpoint, "POST", expected_status=201):
                try:
                    data = response.json()
                    if "id" not in data:
                        response.failure("Response missing ID field")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(1)
    def update_post(self):
        """
        PUT /posts/1 - Update existing post
        SLA: < 800ms
        """
        endpoint = "/posts/1"
        payload = {
            "id": 1,
            "title": "Updated Performance Test Post",
            "body": "This post was updated during load testing",
            "userId": 1
        }
        
        with self.client.put(
            endpoint,
            json=payload,
            catch_response=True,
            name="PUT /posts/1"
        ) as response:
            self.validate_response(response, endpoint, "PUT")

    @task(2)
    def get_users(self):
        """
        GET /users - Browse all users
        SLA: < 500ms
        """
        endpoint = "/users"
        with self.client.get(endpoint, catch_response=True, name="GET /users") as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    if not data or len(data) == 0:
                        response.failure("Empty users list")
                    else:
                        # Validate user structure
                        if "id" not in data[0] or "email" not in data[0]:
                            response.failure("Invalid user structure")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(1)
    def get_user_detail(self):
        """
        GET /users/1 - View specific user
        SLA: < 300ms
        """
        endpoint = "/users/1"
        with self.client.get(endpoint, catch_response=True, name="GET /users/1") as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    required_fields = ["id", "name", "email", "address", "company"]
                    if not all(field in data for field in required_fields):
                        response.failure("Missing required user fields")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(1)
    def get_albums(self):
        """
        GET /albums - Browse all albums
        SLA: < 500ms
        """
        endpoint = "/albums"
        with self.client.get(endpoint, catch_response=True, name="GET /albums") as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    if not data or len(data) == 0:
                        response.failure("Empty albums list")
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")
    
    
    @task(1)
    def get_user_posts(self):
        """
        GET /posts?userId=1 - Get posts by specific user
        SLA: < 600ms
        """
        endpoint = "/posts?userId=1"
        with self.client.get(
            endpoint, 
            catch_response=True, 
            name="GET /posts?userId=1"
        ) as response:
            if self.validate_response(response, endpoint, "GET"):
                try:
                    data = response.json()
                    if not data or len(data) == 0:
                        response.failure("No posts for user")
                    # Validate all posts belong to userId=1
                    for post in data:
                        if post.get("userId") != 1:
                            response.failure("Posts contain wrong userId")
                            break
                except Exception as e:
                    response.failure(f"Invalid JSON: {str(e)}")