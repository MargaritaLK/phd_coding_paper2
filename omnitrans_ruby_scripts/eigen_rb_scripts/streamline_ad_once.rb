# OmniTRANS Job for 'MultiModal'

#create instance of Streamline

streamLine = OtStreamLine.new



#INPUT

streamLine.input.network = [10, 10]


#OD - one- zonder stop
#streamLine.input.odMatrix = [1, 10, 1000, 1]



## OD - at once met leegloop tijd
streamLine.input.odMatrix = [1, 10, [10, 1000 ], 1]
streamLine.input.durations = [1800, 5400]



#TRAFFIC PROPAGATION
streamLine.propagation.duration = 7200
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
#streamLine.output.load =[p, m,  t,  u,  r,i]
streamLine.output.load = [1, 10, 100, 1, 4, 7 ]
streamLine.output.persistCostSnapshots = true




#ECXECUTE

streamLine.execute
