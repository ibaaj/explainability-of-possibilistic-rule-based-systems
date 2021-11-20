from __main__ import *
from inference import *
from rulebase import *
from equations import *
from reductions import *
import sys
import io
from itertools import chain, combinations
import time


params = {
    "two_rules_only": True,
    "random_input_distribution": False,
    "debug": False
}

attributes_input_distributions = {
    "selected-action": {
        "alcohol-consumption": 0,
        "breakfast": 0,
        "dinner": 0,
        "drink-coffee": 1,
        "long-sleep": 0,
        "lunch": 0,
        "sport": 0,
        "walking": 0
    },
    "current-blood-glucose": {
        "low": 0.3,
        "medium": 1,
        "high": 0
    },
}



def printAllDistribInput():
    pprint.pprint(attributes_input_distributions)



params["debug"] = True

listOfRules = buildRulesBase()

if params["debug"] == True:
    print("Les règles:")
    printAllRules(listOfRules)
    print("Les distributions de possibilités des attributs d'entrée:")
    printAllDistribInput()

(sv,rv,lambdav,rhov,inf,distribFinal) = inference(listOfRules,params,\
            attributes_list_input,attributes_list_output,attributes_domain_input,\
            attributes_input_distributions)

n = len(listOfRules)
MR = buildMR([], n, 1)
IV = buildIV(n)
OVn = buildOV(n, "s", "r", strmap["lambda"], strmap["rho"])
OV = buildOVAlphaBeta(n)
Crondn = buildCrond(n)
Dn = buildDi(n)

qsets = setQSets(n, listOfRules, attributes_list_output,
                 attributes_domain_output, params)

(MRval, IVval, OVval, Dival,
 Diresult) = setVarsFromInference(n, sv, rv, lambdav, rhov)

s = 1
mapG = {}
for i, nb in zip(qsets, range(len(qsets))):
    sol = i
    result = min(OVval[sol][1:])
    print("Let u in " + str(Crondn[sol]) + " : " + str(qsets[sol]))
    print(strmap["pi"] + "(u)\t=\t" + Dn[sol] + "\t=\t" + Dival[sol] +
          "\n\t=\t" + Diresult[sol] + "\t=\t" + str(result))

    print("Sensibility Analysis with fixed IV")
    Justification = SensibilityAnalysisFixedIV(IV, OV, IVval, sol, result)
    JPJR(IV,OV,IVval,sol,result)
    red = prepareReductions(listOfRules, inf, attributes_input_distributions)
    print("Justification : [(premisse id, semantic, degree)]")
    print(Justification)
    getIdC= []
    for id, sem, deg in Justification:
        pprint.pprint({id: red[id]})
        if deg == 0:
          getIdC.append(id)
