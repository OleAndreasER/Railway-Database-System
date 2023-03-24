SELECT
    StationOnTrack.stationName,
FROM TrainOccurence
INNER JOIN TrainRoute ON
    TrainOccurence.trainRouteId = TrainRoute.trainRouteId
INNER JOIN TimeTableEntry ON
    TrainRoute.trainRouteId = TimeTableEntry.trainRouteId
INNER JOIN StationOnTrack ON
    TimeTableEntry.trackSectionId = StationOnTrack.trackSectionId AND
    TimeTableEntry.stationIndex = StationOnTrack.stationIndex
WHERE
    TrainOccurence.date = ? AND
    TimeTableEntry.time = ?