#[p,m,t,u,r,i]
#purpose mode time user result iteration


#create instance of Streamline
streamLine = OtStreamLine.new





#INPUT

streamLine.input.network = [1, 2]

#streamLine.input.odMatrix = [p,m,t,u]
streamLine.input.odMatrix = [1, 2, 2, 1]



# ROUTE SET generation (optional)


# ROUTE CHOICE (optional)



#TRAFFIC PROPAGATION
streamLine.propagation.duration = 14400


# OUTPUT
#streamLine.output.load = [p,m,t,u,r,i]
streamLine.output.load = [1, 1, 2, 2, 1, 1 ]





#ECXECUTE

streamLine.execute
