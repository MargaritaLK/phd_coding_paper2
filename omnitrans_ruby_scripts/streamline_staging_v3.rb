# OmniTRANS Job for 'MultiModal'

#create instance of Streamline

streamLine = OtStreamLine.new



#INPUT

streamLine.input.network = [10, 10]

#OD - one- zonder stop
#streamLine.input.odMatrix = [1, 10, 1000, 1]




## OD - for staging
streamLine.input.odMatrix = [1, 10, [10, 20, 1000 ], 1]
streamLine.input.durations = [1800, 1800, 3600]



# route set generation (optional)

# route choice (optional)



#TRAFFIC PROPAGATION

streamLine.propagation.duration = 7200
streamLine.propagation.adjustSegmentLength = true


# OUTPUT
streamLine.output.load = [1, 10, 100, 1, 3, 7 ]

streamLine.output.persistCostSnapshots = true



#ECXECUTE

streamLine.execute
