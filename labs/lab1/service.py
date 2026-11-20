"""Lab 1: small task service. Feature: priority filter. Bug fix: page slice."""
class TaskService:
    def __init__(self):
        self._tasks = []
        self._next = 1
    def add(self, title, priority="normal"):
        task = {"id": self._next, "title": title, "priority": priority, "done": False}
        self._next += 1
        self._tasks.append(task)
        return task
    def list_tasks(self, priority=None, page=1, per_page=10):
        items = [t for t in self._tasks if priority is None or t["priority"] == priority]
        start = (page - 1) * per_page
        # Bug in baseline: start = page * per_page (skips first page). Fixed here.
        return items[start:start + per_page]
    def complete(self, task_id):
        for t in self._tasks:
            if t["id"] == task_id:
                t["done"] = True
                return t
        return None
