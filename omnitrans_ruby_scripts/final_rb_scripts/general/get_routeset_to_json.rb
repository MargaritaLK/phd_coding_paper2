
require 'json'

resultnr = 67


routePMTURI = [1, 10, 100, 1, resultnr, 5 ]


destinationNumber = 80



myRouteSetCube = OtRouteSetCube.new

myRouteSet = myRouteSetCube.get(routePMTURI)

myRouteSet.open



# get routes for this destination

routes = []

myRouteSet.getRoutesByDestination(destinationNumber) { |route|

  routenr = route[0][0]
  orignnr = route[0][1]
  routelinks = route[1]

  route_hash = {"routenr" => routenr,
                "orignnr" => orignnr,
                "routelinks" => routelinks}



  p orignnr

  routes.push(route_hash)

}

File.open("routes.json","w"){ |f| f.write routes.to_json }


myRouteSet.close


file1 = File.read('routes.json')

#p file1
