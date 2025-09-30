from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    users: Mapped[List["User"]] = relationship(
        secondary="follower", back_populates="users")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "is_active": self.is_active
        }


follower = Table(
    "follower",
    db.metadata,
    Column("id", db.Integer, primary_key=True),
    Column("user_from_id", db.Integer, ForeignKey("user.id"), nullable=False),
    Column("user_to_id", db.Integer, ForeignKey("user.id"), nullable=False))


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Media(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    type: Mapped[str] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("post.id"), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }
