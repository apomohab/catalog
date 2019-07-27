# start on 19-6-2019 2:PM

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Catalog(Base):

    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {


            'id': self.id,
            'name': self.name,

        }


class Items(Base):

    __tablename__ = 'menuitem'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    details = Column(String(250))
    category = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# serializable format

    @property
    def serialize(self):

        return {

            'title': self.title,
            'details': self.details,
            'id': self.id,
            'category': self.category,
        }


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
