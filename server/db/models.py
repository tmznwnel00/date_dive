from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, \
    DateTime, JSON, func, Text
from sqlalchemy.orm import relationship, object_session

from .base import Base



class SoftDeletable:
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        session = object_session(self)
        session.add(self)


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    nickname = Column(String(15), unique=True)
    gender = Column(Enum('male', 'female'))
    age = Column(Integer)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), onupdate=func.now())
    # relationships
    hashtags = relationship('Hashtag', secondary='user_hashtag')
    question_answers = relationship("UserQuestionAnswer")
    photos = relationship("UserPhoto")


class Hashtag(Base):
    __tablename__ = 'hashtag'

    hashtag_id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(50))  # sport/music/food/pet/etc.
    name = Column(String(100), nullable=False, unique=True)  # snowboard/rock/vegan/etc.


class UserHashtag(Base, SoftDeletable):
    __tablename__ = 'user_hashtag'

    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey('hashtag.hashtag_id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime)  # null if not deleted
    # relationships


class UserPhoto(Base, SoftDeletable):
    __tablename__ = "user_photo"

    user_photo_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    s3_path = Column(String(500), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime)  # null if not deleted


class MatchStatus(Base):
    __tablename__ = "match_status"

    match_id = Column(Integer, autoincrement=True, primary_key=True)
    swiper_id = Column(Integer, ForeignKey('user.user_id'))
    swiped_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(Enum('view', 'pass', 'wait', 'rejected', 'match', 'broken'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    options = Column(JSON)  # null for text type answer
    multi_allowed = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserQuestionAnswer(Base, SoftDeletable):
    __tablename__ = "user_question_answer"

    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('question.question_id'), primary_key=True)
    order_index = Column(Integer, nullable=False)
    answer = Column(Text)  # key of question.options or text type answer
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime)
    # relationship
    question = relationship("Question")