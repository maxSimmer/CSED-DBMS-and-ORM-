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
    permstaffs: Mapped[List["PermStaff"]] = relationship(back_populates="center", cascade="all, delete-orphan")

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
    center: Mapped["Center"] = relationship(back_populates="students")
    #relation to Class: Takes (M : M)
    classes: Mapped[List["Takes"]] = relationship(back_populates="student") #<--Note the List!
    #relation to Event: Attends (M : M)
    events: Mapped[List["Attends"]] = relationship(back_populates="student")

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

    #relation to Center: AffiliatedP (M PermStaff: 1 Center
    center: Mapped["Center"] = relationship(back_populates="permstaffs")
    #relation to Class: Teaches (M : M)
    classes: Mapped[List["Teaches"]] = relationship(back_populates="permstaff")
    #relation to Event: Runs (M : M)
    events: Mapped[List["Runs"]] = relationship(back_populates="permstaff")

    def __repr__(self) -> str: #represents the object as a string
        return f"PermStaff(pid={self.pid!r}, pfirst={self.pfirst!r}, plast={self.plast!r}, pemail={self.pemail!r}, pphonenumber={self.pphonenumber!r}, ptrainstatus={self.ptrainstatus!r}, ptrainexp={self.ptrainexp!r})"

class Class(Base):
    __tablename__ = 'class'

    cid: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    clevel: Mapped[str] = mapped_column(String(2), nullable=False)
    cdate: Mapped[Date] = mapped_column(Date, nullable=False)
    ctopic: Mapped[str] = mapped_column(String, nullable=False)
    cenid: Mapped[str] = mapped_column(String(2), ForeignKey('center.cenid'), nullable=False)

    #relation to Center: Hosts (m Class : 1 Center)
    center: Mapped["Center"] = relationship(back_populates='classes')
    #relation to Student: Takes (M:M)
    students: Mapped[List["Takes"]] = relationship(back_populates="class_")
    #relation to PermStaff: Teaches (M:M)
    permstaffs: Mapped[List["Teaches"]] = relationship(back_populates="class_")
    
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

    #relation to Events: Helps (M:M)
    events: Mapped[List["Helps"]] = relationship(back_populates="volunteer")

    def __repr__(self) -> str:
        return (
            f"volunteer(vid={self.vid!r}, vfirst={self.vfirst!r}, vlast={self.vlast!r}, "
            f"vphonenumber={self.vphonenumber!r}, vemail={self.vemail!r}, "
            f"vtrainstatus={self.vtrainstatus!r}, vtrainexp={self.vtrainexp!r})"
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
   
    students: Mapped[List["Attends"]] = relationship(back_populates="event")
    permstaffs: Mapped[List["Runs"]] = relationship(back_populates="event")
    volunteers: Mapped[List["Helps"]] = relationship(back_populates="event")

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
    #relation to Student: Takes (M:M)
    student: Mapped["Student"] = relationship(back_populates='classes')
    ##relation to Class: Takes (M : M)
    class_: Mapped["Class"] = relationship(back_populates='students')

    def __repr__(self) -> str:
        return f"takes(cid={self.cid!r}, sid={self.sid!r})"
    
class Teaches(Base):
    __tablename__ = 'teaches'

    cid: Mapped[str] = mapped_column(String, ForeignKey('class.cid'), primary_key=True)
    pid: Mapped[str] = mapped_column(String, ForeignKey('permstaff.pid'), primary_key=True)

    # many to many
    permstaff: Mapped["PermStaff"] = relationship(back_populates='classes')
    class_: Mapped["Class"] = relationship(back_populates='permstaffs')

    def __repr__(self) -> str:
        return f"teaches(cid={self.cid!r}, pid={self.pid!r})"
    
class Runs(Base):
    __tablename__ = 'runs'

    pid: Mapped[str] = mapped_column(String, ForeignKey('permstaff.pid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)

    #many to many
    permstaff: Mapped["PermStaff"] = relationship(back_populates='events')
    event: Mapped["Event"] = relationship(back_populates='permstaffs')

    def __repr__(self) -> str:
        return f"runs(pid={self.pid!r}, eid={self.eid!r})"

class Attends(Base):
    __tablename__ = 'attends'

    sid: Mapped[str] = mapped_column(String, ForeignKey('student.sid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)

    # many to many
    student: Mapped["Student"] = relationship(back_populates='events')
    event: Mapped["Event"] = relationship(back_populates='students')

    def __repr__(self) -> str:
        return f"attends(sid={self.sid!r}, eid={self.eid!r})"

class Helps(Base):
    __tablename__ = 'helps'

    vid: Mapped[str] = mapped_column(String, ForeignKey('volunteer.vid'), primary_key=True)
    eid: Mapped[str] = mapped_column(String, ForeignKey('event.eid'), primary_key=True)
    
     # many to many
    volunteer: Mapped["Volunteer"] = relationship(back_populates='events')
    event: Mapped["Event"] = relationship(back_populates='volunteers')

    def __repr__(self) -> str:
        return f"helps(vid={self.vid!r}, eid={self.eid!r})"
    
Base.metadata.create_all(engine)

# Create a session
session = Session(engine)

#Insert Data
with Session(engine) as session:
     
    sample_centers = [
        Center(cenid='EL', cenname='Elms'),
        Center(cenid='FG', cenname='Forest Glen'),
        Center(cenid='GR', cenname='Grove'),
        Center(cenid='LD', cenname='Lindell'),
        Center(cenid='PW', cenname='Petawa'),
        Center(cenid='SB', cenname='Shellbourne'),
        Center(cenid='SL', cenname='Sherlake'),
        Center(cenid='SH', cenname='Southold'),
    ]

    # Student
    sample_students = [
        Student(sid='LeKoch', sfirst='Leah', slast='Koch', sphonenumber='331-336-8319', sbday='01/05/05', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='738-495-2160', cenid='EL'),
        Student(sid='SaJohnson', sfirst='Sarah', slast='Johnson', sphonenumber='847-874-3158', sbday='03/26/01', slevel='co', sleadership=None, sparentalum=None, semergencyphone='624-809-7315', cenid='EL'),
        Student(sid='RyWilliams', sfirst='Ryan', slast='Williams', sphonenumber='331-924-7168', sbday='09/15/01', slevel='co', sleadership=None, sparentalum='yes', semergencyphone='583-672-9140', cenid='EL'),
        Student(sid='EmDavis', sfirst='Emily', slast='Davis', sphonenumber='312-565-0293', sbday='06/02/02', slevel='co', sleadership='yes', sparentalum='yes', semergencyphone='459-218-6370', cenid='EL'),
        Student(sid='DaMartinez', sfirst='Daniel', slast='Martinez', sphonenumber='618-947-1162', sbday='07/14/03', slevel='co', sleadership=None, sparentalum=None, semergencyphone='726-493-5180', cenid='EL'),
        Student(sid='OlSmith', sfirst='Olivia', slast='Smith', sphonenumber='708-479-2157', sbday='12/13/01', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='362-840-1597', cenid='EL'),
        Student(sid='MaTaylor', sfirst='Matthew', slast='Taylor', sphonenumber='773-466-6844', sbday='08/24/01', slevel='co', sleadership='yes', sparentalum='yes', semergencyphone='950-286-4713', cenid='EL'),
        Student(sid='AvBrown', sfirst='Ava', slast='Brown', sphonenumber='847-647-9798', sbday='10/05/04', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='817-496-3250', cenid='EL'),
        Student(sid='AlLee', sfirst='Alexander', slast='Lee', sphonenumber='331-805-3950', sbday='11/29/02', slevel='co', sleadership=None, sparentalum=None, semergencyphone='204-736-9815', cenid='EL'),
        Student(sid='ChAnderson', sfirst='Chloe', slast='Anderson', sphonenumber='312-384-6007', sbday='01/12/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='675-892-3140', cenid='GR'),
        Student(sid='BeWilson', sfirst='Ben', slast='Wilson', sphonenumber='847-256-5819', sbday='02/05/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='384-762-9150', cenid='GR'),
        Student(sid='MiClark', sfirst='Mia', slast='Clark', sphonenumber='618-184-7893', sbday='03/20/05', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='123-450-8976', cenid='GR'),
        Student(sid='SaWhite', sfirst='Samuel', slast='White', sphonenumber='331-798-6579', sbday='04/08/05', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='892-731-6450', cenid='GR'),
        Student(sid='ChHall', sfirst='Charlotte', slast='Hall', sphonenumber='618-670-1205', sbday='05/16/06', slevel='hs', sleadership=None, sparentalum='yes', semergencyphone='657-234-1890', cenid='GR'),
        Student(sid='AmRodriguez', sfirst='Amelia', slast='Rodriguez', sphonenumber='224-889-4751', sbday='06/25/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='941-582-7306', cenid='GR'),
        Student(sid='HeAdams', sfirst='Henry', slast='Adams', sphonenumber='312-431-9277', sbday='07/09/05', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='392-687-4150', cenid='GR'),
        Student(sid='NoMitchell', sfirst='Noah', slast='Mitchell', sphonenumber='630-675-4148', sbday='08/14/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='546-123-7890', cenid='GR'),
        Student(sid='LiGreen', sfirst='Lily', slast='Green', sphonenumber='630-675-4148', sbday='09/02/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='289-456-1073', cenid='GR'),
        Student(sid='JaMoore', sfirst='James', slast='Moore', sphonenumber='773-971-9466', sbday='10/18/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='810-946-2357', cenid='GR'),
        Student(sid='SoParker', sfirst='Sofia', slast='Parker', sphonenumber='224-416-4139', sbday='11/27/05', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='631-487-5290', cenid='GR'),
        Student(sid='LiWilson', sfirst='Liam', slast='Wilson', sphonenumber='847-795-4328', sbday='08/15/09', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='407-895-3621', cenid='GR'),
        Student(sid='WiHarris', sfirst='William', slast='Harris', sphonenumber='708-778-0943', sbday='11/03/09', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='263-750-8149', cenid='GR'),
        Student(sid='IsRodriguez', sfirst='Isabella', slast='Rodriguez', sphonenumber='618-215-1850', sbday='03/22/10', slevel='ms', sleadership='yes', sparentalum='yes', semergencyphone='859-234-1760', cenid='GR'),
        Student(sid='JaThomas', sfirst='Jackson', slast='Thomas', sphonenumber='630-914-3122', sbday='07/09/11', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='512-406-7983', cenid='GR'),
        Student(sid='MiSmith', sfirst='Michael', slast='Smith', sphonenumber='312-385-6097', sbday='10/12/10', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='746-931-5208', cenid='GR'),
        Student(sid='OlBrown', sfirst='Olivia', slast='Brown', sphonenumber='485-726-9134', sbday='01/05/09', slevel='ms', sleadership=None, sparentalum='yes', semergencyphone='372-916-5840', cenid='GR'),
        Student(sid='WiTaylor', sfirst='William', slast='Taylor', sphonenumber='629-384-7150', sbday='05/18/10', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='981-734-6025', cenid='GR'),
        Student(sid='AvAnderson', sfirst='Ava', slast='Anderson', sphonenumber='314-902-8765', sbday='09/30/10', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='451-820-3796', cenid='GR'),
        Student(sid='BeLee', sfirst='Benjamin', slast='Lee', sphonenumber='572-913-4680', sbday='12/08/09', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='617-482-3905', cenid='GR'),
        Student(sid='ZoCooper', sfirst='Zoe', slast='Cooper', sphonenumber='718-649-2053', sbday='06/08/08', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='586-042-3179', cenid='PW'),
        Student(sid='LoWard', sfirst='Logan', slast='Ward', sphonenumber='109-785-4326', sbday='08/24/05', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='295-607-3841', cenid='PW'),
        Student(sid='ViMurphy', sfirst='Victoria', slast='Murphy', sphonenumber='587-364-1029', sbday='03/17/08', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='730-149-8256', cenid='PW'),
        Student(sid='JaStewart', sfirst='Jackson', slast='Stewart', sphonenumber='236-458-9701', sbday='10/29/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='165-429-7380', cenid='PW'),
        Student(sid='EmRivera', sfirst='Emma', slast='Rivera', sphonenumber='890-612-3475', sbday='01/14/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='493-176-2805', cenid='PW'),
        Student(sid='DaCarter', sfirst='Daniel', slast='Carter', sphonenumber='456-210-7893', sbday='07/05/07', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='714-085-2369', cenid='PW'),
        Student(sid='AdReed', sfirst='Addison', slast='Reed', sphonenumber='721-098-4365', sbday='12/25/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='369-814-5270', cenid='PW'),
        Student(sid='AnRoss', sfirst='Andrew', slast='Ross', sphonenumber='304-917-5826', sbday='05/02/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='872-301-4965', cenid='PW'),
        Student(sid='ElYoung', sfirst='Ella', slast='Young', sphonenumber='638-574-2901', sbday='02/09/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='504-972-6183', cenid='PW'),
        Student(sid='CaMitchell', sfirst='Caleb', slast='Mitchell', sphonenumber='549-302-6871', sbday='11/12/07', slevel='hs', sleadership=None, sparentalum='yes', semergencyphone='610-934-8275', cenid='PW'),
        Student(sid='LiWood', sfirst='Lily', slast='Wood', sphonenumber='765-219-8340', sbday='09/22/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='283-650-1794', cenid='PW'),
        Student(sid='LiScott', sfirst='Liam', slast='Scott', sphonenumber='823-705-6491', sbday='04/18/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='971-245-8063', cenid='PW'),
        Student(sid='AbMorris', sfirst='Abigail', slast='Morris', sphonenumber='193-284-5067', sbday='06/29/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='376-289-5401', cenid='SB'),
        Student(sid='ZaParker', sfirst='Zach', slast='Parker', sphonenumber='408-576-3921', sbday='08/14/07', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='219-674-8503', cenid='SB'),
        Student(sid='ErHayes', sfirst='Ericka', slast='Hayes', sphonenumber='796-125-8340', sbday='03/07/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='465-312-7890', cenid='SB'),
        Student(sid='EmSullivan', sfirst='Emily', slast='Sullivan', sphonenumber='678-149-2053', sbday='10/08/05', slevel='hs', sleadership='yes', sparentalum='yes', semergencyphone='850-129-3467', cenid='SB'),
        Student(sid='SoThompson', sfirst='Sophia', slast='Thompson', sphonenumber='295-748-6130', sbday='01/21/09', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='792-438-5016', cenid='SB'),
        Student(sid='JaMorris', sfirst='Jackson', slast='Morris', sphonenumber='437-289-6105', sbday='07/19/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='136-724-5980', cenid='SB'),
        Student(sid='MiStewart', sfirst='Mia', slast='Stewart', sphonenumber='180-725-9364', sbday='12/11/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='408-917-6253', cenid='SB'),
        Student(sid='MaHernandez', sfirst='Marie', slast='Hernandez', sphonenumber='610-245-7983', sbday='05/26/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='567-812-4309', cenid='SB'),
        Student(sid='OwCarter', sfirst='Owen', slast='Carter', sphonenumber='954-682-3017', sbday='02/15/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='305-246-9817', cenid='SB'),
        Student(sid='JoPeterson', sfirst='Joseph', slast='Peterson', sphonenumber='276-804-9135', sbday='11/10/09', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='924-871-3560', cenid='SB'),
        Student(sid='NiJohnson', sfirst='Nicholas', slast='Johnson', sphonenumber='542-970-1863', sbday='09/05/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='738-019-4652', cenid='SB'),
        Student(sid='LuWilson', sfirst='Luke', slast='Wilson', sphonenumber='832-167-4950', sbday='04/10/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='632-184-7905', cenid='SB'),
        Student(sid='BrMitchell', sfirst='Brayden', slast='Mitchell', sphonenumber='691-237-8045', sbday='02/14/09', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='514-627-8309', cenid='SL'),
        Student(sid='NoClark', sfirst='Nora', slast='Clark', sphonenumber='174-609-2385', sbday='06/04/10', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='697-230-4851', cenid='SL'),
        Student(sid='JaLee', sfirst='Jaxon', slast='Lee', sphonenumber='365-892-4701', sbday='08/27/09', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='890-245-3617', cenid='SL'),
        Student(sid='LiNyugen', sfirst='Lisa', slast='Nyugen', sphonenumber='972-830-1456', sbday='11/11/10', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='345-769-1820', cenid='SL'),
        Student(sid='DaMontgomery', sfirst='David', slast='Montgomery', sphonenumber='536-478-9120', sbday='04/07/09', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='271-398-4605', cenid='SL'),
        Student(sid='StHoffman', sfirst='Stephanie', slast='Hoffman', sphonenumber='890-372-5146', sbday='07/20/11', slevel='ms', sleadership=None, sparentalum='yes', semergencyphone='506-738-1294', cenid='SL'),
        Student(sid='StGuzman', sfirst='Steven', slast='Guzman', sphonenumber='140-785-9623', sbday='09/02/09', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='928-453-1760', cenid='SL'),
        Student(sid='BrRodgers', sfirst='Brett', slast='Rodgers', sphonenumber='862-195-3470', sbday='12/31/10', slevel='ms', sleadership='yes', sparentalum=None, semergencyphone='763-491-8250', cenid='SL'),
        Student(sid='LoShaw', sfirst='Lorena', slast='Shaw', sphonenumber='429-083-6715', sbday='03/01/09', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='123-590-4678', cenid='SL'),
        Student(sid='SaGardner', sfirst='Sara', slast='Gardner', sphonenumber='713-690-2458', sbday='05/12/10', slevel='ms', sleadership=None, sparentalum=None, semergencyphone='419-587-2360', cenid='SL'),
        Student(sid='LoCunningham', sfirst='Louise', slast='Cunningham', sphonenumber='807-912-3465', sbday='06/27/06', slevel='hs', sleadership=None, sparentalum='yes', semergencyphone='874-062-9315', cenid='SL'),
        Student(sid='AnEllis', sfirst='Andrew', slast='Ellis', sphonenumber='346-981-2570', sbday='08/09/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='965-432-0781', cenid='SL'),
        Student(sid='ClHammond', sfirst='Clara', slast='Hammond', sphonenumber='215-876-3490', sbday='03/27/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='346-281-0975', cenid='SL'),
        Student(sid='TaOsborne', sfirst='Tanya', slast='Osborne', sphonenumber='574-308-1629', sbday='10/04/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='283-961-4750', cenid='SL'),
        Student(sid='JoHopkins', sfirst='Joey', slast='Hopkins', sphonenumber='968-145-7320', sbday='01/30/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='507-984-2163', cenid='SL'),
        Student(sid='EmSchneider', sfirst='Emma', slast='Schneider', sphonenumber='341-205-7968', sbday='07/08/08', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='619-827-5304', cenid='SL'),
        Student(sid='ArJensen', sfirst='Arthur', slast='Jensen', sphonenumber='528-467-9130', sbday='12/15/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='652-140-3897', cenid='SL'),
        Student(sid='CaFlores', sfirst='Carroll', slast='Flores', sphonenumber='629-781-0435', sbday='05/15/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='430-789-2165', cenid='SL'),
        Student(sid='CeCollier', sfirst='Cecil', slast='Collier', sphonenumber='195-634-8720', sbday='02/23/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='728-391-0546', cenid='SL'),
        Student(sid='LeMorris', sfirst='Leslie', slast='Morris', sphonenumber='478-921-6053', sbday='11/21/06', slevel='hs', sleadership='yes', sparentalum=None, semergencyphone='296-741-5380', cenid='SL'),
        Student(sid='JoJohnson', sfirst='John', slast='Johnson', sphonenumber='573-629-1480', sbday='09/13/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='981-276-4305', cenid='SL'),
        Student(sid='PaWhite', sfirst='Paul', slast='White', sphonenumber='204-789-6135', sbday='04/25/05', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='543-219-6780', cenid='SL'),
        Student(sid='LeYates', sfirst='Lela', slast='Yates', sphonenumber='436-982-5701', sbday='06/02/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='205-964-1873', cenid='SL'),
        Student(sid='NoWarner', sfirst='Noah', slast='Warner', sphonenumber='681-093-2475', sbday='08/31/06', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='486-321-0957', cenid='SH'),
        Student(sid='LeRuiz', sfirst='Lena', slast='Ruiz', sphonenumber='903-817-6425', sbday='03/04/08', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='317-289-5046', cenid='SH'),
        Student(sid='FaCasey', sfirst='Faith', slast='Casey', sphonenumber='372-546-8019', sbday='10/01/07', slevel='hs', sleadership=None, sparentalum=None, semergencyphone='950-428-3671', cenid='SH'),
        Student(sid='MaHudson', sfirst='Maria', slast='Hudson', sphonenumber='615-794-0283', sbday='11/10/03', slevel='co', sleadership='yes', sparentalum='yes', semergencyphone='760-348-1295', cenid='SH'),
        Student(sid='JaStevenson', sfirst='Jake', slast='Stevenson', sphonenumber='287-415-0936', sbday='04/02/05', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='621-594-0837', cenid='SH'),
        Student(sid='CaBlake', sfirst='Carter', slast='Blake', sphonenumber='549-861-2730', sbday='09/14/01', slevel='co', sleadership=None, sparentalum=None, semergencyphone='397-186-2450', cenid='SH'),
        Student(sid='MaRoberts', sfirst='Maria', slast='Roberts', sphonenumber='209-781-3645', sbday='02/08/04', slevel='co', sleadership=None, sparentalum=None, semergencyphone='185-762-3490', cenid='SH'),
        Student(sid='MaMartinez', sfirst='Marta', slast='Martinez', sphonenumber='836-241-9705', sbday='05/20/03', slevel='co', sleadership=None, sparentalum=None, semergencyphone='349-275-6108', cenid='SH'),
        Student(sid='OlBurns', sfirst='Olivia', slast='Burns', sphonenumber='794-083-1625', sbday='08/17/05', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='702-918-4356', cenid='SH'),
        Student(sid='CaGrant', sfirst='Casey', slast='Grant', sphonenumber='523-746-8901', sbday='12/31/02', slevel='co', sleadership='yes', sparentalum='yes', semergencyphone='518-439-2760', cenid='SH'),
        Student(sid='KaFleming', sfirst='Karla', slast='Fleming', sphonenumber='461-208-9375', sbday='07/05/04', slevel='co', sleadership='yes', sparentalum='yes', semergencyphone='864-207-9315', cenid='SH'),
        Student(sid='RoHunter', sfirst='Rosalie', slast='Hunter', sphonenumber='972-431-6085', sbday='03/25/01', slevel='co', sleadership=None, sparentalum=None, semergencyphone='294-158-7603', cenid='SH'),
        Student(sid='HaMcguire', sfirst='Harper', slast='Mcguire', sphonenumber='134-205-7896', sbday='10/13/03', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='637-819-2045', cenid='SH'),
        Student(sid='LoMiller', sfirst='Logan', slast='Miller', sphonenumber='795-843-2610', sbday='01/03/05', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='970-582-3164', cenid='SH'),
        Student(sid='LuGomez', sfirst='Lucia', slast='Gomez', sphonenumber='680-324-7915', sbday='06/09/02', slevel='co', sleadership='yes', sparentalum=None, semergencyphone='541-283-0976', cenid='SH'),
        Student(sid='KeFisher', sfirst='Kendra', slast='Fisher', sphonenumber='215-479-3608', sbday='11/18/04', slevel='co', sleadership=None, sparentalum=None, semergencyphone='326-845-7190', cenid='SH'),
        Student(sid='MaBecker', sfirst='Mary', slast='Becker', sphonenumber='769-804-2315', sbday='04/14/01', slevel='co', sleadership=None, sparentalum=None, semergencyphone='187-420-9365', cenid='SH'),
        Student(sid='SoMorgan', sfirst='Sofia', slast='Morgan', sphonenumber='301-874-5926', sbday='09/28/03', slevel='co', sleadership=None, sparentalum=None, semergencyphone='913-684-2705', cenid='SH'),
    ]

    # Class

    
    sample_classes = [
        
        Class(cid='ELco101122', clevel='co', cdate=('10/11/22'), ctopic='Cheerfulness', cenid='EL'),
        Class(cid='ELco110822', clevel='co', cdate=('11/08/22'), ctopic='Working Well', cenid='EL'),
        Class(cid='ELco121322', clevel='co', cdate=('12/13/22'), ctopic='Friendship', cenid='EL'),
        Class(cid='ELco011023', clevel='co', cdate=('01/10/23'), ctopic='Fortitude', cenid='EL'),
        Class(cid='ELco021423', clevel='co', cdate=('02/14/23'), ctopic='Justice', cenid='EL'),
        Class(cid='ELco031423', clevel='co', cdate=('03/14/23'), ctopic='Temperance', cenid='EL'),
        Class(cid='ELco041123', clevel='co', cdate=('04/11/23'), ctopic='Prudence', cenid='EL'),
        Class(cid='ELco050923', clevel='co', cdate=('05/09/23'), ctopic='Leadership', cenid='EL'),
        Class(cid='GRhs091522', clevel='hs', cdate=('09/15/22'), ctopic='Friendship', cenid='GR'),
        Class(cid='GRhs100622', clevel='hs', cdate=('10/06/22'), ctopic='Courage', cenid='GR'),
        Class(cid='GRhs102022', clevel='hs', cdate=('10/20/22'), ctopic='Study', cenid='GR'),
        Class(cid='GRhs110322', clevel='hs', cdate=('11/03/22'), ctopic='Cheerfulness', cenid='GR'),
        Class(cid='GRhs111722', clevel='hs', cdate=('11/17/22'), ctopic='Honesty', cenid='GR'),
        Class(cid='GRhs120122', clevel='hs', cdate=('12/01/22'), ctopic='Leadership', cenid='GR'),
        Class(cid='GRhs011923', clevel='hs', cdate=('01/19/23'), ctopic='Service', cenid='GR'),
        Class(cid='GRhs020223', clevel='hs', cdate=('02/02/23'), ctopic='Prudence', cenid='GR'),
        Class(cid='GRhs021623', clevel='hs', cdate=('02/16/23'), ctopic='Justice', cenid='GR'),
        Class(cid='GRhs030223', clevel='hs', cdate=('03/02/23'), ctopic='Temperance', cenid='GR'),
        Class(cid='GRhs031623', clevel='hs', cdate=('03/16/23'), ctopic='Fortitude', cenid='GR'),
        Class(cid='GRhs040623', clevel='hs', cdate=('04/06/23'), ctopic='Respect', cenid='GR'),
        Class(cid='GRhs042023', clevel='hs', cdate=('04/20/23'), ctopic='Motivation', cenid='GR'),
        Class(cid='GRhs050423', clevel='hs', cdate=('05/04/23'), ctopic='Prayer', cenid='GR'),
        Class(cid='GRms091922', clevel='ms', cdate=('09/19/22'), ctopic='Goal Setting', cenid='GR'),
        Class(cid='GRms101722', clevel='ms', cdate=('10/17/22'), ctopic='Friendship', cenid='GR'),
        Class(cid='GRms112122', clevel='ms', cdate=('11/21/22'), ctopic='Courage', cenid='GR'),
        Class(cid='GRms121922', clevel='ms', cdate=('12/19/22'), ctopic='Study', cenid='GR'),
        Class(cid='GRms011623', clevel='ms', cdate=('01/16/23'), ctopic='Cheerfulness', cenid='GR'),
        Class(cid='GRms022023', clevel='ms', cdate=('02/20/23'), ctopic='Honesty', cenid='GR'),
        Class(cid='GRms032023', clevel='ms', cdate=('03/20/23'), ctopic='Service', cenid='GR'),
        Class(cid='GRms041023', clevel='ms', cdate=('04/10/23'), ctopic='Gratitude', cenid='GR'),
        Class(cid='PWhs091522', clevel='hs', cdate=('09/15/22'), ctopic='Friendship', cenid='PW'),
        Class(cid='PWhs100622', clevel='hs', cdate=('10/06/22'), ctopic='Courage', cenid='PW'),
        Class(cid='PWhs102722', clevel='hs', cdate=('10/27/22'), ctopic='Study', cenid='PW'),
        Class(cid='PWhs110322', clevel='hs', cdate=('11/03/22'), ctopic='Cheerfulness', cenid='PW'),
        Class(cid='PWhs111722', clevel='hs', cdate=('11/17/22'), ctopic='Honesty', cenid='PW'),
        Class(cid='PWhs120122', clevel='hs', cdate=('12/01/22'), ctopic='Leadership', cenid='PW'),
        Class(cid='PWhs011923', clevel='hs', cdate=('01/19/23'), ctopic='Service', cenid='PW'),
        Class(cid='PWhs020223', clevel='hs', cdate=('02/02/23'), ctopic='Prudence', cenid='PW'),
        Class(cid='PWhs021623', clevel='hs', cdate=('02/16/23'), ctopic='Justice', cenid='PW'),
        Class(cid='PWhs030223', clevel='hs', cdate=('03/02/23'), ctopic='Temperance', cenid='PW'),
        Class(cid='PWhs031623', clevel='hs', cdate=('03/16/23'), ctopic='Fortitude', cenid='PW'),
        Class(cid='PWhs040623', clevel='hs', cdate=('04/06/23'), ctopic='Respect', cenid='PW'),
        Class(cid='PWhs042023', clevel='hs', cdate=('04/20/23'), ctopic='Motivation', cenid='PW'),
        Class(cid='PWhs050423', clevel='hs', cdate=('05/04/23'), ctopic='Prayer', cenid='PW'),
        Class(cid='PWhs051823', clevel='hs', cdate=('05/18/23'), ctopic='Gratitude', cenid='PW'),
        Class(cid='SBhs093022', clevel='hs', cdate=('09/30/22'), ctopic='Friendship', cenid='SB'),
        Class(cid='SBhs102822', clevel='hs', cdate=('10/28/22'), ctopic='Courage', cenid='SB'),
        Class(cid='SBhs111822', clevel='hs', cdate=('11/18/22'), ctopic='Study', cenid='SB'),
        Class(cid='SBhs121622', clevel='hs', cdate=('12/16/22'), ctopic='Cheerfulness', cenid='SB'),
        Class(cid='SBhs012723', clevel='hs', cdate=('01/27/23'), ctopic='Leadership', cenid='SB'),
        Class(cid='SBhs022423', clevel='hs', cdate=('02/24/23'), ctopic='Service', cenid='SB'),
        Class(cid='SBhs033123', clevel='hs', cdate=('03/31/23'), ctopic='Respect', cenid='SB'),
        Class(cid='SBhs042823', clevel='hs', cdate=('04/28/23'), ctopic='Motivation', cenid='SB'),
        Class(cid='SBhs052623', clevel='hs', cdate=('05/26/23'), ctopic='Gratitude', cenid='SB'),
        Class(cid='SLhs101222', clevel='hs', cdate=('10/12/22'), ctopic='Friendship', cenid='SL'),
        Class(cid='SLhs102622', clevel='hs', cdate=('10/26/22'), ctopic='Study', cenid='SL'),
        Class(cid='SLhs110922', clevel='hs', cdate=('11/09/22'), ctopic='Cheerfulness', cenid='SL'),
        Class(cid='SLhs112322', clevel='hs', cdate=('11/23/22'), ctopic='Gratitude', cenid='SL'),
        Class(cid='SLhs121422', clevel='hs', cdate=('12/14/22'), ctopic='Courage', cenid='SL'),
        Class(cid='SLhs011123', clevel='hs', cdate=('01/11/23'), ctopic='Prudence', cenid='SL'),
        Class(cid='SLhs012523', clevel='hs', cdate=('01/25/23'), ctopic='Justice', cenid='SL'),
        Class(cid='SLhs020823', clevel='hs', cdate=('02/08/23'), ctopic='Temperance', cenid='SL'),
        Class(cid='SLhs022223', clevel='hs', cdate=('02/22/23'), ctopic='Fortitude', cenid='SL'),
        Class(cid='SLhs030823', clevel='hs', cdate=('03/08/23'), ctopic='Respect', cenid='SL'),
        Class(cid='SLhs032223', clevel='hs', cdate=('03/22/23'), ctopic='Leadership', cenid='SL'),
        Class(cid='SLhs041223', clevel='hs', cdate=('04/12/23'), ctopic='Service', cenid='SL'),
        Class(cid='SLhs041923', clevel='hs', cdate=('04/19/23'), ctopic='Prayer', cenid='SL'),
        Class(cid='SLms092622', clevel='ms', cdate=('09/26/22'), ctopic='Goal Setting', cenid='SL'),
        Class(cid='SLms102422', clevel='ms', cdate=('10/24/22'), ctopic='Study', cenid='SL'),
        Class(cid='SLms112822', clevel='ms', cdate=('11/28/22'), ctopic='Friendship', cenid='SL'),
        Class(cid='SLms121922', clevel='ms', cdate=('12/19/22'), ctopic='Courage', cenid='SL'),
        Class(cid='SLms013023', clevel='ms', cdate=('01/30/23'), ctopic='Cheerfulness', cenid='SL'),
        Class(cid='SLms022723', clevel='ms', cdate=('02/27/23'), ctopic='Honesty', cenid='SL'),
        Class(cid='SLms032723', clevel='ms', cdate=('03/27/23'), ctopic='Service', cenid='SL'),
        Class(cid='SLms042423', clevel='ms', cdate=('04/24/23'), ctopic='Respect', cenid='SL'),
        Class(cid='SHhs090722', clevel='hs', cdate=('09/07/22'), ctopic='Friendship', cenid='SH'),
        Class(cid='SHhs110222', clevel='hs', cdate=('11/02/22'), ctopic='Study', cenid='SH'),
        Class(cid='SHhs010423', clevel='hs', cdate=('01/04/23'), ctopic='Cheerfulness', cenid='SH'),
        Class(cid='SHhs030723', clevel='hs', cdate=('03/07/23'), ctopic='Gratitude', cenid='SH'),
        Class(cid='SHhs050223', clevel='hs', cdate=('05/02/23'), ctopic='Leadership', cenid='SH'),
        Class(cid='SHco101322', clevel='co', cdate=('10/13/22'), ctopic='Working Well', cenid='SH'),
        Class(cid='SHco111022', clevel='co', cdate=('11/10/22'), ctopic='Friendship', cenid='SH'),
        Class(cid='SHco120822', clevel='co', cdate=('12/08/22'), ctopic='Fortitude', cenid='SH'),
        Class(cid='SHco020223', clevel='co', cdate=('02/02/23'), ctopic='Justice', cenid='SH'),
        Class(cid='SHco030123', clevel='co', cdate=('03/01/23'), ctopic='Temperance', cenid='SH'),
        Class(cid='SHco040523', clevel='co', cdate=('04/05/23'), ctopic='Prudence', cenid='SH'),
        Class(cid='SHco050323', clevel='co', cdate=('05/03/23'), ctopic='Leadership', cenid='SH')
    ]

    # PermStaff
    sample_perm_staff = [
        PermStaff(pid='MaSmith', pfirst='Margaret', plast='Smith', pemail='margaretsmith87@gmail.com', pphonenumber='773-432-1234', ptrainstatus='initiated', ptrainexp=None, cenid='EL'),
        PermStaff(pid='LiBennett', pfirst='Liam', plast='Bennett', pemail='liam.bennett_123@yahoo.com', pphonenumber='815-123-4567', ptrainstatus='good', ptrainexp='2024-08-09', cenid='EL'),
        PermStaff(pid='OlCarter', pfirst='Olivia', plast='Carter', pemail='oliviacarter22@hotmail.com', pphonenumber='773-234-5678', ptrainstatus='initiated', ptrainexp=None, cenid='EL'),
        PermStaff(pid='NoDavis', pfirst='Noah', plast='Davis', pemail='noah.davis2000@gmail.com', pphonenumber='773-432-1098', ptrainstatus='good', ptrainexp='2024-03-08', cenid='EL'),
        PermStaff(pid='EmEvans', pfirst='Emma', plast='Evans', pemail='e.evansofficial@gmail.com', pphonenumber='815-345-6789', ptrainstatus='initiated', ptrainexp=None, cenid='EL'),
        PermStaff(pid='JaFisher', pfirst='Jackson', plast='Fisher', pemail='jackson.fisher_99@yahoo.com', pphonenumber='773-876-5432', ptrainstatus='flag', ptrainexp='2023-07-02', cenid='EL'),
        PermStaff(pid='AvGreene', pfirst='Ava', plast='Greene', pemail='ava.greene_5678@hotmail.com', pphonenumber='815-987-6543', ptrainstatus='good', ptrainexp='2026-07-07', cenid='FG'),
        PermStaff(pid='AiHayes', pfirst='Aiden', plast='Hayes', pemail='aidenh345@gmail.com', pphonenumber='815-789-0123', ptrainstatus='initiated', ptrainexp=None, cenid='FG'),
        PermStaff(pid='IsIngram', pfirst='Isabella', plast='Ingram', pemail='isabella.ingram@outlook.com', pphonenumber='773-890-1234', ptrainstatus='good', ptrainexp='2024-09-06', cenid='FG'),
        PermStaff(pid='MaSmith1', pfirst='Mary', plast='Smith', pemail='m.smithofficial@gmail.com', pphonenumber='773-678-9012', ptrainstatus='initiated', ptrainexp=None, cenid='LD'),
        PermStaff(pid='LuJensen', pfirst='Lucas', plast='Jensen', pemail='lucas.jensen22@yahoo.com', pphonenumber='815-678-9012', ptrainstatus='good', ptrainexp='2024-07-25', cenid='LD'),
        PermStaff(pid='MiKeller', pfirst='Mia', plast='Keller', pemail='mia.keller_456@hotmail.com', pphonenumber='773-234-5678', ptrainstatus='initiated', ptrainexp=None, cenid='LD'),
        PermStaff(pid='EtLawson', pfirst='Ethan', plast='Lawson', pemail='ethan.lawson_789@gmail.com', pphonenumber='773-890-1234', ptrainstatus='good', ptrainexp='2026-08-12', cenid='LD'),
        PermStaff(pid='HaMitchell', pfirst='Harper', plast='Mitchell', pemail='harper.mitchell_321@yahoo.com', pphonenumber='815-789-0987', ptrainstatus='failed', ptrainexp=None, cenid='LD'),
        PermStaff(pid='OlNelson', pfirst='Oliver', plast='Nelson', pemail='o.nelsonofficial@gmail.com', pphonenumber='815-345-6789', ptrainstatus='good', ptrainexp='2024-11-30', cenid='LD'),
        PermStaff(pid='AmOwens', pfirst='Amelia', plast='Owens', pemail='amelia.owens_22@hotmail.com', pphonenumber='773-234-5678', ptrainstatus='good', ptrainexp='2026-02-07', cenid='PW'),
        PermStaff(pid='ElParker', pfirst='Elijah', plast='Parker', pemail='elijah.parker2001@yahoo.com', pphonenumber='773-678-9012', ptrainstatus='initiated', ptrainexp=None, cenid='PW'),
        PermStaff(pid='EvQuinn', pfirst='Evelyn', plast='Quinn', pemail='evelyn.quinnofficial@gmail.com', pphonenumber='815-678-9012', ptrainstatus='good', ptrainexp='2025-10-14', cenid='PW'),
        PermStaff(pid='JaReynolds', pfirst='James', plast='Reynolds', pemail='james_reynolds22@yahoo.com', pphonenumber='773-432-1098', ptrainstatus='good', ptrainexp='2024-10-12', cenid='PW'),
        PermStaff(pid='AbStewart', pfirst='Abigail', plast='Stewart', pemail='abigail.stewart_567@hotmail.com', pphonenumber='815-987-6543', ptrainstatus='initiated', ptrainexp=None, cenid='PW'),
        PermStaff(pid='BeTurner', pfirst='Benjamin', plast='Turner', pemail='benjamin_turner@gmail.com', pphonenumber='773-876-5432', ptrainstatus='good', ptrainexp='2025-02-21', cenid='PW'),
        PermStaff(pid='ChVaughn', pfirst='Charlotte', plast='Vaughn', pemail='c.vaughnofficial@yahoo.com', pphonenumber='815-123-4567', ptrainstatus='initiated', ptrainexp=None, cenid='SB'),
        PermStaff(pid='WiWallace', pfirst='William', plast='Wallace', pemail='william.wallace_123@hotmail.com', pphonenumber='815-789-0123', ptrainstatus='good', ptrainexp='2023-12-03', cenid='SB'),
        PermStaff(pid='ScYoung', pfirst='Scarlett', plast='Young', pemail='s.youngofficial@gmail.com', pphonenumber='773-432-1098', ptrainstatus='failed', ptrainexp=None, cenid='SB'),
        PermStaff(pid='HeZimmerman', pfirst='Henry', plast='Zimmerman', pemail='h.zimmerman_789@yahoo.com', pphonenumber='773-432-1234', ptrainstatus='good', ptrainexp='2025-11-27', cenid='SB'),
        PermStaff(pid='GrHarrison', pfirst='Grace', plast='Harrison', pemail='graceharrisonofficial@gmail.com', pphonenumber='773-890-1234', ptrainstatus='initiated', ptrainexp=None, cenid='SL'),
        PermStaff(pid='AlDixon', pfirst='Alexander', plast='Dixon', pemail='alexander_dixon22@hotmail.com', pphonenumber='815-123-4567', ptrainstatus='good', ptrainexp='2025-08-09', cenid='SL'),
        PermStaff(pid='LiMason', pfirst='Lily', plast='Mason', pemail='lily.mason_456@yahoo.com', pphonenumber='773-432-1098', ptrainstatus='flag', ptrainexp='2023-09-08', cenid='SL'),
        PermStaff(pid='SaPorter', pfirst='Samuel', plast='Porter', pemail='samuel.porterofficial@gmail.com', pphonenumber='773-234-5678', ptrainstatus='good', ptrainexp='2024-02-18', cenid='SL'),
        PermStaff(pid='ChReed', pfirst='Chloe', plast='Reed', pemail='chloe.reed_22@yahoo.com', pphonenumber='815-345-6789', ptrainstatus='initiated', ptrainexp=None, cenid='SL'),
        PermStaff(pid='DaSanders', pfirst='Daniel', plast='Sanders', pemail='daniel.sanders_123@hotmail.com', pphonenumber='773-678-9012', ptrainstatus='good', ptrainexp='2026-06-20', cenid='SL'),
        PermStaff(pid='ZoWarren', pfirst='Zoey', plast='Warren', pemail='zoey.warrenofficial@gmail.com', pphonenumber='815-789-0123', ptrainstatus='good', ptrainexp='2025-07-22', cenid='SL'),
        PermStaff(pid='CaHughes', pfirst='Caleb', plast='Hughes', pemail='caleb.hughes_567@yahoo.com', pphonenumber='773-876-5432', ptrainstatus='initiated', ptrainexp=None, cenid='SL'),
        PermStaff(pid='ElRoss', pfirst='Ella', plast='Ross', pemail='ella_ross22@hotmail.com', pphonenumber='815-987-6543', ptrainstatus='good', ptrainexp='2026-04-11', cenid='SH'),
        PermStaff(pid='MaPowell', pfirst='Mason', plast='Powell', pemail='mason.powellofficial@gmail.com', pphonenumber='773-432-1234', ptrainstatus='flag', ptrainexp='2023-05-28', cenid='SH'),
        PermStaff(pid='SoBennett', pfirst='Sofia', plast='Bennett', pemail='sofia.bennett_321@yahoo.com', pphonenumber='815-789-0123', ptrainstatus='good', ptrainexp='2023-12-12', cenid='SH')
    ]

    # Volunteer
    sample_volunteers = [
        Volunteer(vid='V01', vfirst='Jane', vlast='Angel', vphonenumber='333-444-5567', vemail='janeangel1@gmail.com', vtrainstatus='good', vtrainexp='2024-10-16'),
        Volunteer(vid='V02', vfirst='David', vlast='Smith', vphonenumber='111-224-3378', vemail='davidsmith@outlook.com', vtrainstatus='good', vtrainexp='2024-11-23'),
        Volunteer(vid='V03', vfirst='Angela', vlast='Precious', vphonenumber='208-447-5583', vemail='angelaprecious3@hotmail.com', vtrainstatus='good', vtrainexp='2024-06-04'),
        Volunteer(vid='V04', vfirst='Leroy', vlast='Prescot', vphonenumber='305-456-7890', vemail='leroyprescot14@gmail.com', vtrainstatus='good', vtrainexp='2025-02-24'),
        Volunteer(vid='V05', vfirst='Adam', vlast='Jake', vphonenumber='224-527-8765', vemail='adamjake@msn.com', vtrainstatus='initiated', vtrainexp=None),
        Volunteer(vid='V06', vfirst='Logan', vlast='Peter', vphonenumber='220-657-7890', vemail='loganpeter@outlook.com', vtrainstatus='good', vtrainexp='2024-08-19'),
        Volunteer(vid='V07', vfirst='Toby', vlast='Tyler', vphonenumber='451-567-6578', vemail='tobytyler@gmail.com', vtrainstatus='initiated', vtrainexp=None),
        Volunteer(vid='V08', vfirst='Tyson', vlast='Chandler', vphonenumber='312-876-4521', vemail='tysonchandler@msn.com', vtrainstatus='flag', vtrainexp='2024-09-14'),
        Volunteer(vid='V09', vfirst='Mary', vlast='Lovely', vphonenumber='512-489-0081', vemail='marylovely@gmail.com', vtrainstatus='good', vtrainexp='2025-04-16'),
        Volunteer(vid='V10', vfirst='James', vlast='Richard', vphonenumber='444-012-6890', vemail='jamesrichard12@outlook.com', vtrainstatus='good', vtrainexp='2024-07-15')
    ]

    # Event
    sample_events = [
        Event(eid='093022ms_wksp', elocation='Grove', ename='Goal Setting', edate='2022-09-30', eaudience='ms', ecategory='workshop'),
        Event(eid='012023ms_wksp', elocation='Grove', ename='Study Techniques', edate='2023-01-20', eaudience='ms', ecategory='workshop'),
        Event(eid='121622ms_service', elocation='St. Anne''s', ename='Food Pantry', edate='2022-12-16', eaudience='ms', ecategory='service'),
        Event(eid='093022hs_workshop', elocation='Sherlake', ename='Optimal Work', edate='2022-09-30', eaudience='hs', ecategory='workshop'),
        Event(eid='100722hs_workshop', elocation='Grove', ename='Leadership', edate='2022-10-07', eaudience='hs', ecategory='workshop'),
        Event(eid='041322hs_workshop', elocation='Lindell', ename='Building Character', edate='2022-04-13', eaudience='hs', ecategory='workshop'),
        Event(eid='031622hs_workshop', elocation='Sherlake', ename='Leadership', edate='2022-03-16', eaudience='hs', ecategory='workshop'),
        Event(eid='100622hs_workshop', elocation='Sherlake', ename='Building Habits', edate='2022-10-06', eaudience='hs', ecategory='workshop'),
        Event(eid='111822hs_service', elocation='St. Anne''s', ename='Food Pantry', edate='2022-11-18', eaudience='hs', ecategory='service'),
        Event(eid='051823hs_service', elocation='Arbor Care', ename='Visit to Elderly', edate='2023-05-18', eaudience='hs', ecategory='service'),
        Event(eid='110422hs_retreat', elocation='Shellbourne', ename='HS Fall Retreat', edate='2022-11-04', eaudience='hs', ecategory='retreat'),
        Event(eid='032323hs_retreat', elocation='Shellbourne', ename='HS Spring Retreat', edate='2023-03-23', eaudience='hs', ecategory='retreat'),
        Event(eid='121722hs_other', elocation='Sherlake', ename='Christmas Party', edate='2022-12-17', eaudience='hs', ecategory='other'),
        Event(eid='102822co_workshop', elocation='Elms', ename='Optimal Work', edate='2022-10-28', eaudience='co', ecategory='workshop'),
        Event(eid='120922co_service', elocation='Elms', ename='Visit the Homeless', edate='2022-12-09', eaudience='co', ecategory='service'),
        Event(eid='021023co_service', elocation='Southold', ename='Visit the Homeless', edate='2023-02-10', eaudience='co', ecategory='service'),
        Event(eid='032323co_service', elocation='St. Anne''s', ename='Food Pantry', edate='2023-03-23', eaudience='co', ecategory='service'),
        Event(eid='011323co_retreat', elocation='Shellbourne', ename='College Winter Retreat', edate='2023-01-13', eaudience='co', ecategory='retreat'),
        Event(eid='042023co_retreat', elocation='Shellbourne', ename='College Spring Retreat', edate='2023-04-20', eaudience='co', ecategory='retreat'),
        Event(eid='110622co_other', elocation='Southold', ename='Dinner', edate='2022-11-06', eaudience='co', ecategory='other'),
        Event(eid='032623co_other', elocation='Southold', ename='Dinner', edate='2023-03-26', eaudience='co', ecategory='other'),
        Event(eid='042823co_other', elocation='Elms', ename='Movie Night', edate='2023-04-28', eaudience='co', ecategory='other')
    ]

    # Takes
    sample_takes = [
        Takes(cid='ELco101122', sid='LeKoch'),
        Takes(cid='ELco101122', sid='RyWilliams'),
        Takes(cid='ELco101122', sid='DaMartinez'),
        Takes(cid='ELco110822', sid='OlSmith'),
        Takes(cid='ELco110822', sid='LeKoch'),
        Takes(cid='ELco110822', sid='SaJohnson'),
        Takes(cid='ELco110822', sid='MaTaylor'),
        Takes(cid='ELco011023', sid='AvBrown'),
        Takes(cid='ELco011023', sid='OlSmith'),
        Takes(cid='ELco021423', sid='LeKoch'),
        Takes(cid='ELco021423', sid='RyWilliams'),
        Takes(cid='ELco021423', sid='EmDavis'),
        Takes(cid='ELco021423', sid='SaJohnson'),
        Takes(cid='ELco031423', sid='DaMartinez'),
        Takes(cid='ELco031423', sid='MaTaylor'),
        Takes(cid='ELco031423', sid='OlSmith'),
        Takes(cid='ELco041123', sid='LeKoch'),
        Takes(cid='ELco041123', sid='RyWilliams'),
        Takes(cid='ELco050923', sid='LeKoch'),
        Takes(cid='ELco050923', sid='MaTaylor'),
        Takes(cid='ELco050923', sid='SaJohnson'),
        Takes(cid='GRhs091522', sid='ChAnderson'),
        Takes(cid='GRhs091522', sid='HeAdams'),
        Takes(cid='GRhs100622', sid='ChHall'),
        Takes(cid='GRhs100622', sid='ChAnderson'),
        Takes(cid='GRhs100622', sid='MiClark'),
        Takes(cid='GRhs100622', sid='SoParker'),
        Takes(cid='GRhs102022', sid='LiGreen'),
        Takes(cid='GRhs102022', sid='AmRodriguez'),
        Takes(cid='GRhs102022', sid='NoMitchell'),
        Takes(cid='GRhs110322', sid='ChAnderson'),
        Takes(cid='GRhs110322', sid='BeWilson'),
        Takes(cid='GRhs110322', sid='SoParker'),
        Takes(cid='GRhs111722', sid='MiClark'),
        Takes(cid='GRhs111722', sid='SaWhite'),
        Takes(cid='GRhs111722', sid='BeWilson'),
        Takes(cid='GRhs111722', sid='NoMitchell'),
        Takes(cid='GRhs120122', sid='BeWilson'),
        Takes(cid='GRhs120122', sid='SoParker'),
        Takes(cid='GRhs011923', sid='SaWhite'),
        Takes(cid='GRhs011923', sid='MiClark'),
        Takes(cid='GRhs011923', sid='AmRodriguez'),
        Takes(cid='GRhs020223', sid='NoMitchell'),
        Takes(cid='GRhs020223', sid='LiGreen'),
        Takes(cid='GRhs030223', sid='BeWilson'),
        Takes(cid='GRhs030223', sid='MiClark'),
        Takes(cid='GRhs030223', sid='SaWhite'),
        Takes(cid='GRhs031623', sid='AmRodriguez'),
        Takes(cid='GRhs031623', sid='SoParker'),
        Takes(cid='GRhs031623', sid='ChHall'),
        Takes(cid='GRhs040623', sid='AmRodriguez'),
        Takes(cid='GRhs040623', sid='MiClark'),
        Takes(cid='GRhs040623', sid='SaWhite'),
        Takes(cid='GRhs042023', sid='NoMitchell'),
        Takes(cid='GRhs042023', sid='SoParker'),
        Takes(cid='GRhs042023', sid='MiClark'),
        Takes(cid='GRhs050423', sid='BeWilson'),
        Takes(cid='GRhs050423', sid='MiClark'),
        Takes(cid='GRhs050423', sid='AmRodriguez'),
        Takes(cid='GRhs050423', sid='SoParker'),
        Takes(cid='GRms091922', sid='IsRodriguez'),
        Takes(cid='GRms091922', sid='JaThomas'),
        Takes(cid='GRms101722', sid='AvAnderson'),
        Takes(cid='GRms101722', sid='IsRodriguez'),
        Takes(cid='GRms112122', sid='IsRodriguez'),
        Takes(cid='GRms112122', sid='JaThomas'),
        Takes(cid='GRms112122', sid='OlBrown'),
        Takes(cid='GRms121922', sid='AvAnderson'),
        Takes(cid='GRms121922', sid='IsRodriguez'),
        Takes(cid='GRms011623', sid='MiSmith'),
        Takes(cid='GRms011623', sid='IsRodriguez'),
        Takes(cid='GRms011623', sid='AvAnderson'),
        Takes(cid='GRms022023', sid='WiHarris'),
        Takes(cid='GRms022023', sid='LiWilson'),
        Takes(cid='GRms041023', sid='AvAnderson'),
        Takes(cid='GRms041023', sid='JaThomas'),
        Takes(cid='PWhs091522', sid='ZoCooper'),
        Takes(cid='PWhs091522', sid='LoWard'),
        Takes(cid='PWhs102722', sid='ZoCooper'),
        Takes(cid='PWhs102722', sid='DaCarter'),
        Takes(cid='PWhs102722', sid='CaMitchell'),
        Takes(cid='PWhs102722', sid='EmRivera'),
        Takes(cid='PWhs110322', sid='EmRivera'),
        Takes(cid='PWhs110322', sid='ZoCooper'),
        Takes(cid='PWhs111722', sid='ZoCooper'),
        Takes(cid='PWhs111722', sid='EmRivera'),
        Takes(cid='PWhs120122', sid='ZoCooper'),
        Takes(cid='PWhs120122', sid='DaCarter'),
        Takes(cid='PWhs020223', sid='LiScott'),
        Takes(cid='PWhs020223', sid='LoWard'),
        Takes(cid='PWhs021623', sid='ZoCooper'),
        Takes(cid='PWhs021623', sid='DaCarter'),
        Takes(cid='PWhs030223', sid='EmRivera'),
        Takes(cid='PWhs030223', sid='ZoCooper'),
        Takes(cid='PWhs031623', sid='JaStewart'),
        Takes(cid='PWhs031623', sid='DaCarter'),
        Takes(cid='PWhs031623', sid='AnRoss'),
        Takes(cid='PWhs042023', sid='ZoCooper'),
        Takes(cid='PWhs042023', sid='ElYoung'),
        Takes(cid='PWhs050423', sid='ZoCooper'),
        Takes(cid='PWhs050423', sid='EmRivera'),
        Takes(cid='PWhs051823', sid='CaMitchell'),
        Takes(cid='PWhs051823', sid='ZoCooper'),
        Takes(cid='SBhs093022', sid='EmSullivan'),
        Takes(cid='SBhs093022', sid='MaHernandez'),
        Takes(cid='SBhs102822', sid='LuWilson'),
        Takes(cid='SBhs111822', sid='ZaParker'),
        Takes(cid='SBhs111822', sid='MiStewart'),
        Takes(cid='SBhs111822', sid='EmSullivan'),
        Takes(cid='SBhs121622', sid='AbMorris'),
        Takes(cid='SBhs012723', sid='EmSullivan'),
        Takes(cid='SBhs012723', sid='MaHernandez'),
        Takes(cid='SBhs012723', sid='OwCarter'),
        Takes(cid='SBhs022423', sid='EmSullivan'),
        Takes(cid='SBhs022423', sid='ZaParker'),
        Takes(cid='SBhs033123', sid='AbMorris'),
        Takes(cid='SBhs033123', sid='JoPeterson'),
        Takes(cid='SBhs042823', sid='JoPeterson'),
        Takes(cid='SBhs042823', sid='EmSullivan'),
        Takes(cid='SBhs042823', sid='ZaParker'),
        Takes(cid='SBhs052623', sid='NiJohnson'),
        Takes(cid='SBhs052623', sid='ZaParker'),
        Takes(cid='SLhs101222', sid='EmSchneider'),
        Takes(cid='SLhs101222', sid='AnEllis'),
        Takes(cid='SLhs102622', sid='ClHammond'),
        Takes(cid='SLhs102622', sid='LeYates'),
        Takes(cid='SLhs102622', sid='CeCollier'),
        Takes(cid='SLhs110922', sid='CaFlores'),
        Takes(cid='SLhs110922', sid='TaOsborne'),
        Takes(cid='SLhs110922', sid='EmSchneider'),
        Takes(cid='SLhs112322', sid='EmSchneider'),
        Takes(cid='SLhs112322', sid='LeMorris'),
        Takes(cid='SLhs121422', sid='ClHammond'),
        Takes(cid='SLhs011123', sid='LoCunningham'),
        Takes(cid='SLhs011123', sid='CeCollier'),
        Takes(cid='SLhs011123', sid='EmSchneider'),
        Takes(cid='SLhs012523', sid='JoJohnson'),
        Takes(cid='SLhs012523', sid='LoCunningham'),
        Takes(cid='SLhs020823', sid='EmSchneider'),
        Takes(cid='SLhs020823', sid='LeMorris'),
        Takes(cid='SLhs022223', sid='LeYates'),
        Takes(cid='SLhs022223', sid='PaWhite'),
        Takes(cid='SLhs022223', sid='CaFlores'),
        Takes(cid='SLhs030823', sid='EmSchneider'),
        Takes(cid='SLhs032223', sid='EmSchneider'),
        Takes(cid='SLhs032223', sid='LoCunningham'),
        Takes(cid='SLhs041223', sid='AnEllis'),
        Takes(cid='SLhs041923', sid='EmSchneider'),
        Takes(cid='SLhs041923', sid='ClHammond'),
        Takes(cid='SLms092622', sid='NoClark'),
        Takes(cid='SLms092622', sid='LiNyugen'),
        Takes(cid='SLms102422', sid='StGuzman'),
        Takes(cid='SLms102422', sid='StHoffman'),
        Takes(cid='SLms102422', sid='NoClark'),
        Takes(cid='SLms112822', sid='DaMontgomery'),
        Takes(cid='SLms112822', sid='NoClark'),
        Takes(cid='SLms121922', sid='BrMitchell'),
        Takes(cid='SLms121922', sid='JaLee'),
        Takes(cid='SLms121922', sid='NoClark'),
        Takes(cid='SLms013023', sid='StGuzman'),
        Takes(cid='SLms013023', sid='SaGardner'),
        Takes(cid='SLms013023', sid='StHoffman'),
        Takes(cid='SLms013023', sid='NoClark'),
        Takes(cid='SLms022723', sid='NoClark'),
        Takes(cid='SLms022723', sid='JaLee'),
        Takes(cid='SLms032723', sid='JaLee'),
        Takes(cid='SLms032723', sid='StGuzman'),
        Takes(cid='SLms042423', sid='SaGardner'),
        Takes(cid='SLms042423', sid='NoClark'),
        Takes(cid='SHhs090722', sid='NoWarner'),
        Takes(cid='SHhs090722', sid='LeRuiz'),
        Takes(cid='SHhs090722', sid='FaCasey'),
        Takes(cid='SHhs110222', sid='NoWarner'),
        Takes(cid='SHhs110222', sid='LeRuiz'),
        Takes(cid='SHhs010423', sid='NoWarner'),
        Takes(cid='SHhs010423', sid='LeRuiz'),
        Takes(cid='SHhs010423', sid='FaCasey'),
        Takes(cid='SHhs030723', sid='FaCasey'),
        Takes(cid='SHhs050223', sid='NoWarner'),
        Takes(cid='SHhs050223', sid='FaCasey'),
        Takes(cid='SHco101322', sid='HaMcguire'),
        Takes(cid='SHco101322', sid='MaRoberts'),
        Takes(cid='SHco111022', sid='HaMcguire'),
        Takes(cid='SHco120822', sid='KaFleming'),
        Takes(cid='SHco120822', sid='HaMcguire'),
        Takes(cid='SHco020223', sid='LuGomez'),
        Takes(cid='SHco020223', sid='HaMcguire'),
        Takes(cid='SHco030123', sid='KaFleming'),
        Takes(cid='SHco030123', sid='LuGomez'),
        Takes(cid='SHco040523', sid='HaMcguire'),
        Takes(cid='SHco040523', sid='CaBlake'),
        Takes(cid='SHco050323', sid='HaMcguire'),
        Takes(cid='SHco050323', sid='MaHudson'),
    ]

    # Teaches
    sample_teaches = [
        Teaches(cid='ELco101122', pid='LiBennett'),
        Teaches(cid='ELco110822', pid='EmEvans'),
        Teaches(cid='ELco121322', pid='MaSmith'),
        Teaches(cid='ELco011023', pid='MiKeller'),
        Teaches(cid='ELco021423', pid='JaReynolds'),
        Teaches(cid='ELco031423', pid='WiWallace'),
        Teaches(cid='ELco041123', pid='AlDixon'),
        Teaches(cid='ELco050923', pid='ChReed'),
        Teaches(cid='GRhs091522', pid='CaHughes'),
        Teaches(cid='GRhs100622', pid='MaSmith'),
        Teaches(cid='GRhs102022', pid='NoDavis'),
        Teaches(cid='GRhs110322', pid='AvGreene'),
        Teaches(cid='GRhs111722', pid='IsIngram'),
        Teaches(cid='GRhs120122', pid='LuJensen'),
        Teaches(cid='GRhs011923', pid='EtLawson'),
        Teaches(cid='GRhs020223', pid='OlNelson'),
        Teaches(cid='GRhs021623', pid='AmOwens'),
        Teaches(cid='GRhs030223', pid='ElParker'),
        Teaches(cid='GRhs031623', pid='AbStewart'),
        Teaches(cid='GRhs040623', pid='WiWallace'),
        Teaches(cid='GRhs042023', pid='HeZimmerman'),
        Teaches(cid='GRhs050423', pid='GrHarrison'),
        Teaches(cid='GRms091922', pid='AlDixon'),
        Teaches(cid='GRms091922', pid='LiMason'),
        Teaches(cid='GRms101722', pid='SaPorter'),
        Teaches(cid='GRms101722', pid='DaSanders'),
        Teaches(cid='GRms112122', pid='ZoWarren'),
        Teaches(cid='GRms112122', pid='CaHughes'),
        Teaches(cid='GRms112122', pid='ElRoss'),
        Teaches(cid='GRms121922', pid='LiBennett'),
        Teaches(cid='GRms121922', pid='AvGreene'),
        Teaches(cid='GRms011623', pid='AiHayes'),
        Teaches(cid='GRms011623', pid='IsIngram'),
        Teaches(cid='GRms022023', pid='MaSmith1'),
        Teaches(cid='GRms032023', pid='LuJensen'),
        Teaches(cid='GRms032023', pid='MiKeller'),
        Teaches(cid='GRms032023', pid='EtLawson'),
        Teaches(cid='GRms041023', pid='ChVaughn'),
        Teaches(cid='GRms041023', pid='HeZimmerman'),
        Teaches(cid='GRms041023', pid='GrHarrison'),
        Teaches(cid='PWhs091522', pid='AlDixon'),
        Teaches(cid='PWhs100622', pid='LiMason'),
        Teaches(cid='PWhs102722', pid='SaPorter'),
        Teaches(cid='PWhs102722', pid='ChReed'),
        Teaches(cid='PWhs111722', pid='CaHughes'),
        Teaches(cid='PWhs111722', pid='ElRoss'),
        Teaches(cid='PWhs120122', pid='SoBennett'),
        Teaches(cid='PWhs120122', pid='OlNelson'),
        Teaches(cid='PWhs120122', pid='AmOwens'),
        Teaches(cid='PWhs020223', pid='BeTurner'),
        Teaches(cid='PWhs021623', pid='ScYoung'),
        Teaches(cid='PWhs021623', pid='HeZimmerman'),
        Teaches(cid='PWhs021623', pid='AlDixon'),
        Teaches(cid='PWhs030223', pid='LiMason'),
        Teaches(cid='PWhs030223', pid='SaPorter'),
        Teaches(cid='PWhs031623', pid='ChReed'),
        Teaches(cid='PWhs031623', pid='ZoWarren'),
        Teaches(cid='PWhs040623', pid='CaHughes'),
        Teaches(cid='PWhs040623', pid='ElRoss'),
        Teaches(cid='PWhs042023', pid='LiBennett'),
        Teaches(cid='PWhs042023', pid='AvGreene'),
        Teaches(cid='PWhs050423', pid='AiHayes'),
        Teaches(cid='PWhs050423', pid='IsIngram'),
        Teaches(cid='SBhs093022', pid='MaSmith1'),
        Teaches(cid='SBhs093022', pid='LuJensen'),
        Teaches(cid='SBhs102822', pid='MiKeller'),
        Teaches(cid='SBhs102822', pid='EtLawson'),
        Teaches(cid='SBhs111822', pid='ChVaughn'),
        Teaches(cid='SBhs111822', pid='HeZimmerman'),
        Teaches(cid='SBhs121622', pid='GrHarrison'),
        Teaches(cid='SBhs121622', pid='LiMason'),
        Teaches(cid='SBhs012723', pid='SaPorter'),
        Teaches(cid='SBhs022423', pid='ChReed'),
        Teaches(cid='SBhs022423', pid='DaSanders'),
        Teaches(cid='SBhs033123', pid='OlNelson'),
        Teaches(cid='SBhs033123', pid='BeTurner'),
        Teaches(cid='SBhs042823', pid='ChVaughn'),
        Teaches(cid='SBhs042823', pid='WiWallace'),
        Teaches(cid='SBhs052623', pid='ScYoung'),
        Teaches(cid='SBhs052623', pid='HeZimmerman'),
        Teaches(cid='SLhs101222', pid='GrHarrison'),
        Teaches(cid='SLhs101222', pid='LiMason'),
        Teaches(cid='SLhs102622', pid='SaPorter'),
        Teaches(cid='SLhs102622', pid='ChReed'),
        Teaches(cid='SLhs110922', pid='DaSanders'),
        Teaches(cid='SLhs110922', pid='WiWallace'),
        Teaches(cid='SLhs112322', pid='HeZimmerman'),
        Teaches(cid='SLhs112322', pid='GrHarrison'),
        Teaches(cid='SLhs121422', pid='AlDixon'),
        Teaches(cid='SLhs121422', pid='LiMason'),
        Teaches(cid='SLhs011123', pid='SaPorter'),
        Teaches(cid='SLhs011123', pid='ChReed'),
        Teaches(cid='SLhs012523', pid='DaSanders'),
        Teaches(cid='SLhs020823', pid='SaPorter'),
        Teaches(cid='SLhs020823', pid='ChReed'),
        Teaches(cid='SLhs020823', pid='DaSanders'),
        Teaches(cid='SLhs022223', pid='GrHarrison'),
        Teaches(cid='SLhs022223', pid='AlDixon'),
        Teaches(cid='SLhs030823', pid='LiMason'),
        Teaches(cid='SLhs030823', pid='WiWallace'),
        Teaches(cid='SLms092622', pid='ScYoung'),
        Teaches(cid='SLms092622', pid='HeZimmerman'),
        Teaches(cid='SLms092622', pid='GrHarrison'),
        Teaches(cid='SLms102422', pid='AlDixon'),
        Teaches(cid='SLms102422', pid='LiMason'),
        Teaches(cid='SLms102422', pid='SaPorter'),
        Teaches(cid='SLms112822', pid='ChReed'),
        Teaches(cid='SLms112822', pid='DaSanders'),
        Teaches(cid='SLms112822', pid='ZoWarren'),
        Teaches(cid='SLms121922', pid='CaHughes'),
        Teaches(cid='SLms121922', pid='ElRoss'),
        Teaches(cid='SLms121922', pid='MaPowell'),
        Teaches(cid='SLms013023', pid='SoBennett'),
        Teaches(cid='SLms013023', pid='AmOwens'),
        Teaches(cid='SLms013023', pid='OlNelson'),
        Teaches(cid='SLms022723', pid='BeTurner'),
        Teaches(cid='SLms022723', pid='ChVaughn'),
        Teaches(cid='SLms022723', pid='WiWallace'),
        Teaches(cid='SHhs090722', pid='HeZimmerman'),
        Teaches(cid='SHhs090722', pid='GrHarrison'),
        Teaches(cid='SHhs090722', pid='LiMason'),
        Teaches(cid='SHhs110222', pid='SaPorter'),
        Teaches(cid='SHhs110222', pid='ChReed'),
        Teaches(cid='SHhs110222', pid='DaSanders'),
        Teaches(cid='SHhs010423', pid='WiWallace'),
        Teaches(cid='SHhs010423', pid='ScYoung'),
        Teaches(cid='SHhs010423', pid='HeZimmerman'),
        Teaches(cid='SHhs030723', pid='GrHarrison'),
        Teaches(cid='SHhs030723', pid='AlDixon'),
        Teaches(cid='SHhs030723', pid='LiMason'),
        Teaches(cid='SHhs050223', pid='SaPorter'),
        Teaches(cid='SHhs050223', pid='ChReed'),
        Teaches(cid='SHhs050223', pid='DaSanders'),
        Teaches(cid='SHco101322', pid='SaPorter'),
        Teaches(cid='SHco101322', pid='ChReed'),
        Teaches(cid='SHco101322', pid='DaSanders'),
        Teaches(cid='SHco111022', pid='GrHarrison'),
        Teaches(cid='SHco111022', pid='AlDixon'),
        Teaches(cid='SHco111022', pid='LiMason'),
        Teaches(cid='SHco120822', pid='WiWallace'),
        Teaches(cid='SHco120822', pid='ScYoung'),
        Teaches(cid='SHco120822', pid='HeZimmerman'),
        Teaches(cid='SHco020223', pid='GrHarrison'),
        Teaches(cid='SHco020223', pid='AlDixon'),
        Teaches(cid='SHco020223', pid='LiMason'),
        Teaches(cid='SHco030123', pid='SaPorter'),
        Teaches(cid='SHco030123', pid='ChReed'),
        Teaches(cid='SHco030123', pid='DaSanders'),
        Teaches(cid='SHco040523', pid='ZoWarren'),
        Teaches(cid='SHco040523', pid='CaHughes'),
        Teaches(cid='SHco050323', pid='ElRoss'),
    ]

    # Runs
    sample_runs = [
        Runs(pid='MaSmith', eid='093022ms_wksp'),
        Runs(pid='LiBennett', eid='093022ms_wksp'),
        Runs(pid='OlCarter', eid='012023ms_wksp'),
        Runs(pid='IsIngram', eid='012023ms_wksp'),
        Runs(pid='NoDavis', eid='121622ms_service'),
        Runs(pid='MaSmith', eid='121622ms_service'),
        Runs(pid='EmEvans', eid='093022hs_workshop'),
        Runs(pid='JaFisher', eid='093022hs_workshop'),
        Runs(pid='LiMason', eid='093022hs_workshop'),
        Runs(pid='AvGreene', eid='100722hs_workshop'),
        Runs(pid='AiHayes', eid='100722hs_workshop'),
        Runs(pid='IsIngram', eid='041322hs_workshop'),
        Runs(pid='MaSmith1', eid='041322hs_workshop'),
        Runs(pid='LuJensen', eid='031622hs_workshop'),
        Runs(pid='IsIngram', eid='031622hs_workshop'),
        Runs(pid='AbStewart', eid='100622hs_workshop'),
        Runs(pid='MiKeller', eid='100622hs_workshop'),
        Runs(pid='EtLawson', eid='111822hs_service'),
        Runs(pid='HaMitchell', eid='111822hs_service'),
        Runs(pid='OlNelson', eid='111822hs_service'),
        Runs(pid='IsIngram', eid='051823hs_service'),
        Runs(pid='AmOwens', eid='051823hs_service'),
        Runs(pid='ElParker', eid='051823hs_service'),
        Runs(pid='WiWallace', eid='110422hs_retreat'),
        Runs(pid='EvQuinn', eid='110422hs_retreat'),
        Runs(pid='ElParker', eid='110422hs_retreat'),
        Runs(pid='JaReynolds', eid='110422hs_retreat'),
        Runs(pid='AbStewart', eid='110422hs_retreat'),
        Runs(pid='ScYoung', eid='121722hs_other'),
        Runs(pid='BeTurner', eid='032323hs_retreat'),
        Runs(pid='ChVaughn', eid='032323hs_retreat'),
        Runs(pid='WiWallace', eid='032323hs_retreat'),
        Runs(pid='HeZimmerman', eid='121722hs_other'),
        Runs(pid='GrHarrison', eid='102822co_workshop'),
        Runs(pid='AlDixon', eid='102822co_workshop'),
        Runs(pid='ScYoung', eid='120922co_service'),
        Runs(pid='LiMason', eid='120922co_service'),
        Runs(pid='SaPorter', eid='021023co_service'),
        Runs(pid='ScYoung', eid='021023co_service'),
        Runs(pid='EtLawson', eid='032323co_service'),
        Runs(pid='LiMason', eid='032323co_service'),
        Runs(pid='DaSanders', eid='011323co_retreat'),
        Runs(pid='ZoWarren', eid='011323co_retreat'),
        Runs(pid='HaMitchell', eid='042023co_retreat'),
        Runs(pid='CaHughes', eid='042023co_retreat'),
        Runs(pid='ElRoss', eid='110622co_other'),
        Runs(pid='DaSanders', eid='110622co_other'),
        Runs(pid='IsIngram', eid='032623co_other'),
        Runs(pid='ChVaughn', eid='032623co_other'),
        Runs(pid='JaReynolds', eid='042823co_other'),
        Runs(pid='ElParker', eid='042823co_other'),
        Runs(pid='HeZimmerman', eid='042823co_other'),
    ]

    # Attends
    sample_attends = [
        Attends(sid='ChAnderson', eid='093022ms_wksp'),
        Attends(sid='AvAnderson', eid='012023ms_wksp'),
        Attends(sid='AnEllis', eid='121622ms_service'),
        Attends(sid='JaMorris', eid='093022hs_workshop'),
        Attends(sid='LoShaw', eid='100722hs_workshop'),
        Attends(sid='HaMcguire', eid='041322hs_workshop'),
        Attends(sid='AvBrown', eid='031622hs_workshop'),
        Attends(sid='KaFleming', eid='100622hs_workshop'),
        Attends(sid='EmDavis', eid='111822hs_service'),
        Attends(sid='MaHudson', eid='051823hs_service'),
        Attends(sid='LeYates', eid='110422hs_retreat'),
        Attends(sid='BrMitchell', eid='032323hs_retreat'),
        Attends(sid='JaLee', eid='121722hs_other'),
        Attends(sid='FaCasey', eid='102822co_workshop'),
        Attends(sid='FaCasey', eid='120922co_service'),
        Attends(sid='MaBecker', eid='021023co_service'),
        Attends(sid='BrMitchell', eid='032323co_service'),
        Attends(sid='LiWood', eid='011323co_retreat'),
        Attends(sid='DaCarter', eid='042023co_retreat'),
        Attends(sid='LoMiller', eid='110622co_other'),
        Attends(sid='ZaParker', eid='032623co_other'),
        Attends(sid='MaRoberts', eid='042823co_other'),
        Attends(sid='JaMorris', eid='093022ms_wksp'),
        Attends(sid='ChAnderson', eid='012023ms_wksp'),
        Attends(sid='EmDavis', eid='121622ms_service'),
        Attends(sid='ChAnderson', eid='093022hs_workshop'),
        Attends(sid='JaMoore', eid='100722hs_workshop'),
        Attends(sid='ClHammond', eid='041322hs_workshop'),
        Attends(sid='OlBrown', eid='031622hs_workshop'),
        Attends(sid='AnEllis', eid='100622hs_workshop'),
        Attends(sid='CeCollier', eid='111822hs_service'),
        Attends(sid='KaFleming', eid='051823hs_service'),
        Attends(sid='SoParker', eid='110422hs_retreat'),
        Attends(sid='SaGardner', eid='032323hs_retreat'),
        Attends(sid='ElYoung', eid='121722hs_other'),
        Attends(sid='CaFlores', eid='102822co_workshop'),
        Attends(sid='NoClark', eid='120922co_service'),
        Attends(sid='ZoCooper', eid='021023co_service'),
        Attends(sid='WiHarris', eid='032323co_service'),
        Attends(sid='SoMorgan', eid='011323co_retreat'),
    ]

    # Helps
    sample_helps = [
        Helps(vid='V01', eid='093022hs_workshop'),
        Helps(vid='V05', eid='102822co_workshop'),
        Helps(vid='V10', eid='032323co_service'),
        Helps(vid='V08', eid='110622co_other'),
        Helps(vid='V03', eid='042823co_other'),
        Helps(vid='V01', eid='102822co_workshop'),
        Helps(vid='V10', eid='042823co_other'),
        Helps(vid='V08', eid='032323co_service'),
        Helps(vid='V08', eid='110422hs_retreat'),
        Helps(vid='V03', eid='100722hs_workshop'),
    ]

# Commit the changes to the database
    #session.add_all(sample_centers)
    #session.add_all(sample_students)
    #session.add_all(sample_volunteers)
    #session.add_all(sample_perm_staff)
    #session.add_all(sample_classes)
    #session.add_all(sample_events)
    #session.add_all(sample_helps)
    #session.add_all(sample_runs)
    #session.add_all(sample_takes)
    #session.add_all(sample_teaches)
    #session.add_all(sample_attends)


    session.commit()


# Queries 
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Max
eventAttendeesAndStaff = (
    session.query(
        Event.eid.label('EventID'),
        Event.ename.label('EventName'),
        func.count(func.distinct(Attends.sid)).label('numberOfAttendees'),
        func.count(func.distinct(Runs.pid)).label('numberOfPermStaff')
    )
    .join(Attends, Attends.eid == Event.eid)
    .join(Runs, Runs.eid == Event.eid)
    .group_by(Event.eid, Event.ename)
    .order_by(func.count(func.distinct(Attends.sid)).desc())
)

print('\n#Query: eventAttendeesAndStaff (Max)') 
for row in eventAttendeesAndStaff:
    print(
        f"EventID: {row.EventID}, EventName: {row.EventName}, "
        f"numberOfAttendees: {row.numberOfAttendees}, numberOfPermStaff: {row.numberOfPermStaff}"
    )

# Rachel
popularTopics = ( 
    session.query( 
        Center.cenname.label("CenterName"), 
        Class.ctopic.label("ClassTopic"), 
        func.count(func.distinct(Student.sid)).label('num_students') 
    ) 
    .join(Class, Class.cenid == Center.cenid) 
    .join(Takes, Takes.cid == Class.cid) 
    .join(Student, Student.sid == Takes.sid) 
    .group_by(Center.cenid, Center.cenname, Class.ctopic) 
    .order_by(func.count(Student.sid).desc()) 
    .limit(10) 
) 

print('\n#Query: popularTopics (Rachel)#') 
for row in popularTopics: 
    print( 
        f"CenterName: {row.CenterName}, ClassTopic: {row.ClassTopic}, num_students:{row.num_students}" 
    ) 

# Taylor 
distinctStudentsAttendingClasses = ( 
    select( 
        Center.cenname, 
        Class.clevel, 
        func.count(func.distinct(Takes.sid)).label("student_count") 
        ) 
    .join(Class, Center.cenid == Class.cenid)  
    .join(Takes, Class.cid == Takes.cid)  
    .group_by(Center.cenid, Center.cenname, Class.clevel) 
    #order by descending student_count, then center name 
    .order_by(desc(func.count(func.distinct(Takes.sid))), Center.cenname)  
    ) 

print('\n#Query: DistinctStudentsAttendingClasses (Taylor)#')  
student_counts = session.execute(distinctStudentsAttendingClasses) 
for entry in student_counts: 
    print( 
        f"CenterName: {entry.cenname}, ClassLevel: {entry.clevel}, DistinctStudents: {entry.student_count}" 
        )
    
# David 
eventVolunteer = ( 
    select( 
        Event.ename, 
        Volunteer.vid, 
        Volunteer.vfirst, 
        Volunteer.vtrainstatus, 
        Volunteer.vphonenumber, 
    )
    .join(Helps, Volunteer.vid == Helps.vid) 
    .join(Event, Helps.eid == Event.eid) 
    .order_by(Volunteer.vfirst.asc()) 
) 

print('\n#Query: eventVolunteer (David)#') 
event_volunteers = session.execute(eventVolunteer)  
for entry in event_volunteers:  
    print(f"Eventname: {entry.ename},VolunteerID: {entry.vid}, VolunteerFirstName: {entry.vfirst}, VolunteerTrainStatus: {entry.vtrainstatus} VolunteerPhoneNumber: {entry.vphonenumber}") 

 
# Kadin
permStaffTeaches = ( 
    session.query( 
        PermStaff.pid,  
        PermStaff.pfirst, 
        PermStaff.plast, 
        func.count(Teaches.cid).label('count') 
    ) 

    .join(Teaches, Teaches.pid == PermStaff.pid)  
    .filter(PermStaff.ptrainstatus == 'good') 
    .group_by(PermStaff.pid, PermStaff.pfirst, PermStaff.plast)  
    .order_by(func.count(Teaches.cid).desc()) 
    .all() 
) 

print('\n#Query: permStaffTeaches (Kadin)#') 
for entry in permStaffTeaches: 
    print(f"PermStaffID: {entry.pid}, PermStaffFirstName: {entry.pfirst}, PermStaffLastName: {entry.plast}, " 
          f"Count: {entry.count}" 
          ) 

 