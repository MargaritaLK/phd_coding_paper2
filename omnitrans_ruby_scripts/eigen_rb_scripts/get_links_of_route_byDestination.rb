# this example will print all routes with destination 1 in the routeset.

destinationNumber = 80



myRouteSetCube = OtRouteSetCube.new

myRouteSet = myRouteSetCube.get([1,11,10,1,3,1])

myRouteSet.open



# get routes for this destination

myRouteSet.getRoutesByDestination(destinationNumber) { |route|

p route

}

myRouteSet.close
