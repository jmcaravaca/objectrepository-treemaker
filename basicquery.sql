SELECT
a.ActivityType
, a.DisplayName as ActivityName
, a.FilePath 
, u.Name As UIObjectName
FROM  activities a
LEFT JOIN uiobjects u
ON a.Reference  = u.Reference 