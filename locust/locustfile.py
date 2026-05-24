# locustfile.py — This is your load test. Locust looks for this file by default.
# Locust will pretend to be many users visiting your website at the same time.

from locust import HttpUser, task, between
# HttpUser  → a class that represents ONE simulated user making HTTP requests
# task      → a decorator that marks a function as something a user "does"
# between   → a helper that makes users wait a random time between actions


# This class represents a single simulated user
# Think of it as: "what does one user do on my site?"
class MyUser(HttpUser):

    # After each task, the user waits between 1 and 3 seconds before doing another
    # This simulates a real person pausing to read the page
    wait_time = between(1, 3)

    # @task means Locust will randomly pick this function for the user to run
    # The number in @task(2) is the "weight" — higher = chosen more often
    # This task has weight 2, so it runs roughly twice as often as a weight-1 task
    @task(2)
    def visit_home(self):
        # self.client is the built-in tool that makes HTTP requests
        # .get("/") sends a GET request to the home page of the target URL
        self.client.get("/")

    # Weight 1 = chosen half as often as the home page
    @task(1)
    def visit_about(self):
        # Visit the /about page
        self.client.get("/about")

    # Weight 1 = same frequency as /about
    @task(1)
    def visit_items(self):
        # Visit the /items page
        self.client.get("/items")

    # on_start runs ONCE when a simulated user first "logs in" / starts
    # Good place to do setup like logging in before the tasks begin
    def on_start(self):
        print("A new simulated user has started!")  # Just a message for us to see
