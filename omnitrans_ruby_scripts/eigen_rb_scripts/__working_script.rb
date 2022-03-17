#create instance of Streamline
streamLine = OtStreamLine.new


#INPUT
##-----------------------------
streamLine.input.network = [10, 10]

#controller aan
#streamLine.input.controls = true

## OD - at once met leegloop tijd
streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
streamLine.input.durations = [7200, 36000]


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
streamLine.routeChoice.periodEndTimes =
       [ 900,  1800,  2700,  3600,  4500,  5400,  6300,  7200,  8100,
        9000,  9900, 10800, 11700, 12600, 13500, 14400, 15300, 16200,
       17100, 18000, 18900, 19800, 20700, 21600, 22500, 23400, 24300,
       25200, 26100, 27000, 27900, 28800, 29700, 30600, 31500, 32400,
       33300, 34200, 35100, 36000, 36900, 37800, 38700, 39600, 40500,
       41400, 42300 ]

streamLine.routeChoice.preTripPercentageApplied = 1.0




##ROUTE COST MODEL
##-------------------------------------------
#hier moet de ouput van de vorige als input.
streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS




#TRAFFIC PROPAGATION
##------------------------------------------
streamLine.propagation.duration = 43200
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
##-------------------------------------
streamLine.output.load = [1, 10, 100, 1, 86, 5 ]
streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet.pmturi = [1, 10, 100, 1, 86, 5 ]


#execute
streamLine.execute
