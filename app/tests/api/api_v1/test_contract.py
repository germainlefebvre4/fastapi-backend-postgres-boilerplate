from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_weekdays
from app.tests.utils.user import create_random_user
from app.tests.utils.contract import create_random_contract


def test_create_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/?user_id={user.id}",
        headers=superuser_token_headers,
        json=data)
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user"]["id"] == user.id
    assert isinstance(content["user"], dict)
    assert content["user"]["id"] == user.id
    assert content["user"]["firstname"] == user.firstname
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers
    )
    user_id = r.json()["id"]
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/?user_id={user_id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["user"]["id"] == user_id
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_create_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    user = create_random_user(db)
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.post(
        f"{settings.API_V1_STR}/contracts/?user_id={user.id}",
        headers=normal_user_token_headers, json=data,
    )
    assert response.status_code == 400


def test_read_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "id" in content["user"]
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_read_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers
    )
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "id" in content["user"]
    assert content["user"]["id"] == user_id
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_read_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.get(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400


def test_update_contract_by_admin(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=superuser_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers
    )
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["start"] == data["start"]
    assert content["end"] == data["end"]


def test_update_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    date_today = date.today()
    data = {
        "start": str(date_today),
        "end": str(date_today + relativedelta(months=+12, days=-1))
    }
    response = client.put(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
        json=data
    )
    assert response.status_code == 400


def test_delete_contract_by_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers
    )
    user_id = r.json()["id"]
    contract = create_random_contract(db, user_id=user_id)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["start"] == str(contract.start)
    assert content["end"] == str(contract.end)


def test_delete_contract_by_another_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    contract = create_random_contract(db)
    response = client.delete(
        f"{settings.API_V1_STR}/contracts/{contract.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
