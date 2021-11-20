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




def printAllDistribInput():
    pprint.pprint(attributes_input_distributions)



attributes_input_distributions = {
"planned-foods": {"no":0,"diet-foods":1,"high-fat-foods":0.2},
"planned-alcohol": {"no":1,"low":0,"important":0},
"current-bloodsugar": {"low":0.3,"medium":1,"high":0},
"planned-physicalactivity" : {"no":1,"short":0,"long":0},
"planned-sleep": {"no":1,"short":0,"long":0,"very-long":0},
"water-intake": {"sufficient":1,"insufficient":0.4},
"last-hypoglycemia": {"no":0.3,"long-time-ago":1,"recent":0,"very-recent":0},
"previous-slept-duration": {"very-short": 0,"short": 1,"long":0.2,"very-long":0},
"environmental-temperature": {"cold":0,"warm":1,"hot":0.2}
}



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
