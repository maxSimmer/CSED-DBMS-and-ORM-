
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, CHAR, Date, CheckConstraint, create_engine, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session

Base = declarative_base()

class Center(Base):
    __tablename__ = 'Center'

    cenID: Mapped[str] = mapped_column(String(2), primary_key=True)
    cenName: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Center(cenID={self.cenID!r}, cenName={self.cenName!r})"

class Student(Base):
    __tablename__ = 'Student'

    sID: Mapped[str] = mapped_column(String, primary_key=True)
    sFirst: Mapped[str] = mapped_column(String, nullable=False)
    sLast: Mapped[str] = mapped_column(String, nullable=False)
    sPhoneNumber: Mapped[str] = mapped_column(String, nullable=False)
    sBday: Mapped[Date] = mapped_column(Date, nullable=False)
    sLevel: Mapped[str] = mapped_column(String(2), nullable=False, server_default='co')
    sLeadership: Mapped[Optional[str]] = mapped_column(String)
    sParentAlum: Mapped[Optional[str]] = mapped_column(String)
    sEmergencyPhone: Mapped[str] = mapped_column(String, nullable=False)
    cenID: Mapped[str] = mapped_column(String(2), ForeignKey('Center.cenID'), nullable=False)
    center: Mapped["Center"] = relationship('Center')

    __table_args__ = (
        CheckConstraint('sLevel IN ("co", "hs", "ms", "ot")', name='check_sLevel'),
    )

    def __repr__(self) -> str:
        return (
            f"Student(sID={self.sID!r}, sFirst={self.sFirst!r}, sLast={self.sLast!r}, "
            f"sPhoneNumber={self.sPhoneNumber!r}, sBday={self.sBday!r}, sLevel={self.sLevel!r}, "
            f"sLeadership={self.sLeadership!r}, sParentAlum={self.sParentAlum!r}, "
            f"sEmergencyPhone={self.sEmergencyPhone!r}, cenID={self.cenID!r})"
        )

class Class(Base):
    __tablename__ = 'Class'

    cID: Mapped[str] = mapped_column(String, primary_key=True)
    cLevel: Mapped[str] = mapped_column(String(2), nullable=False)
    cDate: Mapped[Date] = mapped_column(Date, nullable=False)
    cTopic: Mapped[str] = mapped_column(String, nullable=False)
    cenID: Mapped[str] = mapped_column(String(2), ForeignKey('Center.cenID'), nullable=False)
    center: Mapped["Center"] = relationship('Center')

    def __repr__(self) -> str:
        return f"Class(cID={self.cID!r}, cLevel={self.cLevel!r}, cDate={self.cDate!r}, cTopic={self.cTopic!r}, cenID={self.cenID!r})"

class PermStaff(Base):
    __tablename__ = 'PermStaff'

    pID: Mapped[str] = mapped_column(String, primary_key=True)
    pFirst: Mapped[str] = mapped_column(String, nullable=False)
    pLast: Mapped[str] = mapped_column(String, nullable=False)
    pEmail: Mapped[str] = mapped_column(String, nullable=False)
    pPhoneNumber: Mapped[str] = mapped_column(String(12), nullable=False)
    pTrainStatus: Mapped[str] = mapped_column(String, nullable=False)
    pTrainExp: Mapped[Optional[Date]] = mapped_column(Date)
    cenID: Mapped[str] = mapped_column(String(2), ForeignKey('Center.cenID'), nullable=False)
    center: Mapped["Center"] = relationship('Center')

    def __repr__(self) -> str:
        return (
            f"PermStaff(pID={self.pID!r}, pFirst={self.pFirst!r}, pLast={self.pLast!r}, "
            f"pEmail={self.pEmail!r}, pPhoneNumber={self.pPhoneNumber!r}, "
            f"pTrainStatus={self.pTrainStatus!r}, pTrainExp={self.pTrainExp!r}, cenID={self.cenID!r})"
        )

class Volunteer(Base):
    __tablename__ = 'Volunteer'

    vID: Mapped[str] = mapped_column(String, primary_key=True)
    vFirst: Mapped[str] = mapped_column(String, nullable=False)
    vLast: Mapped[str] = mapped_column(String, nullable=False)
    vPhoneNumber: Mapped[str] = mapped_column(String(12), nullable=False)
    vEmail: Mapped[str] = mapped_column(String, nullable=False)
    vTrainStatus: Mapped[Optional[str]] = mapped_column(String)
    vTrainExp: Mapped[Optional[Date]] = mapped_column(Date)

    def __repr__(self) -> str:
        return (
            f"Volunteer(vID={self.vID!r}, vFirst={self.vFirst!r}, vLast={self.vLast!r}, "
            f"vPhoneNumber={self.vPhoneNumber!r}, vEmail={self.vEmail!r}, "
            f"vTrainStatus={self.vTrainStatus!r}, vTrainExp={self.vTrainExp!r})"
        )

class Event(Base):
    __tablename__ = 'Event'

    eID: Mapped[str] = mapped_column(String, primary_key=True)
    eLocation: Mapped[str] = mapped_column(String, nullable=False)
    eName: Mapped[str] = mapped_column(String, nullable=False)
    eDate: Mapped[Date] = mapped_column(Date, nullable=False)
    eAudience: Mapped[CHAR] = mapped_column(CHAR(2), nullable=False)
    eCategory: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return (
            f"Event(eID={self.eID!r}, eLocation={self.eLocation!r}, eName={self.eName!r}, "
            f"eDate={self.eDate!r}, eAudience={self.eAudience!r}, eCategory={self.eCategory!r})"
        )

class Takes(Base):
    __tablename__ = 'Takes'

    cID: Mapped[str] = mapped_column(String, ForeignKey('Class.cID'), primary_key=True)
    sID: Mapped[str] = mapped_column(String, ForeignKey('Student.sID'), primary_key=True)
    student: Mapped["Student"] = relationship('Student')
    class_: Mapped["Class"] = relationship('Class')

    def __repr__(self) -> str:
        return f"Takes(cID={self.cID!r}, sID={self.sID!r})"

class Teaches(Base):
    __tablename__ = 'Teaches'

    cID: Mapped[str] = mapped_column(String, ForeignKey('Class.cID'), primary_key=True)
    pID: Mapped[str] = mapped_column(String, ForeignKey('PermStaff.pID'), primary_key=True)
    permstaff: Mapped["PermStaff"] = relationship('PermStaff')
    class_: Mapped["Class"] = relationship('Class')

    def __repr__(self) -> str:
        return f"Teaches(cID={self.cID!r}, pID={self.pID!r})"

class Runs(Base):
    __tablename__ = 'Runs'

    pID: Mapped[str] = mapped_column(String, ForeignKey('PermStaff.pID'), primary_key=True)
    eID: Mapped[str] = mapped_column(String, ForeignKey('Event.eID'), primary_key=True)
    permstaff: Mapped["PermStaff"] = relationship('PermStaff')
    event: Mapped["Event"] = relationship('Event')

    def __repr__(self) -> str:
        return f"Runs(pID={self.pID!r}, eID={self.eID!r})"

class Attends(Base):
    __tablename__ = 'Attends'

    sID: Mapped[str] = mapped_column(String, ForeignKey('Student.sID'), primary_key=True)
    eID: Mapped[str] = mapped_column(String, ForeignKey('Event.eID'), primary_key=True)
    student: Mapped["Student"] = relationship('Student')
    event: Mapped["Event"] = relationship('Event')

    def __repr__(self) -> str:
        return f"Attends(sID={self.sID!r}, eID={self.eID!r})"

class Helps(Base):
    __tablename__ = 'Helps'

    vID: Mapped[str] = mapped_column(String, ForeignKey('Volunteer.vID'), primary_key=True)
    eID: Mapped[str] = mapped_column(String, ForeignKey('Event.eID'), primary_key=True)
    volunteer: Mapped["Volunteer"] = relationship('Volunteer')
    event: Mapped["Event"] = relationship('Event')

    def __repr__(self) -> str:
        return f"Helps(vID={self.vID!r}, eID={self.eID!r})"

# Create SQLite database in memory
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a session
session = Session(engine)

#Insert Data
with Session(engine) as session:
     
    sample_centers = [
        Center(cenID='EL', cenName='Elms'),
        Center(cenID='FG', cenName='Forest Glen'),
        Center(cenID='GR', cenName='Grove'),
        Center(cenID='LD', cenName='Lindell'),
        Center(cenID='PW', cenName='Petawa'),
        Center(cenID='SB', cenName='Shellbourne'),
        Center(cenID='SL', cenName='Sherlake'),
        Center(cenID='SH', cenName='Southold'),
    ]

    # Student
    sample_students = [
        Student(sID='LeKoch', sFirst='Leah', sLast='Koch', sPhoneNumber='331-336-8319', sBday='01/05/05', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='738-495-2160', cenID='EL'),
        Student(sID='SaJohnson', sFirst='Sarah', sLast='Johnson', sPhoneNumber='847-874-3158', sBday='03/26/01', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='624-809-7315', cenID='EL'),
        Student(sID='RyWilliams', sFirst='Ryan', sLast='Williams', sPhoneNumber='331-924-7168', sBday='09/15/01', sLevel='co', sLeadership=None, sParentAlum='yes', sEmergencyPhone='583-672-9140', cenID='EL'),
        Student(sID='EmDavis', sFirst='Emily', sLast='Davis', sPhoneNumber='312-565-0293', sBday='06/02/02', sLevel='co', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='459-218-6370', cenID='EL'),
        Student(sID='DaMartinez', sFirst='Daniel', sLast='Martinez', sPhoneNumber='618-947-1162', sBday='07/14/03', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='726-493-5180', cenID='EL'),
        Student(sID='OlSmith', sFirst='Olivia', sLast='Smith', sPhoneNumber='708-479-2157', sBday='12/13/01', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='362-840-1597', cenID='EL'),
        Student(sID='MaTaylor', sFirst='Matthew', sLast='Taylor', sPhoneNumber='773-466-6844', sBday='08/24/01', sLevel='co', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='950-286-4713', cenID='EL'),
        Student(sID='AvBrown', sFirst='Ava', sLast='Brown', sPhoneNumber='847-647-9798', sBday='10/05/04', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='817-496-3250', cenID='EL'),
        Student(sID='AlLee', sFirst='Alexander', sLast='Lee', sPhoneNumber='331-805-3950', sBday='11/29/02', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='204-736-9815', cenID='EL'),
        Student(sID='ChAnderson', sFirst='Chloe', sLast='Anderson', sPhoneNumber='312-384-6007', sBday='01/12/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='675-892-3140', cenID='GR'),
        Student(sID='BeWilson', sFirst='Ben', sLast='Wilson', sPhoneNumber='847-256-5819', sBday='02/05/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='384-762-9150', cenID='GR'),
        Student(sID='MiClark', sFirst='Mia', sLast='Clark', sPhoneNumber='618-184-7893', sBday='03/20/05', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='123-450-8976', cenID='GR'),
        Student(sID='SaWhite', sFirst='Samuel', sLast='White', sPhoneNumber='331-798-6579', sBday='04/08/05', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='892-731-6450', cenID='GR'),
        Student(sID='ChHall', sFirst='Charlotte', sLast='Hall', sPhoneNumber='618-670-1205', sBday='05/16/06', sLevel='hs', sLeadership=None, sParentAlum='yes', sEmergencyPhone='657-234-1890', cenID='GR'),
        Student(sID='AmRodriguez', sFirst='Amelia', sLast='Rodriguez', sPhoneNumber='224-889-4751', sBday='06/25/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='941-582-7306', cenID='GR'),
        Student(sID='HeAdams', sFirst='Henry', sLast='Adams', sPhoneNumber='312-431-9277', sBday='07/09/05', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='392-687-4150', cenID='GR'),
        Student(sID='NoMitchell', sFirst='Noah', sLast='Mitchell', sPhoneNumber='630-675-4148', sBday='08/14/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='546-123-7890', cenID='GR'),
        Student(sID='LiGreen', sFirst='Lily', sLast='Green', sPhoneNumber='630-675-4148', sBday='09/02/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='289-456-1073', cenID='GR'),
        Student(sID='JaMoore', sFirst='James', sLast='Moore', sPhoneNumber='773-971-9466', sBday='10/18/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='810-946-2357', cenID='GR'),
        Student(sID='SoParker', sFirst='Sofia', sLast='Parker', sPhoneNumber='224-416-4139', sBday='11/27/05', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='631-487-5290', cenID='GR'),
        Student(sID='LiWilson', sFirst='Liam', sLast='Wilson', sPhoneNumber='847-795-4328', sBday='08/15/09', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='407-895-3621', cenID='GR'),
        Student(sID='WiHarris', sFirst='William', sLast='Harris', sPhoneNumber='708-778-0943', sBday='11/03/09', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='263-750-8149', cenID='GR'),
        Student(sID='IsRodriguez', sFirst='Isabella', sLast='Rodriguez', sPhoneNumber='618-215-1850', sBday='03/22/10', sLevel='ms', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='859-234-1760', cenID='GR'),
        Student(sID='JaThomas', sFirst='Jackson', sLast='Thomas', sPhoneNumber='630-914-3122', sBday='07/09/11', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='512-406-7983', cenID='GR'),
        Student(sID='MiSmith', sFirst='Michael', sLast='Smith', sPhoneNumber='312-385-6097', sBday='10/12/10', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='746-931-5208', cenID='GR'),
        Student(sID='OlBrown', sFirst='Olivia', sLast='Brown', sPhoneNumber='485-726-9134', sBday='01/05/09', sLevel='ms', sLeadership=None, sParentAlum='yes', sEmergencyPhone='372-916-5840', cenID='GR'),
        Student(sID='WiTaylor', sFirst='William', sLast='Taylor', sPhoneNumber='629-384-7150', sBday='05/18/10', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='981-734-6025', cenID='GR'),
        Student(sID='AvAnderson', sFirst='Ava', sLast='Anderson', sPhoneNumber='314-902-8765', sBday='09/30/10', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='451-820-3796', cenID='GR'),
        Student(sID='BeLee', sFirst='Benjamin', sLast='Lee', sPhoneNumber='572-913-4680', sBday='12/08/09', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='617-482-3905', cenID='GR'),
        Student(sID='ZoCooper', sFirst='Zoe', sLast='Cooper', sPhoneNumber='718-649-2053', sBday='06/08/08', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='586-042-3179', cenID='PW'),
        Student(sID='LoWard', sFirst='Logan', sLast='Ward', sPhoneNumber='109-785-4326', sBday='08/24/05', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='295-607-3841', cenID='PW'),
        Student(sID='ViMurphy', sFirst='Victoria', sLast='Murphy', sPhoneNumber='587-364-1029', sBday='03/17/08', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='730-149-8256', cenID='PW'),
        Student(sID='JaStewart', sFirst='Jackson', sLast='Stewart', sPhoneNumber='236-458-9701', sBday='10/29/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='165-429-7380', cenID='PW'),
        Student(sID='EmRivera', sFirst='Emma', sLast='Rivera', sPhoneNumber='890-612-3475', sBday='01/14/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='493-176-2805', cenID='PW'),
        Student(sID='DaCarter', sFirst='Daniel', sLast='Carter', sPhoneNumber='456-210-7893', sBday='07/05/07', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='714-085-2369', cenID='PW'),
        Student(sID='AdReed', sFirst='Addison', sLast='Reed', sPhoneNumber='721-098-4365', sBday='12/25/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='369-814-5270', cenID='PW'),
        Student(sID='AnRoss', sFirst='Andrew', sLast='Ross', sPhoneNumber='304-917-5826', sBday='05/02/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='872-301-4965', cenID='PW'),
        Student(sID='ElYoung', sFirst='Ella', sLast='Young', sPhoneNumber='638-574-2901', sBday='02/09/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='504-972-6183', cenID='PW'),
        Student(sID='CaMitchell', sFirst='Caleb', sLast='Mitchell', sPhoneNumber='549-302-6871', sBday='11/12/07', sLevel='hs', sLeadership=None, sParentAlum='yes', sEmergencyPhone='610-934-8275', cenID='PW'),
        Student(sID='LiWood', sFirst='Lily', sLast='Wood', sPhoneNumber='765-219-8340', sBday='09/22/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='283-650-1794', cenID='PW'),
        Student(sID='LiScott', sFirst='Liam', sLast='Scott', sPhoneNumber='823-705-6491', sBday='04/18/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='971-245-8063', cenID='PW'),
        Student(sID='AbMorris', sFirst='Abigail', sLast='Morris', sPhoneNumber='193-284-5067', sBday='06/29/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='376-289-5401', cenID='SB'),
        Student(sID='ZaParker', sFirst='Zach', sLast='Parker', sPhoneNumber='408-576-3921', sBday='08/14/07', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='219-674-8503', cenID='SB'),
        Student(sID='ErHayes', sFirst='Ericka', sLast='Hayes', sPhoneNumber='796-125-8340', sBday='03/07/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='465-312-7890', cenID='SB'),
        Student(sID='EmSullivan', sFirst='Emily', sLast='Sullivan', sPhoneNumber='678-149-2053', sBday='10/08/05', sLevel='hs', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='850-129-3467', cenID='SB'),
        Student(sID='SoThompson', sFirst='Sophia', sLast='Thompson', sPhoneNumber='295-748-6130', sBday='01/21/09', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='792-438-5016', cenID='SB'),
        Student(sID='JaMorris', sFirst='Jackson', sLast='Morris', sPhoneNumber='437-289-6105', sBday='07/19/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='136-724-5980', cenID='SB'),
        Student(sID='MiStewart', sFirst='Mia', sLast='Stewart', sPhoneNumber='180-725-9364', sBday='12/11/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='408-917-6253', cenID='SB'),
        Student(sID='MaHernandez', sFirst='Marie', sLast='Hernandez', sPhoneNumber='610-245-7983', sBday='05/26/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='567-812-4309', cenID='SB'),
        Student(sID='OwCarter', sFirst='Owen', sLast='Carter', sPhoneNumber='954-682-3017', sBday='02/15/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='305-246-9817', cenID='SB'),
        Student(sID='JoPeterson', sFirst='Joseph', sLast='Peterson', sPhoneNumber='276-804-9135', sBday='11/10/09', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='924-871-3560', cenID='SB'),
        Student(sID='NiJohnson', sFirst='Nicholas', sLast='Johnson', sPhoneNumber='542-970-1863', sBday='09/05/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='738-019-4652', cenID='SB'),
        Student(sID='LuWilson', sFirst='Luke', sLast='Wilson', sPhoneNumber='832-167-4950', sBday='04/10/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='632-184-7905', cenID='SB'),
        Student(sID='BrMitchell', sFirst='Brayden', sLast='Mitchell', sPhoneNumber='691-237-8045', sBday='02/14/09', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='514-627-8309', cenID='SL'),
        Student(sID='NoClark', sFirst='Nora', sLast='Clark', sPhoneNumber='174-609-2385', sBday='06/04/10', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='697-230-4851', cenID='SL'),
        Student(sID='JaLee', sFirst='Jaxon', sLast='Lee', sPhoneNumber='365-892-4701', sBday='08/27/09', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='890-245-3617', cenID='SL'),
        Student(sID='LiNyugen', sFirst='Lisa', sLast='Nyugen', sPhoneNumber='972-830-1456', sBday='11/11/10', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='345-769-1820', cenID='SL'),
        Student(sID='DaMontgomery', sFirst='David', sLast='Montgomery', sPhoneNumber='536-478-9120', sBday='04/07/09', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='271-398-4605', cenID='SL'),
        Student(sID='StHoffman', sFirst='Stephanie', sLast='Hoffman', sPhoneNumber='890-372-5146', sBday='07/20/11', sLevel='ms', sLeadership=None, sParentAlum='yes', sEmergencyPhone='506-738-1294', cenID='SL'),
        Student(sID='StGuzman', sFirst='Steven', sLast='Guzman', sPhoneNumber='140-785-9623', sBday='09/02/09', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='928-453-1760', cenID='SL'),
        Student(sID='BrRodgers', sFirst='Brett', sLast='Rodgers', sPhoneNumber='862-195-3470', sBday='12/31/10', sLevel='ms', sLeadership='yes', sParentAlum=None, sEmergencyPhone='763-491-8250', cenID='SL'),
        Student(sID='LoShaw', sFirst='Lorena', sLast='Shaw', sPhoneNumber='429-083-6715', sBday='03/01/09', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='123-590-4678', cenID='SL'),
        Student(sID='SaGardner', sFirst='Sara', sLast='Gardner', sPhoneNumber='713-690-2458', sBday='05/12/10', sLevel='ms', sLeadership=None, sParentAlum=None, sEmergencyPhone='419-587-2360', cenID='SL'),
        Student(sID='LoCunningham', sFirst='Louise', sLast='Cunningham', sPhoneNumber='807-912-3465', sBday='06/27/06', sLevel='hs', sLeadership=None, sParentAlum='yes', sEmergencyPhone='874-062-9315', cenID='SL'),
        Student(sID='AnEllis', sFirst='Andrew', sLast='Ellis', sPhoneNumber='346-981-2570', sBday='08/09/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='965-432-0781', cenID='SL'),
        Student(sID='ClHammond', sFirst='Clara', sLast='Hammond', sPhoneNumber='215-876-3490', sBday='03/27/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='346-281-0975', cenID='SL'),
        Student(sID='TaOsborne', sFirst='Tanya', sLast='Osborne', sPhoneNumber='574-308-1629', sBday='10/04/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='283-961-4750', cenID='SL'),
        Student(sID='JoHopkins', sFirst='Joey', sLast='Hopkins', sPhoneNumber='968-145-7320', sBday='01/30/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='507-984-2163', cenID='SL'),
        Student(sID='EmSchneider', sFirst='Emma', sLast='Schneider', sPhoneNumber='341-205-7968', sBday='07/08/08', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='619-827-5304', cenID='SL'),
        Student(sID='ArJensen', sFirst='Arthur', sLast='Jensen', sPhoneNumber='528-467-9130', sBday='12/15/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='652-140-3897', cenID='SL'),
        Student(sID='CaFlores', sFirst='Carroll', sLast='Flores', sPhoneNumber='629-781-0435', sBday='05/15/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='430-789-2165', cenID='SL'),
        Student(sID='CeCollier', sFirst='Cecil', sLast='Collier', sPhoneNumber='195-634-8720', sBday='02/23/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='728-391-0546', cenID='SL'),
        Student(sID='LeMorris', sFirst='Leslie', sLast='Morris', sPhoneNumber='478-921-6053', sBday='11/21/06', sLevel='hs', sLeadership='yes', sParentAlum=None, sEmergencyPhone='296-741-5380', cenID='SL'),
        Student(sID='JoJohnson', sFirst='John', sLast='Johnson', sPhoneNumber='573-629-1480', sBday='09/13/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='981-276-4305', cenID='SL'),
        Student(sID='PaWhite', sFirst='Paul', sLast='White', sPhoneNumber='204-789-6135', sBday='04/25/05', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='543-219-6780', cenID='SL'),
        Student(sID='LeYates', sFirst='Lela', sLast='Yates', sPhoneNumber='436-982-5701', sBday='06/02/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='205-964-1873', cenID='SL'),
        Student(sID='NoWarner', sFirst='Noah', sLast='Warner', sPhoneNumber='681-093-2475', sBday='08/31/06', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='486-321-0957', cenID='SH'),
        Student(sID='LeRuiz', sFirst='Lena', sLast='Ruiz', sPhoneNumber='903-817-6425', sBday='03/04/08', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='317-289-5046', cenID='SH'),
        Student(sID='FaCasey', sFirst='Faith', sLast='Casey', sPhoneNumber='372-546-8019', sBday='10/01/07', sLevel='hs', sLeadership=None, sParentAlum=None, sEmergencyPhone='950-428-3671', cenID='SH'),
        Student(sID='MaHudson', sFirst='Maria', sLast='Hudson', sPhoneNumber='615-794-0283', sBday='11/10/03', sLevel='co', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='760-348-1295', cenID='SH'),
        Student(sID='JaStevenson', sFirst='Jake', sLast='Stevenson', sPhoneNumber='287-415-0936', sBday='04/02/05', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='621-594-0837', cenID='SH'),
        Student(sID='CaBlake', sFirst='Carter', sLast='Blake', sPhoneNumber='549-861-2730', sBday='09/14/01', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='397-186-2450', cenID='SH'),
        Student(sID='MaRoberts', sFirst='Maria', sLast='Roberts', sPhoneNumber='209-781-3645', sBday='02/08/04', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='185-762-3490', cenID='SH'),
        Student(sID='MaMartinez', sFirst='Marta', sLast='Martinez', sPhoneNumber='836-241-9705', sBday='05/20/03', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='349-275-6108', cenID='SH'),
        Student(sID='OlBurns', sFirst='Olivia', sLast='Burns', sPhoneNumber='794-083-1625', sBday='08/17/05', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='702-918-4356', cenID='SH'),
        Student(sID='CaGrant', sFirst='Casey', sLast='Grant', sPhoneNumber='523-746-8901', sBday='12/31/02', sLevel='co', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='518-439-2760', cenID='SH'),
        Student(sID='KaFleming', sFirst='Karla', sLast='Fleming', sPhoneNumber='461-208-9375', sBday='07/05/04', sLevel='co', sLeadership='yes', sParentAlum='yes', sEmergencyPhone='864-207-9315', cenID='SH'),
        Student(sID='RoHunter', sFirst='Rosalie', sLast='Hunter', sPhoneNumber='972-431-6085', sBday='03/25/01', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='294-158-7603', cenID='SH'),
        Student(sID='HaMcguire', sFirst='Harper', sLast='Mcguire', sPhoneNumber='134-205-7896', sBday='10/13/03', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='637-819-2045', cenID='SH'),
        Student(sID='LoMiller', sFirst='Logan', sLast='Miller', sPhoneNumber='795-843-2610', sBday='01/03/05', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='970-582-3164', cenID='SH'),
        Student(sID='LuGomez', sFirst='Lucia', sLast='Gomez', sPhoneNumber='680-324-7915', sBday='06/09/02', sLevel='co', sLeadership='yes', sParentAlum=None, sEmergencyPhone='541-283-0976', cenID='SH'),
        Student(sID='KeFisher', sFirst='Kendra', sLast='Fisher', sPhoneNumber='215-479-3608', sBday='11/18/04', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='326-845-7190', cenID='SH'),
        Student(sID='MaBecker', sFirst='Mary', sLast='Becker', sPhoneNumber='769-804-2315', sBday='04/14/01', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='187-420-9365', cenID='SH'),
        Student(sID='SoMorgan', sFirst='Sofia', sLast='Morgan', sPhoneNumber='301-874-5926', sBday='09/28/03', sLevel='co', sLeadership=None, sParentAlum=None, sEmergencyPhone='913-684-2705', cenID='SH'),
    ]

    # Class

    
    sample_classes = [
        
        Class(cID='ELco101122', cLevel='co', cDate='10/11/22', cTopic='Cheerfulness', cenID='EL'),
        Class(cID='ELco110822', cLevel='co', cDate=('11/08/22'), cTopic='Working Well', cenID='EL'),
        Class(cID='ELco121322', cLevel='co', cDate=('12/13/22'), cTopic='Friendship', cenID='EL'),
        Class(cID='ELco011023', cLevel='co', cDate=('01/10/23'), cTopic='Fortitude', cenID='EL'),
        Class(cID='ELco021423', cLevel='co', cDate=('02/14/23'), cTopic='Justice', cenID='EL'),
        Class(cID='ELco031423', cLevel='co', cDate=('03/14/23'), cTopic='Temperance', cenID='EL'),
        Class(cID='ELco041123', cLevel='co', cDate=('04/11/23'), cTopic='Prudence', cenID='EL'),
        Class(cID='ELco050923', cLevel='co', cDate=('05/09/23'), cTopic='Leadership', cenID='EL'),
        Class(cID='GRhs091522', cLevel='hs', cDate=('09/15/22'), cTopic='Friendship', cenID='GR'),
        Class(cID='GRhs100622', cLevel='hs', cDate=('10/06/22'), cTopic='Courage', cenID='GR'),
        Class(cID='GRhs102022', cLevel='hs', cDate=('10/20/22'), cTopic='Study', cenID='GR'),
        Class(cID='GRhs110322', cLevel='hs', cDate=('11/03/22'), cTopic='Cheerfulness', cenID='GR'),
        Class(cID='GRhs111722', cLevel='hs', cDate=('11/17/22'), cTopic='Honesty', cenID='GR'),
        Class(cID='GRhs120122', cLevel='hs', cDate=('12/01/22'), cTopic='Leadership', cenID='GR'),
        Class(cID='GRhs011923', cLevel='hs', cDate=('01/19/23'), cTopic='Service', cenID='GR'),
        Class(cID='GRhs020223', cLevel='hs', cDate=('02/02/23'), cTopic='Prudence', cenID='GR'),
        Class(cID='GRhs021623', cLevel='hs', cDate=('02/16/23'), cTopic='Justice', cenID='GR'),
        Class(cID='GRhs030223', cLevel='hs', cDate=('03/02/23'), cTopic='Temperance', cenID='GR'),
        Class(cID='GRhs031623', cLevel='hs', cDate=('03/16/23'), cTopic='Fortitude', cenID='GR'),
        Class(cID='GRhs040623', cLevel='hs', cDate=('04/06/23'), cTopic='Respect', cenID='GR'),
        Class(cID='GRhs042023', cLevel='hs', cDate=('04/20/23'), cTopic='Motivation', cenID='GR'),
        Class(cID='GRhs050423', cLevel='hs', cDate=('05/04/23'), cTopic='Prayer', cenID='GR'),
        Class(cID='GRms091922', cLevel='ms', cDate=('09/19/22'), cTopic='Goal Setting', cenID='GR'),
        Class(cID='GRms101722', cLevel='ms', cDate=('10/17/22'), cTopic='Friendship', cenID='GR'),
        Class(cID='GRms112122', cLevel='ms', cDate=('11/21/22'), cTopic='Courage', cenID='GR'),
        Class(cID='GRms121922', cLevel='ms', cDate=('12/19/22'), cTopic='Study', cenID='GR'),
        Class(cID='GRms011623', cLevel='ms', cDate=('01/16/23'), cTopic='Cheerfulness', cenID='GR'),
        Class(cID='GRms022023', cLevel='ms', cDate=('02/20/23'), cTopic='Honesty', cenID='GR'),
        Class(cID='GRms032023', cLevel='ms', cDate=('03/20/23'), cTopic='Service', cenID='GR'),
        Class(cID='GRms041023', cLevel='ms', cDate=('04/10/23'), cTopic='Gratitude', cenID='GR'),
        Class(cID='PWhs091522', cLevel='hs', cDate=('09/15/22'), cTopic='Friendship', cenID='PW'),
        Class(cID='PWhs100622', cLevel='hs', cDate=('10/06/22'), cTopic='Courage', cenID='PW'),
        Class(cID='PWhs102722', cLevel='hs', cDate=('10/27/22'), cTopic='Study', cenID='PW'),
        Class(cID='PWhs110322', cLevel='hs', cDate=('11/03/22'), cTopic='Cheerfulness', cenID='PW'),
        Class(cID='PWhs111722', cLevel='hs', cDate=('11/17/22'), cTopic='Honesty', cenID='PW'),
        Class(cID='PWhs120122', cLevel='hs', cDate=('12/01/22'), cTopic='Leadership', cenID='PW'),
        Class(cID='PWhs011923', cLevel='hs', cDate=('01/19/23'), cTopic='Service', cenID='PW'),
        Class(cID='PWhs020223', cLevel='hs', cDate=('02/02/23'), cTopic='Prudence', cenID='PW'),
        Class(cID='PWhs021623', cLevel='hs', cDate=('02/16/23'), cTopic='Justice', cenID='PW'),
        Class(cID='PWhs030223', cLevel='hs', cDate=('03/02/23'), cTopic='Temperance', cenID='PW'),
        Class(cID='PWhs031623', cLevel='hs', cDate=('03/16/23'), cTopic='Fortitude', cenID='PW'),
        Class(cID='PWhs040623', cLevel='hs', cDate=('04/06/23'), cTopic='Respect', cenID='PW'),
        Class(cID='PWhs042023', cLevel='hs', cDate=('04/20/23'), cTopic='Motivation', cenID='PW'),
        Class(cID='PWhs050423', cLevel='hs', cDate=('05/04/23'), cTopic='Prayer', cenID='PW'),
        Class(cID='PWhs051823', cLevel='hs', cDate=('05/18/23'), cTopic='Gratitude', cenID='PW'),
        Class(cID='SBhs093022', cLevel='hs', cDate=('09/30/22'), cTopic='Friendship', cenID='SB'),
        Class(cID='SBhs102822', cLevel='hs', cDate=('10/28/22'), cTopic='Courage', cenID='SB'),
        Class(cID='SBhs111822', cLevel='hs', cDate=('11/18/22'), cTopic='Study', cenID='SB'),
        Class(cID='SBhs121622', cLevel='hs', cDate=('12/16/22'), cTopic='Cheerfulness', cenID='SB'),
        Class(cID='SBhs012723', cLevel='hs', cDate=('01/27/23'), cTopic='Leadership', cenID='SB'),
        Class(cID='SBhs022423', cLevel='hs', cDate=('02/24/23'), cTopic='Service', cenID='SB'),
        Class(cID='SBhs033123', cLevel='hs', cDate=('03/31/23'), cTopic='Respect', cenID='SB'),
        Class(cID='SBhs042823', cLevel='hs', cDate=('04/28/23'), cTopic='Motivation', cenID='SB'),
        Class(cID='SBhs052623', cLevel='hs', cDate=('05/26/23'), cTopic='Gratitude', cenID='SB'),
        Class(cID='SLhs101222', cLevel='hs', cDate=('10/12/22'), cTopic='Friendship', cenID='SL'),
        Class(cID='SLhs102622', cLevel='hs', cDate=('10/26/22'), cTopic='Study', cenID='SL'),
        Class(cID='SLhs110922', cLevel='hs', cDate=('11/09/22'), cTopic='Cheerfulness', cenID='SL'),
        Class(cID='SLhs112322', cLevel='hs', cDate=('11/23/22'), cTopic='Gratitude', cenID='SL'),
        Class(cID='SLhs121422', cLevel='hs', cDate=('12/14/22'), cTopic='Courage', cenID='SL'),
        Class(cID='SLhs011123', cLevel='hs', cDate=('01/11/23'), cTopic='Prudence', cenID='SL'),
        Class(cID='SLhs012523', cLevel='hs', cDate=('01/25/23'), cTopic='Justice', cenID='SL'),
        Class(cID='SLhs020823', cLevel='hs', cDate=('02/08/23'), cTopic='Temperance', cenID='SL'),
        Class(cID='SLhs022223', cLevel='hs', cDate=('02/22/23'), cTopic='Fortitude', cenID='SL'),
        Class(cID='SLhs030823', cLevel='hs', cDate=('03/08/23'), cTopic='Respect', cenID='SL'),
        Class(cID='SLhs032223', cLevel='hs', cDate=('03/22/23'), cTopic='Leadership', cenID='SL'),
        Class(cID='SLhs041223', cLevel='hs', cDate=('04/12/23'), cTopic='Service', cenID='SL'),
        Class(cID='SLhs041923', cLevel='hs', cDate=('04/19/23'), cTopic='Prayer', cenID='SL'),
        Class(cID='SLms092622', cLevel='ms', cDate=('09/26/22'), cTopic='Goal Setting', cenID='SL'),
        Class(cID='SLms102422', cLevel='ms', cDate=('10/24/22'), cTopic='Study', cenID='SL'),
        Class(cID='SLms112822', cLevel='ms', cDate=('11/28/22'), cTopic='Friendship', cenID='SL'),
        Class(cID='SLms121922', cLevel='ms', cDate=('12/19/22'), cTopic='Courage', cenID='SL'),
        Class(cID='SLms013023', cLevel='ms', cDate=('01/30/23'), cTopic='Cheerfulness', cenID='SL'),
        Class(cID='SLms022723', cLevel='ms', cDate=('02/27/23'), cTopic='Honesty', cenID='SL'),
        Class(cID='SLms032723', cLevel='ms', cDate=('03/27/23'), cTopic='Service', cenID='SL'),
        Class(cID='SLms042423', cLevel='ms', cDate=('04/24/23'), cTopic='Respect', cenID='SL'),
        Class(cID='SHhs090722', cLevel='hs', cDate=('09/07/22'), cTopic='Friendship', cenID='SH'),
        Class(cID='SHhs110222', cLevel='hs', cDate=('11/02/22'), cTopic='Study', cenID='SH'),
        Class(cID='SHhs010423', cLevel='hs', cDate=('01/04/23'), cTopic='Cheerfulness', cenID='SH'),
        Class(cID='SHhs030723', cLevel='hs', cDate=('03/07/23'), cTopic='Gratitude', cenID='SH'),
        Class(cID='SHhs050223', cLevel='hs', cDate=('05/02/23'), cTopic='Leadership', cenID='SH'),
        Class(cID='SHco101322', cLevel='co', cDate=('10/13/22'), cTopic='Working Well', cenID='SH'),
        Class(cID='SHco111022', cLevel='co', cDate=('11/10/22'), cTopic='Friendship', cenID='SH'),
        Class(cID='SHco120822', cLevel='co', cDate=('12/08/22'), cTopic='Fortitude', cenID='SH'),
        Class(cID='SHco020223', cLevel='co', cDate=('02/02/23'), cTopic='Justice', cenID='SH'),
        Class(cID='SHco030123', cLevel='co', cDate=('03/01/23'), cTopic='Temperance', cenID='SH'),
        Class(cID='SHco040523', cLevel='co', cDate=('04/05/23'), cTopic='Prudence', cenID='SH'),
        Class(cID='SHco050323', cLevel='co', cDate=('05/03/23'), cTopic='Leadership', cenID='SH')
    ]

    # PermStaff
    sample_perm_staff = [
        PermStaff(pID='MaSmith', pFirst='Margaret', pLast='Smith', pEmail='margaretsmith87@gmail.com', pPhoneNumber='773-432-1234', pTrainStatus='initiated', pTrainExp=None, cenID='EL'),
        PermStaff(pID='LiBennett', pFirst='Liam', pLast='Bennett', pEmail='liam.bennett_123@yahoo.com', pPhoneNumber='815-123-4567', pTrainStatus='good', pTrainExp='2024-08-09', cenID='EL'),
        PermStaff(pID='OlCarter', pFirst='Olivia', pLast='Carter', pEmail='oliviacarter22@hotmail.com', pPhoneNumber='773-234-5678', pTrainStatus='initiated', pTrainExp=None, cenID='EL'),
        PermStaff(pID='NoDavis', pFirst='Noah', pLast='Davis', pEmail='noah.davis2000@gmail.com', pPhoneNumber='773-432-1098', pTrainStatus='good', pTrainExp='2024-03-08', cenID='EL'),
        PermStaff(pID='EmEvans', pFirst='Emma', pLast='Evans', pEmail='e.evansofficial@gmail.com', pPhoneNumber='815-345-6789', pTrainStatus='initiated', pTrainExp=None, cenID='EL'),
        PermStaff(pID='JaFisher', pFirst='Jackson', pLast='Fisher', pEmail='jackson.fisher_99@yahoo.com', pPhoneNumber='773-876-5432', pTrainStatus='flag', pTrainExp='2023-07-02', cenID='EL'),
        PermStaff(pID='AvGreene', pFirst='Ava', pLast='Greene', pEmail='ava.greene_5678@hotmail.com', pPhoneNumber='815-987-6543', pTrainStatus='good', pTrainExp='2026-07-07', cenID='FG'),
        PermStaff(pID='AiHayes', pFirst='Aiden', pLast='Hayes', pEmail='aidenh345@gmail.com', pPhoneNumber='815-789-0123', pTrainStatus='initiated', pTrainExp=None, cenID='FG'),
        PermStaff(pID='IsIngram', pFirst='Isabella', pLast='Ingram', pEmail='isabella.ingram@outlook.com', pPhoneNumber='773-890-1234', pTrainStatus='good', pTrainExp='2024-09-06', cenID='FG'),
        PermStaff(pID='MaSmith1', pFirst='Mary', pLast='Smith', pEmail='m.smithofficial@gmail.com', pPhoneNumber='773-678-9012', pTrainStatus='initiated', pTrainExp=None, cenID='LD'),
        PermStaff(pID='LuJensen', pFirst='Lucas', pLast='Jensen', pEmail='lucas.jensen22@yahoo.com', pPhoneNumber='815-678-9012', pTrainStatus='good', pTrainExp='2024-07-25', cenID='LD'),
        PermStaff(pID='MiKeller', pFirst='Mia', pLast='Keller', pEmail='mia.keller_456@hotmail.com', pPhoneNumber='773-234-5678', pTrainStatus='initiated', pTrainExp=None, cenID='LD'),
        PermStaff(pID='EtLawson', pFirst='Ethan', pLast='Lawson', pEmail='ethan.lawson_789@gmail.com', pPhoneNumber='773-890-1234', pTrainStatus='good', pTrainExp='2026-08-12', cenID='LD'),
        PermStaff(pID='HaMitchell', pFirst='Harper', pLast='Mitchell', pEmail='harper.mitchell_321@yahoo.com', pPhoneNumber='815-789-0987', pTrainStatus='failed', pTrainExp=None, cenID='LD'),
        PermStaff(pID='OlNelson', pFirst='Oliver', pLast='Nelson', pEmail='o.nelsonofficial@gmail.com', pPhoneNumber='815-345-6789', pTrainStatus='good', pTrainExp='2024-11-30', cenID='LD'),
        PermStaff(pID='AmOwens', pFirst='Amelia', pLast='Owens', pEmail='amelia.owens_22@hotmail.com', pPhoneNumber='773-234-5678', pTrainStatus='good', pTrainExp='2026-02-07', cenID='PW'),
        PermStaff(pID='ElParker', pFirst='Elijah', pLast='Parker', pEmail='elijah.parker2001@yahoo.com', pPhoneNumber='773-678-9012', pTrainStatus='initiated', pTrainExp=None, cenID='PW'),
        PermStaff(pID='EvQuinn', pFirst='Evelyn', pLast='Quinn', pEmail='evelyn.quinnofficial@gmail.com', pPhoneNumber='815-678-9012', pTrainStatus='good', pTrainExp='2025-10-14', cenID='PW'),
        PermStaff(pID='JaReynolds', pFirst='James', pLast='Reynolds', pEmail='james_reynolds22@yahoo.com', pPhoneNumber='773-432-1098', pTrainStatus='good', pTrainExp='2024-10-12', cenID='PW'),
        PermStaff(pID='AbStewart', pFirst='Abigail', pLast='Stewart', pEmail='abigail.stewart_567@hotmail.com', pPhoneNumber='815-987-6543', pTrainStatus='initiated', pTrainExp=None, cenID='PW'),
        PermStaff(pID='BeTurner', pFirst='Benjamin', pLast='Turner', pEmail='benjamin_turner@gmail.com', pPhoneNumber='773-876-5432', pTrainStatus='good', pTrainExp='2025-02-21', cenID='PW'),
        PermStaff(pID='ChVaughn', pFirst='Charlotte', pLast='Vaughn', pEmail='c.vaughnofficial@yahoo.com', pPhoneNumber='815-123-4567', pTrainStatus='initiated', pTrainExp=None, cenID='SB'),
        PermStaff(pID='WiWallace', pFirst='William', pLast='Wallace', pEmail='william.wallace_123@hotmail.com', pPhoneNumber='815-789-0123', pTrainStatus='good', pTrainExp='2023-12-03', cenID='SB'),
        PermStaff(pID='ScYoung', pFirst='Scarlett', pLast='Young', pEmail='s.youngofficial@gmail.com', pPhoneNumber='773-432-1098', pTrainStatus='failed', pTrainExp=None, cenID='SB'),
        PermStaff(pID='HeZimmerman', pFirst='Henry', pLast='Zimmerman', pEmail='h.zimmerman_789@yahoo.com', pPhoneNumber='773-432-1234', pTrainStatus='good', pTrainExp='2025-11-27', cenID='SB'),
        PermStaff(pID='GrHarrison', pFirst='Grace', pLast='Harrison', pEmail='graceharrisonofficial@gmail.com', pPhoneNumber='773-890-1234', pTrainStatus='initiated', pTrainExp=None, cenID='SL'),
        PermStaff(pID='AlDixon', pFirst='Alexander', pLast='Dixon', pEmail='alexander_dixon22@hotmail.com', pPhoneNumber='815-123-4567', pTrainStatus='good', pTrainExp='2025-08-09', cenID='SL'),
        PermStaff(pID='LiMason', pFirst='Lily', pLast='Mason', pEmail='lily.mason_456@yahoo.com', pPhoneNumber='773-432-1098', pTrainStatus='flag', pTrainExp='2023-09-08', cenID='SL'),
        PermStaff(pID='SaPorter', pFirst='Samuel', pLast='Porter', pEmail='samuel.porterofficial@gmail.com', pPhoneNumber='773-234-5678', pTrainStatus='good', pTrainExp='2024-02-18', cenID='SL'),
        PermStaff(pID='ChReed', pFirst='Chloe', pLast='Reed', pEmail='chloe.reed_22@yahoo.com', pPhoneNumber='815-345-6789', pTrainStatus='initiated', pTrainExp=None, cenID='SL'),
        PermStaff(pID='DaSanders', pFirst='Daniel', pLast='Sanders', pEmail='daniel.sanders_123@hotmail.com', pPhoneNumber='773-678-9012', pTrainStatus='good', pTrainExp='2026-06-20', cenID='SL'),
        PermStaff(pID='ZoWarren', pFirst='Zoey', pLast='Warren', pEmail='zoey.warrenofficial@gmail.com', pPhoneNumber='815-789-0123', pTrainStatus='good', pTrainExp='2025-07-22', cenID='SL'),
        PermStaff(pID='CaHughes', pFirst='Caleb', pLast='Hughes', pEmail='caleb.hughes_567@yahoo.com', pPhoneNumber='773-876-5432', pTrainStatus='initiated', pTrainExp=None, cenID='SL'),
        PermStaff(pID='ElRoss', pFirst='Ella', pLast='Ross', pEmail='ella_ross22@hotmail.com', pPhoneNumber='815-987-6543', pTrainStatus='good', pTrainExp='2026-04-11', cenID='SH'),
        PermStaff(pID='MaPowell', pFirst='Mason', pLast='Powell', pEmail='mason.powellofficial@gmail.com', pPhoneNumber='773-432-1234', pTrainStatus='flag', pTrainExp='2023-05-28', cenID='SH'),
        PermStaff(pID='SoBennett', pFirst='Sofia', pLast='Bennett', pEmail='sofia.bennett_321@yahoo.com', pPhoneNumber='815-789-0123', pTrainStatus='good', pTrainExp='2023-12-12', cenID='SH')
    ]

    # Volunteer
    sample_volunteers = [
        Volunteer(vID='V01', vFirst='Jane', vLast='Angel', vPhoneNumber='333-444-5567', vEmail='janeangel1@gmail.com', vTrainStatus='good', vTrainExp='2024-10-16'),
        Volunteer(vID='V02', vFirst='David', vLast='Smith', vPhoneNumber='111-224-3378', vEmail='davidsmith@outlook.com', vTrainStatus='good', vTrainExp='2024-11-23'),
        Volunteer(vID='V03', vFirst='Angela', vLast='Precious', vPhoneNumber='208-447-5583', vEmail='angelaprecious3@hotmail.com', vTrainStatus='good', vTrainExp='2024-06-04'),
        Volunteer(vID='V04', vFirst='Leroy', vLast='Prescot', vPhoneNumber='305-456-7890', vEmail='leroyprescot14@gmail.com', vTrainStatus='good', vTrainExp='2025-02-24'),
        Volunteer(vID='V05', vFirst='Adam', vLast='Jake', vPhoneNumber='224-527-8765', vEmail='adamjake@msn.com', vTrainStatus='initiated', vTrainExp=None),
        Volunteer(vID='V06', vFirst='Logan', vLast='Peter', vPhoneNumber='220-657-7890', vEmail='loganpeter@outlook.com', vTrainStatus='good', vTrainExp='2024-08-19'),
        Volunteer(vID='V07', vFirst='Toby', vLast='Tyler', vPhoneNumber='451-567-6578', vEmail='tobytyler@gmail.com', vTrainStatus='initiated', vTrainExp=None),
        Volunteer(vID='V08', vFirst='Tyson', vLast='Chandler', vPhoneNumber='312-876-4521', vEmail='tysonchandler@msn.com', vTrainStatus='flag', vTrainExp='2024-09-14'),
        Volunteer(vID='V09', vFirst='Mary', vLast='Lovely', vPhoneNumber='512-489-0081', vEmail='marylovely@gmail.com', vTrainStatus='good', vTrainExp='2025-04-16'),
        Volunteer(vID='V10', vFirst='James', vLast='Richard', vPhoneNumber='444-012-6890', vEmail='jamesrichard12@outlook.com', vTrainStatus='good', vTrainExp='2024-07-15')
    ]

    # Event
    sample_events = [
        Event(eID='093022ms_wksp', eLocation='Grove', eName='Goal Setting', eDate='2022-09-30', eAudience='ms', eCategory='workshop'),
        Event(eID='012023ms_wksp', eLocation='Grove', eName='Study Techniques', eDate='2023-01-20', eAudience='ms', eCategory='workshop'),
        Event(eID='121622ms_service', eLocation='St. Anne''s', eName='Food Pantry', eDate='2022-12-16', eAudience='ms', eCategory='service'),
        Event(eID='093022hs_workshop', eLocation='Sherlake', eName='Optimal Work', eDate='2022-09-30', eAudience='hs', eCategory='workshop'),
        Event(eID='100722hs_workshop', eLocation='Grove', eName='Leadership', eDate='2022-10-07', eAudience='hs', eCategory='workshop'),
        Event(eID='041322hs_workshop', eLocation='Lindell', eName='Building Character', eDate='2022-04-13', eAudience='hs', eCategory='workshop'),
        Event(eID='031622hs_workshop', eLocation='Sherlake', eName='Leadership', eDate='2022-03-16', eAudience='hs', eCategory='workshop'),
        Event(eID='100622hs_workshop', eLocation='Sherlake', eName='Building Habits', eDate='2022-10-06', eAudience='hs', eCategory='workshop'),
        Event(eID='111822hs_service', eLocation='St. Anne''s', eName='Food Pantry', eDate='2022-11-18', eAudience='hs', eCategory='service'),
        Event(eID='051823hs_service', eLocation='Arbor Care', eName='Visit to Elderly', eDate='2023-05-18', eAudience='hs', eCategory='service'),
        Event(eID='110422hs_retreat', eLocation='Shellbourne', eName='HS Fall Retreat', eDate='2022-11-04', eAudience='hs', eCategory='retreat'),
        Event(eID='032323hs_retreat', eLocation='Shellbourne', eName='HS Spring Retreat', eDate='2023-03-23', eAudience='hs', eCategory='retreat'),
        Event(eID='121722hs_other', eLocation='Sherlake', eName='Christmas Party', eDate='2022-12-17', eAudience='hs', eCategory='other'),
        Event(eID='102822co_workshop', eLocation='Elms', eName='Optimal Work', eDate='2022-10-28', eAudience='co', eCategory='workshop'),
        Event(eID='120922co_service', eLocation='Elms', eName='Visit the Homeless', eDate='2022-12-09', eAudience='co', eCategory='service'),
        Event(eID='021023co_service', eLocation='Southold', eName='Visit the Homeless', eDate='2023-02-10', eAudience='co', eCategory='service'),
        Event(eID='032323co_service', eLocation='St. Anne''s', eName='Food Pantry', eDate='2023-03-23', eAudience='co', eCategory='service'),
        Event(eID='011323co_retreat', eLocation='Shellbourne', eName='College Winter Retreat', eDate='2023-01-13', eAudience='co', eCategory='retreat'),
        Event(eID='042023co_retreat', eLocation='Shellbourne', eName='College Spring Retreat', eDate='2023-04-20', eAudience='co', eCategory='retreat'),
        Event(eID='110622co_other', eLocation='Southold', eName='Dinner', eDate='2022-11-06', eAudience='co', eCategory='other'),
        Event(eID='032623co_other', eLocation='Southold', eName='Dinner', eDate='2023-03-26', eAudience='co', eCategory='other'),
        Event(eID='042823co_other', eLocation='Elms', eName='Movie Night', eDate='2023-04-28', eAudience='co', eCategory='other')
    ]

    # Takes
    sample_takes = [
        Takes(cID='ELco101122', sID='LeKoch'),
        Takes(cID='ELco101122', sID='RyWilliams'),
        Takes(cID='ELco101122', sID='DaMartinez'),
        Takes(cID='ELco110822', sID='OlSmith'),
        Takes(cID='ELco110822', sID='LeKoch'),
        Takes(cID='ELco110822', sID='SaJohnson'),
        Takes(cID='ELco110822', sID='MaTaylor'),
        Takes(cID='ELco011023', sID='AvBrown'),
        Takes(cID='ELco011023', sID='OlSmith'),
        Takes(cID='ELco021423', sID='LeKoch'),
        Takes(cID='ELco021423', sID='RyWilliams'),
        Takes(cID='ELco021423', sID='EmDavis'),
        Takes(cID='ELco021423', sID='SaJohnson'),
        Takes(cID='ELco031423', sID='DaMartinez'),
        Takes(cID='ELco031423', sID='MaTaylor'),
        Takes(cID='ELco031423', sID='OlSmith'),
        Takes(cID='ELco041123', sID='LeKoch'),
        Takes(cID='ELco041123', sID='RyWilliams'),
        Takes(cID='ELco050923', sID='LeKoch'),
        Takes(cID='ELco050923', sID='MaTaylor'),
        Takes(cID='ELco050923', sID='SaJohnson'),
        Takes(cID='GRhs091522', sID='ChAnderson'),
        Takes(cID='GRhs091522', sID='HeAdams'),
        Takes(cID='GRhs100622', sID='ChHall'),
        Takes(cID='GRhs100622', sID='ChAnderson'),
        Takes(cID='GRhs100622', sID='MiClark'),
        Takes(cID='GRhs100622', sID='SoParker'),
        Takes(cID='GRhs102022', sID='LiGreen'),
        Takes(cID='GRhs102022', sID='AmRodriguez'),
        Takes(cID='GRhs102022', sID='NoMitchell'),
        Takes(cID='GRhs110322', sID='ChAnderson'),
        Takes(cID='GRhs110322', sID='BeWilson'),
        Takes(cID='GRhs110322', sID='SoParker'),
        Takes(cID='GRhs111722', sID='MiClark'),
        Takes(cID='GRhs111722', sID='SaWhite'),
        Takes(cID='GRhs111722', sID='BeWilson'),
        Takes(cID='GRhs111722', sID='NoMitchell'),
        Takes(cID='GRhs120122', sID='BeWilson'),
        Takes(cID='GRhs120122', sID='SoParker'),
        Takes(cID='GRhs011923', sID='SaWhite'),
        Takes(cID='GRhs011923', sID='MiClark'),
        Takes(cID='GRhs011923', sID='AmRodriguez'),
        Takes(cID='GRhs020223', sID='NoMitchell'),
        Takes(cID='GRhs020223', sID='LiGreen'),
        Takes(cID='GRhs030223', sID='BeWilson'),
        Takes(cID='GRhs030223', sID='MiClark'),
        Takes(cID='GRhs030223', sID='SaWhite'),
        Takes(cID='GRhs031623', sID='AmRodriguez'),
        Takes(cID='GRhs031623', sID='SoParker'),
        Takes(cID='GRhs031623', sID='ChHall'),
        Takes(cID='GRhs040623', sID='AmRodriguez'),
        Takes(cID='GRhs040623', sID='MiClark'),
        Takes(cID='GRhs040623', sID='SaWhite'),
        Takes(cID='GRhs042023', sID='NoMitchell'),
        Takes(cID='GRhs042023', sID='SoParker'),
        Takes(cID='GRhs042023', sID='MiClark'),
        Takes(cID='GRhs050423', sID='BeWilson'),
        Takes(cID='GRhs050423', sID='MiClark'),
        Takes(cID='GRhs050423', sID='AmRodriguez'),
        Takes(cID='GRhs050423', sID='SoParker'),
        Takes(cID='GRms091922', sID='IsRodriguez'),
        Takes(cID='GRms091922', sID='JaThomas'),
        Takes(cID='GRms101722', sID='AvAnderson'),
        Takes(cID='GRms101722', sID='IsRodriguez'),
        Takes(cID='GRms112122', sID='IsRodriguez'),
        Takes(cID='GRms112122', sID='JaThomas'),
        Takes(cID='GRms112122', sID='OlBrown'),
        Takes(cID='GRms121922', sID='AvAnderson'),
        Takes(cID='GRms121922', sID='IsRodriguez'),
        Takes(cID='GRms011623', sID='MiSmith'),
        Takes(cID='GRms011623', sID='IsRodriguez'),
        Takes(cID='GRms011623', sID='AvAnderson'),
        Takes(cID='GRms022023', sID='WiHarris'),
        Takes(cID='GRms022023', sID='LiWilson'),
        Takes(cID='GRms041023', sID='AvAnderson'),
        Takes(cID='GRms041023', sID='JaThomas'),
        Takes(cID='PWhs091522', sID='ZoCooper'),
        Takes(cID='PWhs091522', sID='LoWard'),
        Takes(cID='PWhs102722', sID='ZoCooper'),
        Takes(cID='PWhs102722', sID='DaCarter'),
        Takes(cID='PWhs102722', sID='CaMitchell'),
        Takes(cID='PWhs102722', sID='EmRivera'),
        Takes(cID='PWhs110322', sID='EmRivera'),
        Takes(cID='PWhs110322', sID='ZoCooper'),
        Takes(cID='PWhs111722', sID='ZoCooper'),
        Takes(cID='PWhs111722', sID='EmRivera'),
        Takes(cID='PWhs120122', sID='ZoCooper'),
        Takes(cID='PWhs120122', sID='DaCarter'),
        Takes(cID='PWhs020223', sID='LiScott'),
        Takes(cID='PWhs020223', sID='LoWard'),
        Takes(cID='PWhs021623', sID='ZoCooper'),
        Takes(cID='PWhs021623', sID='DaCarter'),
        Takes(cID='PWhs030223', sID='EmRivera'),
        Takes(cID='PWhs030223', sID='ZoCooper'),
        Takes(cID='PWhs031623', sID='JaStewart'),
        Takes(cID='PWhs031623', sID='DaCarter'),
        Takes(cID='PWhs031623', sID='AnRoss'),
        Takes(cID='PWhs042023', sID='ZoCooper'),
        Takes(cID='PWhs042023', sID='ElYoung'),
        Takes(cID='PWhs050423', sID='ZoCooper'),
        Takes(cID='PWhs050423', sID='EmRivera'),
        Takes(cID='PWhs051823', sID='CaMitchell'),
        Takes(cID='PWhs051823', sID='ZoCooper'),
        Takes(cID='SBhs093022', sID='EmSullivan'),
        Takes(cID='SBhs093022', sID='MaHernandez'),
        Takes(cID='SBhs102822', sID='LuWilson'),
        Takes(cID='SBhs111822', sID='ZaParker'),
        Takes(cID='SBhs111822', sID='MiStewart'),
        Takes(cID='SBhs111822', sID='EmSullivan'),
        Takes(cID='SBhs121622', sID='AbMorris'),
        Takes(cID='SBhs012723', sID='EmSullivan'),
        Takes(cID='SBhs012723', sID='MaHernandez'),
        Takes(cID='SBhs012723', sID='OwCarter'),
        Takes(cID='SBhs022423', sID='EmSullivan'),
        Takes(cID='SBhs022423', sID='ZaParker'),
        Takes(cID='SBhs033123', sID='AbMorris'),
        Takes(cID='SBhs033123', sID='JoPeterson'),
        Takes(cID='SBhs042823', sID='JoPeterson'),
        Takes(cID='SBhs042823', sID='EmSullivan'),
        Takes(cID='SBhs042823', sID='ZaParker'),
        Takes(cID='SBhs052623', sID='NiJohnson'),
        Takes(cID='SBhs052623', sID='ZaParker'),
        Takes(cID='SLhs101222', sID='EmSchneider'),
        Takes(cID='SLhs101222', sID='AnEllis'),
        Takes(cID='SLhs102622', sID='ClHammond'),
        Takes(cID='SLhs102622', sID='LeYates'),
        Takes(cID='SLhs102622', sID='CeCollier'),
        Takes(cID='SLhs110922', sID='CaFlores'),
        Takes(cID='SLhs110922', sID='TaOsborne'),
        Takes(cID='SLhs110922', sID='EmSchneider'),
        Takes(cID='SLhs112322', sID='EmSchneider'),
        Takes(cID='SLhs112322', sID='LeMorris'),
        Takes(cID='SLhs121422', sID='ClHammond'),
        Takes(cID='SLhs011123', sID='LoCunningham'),
        Takes(cID='SLhs011123', sID='CeCollier'),
        Takes(cID='SLhs011123', sID='EmSchneider'),
        Takes(cID='SLhs012523', sID='JoJohnson'),
        Takes(cID='SLhs012523', sID='LoCunningham'),
        Takes(cID='SLhs020823', sID='EmSchneider'),
        Takes(cID='SLhs020823', sID='LeMorris'),
        Takes(cID='SLhs022223', sID='LeYates'),
        Takes(cID='SLhs022223', sID='PaWhite'),
        Takes(cID='SLhs022223', sID='CaFlores'),
        Takes(cID='SLhs030823', sID='EmSchneider'),
        Takes(cID='SLhs032223', sID='EmSchneider'),
        Takes(cID='SLhs032223', sID='LoCunningham'),
        Takes(cID='SLhs041223', sID='AnEllis'),
        Takes(cID='SLhs041923', sID='EmSchneider'),
        Takes(cID='SLhs041923', sID='ClHammond'),
        Takes(cID='SLms092622', sID='NoClark'),
        Takes(cID='SLms092622', sID='LiNyugen'),
        Takes(cID='SLms102422', sID='StGuzman'),
        Takes(cID='SLms102422', sID='StHoffman'),
        Takes(cID='SLms102422', sID='NoClark'),
        Takes(cID='SLms112822', sID='DaMontgomery'),
        Takes(cID='SLms112822', sID='NoClark'),
        Takes(cID='SLms121922', sID='BrMitchell'),
        Takes(cID='SLms121922', sID='JaLee'),
        Takes(cID='SLms121922', sID='NoClark'),
        Takes(cID='SLms013023', sID='StGuzman'),
        Takes(cID='SLms013023', sID='SaGardner'),
        Takes(cID='SLms013023', sID='StHoffman'),
        Takes(cID='SLms013023', sID='NoClark'),
        Takes(cID='SLms022723', sID='NoClark'),
        Takes(cID='SLms022723', sID='JaLee'),
        Takes(cID='SLms032723', sID='JaLee'),
        Takes(cID='SLms032723', sID='StGuzman'),
        Takes(cID='SLms042423', sID='SaGardner'),
        Takes(cID='SLms042423', sID='NoClark'),
        Takes(cID='SHhs090722', sID='NoWarner'),
        Takes(cID='SHhs090722', sID='LeRuiz'),
        Takes(cID='SHhs090722', sID='FaCasey'),
        Takes(cID='SHhs110222', sID='NoWarner'),
        Takes(cID='SHhs110222', sID='LeRuiz'),
        Takes(cID='SHhs010423', sID='NoWarner'),
        Takes(cID='SHhs010423', sID='LeRuiz'),
        Takes(cID='SHhs010423', sID='FaCasey'),
        Takes(cID='SHhs030723', sID='FaCasey'),
        Takes(cID='SHhs050223', sID='NoWarner'),
        Takes(cID='SHhs050223', sID='FaCasey'),
        Takes(cID='SHco101322', sID='HaMcguire'),
        Takes(cID='SHco101322', sID='MaRoberts'),
        Takes(cID='SHco111022', sID='HaMcguire'),
        Takes(cID='SHco120822', sID='KaFleming'),
        Takes(cID='SHco120822', sID='HaMcguire'),
        Takes(cID='SHco020223', sID='LuGomez'),
        Takes(cID='SHco020223', sID='HaMcguire'),
        Takes(cID='SHco030123', sID='KaFleming'),
        Takes(cID='SHco030123', sID='LuGomez'),
        Takes(cID='SHco040523', sID='HaMcguire'),
        Takes(cID='SHco040523', sID='CaBlake'),
        Takes(cID='SHco050323', sID='HaMcguire'),
        Takes(cID='SHco050323', sID='MaHudson'),
    ]

    # Teaches
    sample_teaches = [
        Teaches(cID='ELco101122', pID='LiBennett'),
        Teaches(cID='ELco110822', pID='EmEvans'),
        Teaches(cID='ELco121322', pID='MaSmith'),
        Teaches(cID='ELco011023', pID='MiKeller'),
        Teaches(cID='ELco021423', pID='JaReynolds'),
        Teaches(cID='ELco031423', pID='WiWallace'),
        Teaches(cID='ELco041123', pID='AlDixon'),
        Teaches(cID='ELco050923', pID='ChReed'),
        Teaches(cID='GRhs091522', pID='CaHughes'),
        Teaches(cID='GRhs100622', pID='MaSmith'),
        Teaches(cID='GRhs102022', pID='NoDavis'),
        Teaches(cID='GRhs110322', pID='AvGreene'),
        Teaches(cID='GRhs111722', pID='IsIngram'),
        Teaches(cID='GRhs120122', pID='LuJensen'),
        Teaches(cID='GRhs011923', pID='EtLawson'),
        Teaches(cID='GRhs020223', pID='OlNelson'),
        Teaches(cID='GRhs021623', pID='AmOwens'),
        Teaches(cID='GRhs030223', pID='ElParker'),
        Teaches(cID='GRhs031623', pID='AbStewart'),
        Teaches(cID='GRhs040623', pID='WiWallace'),
        Teaches(cID='GRhs042023', pID='HeZimmerman'),
        Teaches(cID='GRhs050423', pID='GrHarrison'),
        Teaches(cID='GRms091922', pID='AlDixon'),
        Teaches(cID='GRms091922', pID='LiMason'),
        Teaches(cID='GRms101722', pID='SaPorter'),
        Teaches(cID='GRms101722', pID='DaSanders'),
        Teaches(cID='GRms112122', pID='ZoWarren'),
        Teaches(cID='GRms112122', pID='CaHughes'),
        Teaches(cID='GRms112122', pID='ElRoss'),
        Teaches(cID='GRms121922', pID='LiBennett'),
        Teaches(cID='GRms121922', pID='AvGreene'),
        Teaches(cID='GRms011623', pID='AiHayes'),
        Teaches(cID='GRms011623', pID='IsIngram'),
        Teaches(cID='GRms022023', pID='MaSmith1'),
        Teaches(cID='GRms032023', pID='LuJensen'),
        Teaches(cID='GRms032023', pID='MiKeller'),
        Teaches(cID='GRms032023', pID='EtLawson'),
        Teaches(cID='GRms041023', pID='ChVaughn'),
        Teaches(cID='GRms041023', pID='HeZimmerman'),
        Teaches(cID='GRms041023', pID='GrHarrison'),
        Teaches(cID='PWhs091522', pID='AlDixon'),
        Teaches(cID='PWhs100622', pID='LiMason'),
        Teaches(cID='PWhs102722', pID='SaPorter'),
        Teaches(cID='PWhs102722', pID='ChReed'),
        Teaches(cID='PWhs111722', pID='CaHughes'),
        Teaches(cID='PWhs111722', pID='ElRoss'),
        Teaches(cID='PWhs120122', pID='SoBennett'),
        Teaches(cID='PWhs120122', pID='OlNelson'),
        Teaches(cID='PWhs120122', pID='AmOwens'),
        Teaches(cID='PWhs020223', pID='BeTurner'),
        Teaches(cID='PWhs021623', pID='ScYoung'),
        Teaches(cID='PWhs021623', pID='HeZimmerman'),
        Teaches(cID='PWhs021623', pID='AlDixon'),
        Teaches(cID='PWhs030223', pID='LiMason'),
        Teaches(cID='PWhs030223', pID='SaPorter'),
        Teaches(cID='PWhs031623', pID='ChReed'),
        Teaches(cID='PWhs031623', pID='ZoWarren'),
        Teaches(cID='PWhs040623', pID='CaHughes'),
        Teaches(cID='PWhs040623', pID='ElRoss'),
        Teaches(cID='PWhs042023', pID='LiBennett'),
        Teaches(cID='PWhs042023', pID='AvGreene'),
        Teaches(cID='PWhs050423', pID='AiHayes'),
        Teaches(cID='PWhs050423', pID='IsIngram'),
        Teaches(cID='SBhs093022', pID='MaSmith1'),
        Teaches(cID='SBhs093022', pID='LuJensen'),
        Teaches(cID='SBhs102822', pID='MiKeller'),
        Teaches(cID='SBhs102822', pID='EtLawson'),
        Teaches(cID='SBhs111822', pID='ChVaughn'),
        Teaches(cID='SBhs111822', pID='HeZimmerman'),
        Teaches(cID='SBhs121622', pID='GrHarrison'),
        Teaches(cID='SBhs121622', pID='LiMason'),
        Teaches(cID='SBhs012723', pID='SaPorter'),
        Teaches(cID='SBhs022423', pID='ChReed'),
        Teaches(cID='SBhs022423', pID='DaSanders'),
        Teaches(cID='SBhs033123', pID='OlNelson'),
        Teaches(cID='SBhs033123', pID='BeTurner'),
        Teaches(cID='SBhs042823', pID='ChVaughn'),
        Teaches(cID='SBhs042823', pID='WiWallace'),
        Teaches(cID='SBhs052623', pID='ScYoung'),
        Teaches(cID='SBhs052623', pID='HeZimmerman'),
        Teaches(cID='SLhs101222', pID='GrHarrison'),
        Teaches(cID='SLhs101222', pID='LiMason'),
        Teaches(cID='SLhs102622', pID='SaPorter'),
        Teaches(cID='SLhs102622', pID='ChReed'),
        Teaches(cID='SLhs110922', pID='DaSanders'),
        Teaches(cID='SLhs110922', pID='WiWallace'),
        Teaches(cID='SLhs112322', pID='HeZimmerman'),
        Teaches(cID='SLhs112322', pID='GrHarrison'),
        Teaches(cID='SLhs121422', pID='AlDixon'),
        Teaches(cID='SLhs121422', pID='LiMason'),
        Teaches(cID='SLhs011123', pID='SaPorter'),
        Teaches(cID='SLhs011123', pID='ChReed'),
        Teaches(cID='SLhs012523', pID='DaSanders'),
        Teaches(cID='SLhs020823', pID='SaPorter'),
        Teaches(cID='SLhs020823', pID='ChReed'),
        Teaches(cID='SLhs020823', pID='DaSanders'),
        Teaches(cID='SLhs022223', pID='GrHarrison'),
        Teaches(cID='SLhs022223', pID='AlDixon'),
        Teaches(cID='SLhs030823', pID='LiMason'),
        Teaches(cID='SLhs030823', pID='WiWallace'),
        Teaches(cID='SLms092622', pID='ScYoung'),
        Teaches(cID='SLms092622', pID='HeZimmerman'),
        Teaches(cID='SLms092622', pID='GrHarrison'),
        Teaches(cID='SLms102422', pID='AlDixon'),
        Teaches(cID='SLms102422', pID='LiMason'),
        Teaches(cID='SLms102422', pID='SaPorter'),
        Teaches(cID='SLms112822', pID='ChReed'),
        Teaches(cID='SLms112822', pID='DaSanders'),
        Teaches(cID='SLms112822', pID='ZoWarren'),
        Teaches(cID='SLms121922', pID='CaHughes'),
        Teaches(cID='SLms121922', pID='ElRoss'),
        Teaches(cID='SLms121922', pID='MaPowell'),
        Teaches(cID='SLms013023', pID='SoBennett'),
        Teaches(cID='SLms013023', pID='AmOwens'),
        Teaches(cID='SLms013023', pID='OlNelson'),
        Teaches(cID='SLms022723', pID='BeTurner'),
        Teaches(cID='SLms022723', pID='ChVaughn'),
        Teaches(cID='SLms022723', pID='WiWallace'),
        Teaches(cID='SHhs090722', pID='HeZimmerman'),
        Teaches(cID='SHhs090722', pID='GrHarrison'),
        Teaches(cID='SHhs090722', pID='LiMason'),
        Teaches(cID='SHhs110222', pID='SaPorter'),
        Teaches(cID='SHhs110222', pID='ChReed'),
        Teaches(cID='SHhs110222', pID='DaSanders'),
        Teaches(cID='SHhs010423', pID='WiWallace'),
        Teaches(cID='SHhs010423', pID='ScYoung'),
        Teaches(cID='SHhs010423', pID='HeZimmerman'),
        Teaches(cID='SHhs030723', pID='GrHarrison'),
        Teaches(cID='SHhs030723', pID='AlDixon'),
        Teaches(cID='SHhs030723', pID='LiMason'),
        Teaches(cID='SHhs050223', pID='SaPorter'),
        Teaches(cID='SHhs050223', pID='ChReed'),
        Teaches(cID='SHhs050223', pID='DaSanders'),
        Teaches(cID='SHco101322', pID='SaPorter'),
        Teaches(cID='SHco101322', pID='ChReed'),
        Teaches(cID='SHco101322', pID='DaSanders'),
        Teaches(cID='SHco111022', pID='GrHarrison'),
        Teaches(cID='SHco111022', pID='AlDixon'),
        Teaches(cID='SHco111022', pID='LiMason'),
        Teaches(cID='SHco120822', pID='WiWallace'),
        Teaches(cID='SHco120822', pID='ScYoung'),
        Teaches(cID='SHco120822', pID='HeZimmerman'),
        Teaches(cID='SHco020223', pID='GrHarrison'),
        Teaches(cID='SHco020223', pID='AlDixon'),
        Teaches(cID='SHco020223', pID='LiMason'),
        Teaches(cID='SHco030123', pID='SaPorter'),
        Teaches(cID='SHco030123', pID='ChReed'),
        Teaches(cID='SHco030123', pID='DaSanders'),
        Teaches(cID='SHco040523', pID='ZoWarren'),
        Teaches(cID='SHco040523', pID='CaHughes'),
        Teaches(cID='SHco050323', pID='ElRoss'),
    ]

    # Runs
    sample_runs = [
        Runs(pID='MaSmith', eID='093022ms_wksp'),
        Runs(pID='LiBennett', eID='093022ms_wksp'),
        Runs(pID='OlCarter', eID='012023ms_wksp'),
        Runs(pID='IsIngram', eID='012023ms_wksp'),
        Runs(pID='NoDavis', eID='121622ms_service'),
        Runs(pID='MaSmith', eID='121622ms_service'),
        Runs(pID='EmEvans', eID='093022hs_workshop'),
        Runs(pID='JaFisher', eID='093022hs_workshop'),
        Runs(pID='LiMason', eID='093022hs_workshop'),
        Runs(pID='AvGreene', eID='100722hs_workshop'),
        Runs(pID='AiHayes', eID='100722hs_workshop'),
        Runs(pID='IsIngram', eID='041322hs_workshop'),
        Runs(pID='MaSmith1', eID='041322hs_workshop'),
        Runs(pID='LuJensen', eID='031622hs_workshop'),
        Runs(pID='IsIngram', eID='031622hs_workshop'),
        Runs(pID='AbStewart', eID='100622hs_workshop'),
        Runs(pID='MiKeller', eID='100622hs_workshop'),
        Runs(pID='EtLawson', eID='111822hs_service'),
        Runs(pID='HaMitchell', eID='111822hs_service'),
        Runs(pID='OlNelson', eID='111822hs_service'),
        Runs(pID='IsIngram', eID='051823hs_service'),
        Runs(pID='AmOwens', eID='051823hs_service'),
        Runs(pID='ElParker', eID='051823hs_service'),
        Runs(pID='WiWallace', eID='110422hs_retreat'),
        Runs(pID='EvQuinn', eID='110422hs_retreat'),
        Runs(pID='ElParker', eID='110422hs_retreat'),
        Runs(pID='JaReynolds', eID='110422hs_retreat'),
        Runs(pID='AbStewart', eID='110422hs_retreat'),
        Runs(pID='ScYoung', eID='121722hs_other'),
        Runs(pID='BeTurner', eID='032323hs_retreat'),
        Runs(pID='ChVaughn', eID='032323hs_retreat'),
        Runs(pID='WiWallace', eID='032323hs_retreat'),
        Runs(pID='HeZimmerman', eID='121722hs_other'),
        Runs(pID='GrHarrison', eID='102822co_workshop'),
        Runs(pID='AlDixon', eID='102822co_workshop'),
        Runs(pID='ScYoung', eID='120922co_service'),
        Runs(pID='LiMason', eID='120922co_service'),
        Runs(pID='SaPorter', eID='021023co_service'),
        Runs(pID='ScYoung', eID='021023co_service'),
        Runs(pID='EtLawson', eID='032323co_service'),
        Runs(pID='LiMason', eID='032323co_service'),
        Runs(pID='DaSanders', eID='011323co_retreat'),
        Runs(pID='ZoWarren', eID='011323co_retreat'),
        Runs(pID='HaMitchell', eID='042023co_retreat'),
        Runs(pID='CaHughes', eID='042023co_retreat'),
        Runs(pID='ElRoss', eID='110622co_other'),
        Runs(pID='DaSanders', eID='110622co_other'),
        Runs(pID='IsIngram', eID='032623co_other'),
        Runs(pID='ChVaughn', eID='032623co_other'),
        Runs(pID='JaReynolds', eID='042823co_other'),
        Runs(pID='ElParker', eID='042823co_other'),
        Runs(pID='HeZimmerman', eID='042823co_other'),
    ]

    # Attends
    sample_attends = [
        Attends(sID='ChAnderson', eID='093022ms_wksp'),
        Attends(sID='AvAnderson', eID='012023ms_wksp'),
        Attends(sID='AnEllis', eID='121622ms_service'),
        Attends(sID='JaMorris', eID='093022hs_workshop'),
        Attends(sID='LoShaw', eID='100722hs_workshop'),
        Attends(sID='HaMcguire', eID='041322hs_workshop'),
        Attends(sID='AvBrown', eID='031622hs_workshop'),
        Attends(sID='KaFleming', eID='100622hs_workshop'),
        Attends(sID='EmDavis', eID='111822hs_service'),
        Attends(sID='MaHudson', eID='051823hs_service'),
        Attends(sID='LeYates', eID='110422hs_retreat'),
        Attends(sID='BrMitchell', eID='032323hs_retreat'),
        Attends(sID='JaLee', eID='121722hs_other'),
        Attends(sID='FaCasey', eID='102822co_workshop'),
        Attends(sID='FaCasey', eID='120922co_service'),
        Attends(sID='MaBecker', eID='021023co_service'),
        Attends(sID='BrMitchell', eID='032323co_service'),
        Attends(sID='LiWood', eID='011323co_retreat'),
        Attends(sID='DaCarter', eID='042023co_retreat'),
        Attends(sID='LoMiller', eID='110622co_other'),
        Attends(sID='ZaParker', eID='032623co_other'),
        Attends(sID='MaRoberts', eID='042823co_other'),
        Attends(sID='JaMorris', eID='093022ms_wksp'),
        Attends(sID='ChAnderson', eID='012023ms_wksp'),
        Attends(sID='EmDavis', eID='121622ms_service'),
        Attends(sID='ChAnderson', eID='093022hs_workshop'),
        Attends(sID='JaMoore', eID='100722hs_workshop'),
        Attends(sID='ClHammond', eID='041322hs_workshop'),
        Attends(sID='OlBrown', eID='031622hs_workshop'),
        Attends(sID='AnEllis', eID='100622hs_workshop'),
        Attends(sID='CeCollier', eID='111822hs_service'),
        Attends(sID='KaFleming', eID='051823hs_service'),
        Attends(sID='SoParker', eID='110422hs_retreat'),
        Attends(sID='SaGardner', eID='032323hs_retreat'),
        Attends(sID='ElYoung', eID='121722hs_other'),
        Attends(sID='CaFlores', eID='102822co_workshop'),
        Attends(sID='NoClark', eID='120922co_service'),
        Attends(sID='ZoCooper', eID='021023co_service'),
        Attends(sID='WiHarris', eID='032323co_service'),
        Attends(sID='SoMorgan', eID='011323co_retreat'),
    ]

    # Helps
    sample_helps = [
        Helps(vID='V01', eID='093022hs_workshop'),
        Helps(vID='V05', eID='102822co_workshop'),
        Helps(vID='V10', eID='032323co_service'),
        Helps(vID='V08', eID='110622co_other'),
        Helps(vID='V03', eID='042823co_other'),
        Helps(vID='V01', eID='102822co_workshop'),
        Helps(vID='V10', eID='042823co_other'),
        Helps(vID='V08', eID='032323co_service'),
        Helps(vID='V08', eID='110422hs_retreat'),
        Helps(vID='V03', eID='100722hs_workshop'),
    ]

# Commit the changes to the database
session.commit()

# Close the session

# Print sample data
def print_sample_data():
    # Centers
    print("Sample Centers:")
    for center in sample_centers:
        print(center.cenID, center.cenName)

    # Students
    print("\nSample Students:")
    for student in sample_students:
        print(student.sID, student.sFirst, student.sLast, student.sPhoneNumber, student.sBday, student.sLevel, student.sLeadership, student.sParentAlum, student.sEmergencyPhone, student.cenID)

    # Classes
    '''
    print("\nSample Classes:")
    for class_ in sample_classes:
        print(class_.cID, class_.cLevel, class_.cDate, class_.cTopic, class_.cenID)
    '''
    # PermStaff
    print("\nSample Permanent Staff:")
    for perm_staff in sample_perm_staff:
        print(perm_staff.pID, perm_staff.pFirst, perm_staff.pLast, perm_staff.pEmail, perm_staff.pPhoneNumber, perm_staff.pTrainStatus, perm_staff.pTrainExp, perm_staff.cenID)

    # Volunteers
    print("\nSample Volunteers:")
    for volunteer in sample_volunteers:
        print(volunteer.vID, volunteer.vFirst, volunteer.vLast, volunteer.vPhoneNumber, volunteer.vEmail, volunteer.vTrainStatus, volunteer.vTrainExp)

    # Events
    print("\nSample Events:")
    for event in sample_events:
        print(event.eID, event.eLocation, event.eName, event.eDate, event.eAudience, event.eCategory)

    # Takes
    print("\nSample Takes:")
    for takes in sample_takes:
        print(takes.cID, takes.sID)

    # Teaches
    print("\nSample Teaches:")
    for teaches in sample_teaches:
        print(teaches.cID, teaches.pID)

    # Runs
    print("\nSample Runs:")
    for runs in sample_runs:
        print(runs.pID, runs.eID)

    # Attends
    print("\nSample Attends:")
    for attends in sample_attends:
        print(attends.sID, attends.eID)

    # Helps
    print("\nSample Helps:")
    for helps in sample_helps:
        print(helps.vID, helps.eID)

print_sample_data()