from sqlalchemy import Column, String, ForeignKey, DateTime
from src.entities.Base import Base
from src.utils.id_gen import generate_uuid


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_monitor_id = Column(
        String, ForeignKey("model_monitors.id", ondelete="CASCADE")
    )
    timestamp = Column(DateTime)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
