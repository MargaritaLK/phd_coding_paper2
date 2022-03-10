# Skim generation car distance (in km)

# Dimensions (see Project Setup)
# Purpose:   1  = Total
# Mode:      10 = Car
# Time:      10 = AM
# User:      1  = Total
# Result:    12 = Distance, 13 = Free-flow travel time
# Iteration: 1  = Iteration1

makeSkim = OtTraffic.new
makeSkim.network = [10,10]
makeSkim.skimMatrix = [1,10,10,1,[0,12,13],1]
makeSkim.skimFactors = [1,1,60]
makeSkim.execute

# Fill intrazonal impedances
sc = OtSkimCube.open
mat = sc[1,10,10,1,12,1]
ok = mat.fillIntra(3)
sc[1,10,10,1,12,1] = mat
