from sqlalchemy import (
    BOOLEAN,
    Column,
    INTEGER,
    TEXT,
    TIMESTAMP,
    VARCHAR,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class BaseModel(Base):
    """ ベースモデル
    """
    __abstract__ = True

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        'created_at',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )

    updated_at = Column(
        'updated_at',
        TIMESTAMP(timezone=True),
        onupdate=current_timestamp(),
        default=current_timestamp(),
        comment='最終更新日時',
    )

    @declared_attr
    def __mapper_args__(cls):
        """ デフォルトのオーダリングは主キーの昇順

        降順にしたい場合
        from sqlalchemy import desc
        # return {'order_by': desc('id')}
        """
        return {'order_by': 'id'}


class User(BaseModel):
    __tablename__ = 'users'

    username = Column(TEXT, unique=True, nullable=False)
    password = Column(VARCHAR(128), nullable=False)
    last_name = Column(VARCHAR(100), nullable=False)
    first_name = Column(VARCHAR(100), nullable=False)
    is_admin = Column(BOOLEAN, nullable=False, default=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
