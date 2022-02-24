# OmniTRANS Job for 'denHelder_fromScratch_v1'
# Created 24/02/2022 12:06:49

writeln "van voorbeeld - comprehensive example of single mode (SL_MADAM)"




# Step 0: Create a StreamLine instance
streamLine = OtStreamLine.new()





# Step 1 (Input): Set all properties regarding the input
#------------------------------------------------------
streamLine.input.network = [11,10]
streamLine.input.odMatrix = [1,11,10,1]

# Distribute the OD matrix over six period with the following fractions
streamLine.input.fractions = [0.2, 0.225, 0.25, 0.25, 0.2625, 0.2, 0, 0]


# Variation: When using multiple OD-Matrice as input, use the property durations
# to define the time duration of each OD matrix

#~ streamLine.input.odMatrix = [1,1,[101,102,103,104,105,106],1]
#~ streamLine.durations = [900, 1200, 1200, 1200, 1200, 1500]

# Option: Define the pmturi of the initial costs if necessary
#~ streamLine.input.initialCosts = [1,1,1,1,1001,1]


# The following lines of code illustrate some input properties with their default values
streamLine.input.defaultApproachLength = 0.1
streamLine.input.impedanceMultiplier = 1.0
streamLine.input.initialCostsMultiplier = 1.





# Step 2: Route Generation
#--------------------------------------------------------

# 2.1: Choose the configuration for the generation of alternative routes
# This is done via the routeGenerator available on the streamLine instance:
streamLine.routeGenerator.alternativeGenerator.minIterations= 2
streamLine.routeGenerator.alternativeGenerator.maxIterations= 50
streamLine.routeGenerator.alternativeGenerator.initialVariance= 0.09
streamLine.routeGenerator.alternativeGenerator.varianceGrowValue= 0.02
streamLine.routeGenerator.alternativeGenerator.maxVariance = 0.3
streamLine.routeGenerator.alternativeGenerator.threshold = 3
streamLine.routeGenerator.alternativeGenerator.consecutiveThreshold = true


# 2.2: Configure the route filter that chooses viable routes from the generated alternatives.
# This category of properties is also accessed via the routeGenerator on the streamLine instance
streamLine.routeGenerator.filter.maxTotalDetourFactor = 1.9
streamLine.routeGenerator.filter.minNonCommonDetourFactor = 0.01
streamLine.routeGenerator.filter.maxNonCommonDetourFactor = 2.0
streamLine.routeGenerator.filter.maxOverlapFactor = 0.6
streamLine.routeGenerator.filter.maxNumberOfRoutes = 5




# Step 3: Create a Route Choice Manager
#------------------------------------------------------------
# In the following case, a 'One Shot' simulation is selected. 'One Shot' means a single iteration.
# Use this instance to access and set the other properties that are relevant for route choice during the simulation
#~ streamLine.routeChoice = SL_ONESHOT

# Let us define a Route Choice Manager for multiple iterations
# using the Method of Successive Average (MSA)
streamLine.routeChoice = SL_MSA

# Sample properties with default values
streamLine.routeChoice.maxIterations = 10
streamLine.routeChoice.lambda = 1
streamLine.routeChoice.dualityGap = 0.01
streamLine.routeChoice.successiveAverageOffset = 0

# Option: Define a static OD Matrix
#~ streamLine.routeChoice.staticODMatrix = [p,m,t,u,r,i]

# 3.1: Configure an initial route choice object to be used at the start of the first iteration
streamLine.routeChoice.initial = SL_PCL
streamLine.routeChoice.initial.spread = 0.14
streamLine.routeChoice.initial.relativeSpread = true
streamLine.routeChoice.initial.relativeSpreadBasedOnCost = true

# 3.2: Configure a successive route choice object to be used at the start of all other iterations
streamLine.routeChoice.successive = SL_PCL
streamLine.routeChoice.successive.spread = 0.14
streamLine.routeChoice.successive.relativeSpread = true
streamLine.routeChoice.successive.relativeSpreadBasedOnCost = true

# 3.3: Configure a pre-trip route choice object to support within simulation route choice.
streamLine.routeChoice.preTrip = SL_PCL
streamLine.routeChoice.preTrip.spread = 0.14
streamLine.routeChoice.preTrip.relativeSpread = true
streamLine.routeChoice.preTrip.relativeSpreadBasedOnCost = true
#streamLine.routeChoice.periodEndTimes = [enTimPeriod1, ....endTimePeriodn]
streamLine.routeChoice.periodEndTimes = [900,1800,2700,3600,4500,5400]
streamLine.routeChoice.preTripPercentageApplied = 1.0




#Step 4: Route Cost
#-----------------------------------------------------------------------
# The route cost manager controls how the route costs are being calculated.

streamLine.routeCost.initialReactive = true
streamLine.routeCost.successiveReactive = true
streamLine.routeCost.valueOfTime = [[1,1]]
streamLine.routeCost.valueOfDistance = [[1,0]]
streamLine.routeCost.collectionInterval = 300

# Set the initial route data set if route information from a previous run
#  is being used to calculate initial route costs.
#~ streamLine.routeCost.initialRouteDataSet.pmturi = [p,m,t,u,r,i]



# 4.1: Collect the route costs via a Route Dataset object

# Use a route data set to store the route cost and fractions collected during the simulation.
# This component can be accessed via the routeCost property of streamLine.
# There are two options a memory route data set (SL_MEMORY) or a persistent route data set (SL_OMNITRANS)
streamLine.routeCost.routeDataSet = SL_OMNITRANS
streamLine.routeCost.routeDataSet.saveIterations = false

# or
#~ streamLine.routeCost.routeDataSet = SL_MEMORY

# Option: Specify where to store the final route data set (last iteration)
#~ streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS
#~ streamLine.routeCost.finalRouteDataSet.pmturi = [p,m,t,u,r,i]



# Step 5: Set a propagation model
#---------------------------------------------
# Choose MaDAM as propagation model in this example and configure the a number of relevant properties

streamLine.propagation = SL_MADAM
streamLine.propagation.duration = 7200
streamLine.propagation.timeStep = 2
# DEFAULT: maxDensity is 180 VEH/KM/LANE
streamLine.propagation.maxDensity = 180


# Example of propagation properties with their default values
streamLine.propagation.minSpeed = 7
streamLine.propagation.segmentLength = 0.3
streamLine.propagation.adjustSegmentLength = false
streamLine.propagation.delta = 0.8
streamLine.propagation.kappa = 13
streamLine.propagation.nue = 35
streamLine.propagation.phi = 2


# Step 6: Set the junction model (Optional)
#-------------------------------------------------



# Step 7: Configure the output of the streamLine simulation
#-------------------------------------------------------------
# Aggregate the output data for each 120 seconds and increment the time dimension by 1
streamLine.output.aggregation = [120,1]
# Option: Specify the start and end time for collecting the output
# if different than the simulation time
streamLine.output.startTime = 0
streamLine.output.endTime = 6000
# Option: Specify the iterations for which the iterations should be ignored
streamLine.output.ignoreIterations = [2,4]
# Option: Persist the cost snapshots for advanced analysis
streamLine.output.persistCostSnapshots = true
# Specify whether the routes must be saved
streamLine.output.routeSet = SL_OMNITRANS
# Specify the PMTURI storing the route results
streamLine.output.routeSet.pmturi = [1,11,1420,1,6,1]
# Specify the PMTURI storing the first output results
streamLine.output.load = [1,11,1420,1,6,1]





# Step 8: Execute StreamLine
streamLine.execute
