originNumber = 1
destinationNumber = 10


myRouteSetCube = OtRouteSetCube.new
myRouteSet = myRouteSetCube.get([1,11,10,1,3,1])

myRouteSet.open



# get routes for this origin and destination
myRouteSet.getRoutesByOriginAndDestination(originNumber, destinationNumber) { |route|
# print route
p route
}

myRouteSet.close
