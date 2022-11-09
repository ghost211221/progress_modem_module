from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Modems(Base):
    __tablename__ = 'modems'

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Наименование модема')
    links = relationship("At_gropus_modems_links")

class Groups(Base):
    __tablename__ = 'groups'

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Наименование группы')
    links = relationship("At_gropus_modems_links")

class At_commands(Base):
    __tablename__ = 'at_commands'

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(128), comment='Команда')
    links = relationship("At_gropus_modems_links")

class At_gropus_modems_links(Base):
    __tablename__ = "at_gropus_modems_links"

    modem_id = Column(ForeignKey("modems.id"), primary_key=True)
    group_id = Column(ForeignKey("groups.id"), primary_key=True)
    at_command_id = Column(ForeignKey("at_commands.id"), primary_key=True)

    modem = relationship("Modems", back_populates="modems")
    group = relationship("Groups", back_populates="groups")
    at_command = relationship("At_commands", back_populates="at_commands")


engine = create_engine("sqlite:///modems_commands.db")

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

Base.metadata.create_all(engine)
