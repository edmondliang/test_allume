import pytest
from allume import create_app
from allume.core.db import DBAPI


@pytest.fixture(scope='function')
def client():
    app = create_app('testing')
    with DBAPI() as db:
        db.query("truncate table orders")
        db.query("truncate table bookings")
        db.query("truncate table slots cascade")

    with app.app_context():
        yield app.test_client()


@pytest.fixture()
def get_db_result(sql):
    with DBAPI() as db:
        return db.query(sql)
