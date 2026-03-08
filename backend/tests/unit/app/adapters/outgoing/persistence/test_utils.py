"""Tests for the sqlite_retry_on_locked decorator in utils.py."""
import sqlite3
import pytest


def test_retry_succeeds_on_first_attempt():
    from app.adapters.outgoing.persistence.utils.utils import sqlite_retry_on_locked

    class FakeRepo:
        calls = 0

        @sqlite_retry_on_locked(max_retries=3, initial_delay=0.01, backoff=1)
        def do_work(self):
            self.calls += 1
            return "ok"

    repo = FakeRepo()
    result = repo.do_work()
    assert result == "ok"
    assert repo.calls == 1


def test_retry_raises_after_max_retries():
    from app.adapters.outgoing.persistence.utils.utils import sqlite_retry_on_locked

    class FakeRepo:
        db = type("FakeDB", (), {"rollback": lambda self: None})()
        calls = 0

        @sqlite_retry_on_locked(max_retries=2, initial_delay=0.001, backoff=1)
        def do_work(self):
            self.calls += 1
            raise sqlite3.OperationalError("persistence is locked")

    repo = FakeRepo()
    with pytest.raises(sqlite3.OperationalError, match="persistence is locked"):
        repo.do_work()
    assert repo.calls == 2


def test_retry_reraises_non_lock_error():
    from app.adapters.outgoing.persistence.utils.utils import sqlite_retry_on_locked

    class FakeRepo:
        db = type("FakeDB", (), {"rollback": lambda self: None})()

        @sqlite_retry_on_locked(max_retries=3, initial_delay=0.001, backoff=1)
        def do_work(self):
            raise sqlite3.OperationalError("no such table: assets")

    repo = FakeRepo()
    with pytest.raises(sqlite3.OperationalError, match="no such table"):
        repo.do_work()


def test_retry_succeeds_after_locked_then_ok():
    from app.adapters.outgoing.persistence.utils.utils import sqlite_retry_on_locked

    class FakeRepo:
        db = type("FakeDB", (), {"rollback": lambda self: None})()
        calls = 0

        @sqlite_retry_on_locked(max_retries=3, initial_delay=0.001, backoff=1)
        def do_work(self):
            self.calls += 1
            if self.calls < 2:
                raise sqlite3.OperationalError("persistence is locked")
            return "success"

    repo = FakeRepo()
    result = repo.do_work()
    assert result == "success"
    assert repo.calls == 2
