from locust import HttpUser, task, between


class SmokeTestUser(HttpUser):
    wait = between(1, 2)
    

    @task
    def visit_home(self):
        self.client.get("/", name="Home")
