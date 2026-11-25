from taskboard import db


def test_init_db_is_idempotent():
    conn = db.get_connection(":memory:")
    db.init_db(conn)
    db.init_db(conn)
    assert conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0
    conn.close()
