#Run multiple dynamic assignments consecutively
writeln Time.now

PURPOSE = 1
MODE = 1

#The selection of controls you would like to run (i.e., User dimension):
#1: weather only, 2: maintenance only, 3: accidents only
#4: weather + maintenance, 5: weather + accidents, 6: maintenanc + accidents
#7: all
#8: no disruptions
#(edit the for-loop to only run certain selections of control)

for USER in 1..8 do
  for RESULT in 1..10 do

starttime = Time.now

#Set all controls to inactive
myQuery = OtQuery.new
myQuery.sql = 'update control SET active = 0 WHERE active = 1'
myQuery.execute
#Set the correct set of controls to active (according to RESULT number)
if USER < 8
  selection = RESULT * 100 + USER
  myQuery = OtQuery.new
  myQuery.sql = "update control SET active = 1 WHERE controlnr IN (SELECT objectnr FROM public.selectionobjects as a WHERE selectionnr = #{selection})"
  myQuery.execute
end

#Possibly, set own added controls (measures) to active
 # myQuery = OtQuery.new
 # myQuery.sql = "update control SET active = 1 WHERE controlnr = 90770"
 # myQuery.execute

#Create StreamLine instance
sl = OtStreamLine.new

#Open network
sl.input.network = [MODE,1000]
sl.input.odMatrix = [PURPOSE,MODE,1000,1]

#Deactivate controls if "no disruptions" (=8) is selected (for speed-up purposes)
#Note: Change if you're running no disruptions, but you do want to have your own controls (measures) tested
if USER < 8
  sl.input.controls = true
else
    sl.input.controls = false
end

# Simulation run from 5:30 till 12:00
# 0.5 hour to fill the network (5:30-6:00)
# 4 hours to analyse (6:00-10:00)
# 2 hours to empty the model (10:00-12:00)
# Departure time profile specified per 15 minutes
sl.propagation.duration = 23400 #6.5 hour * 60 minutes * 60 seconds
sl.input.fractions = [0.017414379, 0.025706941, 0.034828759, 0.034828759, 0.043784725, 0.055311386, 0.067252674, 0.073555021, 0.079276889, 0.082013434, 0.082925616, 0.081764657, 0.067501451, 0.060950328, 0.054979683, 0.049672444, 0.045277386, 0.042955469,0,0,0,0,0,0,0,0]
sl.output.startTime = 1800 #Start writing results after 0.5 hours of simulation (at 6:00)
sl.output.endTime = 16200 #End after  4 hours of simulation (at 10:00)

sl.propagation.timeStep = 5 #seconds
sl.propagation.segmentLength= 0.5 #500 meters
sl.propagation.adjustSegmentLength = true #extend links<500m to 500m to avoid skipping of links

# Generate routes for the first RESULT
# The same routes will be used for the next draws (to speed up computation time)
if RESULT == 1
  sl.routeGenerator = SL_DIJKSTRA
  sl.routeGenerator.alternativeGenerator = SL_MONTECARLO
  sl.routeGenerator.alternativeGenerator.maxIterations = 20
  sl.routeGenerator.filter.maxOverlapFactor = 0.8
  sl.output.routeSet = SL_OMNITRANS
else
  sl.routeGenerator = SL_NONE
  sl.input.routeSet = SL_OMNITRANS
  sl.input.routeSet.pmturi = [PURPOSE,MODE,1000,USER,1,1]
  sl.output.routeSet = SL_NONE
end

sl.routeChoice = SL_MSA
sl.routeChoice.maxIterations = 7

#Uncomment to store the route data set & costs.
#sl.routeCost.routeDataSet = SL_OMNITRANS
#sl.routeCost.routeDataSet.saveIterations = false
#sl.routeCost.finalRouteDataSet = SL_OMNITRANS
#sl.routeCost.finalRouteDataSet.pmturi = [PURPOSE,MODE,1000,USER,RESULT,1]
#sl.output.persistCostSnapshots = true

sl.output.aggregation = [300,5]
sl.output.load = [PURPOSE,MODE,1000,USER,RESULT,1]

sl.execute

#Remove all iterations from the database (only keep the last one)
maxIteration = OtQuery.execute("SELECT MAX(iteration) FROM link5_2data1 WHERE linknr = 1 AND time = 1030 AND purpose= #{PURPOSE} AND mode= #{MODE} AND \"user\"= #{USER} AND result= #{RESULT}")[0]
if maxIteration > 1
  OtQuery.execute("DELETE FROM link5_2data1 WHERE purpose= #{PURPOSE} AND mode= #{MODE} AND \"user\"= #{USER} AND result= #{RESULT} AND iteration < #{maxIteration}")
  OtQuery.execute("UPDATE link5_2data1 SET iteration = 1 WHERE purpose= #{PURPOSE} AND mode= #{MODE} AND \"user\"= #{USER} AND result= #{RESULT} AND iteration = #{maxIteration}")
end

endtime = Time.now
writeln 'Computation of ', USER, ',', RESULT, ': Start time = ',starttime, 'end time = ',endtime, ', difference = ', endtime-starttime;

end
end
