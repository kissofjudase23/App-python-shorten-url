from sqlalchemy import Column
from sqlalchemy.dialects.mysql import (BIGINT,
                                       DATETIME)
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from shorten_url.storages.mysql.vars import ENGINE, CHARSET, COLLATE
from shorten_url.storages.mysql.tables.base import BASE


class UserUrlMap(BASE):

    __tablename__ = 'user_url_map'

    # composite primary key
    user_id = Column(BIGINT(unsigned=True),
                 ForeignKey('user.id', ondelete="CASCADE"),
                 primary_key=True)

    url_id = Column(BIGINT(unsigned=True),
                    ForeignKey('url.id', ondelete="CASCADE"),
                    primary_key=True)

    user = relationship('User', back_populates='user_url_maps')
    url = relationship('Url', back_populates='user_url_maps')

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    # composite foreign keys
    __table_args__ = (
        UniqueConstraint(user_id, url_id),
        {'mysql_engine': ENGINE,
         'mysql_charset': CHARSET,
         'mysql_collate': COLLATE}
    )

    def __init__(self, user_id, url_id):
        self.user_id = user_id
        self.url_id = url_id
