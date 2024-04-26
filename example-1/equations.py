from __main__ import *
import codecs
import sys
import numpy as np
import random
import math

strmap = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
    "7": "₇", "8": "₈", "9": "₉", "10":"₁₀",

    "lambda": "\u03BB", "alpha": "\u03B1", "beta": "\u03B2", "rho": "\u03C1",
    "Qbar" : u'Q\u0305', 'bar' : u'\u0305',
    "in" : 	u"\u2208", "pi" : u"\u03C0", "notequal" : u"\u2260",
    "tau" : u"\u03C4"
}

sval = {}
rval = {}
lambdaval = {}
rhoval = {}
alphaval = {}
betaval = {}


def nbAsStrSub(nb):
    return ''.join([strmap[c] for c in str(nb)])

def printMatrix(matrix):
    print(stringMatrix(matrix))

def stringMatrix(matrix):
    return '\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix])

def printTwoMatrix(m1,m2):
    print('\n'.join(['\t'.join([c1 + "=" + str(c2) \
     if isinstance(c1,str) else str(c1) for c1,c2 in zip(r1,r2)]) \
      for r1,r2 in zip(m1,m2)]))

def printOneCol(matrix):
    for row in matrix:
        print(row)

def printOneColTwoMatrix(m1,m2):
    for r1,r2 in zip(m1,m2):
        print(str(r1) + "\t=\t" + str(r2))

def printOneColThreeMatrix(m1,m2,m3):
    for r1,r2,r3 in zip(m1,m2,m3):
        print(str(r1) + "\t=\t" + str(r2) + "\t=\t" + str(r3))

def buildMR(matrix,n,i):
    if i == 1:
        matrix = [["s" + nbAsStrSub(1), 1], [1, "r" + nbAsStrSub(1)]]
    else:
        matrix1 = []
        matrix2 = []
        for x in matrix:
            l1 = []
            l2 = []
            for y in x:
                l1.append(y)
                l2.append(y)
            l1.extend(["s" + nbAsStrSub(i), 1])
            l2.extend([1,"r" + nbAsStrSub(i)])
            matrix1.append(l1)
            matrix2.append(l2)
        matrix = matrix1 + matrix2

    if i == n:
        return matrix
    else:
        return buildMR(matrix,n,i+1)

def buildIV(n,terminaison=""):
    matrix = []
    for i in range(1,n+1):
        if i == 1:
            matrix = [strmap["lambda"] + terminaison + nbAsStrSub(1), strmap["rho"] + terminaison + nbAsStrSub(1)]
        else:
            matrix.append(strmap["lambda"] + terminaison + nbAsStrSub(i))
            matrix.append(strmap["rho"] + terminaison + nbAsStrSub(i))
    return matrix



def buildmatrix(matrix,letter1,letter2,n,mode,i = 1):
    if i == 1:
        if mode == "uplet":
            matrix = [(letter1 + nbAsStrSub(1),),(letter2 + nbAsStrSub(1),)]
        if mode == "func":
            matrix = [letter1 + nbAsStrSub(1),letter2 + nbAsStrSub(1)]
    else:
        matrix1 = []
        matrix2 = []
        for x in matrix:
            l1 = x
            l2 = x
            if mode == "uplet":
                l1 = l1 + (letter1 + nbAsStrSub(i),)
                l2 = l2 + (letter2 + nbAsStrSub(i),)
            if mode == "func":
                l1 = l1 + letter1 + nbAsStrSub(i)
                l2 = l2 + letter2 + nbAsStrSub(i)

            matrix1.append(l1)
            matrix2.append(l2)
        matrix = matrix1 + matrix2

    if i == n:
        return matrix
    else:
        return buildmatrix(matrix,letter1,letter2,n,mode,i+1)



def buildBi(n,x1,y1,x2,y2):
    m1 = buildmatrix([],x1,y1,n,"uplet")
    m2 = buildmatrix([],x2,y2,n,"uplet")

    Bi = []
    for x1,x2 in zip(m1,m2):
        l = []
        for y1,y2 in zip(x1,x2):
            r = ('max', y1, y2)
            l.append(r)
        Bi.append(l.copy())
    return Bi


def buildOV(n,x1,y1,x2,y2):
    Bi = buildBi(n,x1,y1,x2,y2)
    OV = []
    for x in Bi:
        l = ("min",x)
        OV.append(l)
    return OV



def setAlphaBeta(matrix,terminaison):
    nmatrix = []
    for x in matrix:
        l = len(x[1])
        i = 0
        c = ("min",)
        for z in x[1]:
            if z[1][0] == "s" and z[2][0] == strmap["lambda"]:
                c = c + (strmap["alpha"]+terminaison + z[1][1:],)
            if z[1][0] == "r" and z[2][0] == strmap["rho"]:
                c = c + (strmap["beta"]+terminaison + z[1][1:],)
            i+=1
            if i == l:
                nmatrix.append(c)
    return nmatrix

def buildOVAlphaBeta(n, terminaison=""):
    return setAlphaBeta(buildOV(n,"s",
            "r" ,
             strmap["lambda"],
              strmap["rho"]), terminaison)


def buildCrond(n, terminaison=""):
    return buildmatrix([],"Q" + terminaison,strmap["Qbar"] + terminaison,n,"func")

def buildDi(n, terminaison=""):
    OV = buildOVAlphaBeta(n, terminaison)
    Crondi = buildCrond(n, terminaison)

    m = []
    for x1,x2 in zip(OV,Crondi):
        l = "min" + str(x1[1:]) + "*" + str(x2)
        m.append(l)
    return m



def setVarsRandom(n):
    for i in range(1,n+1):
        sval["s" + nbAsStrSub(i)] = round(random.uniform(0,1), 2)
        rval["r" + nbAsStrSub(i)] = round(random.uniform(0,1), 2)
        lambdaval[strmap["lambda"] + nbAsStrSub(i)] = round(random.uniform(0,1), 2)
        rhoval[strmap["rho"] + nbAsStrSub(i)] = round(random.uniform(0,1), 2)
        alphaval[strmap["alpha"] + nbAsStrSub(i)] =\
            max(sval["s" + nbAsStrSub(i)],lambdaval[strmap["lambda"] + nbAsStrSub(i)])
        betaval[strmap["beta"] + nbAsStrSub(i)] =\
            max(rval["r" + nbAsStrSub(i)],rhoval[strmap["rho"] + nbAsStrSub(i)])
    return setVars(n)



def setQSets(n,listOfRules,attributes_list_output,attributes_domain_output,params):
    fixedmatrix = {}
    Crondn = buildCrond(n)
    i = 1
    for r in listOfRules:
        for k,v in r[1].items():
            fixedmatrix["Q" + nbAsStrSub(i)] = set(v)
            fixedmatrix[strmap["Qbar"] + nbAsStrSub(i)] =\
                                set(attributes_domain_output[k].difference(v))
        i+=1
    w = ""
    qsets = {}
    j = 0
    for c in Crondn:
        ctmp = c
        s = set()
        i = 0
        while len(c) != 0:
            for k in fixedmatrix.keys():
                if c.startswith(k):
                    if len(s) == 0 and i == 0:
                        s = fixedmatrix[k]
                        i = 1
                    else:
                        s = set(s).intersection(set(fixedmatrix[k]))
                    c = c.split(k,1)[1]

        if len(s) > 0:
            if params["debug"] == True:
                qsets[j] = s
                w = ctmp + " is " + str(s) + "\n"
                print(w)
        j+=1


    return qsets






def setVarsFromInference(n,sv,rv,lambdav,rhov):
    for i in range(1,n+1):
        sval["s" + nbAsStrSub(i)] = sv[i-1]
        rval["r" + nbAsStrSub(i)] = rv[i-1]
        lambdaval[strmap["lambda"] + nbAsStrSub(i)] = lambdav[i-1]
        rhoval[strmap["rho"] + nbAsStrSub(i)] = rhov[i-1]
    return setVars(n)

def setVars(n):
    for i in range(1,n+1):
        alphaval[strmap["alpha"] + nbAsStrSub(i)] =\
            max(sval["s" + nbAsStrSub(i)],lambdaval[strmap["lambda"] + nbAsStrSub(i)])
        betaval[strmap["beta"] + nbAsStrSub(i)] =\
            max(rval["r" + nbAsStrSub(i)],rhoval[strmap["rho"] + nbAsStrSub(i)])
    MR = buildMR([],n,1)

    MRval = []
    for x in MR:
        l = []
        for y in x:
            if isinstance(y, int):
                l.append(y)
                continue
            if y.startswith("s"):
                l.append(sval[y])
            else:
                l.append(rval[y])
        MRval.append(l.copy())
    IV = buildIV(n)
    IVval = []
    for x in IV:
        if x.startswith(strmap["lambda"]):
            IVval.append(lambdaval[x])
        if x.startswith(strmap["rho"]):
            IVval.append(rhoval[x])

    OV = buildOVAlphaBeta(n)
    OVval = []
    for x in OV:
        l = ()
        for y in x:
            if y.startswith("min"):
                l = l + ("min",)
            if y.startswith(strmap["alpha"]):
                l = l + (alphaval[y],)
            if y.startswith(strmap["beta"]):
                l = l + (betaval[y],)
        OVval.append(l)

    Crondi = buildCrond(n)
    Dival = []
    Diresult = []
    for x1,x2 in zip(OVval,Crondi):  # recreating
        l = "min" + str(x1[1:]) + "*" + str(x2)
        Dival.append(l)
        Diresult.append(str(min(x1[1:])) + "*" + str(x2))

    return (MRval,IVval,OVval,Dival,Diresult)



def SensibilityAnalysisFixedIV(IV,OV,IVval,sol,result):
    Justification = []
    for x1,x2 in zip(IV,IVval):
        s = x1+"="+str(x2) + "\t:\t"
        if x1.startswith(strmap["lambda"]):
            id = x1.split(strmap["lambda"],1)[1]
            realid = int(list(strmap.keys())[list(strmap.values()).index(id)][0])
            if strmap["alpha"] + id  in OV[sol]:
                s += "u in Q" + id + "\t\t"
                if x2 == alphaval[strmap["alpha"] + id]:
                    s += x1 + "=" + strmap["alpha"] + id + "=" +\
                    "max(s"+ id +","+ strmap["lambda"] + id + ")" +\
                    "=max("+str(sval["s" + id])+","+\
                    str(lambdaval[strmap["lambda"] + id])+")" +\
                    "\t"
                    if lambdaval[strmap["lambda"]+id] == result:
                        s += strmap["alpha"] + id + "=" + strmap["pi"] +\
                         "(u)" +"=" + str(result) + "\t" + "yes"
                        Justification.append((realid-1,"possible", result))
                    else:
                        s += strmap["alpha"] + id + strmap["notequal"] +\
                         strmap["pi"] + "(u)" +"=" + str(result) + "\t" + " no"
                else:
                    s += x1 + strmap["notequal"] + strmap["alpha"] + id + "=" +\
                    "max(s"+ id +","+\
                     strmap["lambda"] + id + ")" +\
                    "=max("+str(sval["s" + id])+","+\
                    str(lambdaval[strmap["lambda"] + id])+")" +\
                    "\t\t no"
            else:
                s += "u not in Q" + id + "\t\t\t\t\t\t\t no"
        if x1.startswith(strmap["rho"]):
            id = x1.split(strmap["rho"],1)[1]
            if strmap["beta"] + id  in OV[sol]:
                s += "u in " + strmap["Qbar"] + id + "\t"
                if x2 == betaval[strmap["beta"] + id]:
                    s += x1 + "=" + strmap["beta"] + id + "=" +\
                    "max(r"+ id +","+ strmap["rho"] + id + ")" +\
                    "=max("+str(rval["r" + id])+","+\
                    str(rhoval[strmap["rho"] + id])+")" +\
                    "\t"
                    if rhoval[strmap["rho"]+id] == result:
                        s += str(rhoval[strmap["rho"]+id]) + "=" + strmap["pi"] +\
                         "(u)" +"=" + str(result) + "\t" + "yes"
                        Justification.append((realid-1,"certain", 1-result))
                    else:
                        s += strmap["beta"] + id + strmap["notequal"] +\
                         strmap["pi"] + "(u)" +"=" + str(result) + "\t" + " no"
                else:
                    s += x1 + strmap["notequal"] + strmap["beta"] + id + "=" +\
                    "max(r"+ id +","+\
                     strmap["rho"] + id + ")" +\
                    "=max("+str(rval["r" + id])+","+\
                    str(rhoval[strmap["rho"] + id])+")" +\
                    "\t\t\t no"
            else:
                s += "u not in " + strmap["Qbar"] + id + "\t\t\t\t\t\t\t no"
        print(s)

    return Justification


def JPJR(IV,OV,IVval,sol,result):
    JP = []
    JR = []
    ctheta = 1
    ct = 1
    for x1,x2 in zip(IV,IVval):
        s = x1+"="+str(x2) + "\t:\t"
        if x1.startswith(strmap["lambda"]):
            id = x1.split(strmap["lambda"],1)[1]
            realid = int(list(strmap.keys())[list(strmap.values()).index(id)][0])
            if strmap["alpha"] + id  in OV[sol]:
                if sval["s" + id] <= lambdaval[strmap["lambda"] + id]:
                    JP.append(id)
                    ctheta = min(ctheta,lambdaval[strmap["lambda"] + id])
                if sval["s" + id] >= lambdaval[strmap["lambda"] + id]:
                    JR.append(id)
                    ct = min(ct, sval["s" + id])
        if x1.startswith(strmap["rho"]):
            id = x1.split(strmap["rho"],1)[1]
            if strmap["beta"] + id  in OV[sol]:
                if rval["r" + id] <= rhoval[strmap["rho"] + id]:
                    JP.append(id)
                    ctheta = min(ctheta,rhoval[strmap["rho"] + id])
                if rval["r" + id] >= rhoval[strmap["rho"] + id]:
                    JR.append(id)
                    ct = min(ct, rval["r" + id])
    print("JP")
    print(JP)
    print("JR")
    print(JR)
    print("ctheta:" + str(ctheta))
    print("ct:" + str(ct))
