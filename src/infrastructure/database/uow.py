from contextlib import contextmanager

from .base import SessionLocal
from .exceptions import UnitOfWorkError

class UnitOfWork:

    def __init__(self):
        self.session = SessionLocal()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()

@contextmanager
def unit_of_work():
    uow = UnitOfWork()
    try:
        yield uow
        uow.commit()
    except Exception:
        uow.rollback()
        raise UnitOfWorkError("Session error")
    finally:
        uow.close()