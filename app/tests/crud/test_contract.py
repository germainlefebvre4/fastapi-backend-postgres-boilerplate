from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud
from app.schemas.contract import ContractCreate, ContractUpdate
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string, random_weekdays)

from app.tests.utils.user import create_random_user


def test_create_contract(db: Session) -> None:
    user = create_random_user(db)

    date_today = date.today()
    start_date = date_today
    start = str(start_date)
    end_date = date_today + relativedelta(months=+12, days=-1)
    end = str(end_date)
    created_on = datetime.now()

    contract_in = ContractCreate(
        user_id=user.id, start=start, end=end)
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user.id)

    assert contract.user_id == user.id
    assert contract.user.id == user.id
    assert contract.user.firstname == user.firstname
    assert contract.user.email == user.email
    assert contract.start == start_date
    assert contract.end == end_date
    assert isinstance(contract.created_on, datetime)
    assert contract.updated_on == None


def test_get_contract(db: Session) -> None:
    user = create_random_user(db)

    date_today = date.today()
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))

    contract_in = ContractCreate(
        user_id=user.id, start=start, end=end)
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user.id)
    stored_contract = crud.contract.get(db=db, id=contract.id)

    assert stored_contract
    assert contract.id == stored_contract.id
    assert contract.user_id == stored_contract.user_id
    assert contract.user.id == stored_contract.user.id
    assert contract.user.firstname == stored_contract.user.firstname
    assert contract.user.email == stored_contract.user.email
    assert contract.start == stored_contract.start
    assert contract.end == stored_contract.end
    assert isinstance(stored_contract.created_on, datetime)
    assert stored_contract.updated_on == None


def test_get_contract_by_user(db: Session) -> None:
    user = create_random_user(db)

    date_today = date.today()
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))

    contract_in = ContractCreate(
        user_id=user.id, start=start, end=end)
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user.id)
    stored_contracts = crud.contract.get_multi_by_user(db=db, user_id=contract.user_id)
    stored_contract = [x for x in stored_contracts if x.id == contract.id][0]
    assert isinstance(stored_contracts, list)
    assert stored_contract
    assert contract.id == stored_contract.id
    assert contract.user_id == stored_contract.user_id
    assert contract.user.id == stored_contract.user.id
    assert contract.user.firstname == stored_contract.user.firstname
    assert contract.user.email == stored_contract.user.email
    assert contract.start == stored_contract.start
    assert contract.end == stored_contract.end


def test_update_contract(db: Session) -> None:
    user = create_random_user(db)

    date_today = date.today()
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))
    created_on = datetime.now()
    updated_on = datetime.now()

    contract_in = ContractCreate(
        user_id=user.id, start=start, end=end)
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user.id)
    contract_update = ContractUpdate(
        start=start, end=end)
    contract2 = crud.contract.update(db=db, db_obj=contract, obj_in=contract_update)
    assert contract.id == contract2.id
    assert contract.user_id == contract2.user_id
    assert contract.user.id == contract2.user.id
    assert contract.user.firstname == contract2.user.firstname
    assert contract.user.email == contract2.user.email
    assert contract.start == contract2.start
    assert contract.end == contract2.end
    assert isinstance(contract2.created_on, datetime)
    assert isinstance(contract2.updated_on, datetime)


def test_delete_contract(db: Session) -> None:
    user = create_random_user(db)

    date_today = date.today()
    start = str(date_today)
    end = str(date_today + relativedelta(months=+12, days=-1))

    contract_in = ContractCreate(
        user_id=user.id, start=start, end=end)
    contract = crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user.id)
    contract2 = crud.contract.remove(db=db, id=contract.id)
    contract3 = crud.contract.get(db=db, id=contract.id)
    assert contract3 is None
    assert contract.id == contract.id
    assert contract2.user_id == contract.user_id
    assert contract2.user.id == contract.user.id
    assert contract2.user.firstname == contract.user.firstname
    assert contract2.user.email == contract.user.email
    assert contract2.start == contract.start
    assert contract2.end == contract.end
