from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, BIGINT

from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship

from shorten_url.storages.mysql.vars import ENGINE, CHARSET, COLLATE
from shorten_url.storages.mysql.tables.base import BASE


class Url(BASE):

    __tablename__ = "url"

    __table_args__ = {"mysql_engine": ENGINE, "mysql_charset": CHARSET, "mysql_collate": COLLATE}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    user_url_maps = relationship(
        "UserUrlMap",
        cascade="all, delete-orphan",
        passive_deletes=True,
        back_populates="url",
        lazy="noload",
    )

    ori_url = Column(VARCHAR(256), nullable=False, index=True, unique=True)

    create_time = Column(DATETIME(), server_default=func.now(), nullable=False)

    def __init__(self, ori_url):
        self.ori_url = ori_url
