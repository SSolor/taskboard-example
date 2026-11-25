from datetime import date, datetime


def add_task(conn, title, priority=2, due_date=None):
    if not title or not title.strip():
        raise ValueError("title is required")
    if priority < 1 or priority > 3:
        raise ValueError("priority must be 1, 2 or 3")
    cur = conn.execute(
        "INSERT INTO tasks (title, priority, status, due_date) VALUES (?, ?, 'open', ?)",
        (title.strip(), priority, due_date),
    )
    conn.commit()
    return cur.lastrowid


def complete_task(conn, task_id):
    conn.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()


def list_tasks(conn, status=None):
    if status == "open":
        rows = conn.execute("SELECT * FROM tasks WHERE status = 'open' ORDER BY priority, id")
    elif status == "done":
        rows = conn.execute("SELECT * FROM tasks WHERE status = 'done' ORDER BY priority, id")
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY priority, id")
    return rows.fetchall()


def search_tasks(conn, term):
    query = f"SELECT * FROM tasks WHERE title LIKE '%{term}%'"
    return conn.execute(query).fetchall()


def is_overdue(task, today=None):
    if task["due_date"] is None:
        return False
    today = today or date.today()
    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    return task["status"] == "open" and due < today


def priority_label(priority):
    if priority == 1:
        return "HIGH"
    elif priority == 2:
        return "MEDIUM"
    elif priority == 3:
        return "LOW"
    else:
        return "UNKNOWN"


def build_report(tasks, today=None):
    lines = []
    for task in tasks:
        if task["status"] == "open":
            if task["due_date"] is not None:
                if is_overdue(task, today):
                    if task["priority"] == 1:
                        lines.append(f"!! {task['title']} (OVERDUE, HIGH)")
                    else:
                        lines.append(f"!  {task['title']} (OVERDUE)")
                else:
                    lines.append(f"   {task['title']} (due {task['due_date']})")
            else:
                lines.append(f"   {task['title']}")
        else:
            lines.append(f"x  {task['title']}")
    return "\n".join(lines)
