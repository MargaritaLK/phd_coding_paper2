#create instance of Streamline
streamLine = OtStreamLine.new


#INPUT
##-----------------------------
streamLine.input.network = [10, 10]


#controller aan
streamLine.input.controls = true

#OD - one- zonder stop
#streamLine.input.odMatrix = [1, 10, 10, 1]

# # OD - at once met leegloop tijd
streamLine.input.odMatrix = [1, 10, [10, 225 ], 1]
streamLine.input.durations = [1800, 127800]


#ROUTE SET GENERATION
##--------------------------------------
streamLine.routeGenerator = SL_DIJKSTRA

streamLine.routeGenerator.alternativeGenerator = SL_MONTECARLO
streamLine.routeGenerator.alternativeGenerator.initialVariance = 1
streamLine.routeGenerator.alternativeGenerator.maxVariance = 20
streamLine.routeGenerator.alternativeGenerator.threshold = 2
streamLine.routeGenerator.alternativeGenerator.varianceGrowValue = 1

streamLine.routeGenerator.filter.maxNumberOfRoutes = 200  ##default 5
streamLine.routeGenerator.filter.maxOverlapFactor = 1   ##default 0.6
streamLine.routeGenerator.filter.minNonCommonDetourFactor = 1   ##default 0.01
streamLine.routeGenerator.filter.maxNonCommonDetourFactor = 20  ##detault  2.0
streamLine.routeGenerator.filter.maxTotalDetourFactor = 10  ##default 1.9



##ROUTE CHOICE MODEL
##----------------------------------------
# streamLine.routeChoice = SL_ONESHOT
# streamLine.routeChoice.preTrip = SL_UNIFORM

# 3.3: Configure a pre-trip route choice object to support within simulation route choice.
streamLine.routeChoice.preTrip = SL_MNL
streamLine.routeChoice.preTrip.spread = 0.14
streamLine.routeChoice.preTrip.relativeSpread = true
streamLine.routeChoice.preTrip.relativeSpreadBasedOnCost = true
#streamLine.routeChoice.periodEndTimes = [enTimPeriod1, ....endTimePeriodn]
streamLine.routeChoice.periodEndTimes = [ 900,  1800,  2700,  3600,  4500,  5400,  6300,  7200]

streamLine.routeChoice.preTripPercentageApplied = 1.0




##ROUTE COST MODEL
##-------------------------------------------
#hier moet de ouput van de vorige als input.
#streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS
#streamLine.routeCost.routeDataSet.saveIterations = true

streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS
#streamLine.routeCost.finalRouteDataSet.pmturi = [1, 10, 100, 1, 60, 5]



#TRAFFIC PROPAGATION
##------------------------------------------
streamLine.propagation.duration = 129600
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
##-------------------------------------
streamLine.output.load = [1, 10, 100, 1, 62, 5 ]
streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet.pmturi = [1, 10, 100, 1, 62, 5 ]



#execute
streamLine.execute
