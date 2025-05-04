import time
import math
import requests

def addRandomTask(toskr_tasks):
    """Add a random task to the task list."""
    id = 2
    name = f"Task {id}"
    start = "A"
    end = "B"
    requests.get(f"http://localhost:8000/tasks/create?id={id}&name={name}&start={start}&end={end}&priority=0")


if __name__ == '__main__':
    # Simulate adding random tasks to the task list
    for i in range(5):
        addRandomTask(None)  # Replace None with actual task list object if needed
        time.sleep(5)  # Wait for 1 second before adding the next task