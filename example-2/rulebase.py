
import pprint
import random



#### Attributes #####
attributes_list_input = set([
                            "planned-foods",
                            "planned-alcohol",
                            "current-bloodsugar",
                            "planned-physicalactivity",
                            "planned-sleep",
                            "water-intake",
                            "last-hypoglycemia",
                            "previous-slept-duration",
                            "environmental-temperature"
                            ])
attributes_list_output = set(["insulin-dose"])

attributes_domain_input = {
                    "planned-foods": set(["no", "diet-foods", "high-fat-foods"]),
                    "planned-alcohol": set(["no", "low", "important"]),
                    "current-bloodsugar": set(["low", "medium", "high"]),
                    "planned-physicalactivity" : set(["no", "short", "long"]),
                    "planned-sleep": set(["no", "short", "long", "very-long"]),
                    "water-intake": set(["sufficient", "insufficient"]),
                    "last-hypoglycemia": set(["no", "long-time-ago", "recent", "very-recent"]),
                    "previous-slept-duration": set(["very-short","short","long", "very-long"]),
                    "environmental-temperature": set(["cold", "warm", "hot"]),
                    }
attributes_domain_output = {"insulin-dose" : set(["low", "medium", "high"])}



##### Rules ######
# p : premisse, q : conclusion,
# r_param: paramètre "r" de m : matrice des distrib. poss. cond. de la règle
listOfRules = []
def buildRulesBase():
    p_1 = {
    "planned-foods": set(["diet-foods", "high-fat-foods"]),
    "planned-alcohol" : set(["no", "low"])
    }
    q_1 = {"insulin-dose" : set([ "medium", "high"])}
    r_param_1 = 0
    s_param_1 = 0.3
    m_1 = [[1,s_param_1],[r_param_1,1]]

    p_2 = {
    "current-bloodsugar": set(["high"]),
    "planned-physicalactivity" : set(["no", "short"])
    }
    q_2 = {"insulin-dose" : set(["low"])}
    r_param_2 = 0
    s_param_2 = 1
    m_2 = [[1,s_param_2],[r_param_2,1]]

    p_3 = {
    "current-bloodsugar": set(["low", "medium"]),
    "planned-foods" : set(["no"]),
    "planned-sleep": set(["long", "very-long"])
    }
    q_3 = {"insulin-dose" : set(["low"])}
    r_param_3 = 0
    s_param_3 = 0.7
    m_3 = [[1,s_param_3],[r_param_3,1]]

    p_4 = {
    "water-intake": set(["sufficient"]),
    "last-hypoglycemia" : set(["no", "long-time-ago"]),
    "previous-slept-duration": set(["long", "very-long"])
    }
    q_4 = {"insulin-dose" : set(["low","medium"])}
    r_param_4 = 0
    s_param_4 = 0.4
    m_4 = [[1,s_param_4],[r_param_4,1]]

    p_5 = {
    "environmental-temperature": set(["cold", "warm"])
    }
    q_5 = {"insulin-dose" : set(["low","medium"])}
    r_param_5 = 1
    s_param_5 = 0
    m_5 = [[1,s_param_5],[r_param_5,1]]

    return [[p_1,q_1,m_1],[p_2,q_2,m_2],[p_3,q_3,m_3],[p_4,q_4,m_4],[p_5,q_5,m_5]]






def randomizeDistribution():
    for attr in attributes_input_distributions:
        nb_elem = len(attributes_input_distributions[attr])
        new_val = [random() for x in range(0,nb_elem)]
        new_val_norm = [1 if x==max(new_val) else 0 if x==min(new_val) else x for x in new_val]
        i = 0
        for elem in attributes_input_distributions[attr]:
            attributes_input_distributions[attr][elem] = new_val_norm[i]
            i+=1
def buildAttributeDistrib(params,attributes_input_distributions):
    if params["random_input_distribution"] is True:
        randomizeDistribution()
    return (attributes_list_input,attributes_list_output,\
    attributes_domain_input,attributes_input_distributions)


### printer ###


def printRule(r,i):
    print(str(i) + ": IF " + pprint.pformat(r[0]) + " THEN " +\
            pprint.pformat(r[1]) + " de matrice " + pprint.pformat(r[2]))
def printAllRules(listOfRules):
    i = 0
    for r in listOfRules:
        printRule(r,i)
        i+=1
