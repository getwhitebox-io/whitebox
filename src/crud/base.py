from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.db import Base
from sqlalchemy.orm import defer
import datetime

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, _id: str) -> Optional[ModelType]:
        if self.model.__tablename__ in ["users"]:
            return (
                db.query(self.model)
                .options(defer("password"))
                .filter(self.model.id == _id)
                .first()
            )
        else:
            return db.query(self.model).filter(self.model.id == _id).first()

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        date_now = datetime.datetime.utcnow()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_at=date_now, updated_at=date_now)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        date_now = datetime.datetime.utcnow()
        obj_data = jsonable_encoder(db_obj)
        #### Fix me
        obj_in2 = jsonable_encoder(obj_in)
        obj_in2 = {**obj_in2, "updated_at": date_now}
        if isinstance(obj_in2, dict):
            update_data = obj_in2
        else:
            update_data = obj_in2.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        #######
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, _id: str):
        db.query(self.model).filter(self.model.id == _id).delete()
        db.commit()
        return
