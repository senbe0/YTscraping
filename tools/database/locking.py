import sqlite3
import threading


class SQLiteLock:
    def __init__(self, *db_paths):
        self.locks = []
        for db_path in db_paths:
            self.locks.append(threading.Lock())
        self.conns = []
        for db_path in db_paths:
            self.conns.append(sqlite3.connect(db_path))

    def __enter__(self):
        for lock in self.locks:
            lock.acquire()
        return self.conns

    def __exit__(self, exc_type, exc_val, exc_tb):
        for conn in self.conns:
            conn.commit()
            conn.close()
        for lock in self.locks:
            lock.release()
