
import pprint
import random



#### Attributes #####
attributes_list_input = set(["selected-action","current-blood-glucose"])
attributes_list_output = set(["future-blood-glucose"])

attributes_domain_input = {
                    "selected-action": set(["alcohol-consumption","breakfast","dinner","drink-coffee",
                    "long-sleep","lunch","sport","walking"]),
                    "current-blood-glucose" : set(["low", "medium", "high"])
                    }
attributes_domain_output = {"future-blood-glucose" : set(["low", "medium", "high"])}



##### Rules ######
# p : premisse, q : conclusion,
# r_param: paramètre "r" de m : matrice des distrib. poss. cond. de la règle
listOfRules = []
def buildRulesBase():
    p_1 = {"selected-action" : set(["lunch", "dinner", "drink-coffee"]),
           "current-blood-glucose" : set(["medium","high"])
          }
    q_1 = {"future-blood-glucose" : set(["high"])}
    r_param_1 = 0
    s_param_1 = 1
    m_1 = [[1,s_param_1],[r_param_1,1]]
    p_2 = {"selected-action" : set(["sport", "walking", "long-sleep"]),
             "current-blood-glucose" : set(["low","medium"])
            }
    q_2 = {"future-blood-glucose" : set(["low"])}
    r_param_2 = 0
    s_param_2 = 0.7
    m_2 = [[1,s_param_2],[r_param_2,1]]
    p_3 = {"selected-action" : set(["alcohol-consumption", "breakfast"]),
              "current-blood-glucose" : set(["low","medium"])
             }
    q_3 = {"future-blood-glucose" : set(["low","medium"])}
    r_param_3 = 0
    s_param_3 = 1
    m_3 = [[1,s_param_3],[r_param_3,1]]

    return [[p_1,q_1,m_1],[p_2,q_2,m_2],[p_3,q_3,m_3]]






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
