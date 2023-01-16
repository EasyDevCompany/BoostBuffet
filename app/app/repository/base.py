from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class RepositoryBase(Generic[ModelType, ]):
    def __init__(self, model: Type[ModelType], session) -> None:
        self._model = model
        self._session = session.session

    def create(
        self, obj_in, commit=False
    ) -> ModelType:
        obj_in_data = dict(obj_in)
        db_obj = self._model(**obj_in_data)
        self._session.add(db_obj)
        self._session.flush()
        if commit:
            self._session.commit()
        return db_obj

    def get(self, *args, **kwargs,) -> Optional[ModelType]:
        return self._session.query(self._model).filter(*args).filter_by(**kwargs).first()

    def list(self, *args, **kwargs):
        return self._session.query(self._model).filter(*args).filter_by(**kwargs).all()

    def update(
            self,
            *,
            db_obj: ModelType,
            obj_in
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        print(jsonable_encoder(db_obj))
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self._session.add(db_obj)
        self._session.flush()
        self._session.commit()
        return db_obj

    def delete(self, commit=False, *args, db_obj: Optional[ModelType], **kwargs,) -> ModelType:
        self._session.delete(db_obj)
        self._session.flush()
        if commit:
            self._session.commit()

