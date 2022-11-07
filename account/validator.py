from typing import Optional

from sqlalchemy.orm import Session

from . models import Account


async def verify_email_exist(email: str, db_session: Session) -> Optional[Account]:
    return db_session.query(Account).filter(Account.email == email).first()
