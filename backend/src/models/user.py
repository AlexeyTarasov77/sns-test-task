from models.base import DatabaseBaseModel, int_pk_type, created_at_type
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(DatabaseBaseModel):
    id: Mapped[int_pk_type]
    username: Mapped[str] = mapped_column(unique=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
    tg_account: Mapped["TelegramAccount | None"] = relationship(back_populates="user")
    created_at: Mapped[created_at_type]

    def __eq__(self, other):
        return (
            isinstance(other, User)
            and self.id == other.id
            and self.username == other.username
            and self.phone_number == other.phone_number
            and self.password_hash == other.password_hash
            and self.is_active == other.is_active
        )


class TelegramAccount(DatabaseBaseModel):
    id: Mapped[int_pk_type]
    api_id: Mapped[int]
    api_hash: Mapped[str]
    phone_number: Mapped[str]
    user: Mapped[User] = relationship(back_populates="tg_account")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True
    )
    created_at: Mapped[created_at_type]

    def __eq__(self, other):
        return (
            isinstance(other, TelegramAccount)
            and self.user_id == other.user_id
            and self.phone_number == other.phone_number
            and self.api_id == other.api_id
            and self.api_hash == other.api_hash
        )
