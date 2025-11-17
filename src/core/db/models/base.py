from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        if cls.__tablename__[-1] == "y":
            return f"{cls.__tablename__[:-1]}ies"
        else:
            return f"{cls.__name__.lower()}s"
