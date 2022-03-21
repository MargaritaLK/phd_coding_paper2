#create instance of Streamline
streamLine = OtStreamLine.new


#INPUT
##-----------------------------
streamLine.input.network = [10, 10]

#controller aan
streamLine.input.controls = true

## OD - at once met leegloop tijd
streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
streamLine.input.durations = [7200, 79200]


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
streamLine.routeChoice.periodEndTimes = [900,1800,2700,3600,4500,5400,6300,7200,8100,9000,9900,10800,11700,12600,13500,14400,15300,16200,17100,18000,18900,19800,20700,21600,22500,23400,24300,25200]
streamLine.routeChoice.preTripPercentageApplied = 1.0




##ROUTE COST MODEL
##-------------------------------------------


#TRAFFIC PROPAGATION
##------------------------------------------
streamLine.propagation.duration = 86400
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
##-------------------------------------
streamLine.output.load = [1, 10, 100, 1, 3, 5 ]
streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet.pmturi = [1, 10, 100, 1, 3, 5 ]


#execute
streamLine.execute
