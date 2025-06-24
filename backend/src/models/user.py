from models.base import DatabaseBaseModel, int_pk_type
from sqlalchemy.orm import Mapped, mapped_column


class User(DatabaseBaseModel):
    id: Mapped[int_pk_type]
    username: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
