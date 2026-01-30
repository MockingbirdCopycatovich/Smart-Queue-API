import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

TEST_DB_URL = "sqlite+pysqlite:///:memory:"

@pytest.fixture
def session():
    engine = create_engine(TEST_DB_URL, echo=False, future=True)
    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    with TestingSessionLocal() as session:
        yield session
