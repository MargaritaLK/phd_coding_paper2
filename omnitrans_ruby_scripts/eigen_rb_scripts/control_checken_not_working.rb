#create instance of Streamline
streamLine = OtStreamLine.new



#INPUT
##-----------------------------
streamLine.input.network = [10, 10]

#controller aan
streamLine.input.controls = true

## OD - at once met leegloop tijd
streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
streamLine.input.durations = [3600, 82800]



#ROUTE GENERATION
#--------------------------------------
#streamLine.output.routeSet = SL_OMNITRANS




#ROUTE GENERATION
#-------------------------------------------------
streamLine.routeChoice = SL_MSA






#ROUTE COST
streamLine.routeCost.routeDataSet = SL_OMNITRANS
streamLine.routeCost.finalRouteDataSet = SL_OMNITRANS
streamLine.routeCost.finalRouteDataSet.pmturi = [1,10,100,1,3,7]





#TRAFFIC PROPAGATION
#--------------------------------------------
streamLine.propagation.duration = 86400
streamLine.propagation.adjustSegmentLength = true




# OUTPUT
#-----------------------------------------
#streamLine.output.load =[p, m,  t,  u,  r,i]
streamLine.output.load = [1, 10, 100, 2, 3, 1 ]
streamLine.output.persistCostSnapshots = true
streamLine.output.routeSet = SL_OMNITRANS





#execute
streamLine.execute
