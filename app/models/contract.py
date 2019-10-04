from sqlalchemy import Column, ForeignKey, Integer, Float, Date, DateTime, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(Date)
    end = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete='CASCADE'),
        nullable=False)

    user = relationship("User", foreign_keys=[user_id])
