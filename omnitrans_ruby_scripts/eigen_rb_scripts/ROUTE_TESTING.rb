#create instance of Streamline
streamLine = OtStreamLine.new



#INPUT
##-----------------------------
streamLine.input.network = [10, 10]


#controller aan
streamLine.input.controls = true


#OD - one- zonder stop
streamLine.input.odMatrix = [1, 10, 10, 1]



# ## OD - at once met leegloop tijd
# streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
# streamLine.input.durations = [3600, 39600]




#ROUTE GENERATION
#--------------------------------------
streamLine.routeGenerator.alternativeGenerator.minIterations= 2
streamLine.routeGenerator.alternativeGenerator.maxIterations= 50
streamLine.routeGenerator.alternativeGenerator.initialVariance= 0.09
streamLine.routeGenerator.alternativeGenerator.varianceGrowValue= 0.02
streamLine.routeGenerator.alternativeGenerator.maxVariance = 0.3
streamLine.routeGenerator.alternativeGenerator.threshold = 3
streamLine.routeGenerator.alternativeGenerator.consecutiveThreshold = true


streamLine.routeGenerator.filter.maxTotalDetourFactor = 1.9
streamLine.routeGenerator.filter.minNonCommonDetourFactor = 0.01
streamLine.routeGenerator.filter.maxNonCommonDetourFactor = 2.0
streamLine.routeGenerator.filter.maxOverlapFactor = 0.6
streamLine.routeGenerator.filter.maxNumberOfRoutes = 5





#ROUTE CHOICE MODEL
#-------------------------------------


streamLine.routeChoice = SL_MSA
streamLine.routeChoice.maxIterations = 10
streamLine.routeChoice.lambda = 1
streamLine.routeChoice.dualityGap = 0.01
streamLine.routeChoice.successiveAverageOffset = 0

streamLine.routeChoice.preTrip = SL_NONE

streamLine.routeChoice.successive = SL_PCL


#ROUTE COST MODEL
#--------------------------------------------------


streamLine.routeCost.routeDataSet = SL_OMNITRANS
streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS
streamLine.routeCost.finalRouteDataSet.pmturi = [1,10,100,1,99,5]






#TRAFFIC PROPAGATION
#-------------------------------------------

streamLine.propagation.duration = 43200
streamLine.propagation.adjustSegmentLength = true




# OUTPUT
#-----------------------------------------
#streamLine.output.load =[p, m,  t,  u,  r, i]
streamLine.output.load = [1, 10, 100, 1, 99, 5 ]
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.routeSet.pmturi = [1, 10, 100, 1, 99, 5 ]




#execute
streamLine.execute
