

routePMTURI = [1,10,100,1,99,5]

originNumber = 22

myRouteSetCube = OtRouteSetCube.new
myRouteSet = myRouteSetCube.get([1,10,100,1,99,5])
myRouteSet.open


# get routes for this origin
myRouteSet.getRoutesByOrigin(originNumber) { |route|
# print route
p route
}

myRouteSet.close
