# OmniTRANS Job for 'lk_testen_zelf_v2'
# Created 18/02/2022 17:07:07


# Create a Simple StreamLine instance
streamLine = OtStreamLine.new



#--step 1---INPUT-----

## network - static
streamLine.input.network = [10,10]


## OD matrix - static
#streamLine.input.odMatrix = [1,10,10,1]



## OD matrix - for staging
streamLine.input.odMatrix = [1, 10, [10, 20, 30], 1]
streamLine.input.durations = [1800, 1800, 10800]

streamLine.input.controls = true





##--step 2- ROUTE SET GENERATION -------------

# route generator model # default is onetoall
streamLine.routeGenerator.multiplicity = SL_ONETOALL




##- step 3----- ROUTE CHOICE -------
streamLine.routeChoice = SL_ONESHOT



#--step 4 --- ROUTE COST-----




#-- step 5 --PROPAGATION MODEL ----

## duration of simulation, must be sum of durations of matrices
streamLine.propagation.duration = 14400





# step 6--- OUTPUT------
#streamLine.routeCost.routeDataSet = SL_MEMORY

streamLine.output.routeSet = SL_OMNITRANS
streamLine.output.routeSet.pmturi = [1,10,150,1,8,1]

#streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS


streamLine.output.persistCostSnapshots = true


# Store the loads
#streamLine.output.load = [p,m,t,u,r,i]
streamLine.output.load = [1,10,100,1,19,1]





# Execute
streamLine.execute
