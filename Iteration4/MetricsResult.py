class MetricsResult:
    def __init__ (self, length, startTime, endTime, numUndetected, numIDChanges, minDist, maxDist, totalDist, numAboveRadius):
        self.startTime = startTime
        self.endTime = endTime
        self.detectionPercent = float(length - numUndetected) / length * 100
        self.idChanges = numIDChanges
        self.minPositonalAccuracy = minDist
        self.maxPositionalAccuracy = maxDist
        if length - numUndetected > 0:
            self.averagePositionalAccuracy = totalDist / float(length - numUndetected)
            self.percentWithinMaxRadius = ((length - numUndetected) - numAboveRadius) / float(length - numUndetected) * 100
        else:
            self.averagePositionalAccuracy = -1
            self.percentWithinMaxRadius = -1
