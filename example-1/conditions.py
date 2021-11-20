import pprint
from rulebase import *

cond = {}


def formConditionOnProposition(listOfRules, inf, propname, op, tau):
    i = 0
    m =""
    for r in listOfRules:
        p = r[0]
        j = 0
        for propattr in p:
            attr = propattr
            sdomain  = p[propattr]
            arrayidname = "neg p" if propname.startswith("neg") else "p"
            if propname in inf[i][arrayidname]["propositions"] and\
             attr == inf[i][arrayidname]["propositions"][propname]["attribute"]:
                if propname.startswith("neg"):
                    dom = attributes_domain_input[attr].difference(sdomain)
                else:
                    dom = sdomain
                if op == "=":
                    m +="il existe v \in " + str(dom)
                    m +="\pi_{"+ attr + "(x)}(v) = " + str(tau)
                    m +=" et pour tout v \in " + str(dom)
                    m +=" on a \pi_{"+ attr + "(x)}(v) <=" + str(tau) + "\n"

                if op == "<":
                    m +="pour tout v \in " + str(dom)
                    m +=" on a \pi_{"+ attr + "(x)}(v) <" + str(tau)+ "\n"

                if op == "<=":
                    m +="pour tout v \in " + str(dom)
                    m +=" on a \pi_{"+ attr + "(x)}(v) <=" + str(tau)+ "\n"

                if op == ">":
                    m +="il existe v \in " + str(dom)
                    m +=" \pi_{"+ attr + "(x)}(v) > " + str(tau)+ "\n"

                if op == ">=":
                    m +="il existe v \in " + str(dom)
                    m +=" \pi_{"+ attr + "(x)}(v) >= " + str(tau)+ "\n"
        i+=1
    return m

def formConditionFromLambdaRho(listOfRules, inf, idrule, lambdaOrRho, op, tau):
    i = 0
    m ="";
    for r in listOfRules:
        p = r[0]

        if idrule == i:
            if op == "<":
                if lambdaOrRho == "lambda":
                    m ="Il faut qu'au moins une de ces conditions soit vraie: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m +="- " + formConditionOnProposition(listOfRules, inf, prop, op, tau)

                if lambdaOrRho == "rho":
                    m ="Il faut que toutes ces conditions soient vraies: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m += "- " + formConditionOnProposition(listOfRules, inf, "neg " + prop, op, tau)

            if op == ">":
                if lambdaOrRho == "lambda":
                    m ="Il faut que toutes ces conditions soient vraies: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m += "- " + formConditionOnProposition(listOfRules, inf, prop, op, tau)
                if lambdaOrRho == "rho":
                    m ="Il faut qu'au moins une de ces conditions soit vraie: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m += "- " +formConditionOnProposition(listOfRules, inf, "neg " + prop, op, tau)
            if op == ">=":
                      if lambdaOrRho == "lambda":
                          m ="Il faut que toutes ces conditions soient vraies: \n"
                          for prop in inf[i]["p"]["propositions"]:
                              m += "- " + formConditionOnProposition(listOfRules, inf, prop, op, tau)
                      if lambdaOrRho == "rho":
                          m ="Il faut qu'au moins une de ces conditions soit vraie: \n"
                          for prop in inf[i]["p"]["propositions"]:
                              m += "- " +formConditionOnProposition(listOfRules, inf, "neg " + prop, op, tau)
            if op == "=":
                if lambdaOrRho == "lambda":
                    m ="Il faut qu'au moins une de ces conditions soit vraie: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m += "- " + formConditionOnProposition(listOfRules, inf, prop, op, tau)
                    m +="et que toutes ces conditions soient vraies :\n"
                    for prop in inf[i]["p"]["propositions"]:
                        m += "- " + formConditionOnProposition(listOfRules, inf, prop, ">=", tau)
                if lambdaOrRho == "rho":
                    m ="Il faut qu'au moins une de ces conditions soit vraie: \n"
                    for prop in inf[i]["p"]["propositions"]:
                        m +=formConditionOnProposition(listOfRules, inf, "neg " + prop, op, tau)
                    m +="et que toutes ces conditions soient vraies :\n"
                    for prop in inf[i]["p"]["propositions"]:
                        m +=formConditionOnProposition(listOfRules, inf, prop, "<=", tau)
        i+=1
    return m
