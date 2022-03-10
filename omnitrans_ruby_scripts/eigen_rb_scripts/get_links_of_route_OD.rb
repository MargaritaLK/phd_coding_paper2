
routePMTURI = [1,10,100,1,99,3]


originNumber = 45
destinationNumber = 80


myRouteSetCube = OtRouteSetCube.new
myRouteSet = myRouteSetCube.get(routePMTURI)

myRouteSet.open



# get routes for this origin and destination
myRouteSet.getRoutesByOriginAndDestination(originNumber, destinationNumber) { |route|
# print route
p route
}

myRouteSet.close



#return all linknr van routes
