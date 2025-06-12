import time

from locust import HttpUser, task, between


class HelloWorldUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("http://127.0.0.1:8001/health")

    @task(3)
    def view_environments(self):
        for item in range(10):
            self.client.get("http://127.0.0.1:8001/api/modules/?skip=0&limit=100")
            time.sleep(1)

    def on_start(self):
        self.client.get("http://127.0.0.1:8001/api/environments/?skip=0&limit=100")
