
#create instance of Streamline

streamLine = OtStreamLine.new


#Purpose
#1  totaal

#Mode
#1 auto

#Time
#2 period2

#User
#1 totaal

#Result
#1 dynamic

#Iteration
#1 iteration



#INPUT

streamLine.input.network = [1, 2]

streamLine.input.odMatrix = [1, 2, 2, 1]



# route set generation (optional)

# route choice (optional)



#TRAFFIC PROPAGATION
streamLine.propagation.duration = 14400


# OUTPUT
streamLine.output.load = [1, 1, 2, 2, 1, 1 ]





#ECXECUTE

streamLine.execute
