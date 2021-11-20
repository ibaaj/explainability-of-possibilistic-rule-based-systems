
import pprint
from rulebase import *

def inference(listOfRules,params,attributes_list_input,attributes_list_output,\
attributes_domain_input,attributes_input_distributions):
    ### build structure ###
    inf = []
    for i in range(0,len(listOfRules)):
        x = {
            "index" : i,
            "p" : {"propositions": {}, "deg": 0},
            "neg p" : {"propositions": {}, "deg": 0},
            "distrib_output" : {},
            }
        inf.append(x.copy())


    ### Inference Step 1 : calculer des degrés des propositions ###
    i = 0
    for r in listOfRules:
        p = r[0]
        j = 0
        for propattr in p:
            attr = propattr
            sdomain  = p[propattr]
            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)] = {}
            inf[i]["neg p"]["propositions"]["neg p_" + str(j) + "^" + str(i)] = {}

            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["attribute"] = attr
            inf[i]["neg p"]["propositions"]["neg p_" + str(j) + "^" + str(i)]["attribute"] = attr

            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"] =\
                    max([attributes_input_distributions[attr][d] for d in sdomain])
            inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["necessity"] =\
                    1 - max([attributes_input_distributions[attr][d] \
                        for d in attributes_domain_input[attr].difference(sdomain)])

            inf[i]["neg p"]["propositions"]["neg p_" + str(j) + "^" + str(i)]["possibility"] =\
                    max([attributes_input_distributions[attr][d] \
                        for d in attributes_domain_input[attr].difference(sdomain)])
            j+=1
        i+=1


    i = 0
    if params["debug"] is True:
        pprint.pprint(inf)
        print("\n inference step 1 : calcul des degrés des propositions \n")
        for r in listOfRules:
            p = r[0]
            j = 0
            for propattr in p:
                attr = propattr
                sdomain  = p[propattr]

                print("proposition: p_" + str(j) + "^" + str(i) + " : " +
                    attr + " in " + str(sdomain) + " is " +
                    str(inf[i]["p"]["propositions"]["p_" + str(j) + "^" + str(i)]["possibility"])
                    + " and " +
                    "neg p_" + str(j) + "^" + str(i) + " :" +
                    str(inf[i]["neg p"]["propositions"]["neg p_" + str(j) + "^" + str(i)])
                    + "\n" +
                    "because: " + pprint.pformat(attributes_input_distributions[attr])
                )
                j+=1
            i+=1


    ### Inference Step 2 : calcul des degré des prémisses et negation de prémisse ###

    i = 0
    for r in listOfRules:
        p = r[0]

        inf[i]["p"]["possibility"] =\
        min([inf[i]["p"]["propositions"][x]["possibility"] \
            for x in inf[i]["p"]["propositions"].keys()])

        inf[i]["neg p"]["possibility"] =\
        max([inf[i]["neg p"]["propositions"][x]["possibility"] \
            for x in inf[i]["neg p"]["propositions"].keys()])

        inf[i]["p"]["necessity"] = 1 - inf[i]["neg p"]["possibility"]
        inf[i]["neg p"]["necessity"] = 1 - inf[i]["p"]["possibility"]

        i+=1


    i = 0
    if params["debug"] is True:
        print("\n inference step 2 : calcul des degrés de possibilité des prémisses\n")
        for r in listOfRules:
            p = r[0]
            print("premisse : p^" + str(i) + " : " + pprint.pformat(p) + " is " +
            str(inf[i]["p"]["possibility"]) + " because: min("+str([x  \
             for x in inf[i]["p"]["propositions"].keys()]) +\
            ") = min("+ str([inf[i]["p"]["propositions"][x]["possibility"] \
             for x in inf[i]["p"]["propositions"].keys()])  +\
            ") = " + str(inf[i]["p"]["possibility"]))
            print("neg premisse : neg p^" + str(i) + " is " +
            str(inf[i]["neg p"]["possibility"]) + " because: max("+str([x  \
             for x in inf[i]["neg p"]["propositions"].keys()]) +\
            ") = max("+ str([inf[i]["neg p"]["propositions"][x]["possibility"] \
             for x in inf[i]["neg p"]["propositions"].keys()]) +") = "
             + str(inf[i]["neg p"]["possibility"]))
            i+=1

    ### Inference Step 3 ###

    i = 0
    for r in listOfRules:
        m = r[2]
        inf[i]["q"] = max(min(m[0][0], inf[i]["p"]["possibility"]),
                          min(m[0][1], inf[i]["neg p"]["possibility"]))
        inf[i]["neg q"] = max(min(m[1][0],inf[i]["p"]["possibility"]),
                              min(m[1][1],inf[i]["neg p"]["possibility"] ))

        i+=1

    if params["debug"] is True:
        print("\n inference step 3 : q et neg q pour chaque règle \n")
        i=0
        for r in listOfRules:
            printRule(r,i)
            m = r[2]
            print("deg q : " + str(inf[i]["q"]) + " because " +
             "max(min(" + str(m[0][0])+ "," + str(inf[i]["p"]["possibility"]) + "),"
                             + "min("+ str(m[0][1]) + "," +
                              str(inf[i]["neg p"]["possibility"]) + "))="
                              + str(inf[i]["q"]) )
            print("deg neg q : " + str(inf[i]["neg q"]) + " because " +
             "max(min(" + str(m[1][0])+ "," + str(inf[i]["p"]["possibility"]) + "),"
                             + "min("+ str(m[1][1]) + "," +
                              str(inf[i]["neg p"]["possibility"]) + "))="
                              + str(inf[i]["neg q"]) )

            i+=1

    ### Inference Step 4 ###

    i = 0
    for r in listOfRules:
        q = r[1]
        for propattr in q:
            attr = propattr
            sdomain  = q[propattr]
        inf[i]["distrib_output"][attr] = {}
        for e in attributes_domain_output[attr]:
            if e in sdomain:
                inf[i]["distrib_output"][attr][e] = inf[i]["q"]
            else:
                inf[i]["distrib_output"][attr][e] = inf[i]["neg q"]

        i+=1

    if params["debug"] is True:
        print("\n inference step 4 : distribution de possibilité de l'attribut de conclusion \n")
        i = 0
        for r in listOfRules:
            printRule(r,i)
            q = r[1]
            for propattr in q:
                attr = propattr
                sdomain  = q[propattr]
            for e in attributes_domain_output[attr]:
                if e in sdomain:
                    print(attr + "," + e + " is " + str(inf[i]["distrib_output"][attr][e])
                    + " the deg of q because " + str(e) + " is in " + str(sdomain))
                else:
                    print(attr + "," + e + " is " + str(inf[i]["distrib_output"][attr][e])
                    + " the deg of  neg q  because " + str(e) + " is not in " + str(sdomain))
            i+=1

    ### Inference Step 5 ###

    i = 0
    distribFinal = {}
    for r in listOfRules:
        q = r[1]
        for propattr in q:
            attr = propattr
            sdomain  = q[propattr]

        if attr in distribFinal.keys():
            #print("current new is" + str(inf[i]["distrib_output"][attr]))
            #print("from")
            #printRule(r,i)
            for v in inf[i]["distrib_output"][attr]:
                #print("may "+ str(attr) + ":" + str(v)+ "udapte with" + str(inf[i]["distrib_output"][attr][v]))
                if inf[i]["distrib_output"][attr][v] < distribFinal[attr][v]:
                    distribFinal[attr][v] = inf[i]["distrib_output"][attr][v]
        else:
            distribFinal[attr] = inf[i]["distrib_output"][attr]
            #print("init value for " + str(attr) + " is " + str(inf[i]["distrib_output"][attr]))
        i+=1

    if params["debug"] is True:
        pprint.pprint(distribFinal)
        print("\n inference step 5 : combination conjonctive par le min \n")
        for attr in distribFinal:
            print(attr + ":" )
            for v in distribFinal[attr]:
                print(v + " is " + str(distribFinal[attr][v]) + " because min("
                + str([inf[j]["distrib_output"][attr][v] for j in range(0,len(listOfRules))]) +
                ")=" + str(distribFinal[attr][v]))



    i = 0
    sv = []
    rv = []
    lambdav = []
    rhov = []
    for r in listOfRules:
        lambdav.append(inf[i]["p"]["possibility"])
        rhov.append(inf[i]["neg p"]["possibility"])
        rv.append(r[2][1][0])
        sv.append(r[2][0][1])
        i+=1


    return (sv,rv,lambdav,rhov,inf,distribFinal)
