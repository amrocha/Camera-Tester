class MetricsResult:
    """
    Attributes:
    startTime, endTime: The time segment that these results fall between
    detectionPercent: Percentage of time that the gps vehicle was identified during this
    idChanges: Number of times the tracknum changed during this time segment
    minPositonalAccuracy: Closest distance between the gps and core
    maxPositionalAccuracy: Farthest distance between the gps and core
    averagePositionalAccuracy: Average distance between the gps and core
    percentWithinMaxRadius: Percentage of time the distance was within Maximum Radius
    """
    def __init__ (self, startTime, endTime, detectionPercent, numIDChanges, minDist, maxDist, totalDist, percentWithinMaxRadius):
        self.startTime = startTime
        self.endTime = endTime
        self.detectionPercent = detectionPercent
        self.idChanges = numIDChanges
        self.minPositonalAccuracy = minDist
        self.maxPositionalAccuracy = maxDist
        self.averagePositionalAccuracy = totalDist
        self.percentWithinMaxRadius = percentWithinMaxRadius

