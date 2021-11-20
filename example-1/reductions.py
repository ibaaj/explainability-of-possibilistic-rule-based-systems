
import pprint
from rulebase import *


red = {}
def prepareReductions(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        red[i] = {}
        red[i]["p"] = {}
        red[i]["p"]["P_propositions_reduites_possibility"] = {}
        red[i]["p"]["P_propositions_reduites_necessity"] = {}

        i+=1
    P_possibility(listOfRules,inf,attributes_input_distributions)
    P_necessity(listOfRules,inf,attributes_input_distributions)
    R_possibility(listOfRules,inf,attributes_input_distributions)
    R_necessity(listOfRules,inf,attributes_input_distributions)
    C_possibility(listOfRules,inf,attributes_input_distributions)
    C_necessity(listOfRules,inf,attributes_input_distributions)
    return red

def P_possibility(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        j = 0

        for propattr in p:
            attr = propattr
            sdomain  = p[propattr]

            red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)] = {}

            if inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"] < 0.1:
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr] ={}
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr]['deg'] = \
                inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"]
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr]['subdomain']  =\
                set([d for d in sdomain])
            else:
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr] ={}
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr]['deg'] = \
                inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"]
                red[i]["p"]["P_propositions_reduites_possibility"]["p_" + str(j) + "^" + str(i)][attr]['subdomain'] =\
                    set([d for d in sdomain \
                        if attributes_input_distributions[attr][d] ==
                            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"]])
            j+=1
        i+=1

def P_necessity(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        j = 0

        for propattr in p:
            attr = propattr
            sdomain  = p[propattr]

            red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)] = {}

            if inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["necessity"] < 0.1:
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr] = {}
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr]['deg'] = \
                inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["necessity"]
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr]['subdomain'] =\
                    set([d for d in sdomain])
            else:
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr] = {}
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr]['deg'] = \
                inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["necessity"]
                red[i]["p"]["P_propositions_reduites_necessity"]["p_" + str(j) + "^" + str(i)][attr]['subdomain']=\
                set([d for d in sdomain]).union(
                        set(
                        [d for d in attributes_domain_input[attr].difference(sdomain) \
                        if 1 - attributes_input_distributions[attr][d] >
                            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["necessity"]]
                            )
                        )
            j+=1
        i+=1

def R_possibility(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        if inf[i]["p"]["possibility"] >= 0.1:
            red[i]["p"]["R_possibility"] = set([x for x in inf[i]["p"]["propositions"].keys()])
        else:
            red[i]["p"]["R_possibility"] = set([x for x in inf[i]["p"]["propositions"].keys()\
                                        if inf[i]["p"]["propositions"][x]["possibility"] < 0.1])
        i+=1

def R_necessity(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        if inf[i]["p"]["necessity"] >= 0.1:
            red[i]["p"]["R_necessity"] = set([x for x in inf[i]["p"]["propositions"].keys()])
        else:
            red[i]["p"]["R_necessity"] = set([x for x in inf[i]["p"]["propositions"].keys()\
                                        if inf[i]["p"]["propositions"][x]["necessity"] < 0.1])
        i+=1


def C_possibility(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        if inf[i]["p"]["possibility"] < 0.1:
            red[i]["p"]["C_possibility"] = set([x for x in inf[i]["p"]["propositions"].keys()\
                                        if inf[i]["p"]["propositions"][x]["possibility"] >= 0.1])
        else:
            red[i]["p"]["C_possibility"] = set()
        i+=1
    return

def C_necessity(listOfRules,inf,attributes_input_distributions):
    i = 0
    for r in listOfRules:
        p = r[0]
        if inf[i]["p"]["necessity"] < 0.1:
            red[i]["p"]["C_necessity"] = set([x for x in inf[i]["p"]["propositions"].keys()\
                                        if inf[i]["p"]["propositions"][x]["necessity"] >= 0.1])
        else:
            red[i]["p"]["C_necessity"] = set()
        i+=1
