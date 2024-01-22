#NOTE: Drop the address & user_account tables before running this script
from sqlite3 import Date
from sqlalchemy import CHAR, Date
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:Flyerz123!@localhost/testDB2")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

class Center(Base):
    __tablename__ = "center" #NOTE LOWERCASE

    cenid: Mapped[str] = mapped_column(String(2), primary_key=True) #NOTE LOWERCASE cenid
    cenname: Mapped[str] = mapped_column(String)

    #relation to Student: AffiliatedS (M Student : 1 Center)
    students: Mapped[List["Student"]] = relationship(back_populates="center", cascade="all, delete-orphan") #List to class object, back_populates to relationship on other end
    #relation to Class: Hosts (M Class : 1 Center)
    classes: Mapped[List["Class"]] = relationship(back_populates="center", cascade="all, delete-orphan")
    #relation to PermStaff: AffiliatedP (M PermStaff : 1 Center)
    permstaff: Mapped[List["Class"]] = relationship(back_populates="center", cascade="all, delete-orphan")

    def __repr__(self) -> str: #represents the object as a string
        return f"Center(cenid={self.cenid!r}, cenname={self.cenname!r})"

class Student(Base):
    __tablename__ = "student"

    sid: Mapped[str] = mapped_column(String, primary_key=True)
    sfirst: Mapped[str] = mapped_column(String)
    slast: Mapped[str] = mapped_column(String)
    sphonenumber: Mapped[str] = mapped_column(String(12))
    sbday: Mapped[Date] = mapped_column(Date)
    slevel: Mapped[str] = mapped_column(String)
    sleadership: Mapped[str] = mapped_column(String, nullable=True)
    sparentalum: Mapped[str] = mapped_column(String, nullable=True)
    semergencyphone: Mapped[str] = mapped_column(String)
    cenid: Mapped[str] = mapped_column(String(2), ForeignKey("center.cenid"))

    #relation to Center: AffiliatedS (M Student : 1 Center)
    center: Mapped["Center"] = relationship(back_populates="student")
    #relation to Class: Takes (M : M)???
    takes: Mapped["Takes"] = relationship(back_populates="student")
    #relation to Event: Attends (M : M)???
    attends: Mapped["Attends"] = relationship(back_populates="student")

    def __repr__(self):
        return f"Student(sid={self.sid!r}, sfirst={self.sfirst!r}, slast={self.slast!r})"

class PermStaff(Base):
    __tablename__ = "permstaff"

    pid: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    pfirst: Mapped[str] = mapped_column(String, nullable=False)
    plast: Mapped[str] = mapped_column(String, nullable=False)
    pemail: Mapped[str] = mapped_column(String, nullable=False)
    pphonenumber: Mapped[str] = mapped_column(String(12))
    ptrainstatus: Mapped[str] = mapped_column(String, nullable=False)
    ptrainexp: Mapped[Date] = mapped_column(Date, nullable=True)
    cenid: Mapped[str] = mapped_column(String(2), ForeignKey('center.cenid'), nullable=False)

    #relation to Center: AffiliatedP
    center: Mapped["Center"] = relationship(back_populates="permstaff")
    #relation to Class: Teaches
    teaches: Mapped[List["Teaches"]] = relationship(back_populates="permstaff")
    #relation to Event: Runs
    runs: Mapped[List["Runs"]] = relationship(back_populates="permstaff")

    def __repr__(self) -> str: #represents the object as a string
        return f"PermStaff(pid={self.pid!r}, pfirst={self.pfirst!r}, plast={self.plast!r}, pemail={self.pemail!r}, pphonenumber={self.pphonenumber!r}, ptrainstatus={self.ptrainstatus!r}, ptrainexp={self.ptrainexp!r})"

class Class(Base):
    __tablename__ = 'class'

    cid: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    clevel: Mapped[str] = mapped_column(String(2), nullable=False)
    cdate: Mapped[Date] = mapped_column(Date, nullable=False)
    ctopic: Mapped[str] = mapped_column(String, nullable=False)
    cenid: Mapped[str] = mapped_column(String(2), ForeignKey('center.cenid'), nullable=False)

    center: Mapped["Center"] = relationship(back_populates='class')
    takes: Mapped["Takes"] = relationship(back_populates="class")
    teaches: Mapped["Teaches"] = relationship(back_populates="class")
    
    def __repr__(self) -> str:
        return f"class(cid={self.cid!r}, clevel={self.clevel!r}, cdate={self.cdate!r}, ctopic={self.ctopic!r}, cenid={self.cenid!r})"

class Volunteer(Base):
    __tablename__ = 'volunteer'

    vid: Mapped[str] = mapped_column(String, primary_key=True)
    vfirst: Mapped[str] = mapped_column(String, nullable=False)
    vlast: Mapped[str] = mapped_column(String, nullable=False)
    vphonenumber: Mapped[str] = mapped_column(String(12), nullable=False)
    vemail: Mapped[str] = mapped_column(String, nullable=False)
    vtrainstatus: Mapped[Optional[str]] = mapped_column(String)
    vtrainexp: Mapped[Optional[Date]] = mapped_column(Date)

    helps: Mapped["Helps"] = relationship(back_populates="volunteer")

    def __repr__(self) -> str:
        return (
            f"volunteer(vID={self.vid!r}, vfirst={self.vfirst!r}, vlast={self.vlast!r}, "
            f"vphonenumber={self.vphonenumber!r}, vemail={self.vemail!r}, "
            f"vtrainstatus={self.vtrainstatus!r}, vtrainExp={self.vtrainexp!r})"
        )
    
class Event(Base):
    __tablename__ = 'event'

    eid: Mapped[str] = mapped_column(String, primary_key=True)
    elocation: Mapped[str] = mapped_column(String, nullable=False)
    ename: Mapped[str] = mapped_column(String, nullable=False)
    edate: Mapped[Date] = mapped_column(Date, nullable=False)
    eaudience: Mapped[CHAR] = mapped_column(CHAR(2), nullable=False)
    ecategory: Mapped[str] = mapped_column(String, nullable=False)

    # relationship to volunteer, permstaff, and students
    # attends, runs, helps?
   
    attends: Mapped[List["Attends"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    runs: Mapped[List["Runs"]] = relationship(back_populates="permstaff", cascade="all, delete-orphan")
    helps: Mapped[List["Helps"]] = relationship(back_populates="volunteer", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"event(eid={self.eid!r}, elocation={self.elocation!r}, ename={self.ename!r}, "
            f"edate={self.edate!r}, eaudience={self.eaudience!r}, ecategory={self.ecategory!r})"
        )
    
class Takes(Base):
    __tablename__ = 'takes'

    cid: Mapped[str] = mapped_column(String, ForeignKey('class.cid'), primary_key=True)
    sid: Mapped[str] = mapped_column(String, ForeignKey('student.sid'), primary_key=True)

    #many to many
    student: Mapped["Student"] = relationship(back_populates='class')
    class_: Mapped["Class"] = relationship(back_populates='student')

    def __repr__(self) -> str:
        return f"takes(cid={self.cid!r}, sid={self.sid!r})"
    
class Teaches(Base):
    __tablename__ = 'teaches'

    cid: Mapped[str] = mapped_column(String, ForeignKey('class.cid'), primary_key=True)
    pid: Mapped[str] = mapped_column(String, ForeignKey('permstaff.pid'), primary_key=True)

    # many to many
    permstaff: Mapped["PermStaff"] = relationship(back_populates='class')
    class_: Mapped["Class"] = relationship(back_populates='permstaff')

    def __repr__(self) -> str:
        return f"teaches(cid={self.cid!r}, pid={self.pid!r})"
    
class Runs(Base):
    __tablename__ = 'runs'

    pid: Mapped[str] = mapped_column(String, ForeignKey('permstaff.pid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)

    #many to many
    permstaff: Mapped["PermStaff"] = relationship(back_populates='event')
    event: Mapped["Event"] = relationship(back_populates='permstaff')

    def __repr__(self) -> str:
        return f"runs(pid={self.pid!r}, eid={self.eid!r})"

class Attends(Base):
    __tablename__ = 'attends'

    sid: Mapped[str] = mapped_column(String, ForeignKey('student.sid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)

    # many to many
    student: Mapped["Student"] = relationship(back_populates='event')
    event: Mapped["Event"] = relationship(back_populates='student')

    def __repr__(self) -> str:
        return f"attends(sid={self.sid!r}, eid={self.eid!r})"

class Helps(Base):
    __tablename__ = 'helps'

    vid: Mapped[str] = mapped_column(String, ForeignKey('volunteer.vid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)
    
    # many to many
    volunteer: Mapped["Volunteer"] = relationship(back_populates='event')
    event: Mapped["Event"] = relationship(back_populates='volunteer')

    def __repr__(self) -> str:
        return f"helps(vid={self.vid!r}, eid={self.eid!r})"
    
Base.metadata.create_all(engine)

with Session(engine) as session:

    session.commit()

''' from sqlalchemy import create_engine
from sqlalchemy.orm import Session

session = Session(bind=engine)

def get_students_from_center(session, center_id):
    # Assuming 'center_id' is the ID of the specific center you are interested in

    # Query to retrieve students from a specific center
    students_from_center = (
        session.query(Student)
        .join(Center)
        .filter(Center.cenid == center_id)
        .all()
    )

    return students_from_center

# Example usage:
# Assuming you have a SQLAlchemy session object named 'session'
center_id_to_query = "EL"  # Replace with the actual center ID
result = get_students_from_center(session, center_id_to_query)

# Print the results
for student in result:
    print("Student in EL", student) '''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Assuming you already have a SQLAlchemy session object named 'session'
center_id_to_query = "EL"  # Replace with the actual center ID you are interested in

# Query to retrieve students from a specific center
students_from_center = (
    session.query(Student)
    .join(Center)  # Join with the Center table
    .filter(Center.cenid == center_id_to_query)  # Filter by the specific center ID
    .all()
)

# Print the results
for student in students_from_center:
    print("Student in", center_id_to_query, ":", student)
