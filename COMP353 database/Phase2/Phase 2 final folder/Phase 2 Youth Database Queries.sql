/*Highlight and execute*/

/*VolunteerHelp Query (David)*/ 
Select V.VID,V.vFirst,V.VtrainStatus,V.vPhoneNumber, Count(DISTINCT H.eid) AS Numberofeventsmanaged  
From Helps H, Volunteer V, Event E  
Where H.VID= V.VID And E.eid =  H.EID  
Group by V.VID,V.vfirst,V.VtrainStatus,V.vPhoneNumber  
Having Count(H.eid) >= 1 
Order by V.vfirst ASC; 

/*AvgStudentsClassLevel Query (Rachel)*/ 
SELECT cenName, cLevel, num_students/num_classes as avg_students_per_class 
FROM (/* find the total number of classes of a particular level offered at each center  
		and the total number of students who have attended those classes*/ 
		SELECT C.cenID, C.cenName, CL.cLevel, count(S.sID) as num_students, count(distinct CL.cID) as num_classes 
		FROM student S, takes T, class CL, center C  
		WHERE S.sID = T.sID and T.cID = CL.cID and CL.cenID = C.cenID 
		GROUP BY CL.clevel, C.cenID, C.cenName) 
GROUP BY cLevel, cenID, cenName, num_students, num_classes 
ORDER BY cenName; 

/*Query: leadershipGroupClassAttendance (Taylor)*/ 
SELECT Cen.cenName, Tot.cLevel, TotalStudentCount, LeadershipStudentCount 
FROM Center Cen, 
/*Inner query for count of distinct leadership group students attending classes*/ 
(SELECT C.cenID, C.cLevel, count(distinct S.sID) as LeadershipStudentCount 
FROM Student S, Takes T, Class C 
WHERE T.sID=S.sID and C.cID=T.cID and S.sLeadership='yes' 
GROUP BY C.cenID, c.cLevel 
) Lead, 
/*Inner query for count of total distinct students attending classes*/ 
(SELECT C.cenID, C.cLevel, count(distinct S.sID) as TotalStudentCount 
FROM Student S, Takes T, Class C 
WHERE T.sID=S.sID and C.cID=T.cID 
GROUP BY C.cenID, c.cLevel 
) Tot 
WHERE Lead.cenID=Tot.cenID and Lead.cLevel=Tot.cLevel and Lead.cenID=Cen.cenID 
ORDER By Cen.cenName, Tot.cLevel;

/*numberOfEvents Query (Max)*/ 
SELECT 
    s.sID AS StudentID, 
    s.sFirst AS FirstName, 
    s.sLast AS LastName, 
    COUNT(DISTINCT a.eID) AS numberOfEvents, 
    STRING_AGG(e.eName, ', ' ORDER BY e.eName) AS AttendedEvents 
FROM attends a, student s, event e
WHERE a.sID = s.sID and a.eID = e.eID
GROUP BY s.sID, s.sFirst, s.sLast 
HAVING COUNT(DISTINCT a.eID) > 1 
ORDER BY numberOfEvents DESC; 

/*StudentAttendance Query (Kadin)*/ 
SELECT s.sFirst as FirstName,  
       s.sLast as LastName,  
       COUNT(DISTINCT C.cID) as classAttend, 
       COUNT(DISTINCT E.eID) as eventAttend 
FROM Student S, Event E, Class C, Takes T, Attends A 
WHERE A.eID = E.eID and A.sID = S.sID and S.sID = T.sID and T.cID = C.cID 
GROUP BY s.sFirst, s.sLast 
HAVING COUNT(DISTINCT C.cID) <= 1 
ORDER BY classAttend ASC; 