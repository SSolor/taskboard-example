from datetime import date

import pytest

from taskboard import db, service


@pytest.fixture
def conn():
    connection = db.get_connection(":memory:")
    db.init_db(connection)
    yield connection
    connection.close()


def test_add_task_returns_id(conn):
    assert service.add_task(conn, "Write report") == 1


def test_add_task_rejects_blank_title(conn):
    with pytest.raises(ValueError):
        service.add_task(conn, "   ")


def test_add_task_rejects_bad_priority(conn):
    with pytest.raises(ValueError):
        service.add_task(conn, "Task", priority=9)


def test_complete_task_marks_done(conn):
    task_id = service.add_task(conn, "Task")
    service.complete_task(conn, task_id)
    assert service.list_tasks(conn, "done")[0]["id"] == task_id


def test_list_tasks_filters_by_status(conn):
    first = service.add_task(conn, "One")
    service.add_task(conn, "Two")
    service.complete_task(conn, first)
    assert len(service.list_tasks(conn, "open")) == 1
    assert len(service.list_tasks(conn)) == 2


def test_search_tasks_finds_match(conn):
    service.add_task(conn, "Buy milk")
    service.add_task(conn, "Call bank")
    assert [r["title"] for r in service.search_tasks(conn, "milk")] == ["Buy milk"]


def test_is_overdue(conn):
    task_id = service.add_task(conn, "Late", due_date="2020-01-01")
    task = service.list_tasks(conn)[0]
    assert task["id"] == task_id
    assert service.is_overdue(task, today=date(2026, 1, 1)) is True


def test_priority_label():
    assert service.priority_label(1) == "HIGH"
    assert service.priority_label(3) == "LOW"


def test_build_report_all_cases(conn):
    service.add_task(conn, "Plain")
    service.add_task(conn, "Upcoming", due_date="2030-01-01")
    service.add_task(conn, "Late low", priority=3, due_date="2020-01-01")
    service.add_task(conn, "Late high", priority=1, due_date="2020-01-01")
    done_id = service.add_task(conn, "Finished")
    service.complete_task(conn, done_id)

    report = service.build_report(service.list_tasks(conn), today=date(2026, 1, 1))

    assert "!! Late high (OVERDUE, HIGH)" in report
    assert "!  Late low (OVERDUE)" in report
    assert "   Upcoming (due 2030-01-01)" in report
    assert "   Plain" in report
    assert "x  Finished" in report