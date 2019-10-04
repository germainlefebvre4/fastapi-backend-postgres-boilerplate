from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import random
import json

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.contract import ContractCreate
from app.tests.utils.utils import (
    random_int_range, random_float_range, random_lower_string,
    random_time_range, random_weekdays)

from app.tests.utils.user import create_random_user


def create_random_contract(
        db: Session,
        user_id: int = None,
        ) -> models.Contract:
    if not user_id:
        user = create_random_user(db)
        user_id = user.id
    
    today_date = date.today()
    first_day_previous_month_date = datetime.strptime(str(today_date)[:7]+"-01", "%Y-%m-%d").date() + relativedelta(months=-1)
    
    start = str(first_day_previous_month_date)
    end = str(first_day_previous_month_date + relativedelta(months=+12, days=-1))

    contract_in = ContractCreate(
        start=start, end=end)
    return crud.contract.create_with_owner(
        db=db, obj_in=contract_in, user_id=user_id)
