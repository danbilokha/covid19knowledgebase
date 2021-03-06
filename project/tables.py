from datetime import datetime

from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class KnowledgeSchema(Base):
    __tablename__ = 'knowledge'
    id = Column(Integer, primary_key=True)
    question = Column(String(2056), nullable=False)
    category = Column(String(512), nullable=False)
    answer = Column(TEXT, nullable=True)
    links = Column(TEXT, nullable=True)
    countries = Column(TEXT, nullable=True)
    additional_answers = Column(TEXT, nullable=True)
    additional_links = Column(TEXT, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self,
                 question=None,
                 category=None,
                 answer=None,
                 links=None,
                 countries=None,
                 additional_answers=None,
                 additional_links=None):
        self.question = question
        self.category = category
        self.answer = answer
        self.links = links
        self.countries = countries
        self.additional_answers = additional_answers
        self.additional_links = additional_links

    def __repr__(self):
        return self.id


@dataclass
class LogsSchema(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    type = Column(String(2056), nullable=False)
    message = Column(TEXT, nullable=False)
    info = Column(TEXT, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def __init__(self,
                 type=None,
                 message=None,
                 info=None):
        self.type = type
        self.message = message
        self.info = info

    def __repr__(self):
        return self.id


@dataclass
class UnansweredQuestions(Base):
    __tablename__ = 'unanswered'
    id = Column(Integer, primary_key=True)
    question = Column(TEXT, nullable=False)
    asked = Column(Integer, nullable=False)

    def __init__(self,
                 question=None,
                 asked=1):
        self.question = question
        self.asked = asked

    def __repr__(self):
        return self.id
