SELECT
actref.ProcessName , actref.ActivityName , actref.Assembly,  act.FilePath 
, uiref.ActivityType , uiref.DisplayName  
, uiobj.Name, uiobj.Type
FROM  activityreferences actref
LEFT JOIN activities act
ON actref.ActivityName  = act.Name
LEFT JOIN uireferences uiref
ON uiref.FilePath  = act.FilePath 
LEFT JOIN uiobjects uiobj
ON uiref.Reference  = uiobj.Reference 