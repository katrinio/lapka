

from typing import TYPE_CHECKING, Sequence

from sqlalchemy import String, select
from sqlalchemy.future import select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.session import Session

from src.core.database import engine
from src.orm.base import Base
from src.orm.milestone_tags import milestone_tags

if TYPE_CHECKING:
    from src.orm.milestone import Milestone


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    milestones: Mapped[list["Milestone"]] = relationship(
        secondary=milestone_tags,
        back_populates="tags",
        lazy="selectin",
    )

    @classmethod
    def all(cls) -> Sequence["Tag"]:
        with Session(engine) as session:
            return session.execute(select(cls)).scalars().all()

    @classmethod
    def get_by_name(cls, name: str) -> "Tag | None":
        with Session(engine) as session:
            return session.execute(select(cls).where(cls.name == name)).scalars().first()
