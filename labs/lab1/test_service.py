from service import TaskService

def make():
    s = TaskService()
    for i in range(1, 26):
        s.add(f"task {i}", priority="high" if i % 5 == 0 else "normal")
    return s

def test_first_page_has_first_items():
    s = make()
    page = s.list_tasks(page=1, per_page=10)
    assert [t["id"] for t in page] == list(range(1, 11))

def test_second_page():
    s = make()
    page = s.list_tasks(page=2, per_page=10)
    assert [t["id"] for t in page] == list(range(11, 21))

def test_priority_filter():
    s = make()
    high = s.list_tasks(priority="high", per_page=50)
    assert [t["id"] for t in high] == [5, 10, 15, 20, 25]

def test_filter_and_page():
    s = make()
    page = s.list_tasks(priority="normal", page=2, per_page=10)
    assert len(page) == 10 and all(t["priority"] == "normal" for t in page)

def test_complete():
    s = make()
    t = s.complete(3)
    assert t["done"] is True
    assert s.complete(999) is None
