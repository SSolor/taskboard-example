import argparse
import os
import sys

from taskboard import db, service


def build_parser():
    parser = argparse.ArgumentParser(prog="taskboard")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    add.add_argument("--priority", type=int, default=2)
    add.add_argument("--due", default=None, help="YYYY-MM-DD")

    sub.add_parser("list", help="list tasks")

    done = sub.add_parser("done", help="mark a task done")
    done.add_argument("task_id", type=int)

    find = sub.add_parser("search", help="search tasks by title")
    find.add_argument("term")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    conn = db.get_connection()
    db.init_db(conn)

    try:
        if args.command == "add":
            task_id = service.add_task(conn, args.title, args.priority, args.due)
            print(f"Added task {task_id}")
        elif args.command == "list":
            print(service.build_report(service.list_tasks(conn)))
        elif args.command == "done":
            service.complete_task(conn, args.task_id)
            print("Done")
        elif args.command == "search":
            for row in service.search_tasks(conn, args.term):
                print(row["id"], row["title"])
    except:
        print("Something went wrong")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
