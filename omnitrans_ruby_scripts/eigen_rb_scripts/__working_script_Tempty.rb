#create instance of Streamline
streamLine = OtStreamLine.new


#INPUT
##-----------------------------
streamLine.input.network = [10, 10]



#OD - one- zonder stop
streamLine.input.odMatrix = [1, 10, 10, 1]

# # OD - at once met leegloop tijd
# streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
# streamLine.input.durations = [7200, 7200]


#ROUTE SET GENERATION
##--------------------------------------
##optional



##ROUTE CHOICE MODEL
##----------------------------------------
# streamLine.routeChoice = SL_ONESHOT
# streamLine.routeChoice.preTrip = SL_UNIFORM

# 3.3: Configure a pre-trip route choice object to support within simulation route choice.
streamLine.routeChoice.preTrip = SL_PCL
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





#TRAFFIC PROPAGATION
##------------------------------------------
streamLine.propagation.duration = 43200
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
##-------------------------------------
streamLine.output.load = [1, 10, 215, 1, 99, 5 ]
streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet.pmturi = [1, 10, 215, 1, 99, 5 ]
#streamLine.output.routeCost.pmturi = [1, 10, 100, 1, 60, 5 ]


#execute
streamLine.execute
