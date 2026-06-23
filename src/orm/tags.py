from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.orm.base import Base
from src.orm.milestone_tags import milestone_tags


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    milestones: Mapped[list["Milestone"]] = relationship(
        secondary=milestone_tags,
        back_populates="tags",
    )
