# OmniTRANS Job for 'lk_testen_zelf_v2'
# Created 18/02/2022 17:07:07


# Create a Simple StreamLine instance
streamLine = OtStreamLine.new



#--- INPUT -----

## network - static
streamLine.input.network = [10,10]

## OD matrix - static
#streamLine.input.odMatrix = [1,10,10,1]


## OD matrix for staging
streamLine.input.odMatrix = [1, 10, [10, 20, 30], 1]
streamLine.input.durations = [1800, 1800, 10800]






#--- SIMULATION -----

## duration of simulation, must be sum of durations of matrices
streamLine.propagation.duration = 14400




# ---- OUTPUT

# Store the loads
streamLine.output.load = [1,10,100,1,19,1]

# Execute
streamLine.execute
