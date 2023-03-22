        SELECT
            RunsOnWeekday.weekdayName,
            StartStationEntry.time,
            StartStation.stationName,
            EndStationEntry.time,
            EndStation.stationName
        FROM RunsOnWeekday
        INNER JOIN TrainRoute ON
            TrainRoute.trainRouteId = RunsOnWeekday.trainRouteId
        INNER JOIN TimeTableEntry AS StartStationEntry ON
            TrainRoute.trainRouteId = StartStationEntry.trainRouteId
        INNER JOIN TimeTableEntry AS EndStationEntry ON
            TrainRoute.trainRouteId = EndStationEntry.trainRouteId
        INNER JOIN StationOnTrack AS StartStation ON
            StartStationEntry.trackSectionId = StartStation.trackSectionId AND
            StartStationEntry.stationIndex = StartStation.stationIndex
        INNER JOIN StationOnTrack AS EndStation ON
            EndStationEntry.trackSectionId = EndStation.trackSectionId AND
            EndStationEntry.stationIndex = EndStation.stationIndex
        WHERE
            ((weekdayName = ? AND StartStationEntry.time > ?) OR
            weekdayName = ?) AND
            StartStation.stationName = ? AND
            EndStation.stationName = ? AND
            (TrainRoute.direction = 'main' AND StartStation.stationIndex <= EndStation.stationIndex) OR
            (TrainRoute.direction = 'opposite' AND EndStation.stationIndex <= StartStation.startIndex)