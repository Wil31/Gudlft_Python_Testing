from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("")

    @task
    def login(self):
        self.client.post("showSummary", data=dict(email="john@simplylift.co"))

    @task
    def booking(self):
        self.client.get("book/Spring Festival/Simply Lift")

    @task
    def clubsBoard(self):
        self.client.get("clubsBoard")

    @task
    def logout(self):
        self.client.get("logout")
