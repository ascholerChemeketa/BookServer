# In this file we define our SQLAlchemy data models. These get translated into relational database tables.

# Because of the interface with the `databases package <https://www.encode.io/databases/>`_ we will use the `SQLAlchemy core API <https://docs.sqlalchemy.org/en/14/core/>`_

# Migrations
# ----------
# We use `Alembic <https://alembic.sqlalchemy.org/en/latest/>`_ for tracking database migration information.
# To create a new migration automatically after you have made changes to this file run
# `alembic revision --autogenerate -m "simple message"`
# this will generate a new file in `alembic/versions`
# To apply changes to the database run `alembic upgrade head`
# It is also possible

# Schema Definition
# =================
#
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    DateTime,
    MetaData,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


# this object is a container for the table objects and can be used by alembic to autogenerate
# the migration information.
metadata = MetaData()

# Useinfo
# -------
#
# This defines the useinfo table in the database.  This table logs nearly every click
# generated by a student.  It gets very large and needs a lot of indexes to keep Runestone
# from bogging down.
#
logitem = Table(
    "useinfo",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("timestamp", DateTime, unique=False, index=True),
    Column("sid", String, unique=False, index=True),
    Column("event", String, unique=False, index=True),
    Column("act", String, unique=False, index=False),
    Column(
        "div_id",
        String,
        unique=False,
        index=True,
    ),  # unique identifier for a component
    Column("course_id", String, unique=False, index=True),
    Column("chapter", String, unique=False, index=False),
    Column("sub_chapter", String, unique=False, index=False),
)

# Answer Tables
# -------------
#
# Each gradable Runestone component has its own answer table.  Most of them are identical.
# This table contains correctness information.
ANSWER_TABLE_NAMES = [
    "mchoice_answers",
    "clickablearea_answers",
    "codelens_answers",
    "dragndrop_answers",
    "fitb_answers",
    "lp_answers",
    "parsons_answers",
    "shortanswer_answers",
    "unittest_answers",
]

answer_columns = []

# This should make working with answer tables much easier across the board as we can now just access them by name instead of duplicating code for each case.
answer_tables = {}

for tbl in ANSWER_TABLE_NAMES:
    answer_tables[tbl] = Table(
        tbl,
        metadata,
        Column("id", Integer, primary_key=True, index=True, autoincrement=True),
        Column("timestamp", DateTime, unique=False, index=True),
        Column("sid", String, unique=False, index=True),
        Column(
            "div_id",
            String,
            unique=False,
            index=True,
        ),  # unique identifier for a component
        Column("course_name", String, index=True),
        Column("correct", Boolean),
        Column("answer", String),
    )

# The parsons_answers table is the only outlier in that it adds a source column to keep
# track of which blocks were not used in the answer.
answer_tables["parsons_answers"] = Table(
    "parsons_answers", metadata, Column("source", String), extend_existing=True
)

# Code
# ----
#
# The code table captures every run/change of the students code.  It is used to load
# the history slider of the activecode component.
#
code = Table(
    "code",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("timestamp", DateTime, unique=False, index=True),
    Column("sid", String, unique=False, index=True),
    Column(
        "acid",
        String,
        unique=False,
        index=True,
    ),  # unique identifier for a component
    Column("course_name", String, index=True),
    Column("course_id", Integer, index=False),
    Column("code", String, index=False),
    Column("language", String, index=False),
    Column("emessage", String, index=False),
    Column("comment", String, index=False),
)

# Courses
# -------
#
# Every Course in the runestone system must have an entry in this table
# the id column is really an artifact of the original web2py/pydal implementation of 
# Runestone.  The 'real' primary key of this table is the course_name
courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("course_name", String, index=False, nullable=False),
    Column("term_start_date", Date, index=False),
    Column("institution", String),
    Column("base_course", String, ForeignKey("courses.course_name"), nullable=False),
    Column("login_required", Boolean, default=False),
    Column("allow_pairs", Boolean),
    Column("student_price", Integer),
    Column("downloads_enabled", Boolean),
    Column("courselevel", String),
    UniqueConstraint("course_name", name="unique_course_name")
)
