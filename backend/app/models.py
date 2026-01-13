# backend/app/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    Boolean,
    CheckConstraint,
    Table,
)
from sqlalchemy.orm import relationship
from .database import Base

# Связь многие-ко-многим: студенты ↔ группы
student_group_association = Table(
    "student_groups",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(
        String(20),
        CheckConstraint("role IN ('student', 'teacher', 'admin', 'dean')"),
        nullable=False,
    )

    # Связи
    groups = relationship(
        "Group",
        secondary=student_group_association,
        back_populates="students"
    )
    taught_subjects = relationship("Subject", back_populates="teacher")
    attendances = relationship("Attendance", back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    # Связи
    students = relationship(
        "User",
        secondary=student_group_association,
        back_populates="groups"
    )
    schedules = relationship("Schedule", back_populates="group")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связи
    teacher = relationship("User", back_populates="taught_subjects")
    schedules = relationship("Schedule", back_populates="subject")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)

    # Связи
    subject = relationship("Subject", back_populates="schedules")
    group = relationship("Group", back_populates="schedules")
    attendances = relationship("Attendance", back_populates="schedule_item")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(
        String(10),
        CheckConstraint("status IN ('present', 'absent', 'late')"),
        default="absent",
        nullable=False,
    )

    # Связи
    schedule_item = relationship("Schedule", back_populates="attendances")
    student = relationship("User", back_populates="attendances")

    # Уникальность: один студент — одна запись на одно занятие
    __table_args__ = (
        CheckConstraint("status IN ('present', 'absent', 'late')", name="valid_status"),
    )