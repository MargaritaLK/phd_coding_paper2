# This example retreives all route data for a given origin and destination

routePMTURI = [1,10,100,1,99,3]

# open routeset
myRouteSetCube = OtRouteSetCube.new
myRouteSet = myRouteSetCube.get(routePMTURI)
myRouteSet.open

#open route data set
myRouteDataSetCube = OtRouteDataCube.new
myRouteDataSet = myRouteDataSetCube.get(routePMTURI)
myRouteDataSet.open


# get the fields in this data set
fields = myRouteDataSet.fields


originNumber = 45
destinationNumber = 80


# get routes for this origin
myRoutes = myRouteDataSet.getRoutesByOriginAndDestination(originNumber, destinationNumber)
for i in 0..myRoutes.length-1
   myRoute = myRoutes[i]

   # get route ID
   routeID = myRoute[0][0]

   # get route data for this route
   values = myRouteDataSet.get(routeID)

   for i in 0..values.length-1
      # ..and write out the name of the field, the value and its type (the class method)
      write fields[i][0],' = ',values[i],' (',values[i].class,'), '
   end

   writeln ""


end

myRouteSet.close
myRouteDataSet.close
