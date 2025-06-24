from models.base import DatabaseBaseModel, int_pk_type


class User(DatabaseBaseModel):
    id: Mapped[int_pk_type]
