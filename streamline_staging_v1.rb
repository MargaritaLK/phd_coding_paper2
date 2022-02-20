# OmniTRANS Job for 'lk_testen_zelf_v2'
# Created 18/02/2022 17:07:07

# Create a Simple StreamLine instance
streamLine = OtStreamLine.new


# NETWORK - INOUT
streamLine.input.network = [10,10]


## OD - INPOUT
#streamLine.input.odMatrix = [1,10,10,1]


## STAGING
streamLine.input.odMatrix = [1, 10, [10, 20, 30], 1]
streamLine.input.durations = [1800, 1800, 10800]


## duration of simulation, must be sum of durations of matrices
streamLine.propagation.duration = 14400




# Store the loads
streamLine.output.load = [1,10,100,1,19,1]

# Execute
streamLine.execute
