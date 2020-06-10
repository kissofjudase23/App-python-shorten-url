from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (VARCHAR,
                                       DATETIME,
                                       BIGINT)
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship

from shorten_url.storages.mysql.vars import ENGINE, CHARSET, COLLATE
from shorten_url.storages.mysql.tables.base import BASE


class User(BASE):

    __tablename__ = 'user'

    __table_args__ = {'mysql_engine': ENGINE,
                      'mysql_charset': CHARSET,
                      'mysql_collate': COLLATE}

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    user_url_maps = relationship('UserUrlMap',
                                 cascade='all, delete-orphan',
                                 passive_deletes=True,
                                 back_populates='user')

    email = Column(VARCHAR(256), nullable=False, index=True, unique=True)
    name = Column(VARCHAR(128), nullable=False)

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email