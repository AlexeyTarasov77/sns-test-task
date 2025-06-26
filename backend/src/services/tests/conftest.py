from faker import Faker
import pytest


@pytest.fixture
def fake():
    print("\nCREATING FAKER INSTANCE\n")
    return Faker()
