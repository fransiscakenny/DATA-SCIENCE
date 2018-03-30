import os
import csv
import json
import sys
from math import*
from scipy.stats.stats import pearsonr
import numpy as np
import heapq, random

userID = 'null'
movieID = 'null'
sums = 0
total = 0
rows = [] #MAKE DATA ACCESS EASIER & FASTER
rowss = {}
userMovies = [] #movies rated by user other than we predict
userMovDict = []
Edistance = {} #pair of userID compared with and the Euclid distance

sums = 0
total = 0
ave = 0
EU = []
PER = []
COS = []
EUDIF = []
NE = 0
PERDIF = []
NP = 0
COSDIF = []
NC = []

def average():
    print("AVERAGE!")
def euclid(X, Y):
    print("EUCLID!")
    return sqrt(sum(pow(a-b,2) for a, b in zip(X, Y)))
def pearson():
    print("PEARSON!")
def cosine():
    print("COSINE!")
def distance():
    print("distance!")

####################################################################################################
def cosine1(UID, MID, kk, trainf, actual):
    COSrow = {}
    userID = str(UID)
    movieID = str(MID)
    f = open(trainf, 'r')
    content = f.read()
    f.close()

    for cos in content.split("\n"):
        if(len(cos) > 0):
            if(COSrow.get(cos.split()[0], "no") == "no"): #first one:
                moviedict = {}
                COSrow[cos.split()[0]] = moviedict
                moviedict[cos.split()[1]] = cos.split()
            else:
                COSrow[cos.split()[0]][cos.split()[1]] = cos.split()


    userMoves = [COSrow[userID]]

    collectSim = []
    collectSimRate = []

    for us in COSrow:
        if(us != userID):
            otherMoves = [COSrow[us]]
            A1 = []
            B1 = []
            for moves in COSrow[userID]:
                if(COSrow[us].get(moves, "no") != "no"):
                    A1.append(float(COSrow[userID][moves][2]))
                    B1.append(float(COSrow[us].get(moves)[2]))
            if(len(A1) > 0 or len(B1) > 0):
                ABOVE1 = 0;
                indB = 0
                for ii in A1:
                    ABOVE1 = ABOVE1 + (ii*B1[indB])
                    indB += 1
                SQRa = 0
                SQRb = 0
                for iii in A1:
                    SQRa = SQRa + (iii**2)
                for bbb in A1:
                    SQRb = SQRb + (bbb**2)
                ACTSQA = sqrt(SQRa)
                ACTSQB = sqrt(SQRb)
                MULT = ACTSQA*ACTSQB

                if(MULT != 0):
                    COSINESIM = float(ABOVE1/MULT)
                    if(COSrow[us].get(movieID, "no") != "no"):
                        simrate = float(COSINESIM * float(COSrow[us][movieID][2]))
                        collectSim.append(COSINESIM)
                        collectSimRate.append(simrate)

    sumcsim = 0
    sumcsimrate = 0

    for csim in collectSim:
        sumcsim = float(sumcsim + csim)
    for csimr in collectSimRate:
        sumcsimrate = float(sumcsimrate + csimr)

    COSpredict = float(sumcsimrate / sumcsim)
    COS.append(COSpredict)
    if(actual == -1):
        print("pittrecsys.prediction =",COSpredict)
    if(actual != -1):
        COSDIF.append((float(actual)-COSpredict)**2)


####################################################################################################
def euclid1(UID, MID, kk, trainf, actual):
    userID = str(UID)
    movieID = str(MID)
    K = kk
    f = open(trainf, 'r')
    content = f.read()
    f.close()
    EUrow = {}
    for cos in content.split("\n"):
        if(len(cos) > 0):
            if(EUrow.get(cos.split()[0], "no") == "no"): #first one:
                moviedict = {}
                EUrow[cos.split()[0]] = moviedict
                moviedict[cos.split()[1]] = cos.split()
            else:
                EUrow[cos.split()[0]][cos.split()[1]] = cos.split()

    EUSERMOV = EUrow[UID]
    SIMIS = {}
    for euser in EUrow:
        rateDif = []
        if(euser != userID):
            difsq = []
            for mov in EUSERMOV:
                if(EUrow[euser].get(mov,"no") != "no"):
                    temp = (float(EUrow[euser][mov][2]) - float(EUrow[userID][mov][2]))**2
                    difsq.append(temp)
            sumdf = 0
            for ds in difsq:
                sumdf = sumdf + ds
            eudis = sqrt(sumdf)
            simi = 1/(1+eudis)
            if(EUrow[euser].get(movieID,"no") != "no"):
                SIMIS[simi] = euser
    CLOSESTSIM = heapq.nlargest(K, SIMIS.keys())

    sumweighted = 0
    sumweight = 0
    for cp in CLOSESTSIM:
        if(EUrow[str(SIMIS[cp])].get(movieID,"no") != "no"):
            rateus = EUrow[str(SIMIS[cp])][movieID][2]
            mull = float(rateus)*cp
            sumweighted = sumweighted + mull
            sumweight = sumweight + cp
    EUPREDICT = sumweighted/sumweight
    if(actual == -1):
        print("pittrecsys.prediction =",EUPREDICT)
    if(actual != -1):
        EUDIF.append((float(actual)-EUPREDICT)**2)
###########################################################################################
#PEARSON ALGORITHM
def pearson1(UID, MID, kk, trainf, actual):
        userID = str(UID)
        movieID = str(MID)
        K = kk
        i = 0
        pearson();
        X = [2, 2, 3, 3, 4]
        Y = [2, 3, 2, 3, 4]
        PE1 = pearsonr(X, Y)
        print("PE1")
        print(PE1)
        Z = [2, 3, 3, 4, 4]
        T = [1, 1, 3, 2, 3]
        PE2 = pearsonr(Z, T)
        print("PE2")
        print(PE2)
        i = 0
        DIFFS = []
        f = open(trainf, 'r')
        content = f.read()
        f.close()

        sums = 0;
        total = 0;
        ave = 0;

        for row in content.split("\n"):
            rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        if(len(row) > 0 and row.split()[1] == movieID):
            if(row.split()[0] != userID):
                print(sums)
                sums = sums + int(row.split()[2])
                total = total + 1
                ave = sums / total

        rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        if(len(row) > 0 and row.split()[1] == movieID):
            if(row.split()[0] != userID):
                sums = sums + int(row.split()[2])
                total = total + 1
                ave = sums / total
        othermovies = {}
        done = {}
        PEARSONdiff = []
        peard = {}
        pearsondict = {}
        specialmovies = {}

        for other in rows:
            if(len(other) > 0 and other[0] != userID and done.get(other[0],"NOPE") != "DONE"):
                othermovies[other[0]] = {}
                for o in rows:
                    if(len(o) > 0):
                        if(o[0] == other[0]):
                            othermovies[other[0]][o[1]] = o[2]
                done[other[0]] = "DONE"
                A = []
                B = []
                for u in userMovies:
                    if(othermovies[other[0]].get(u[1],"NOPE") != "NOPE"):
                        A.append(int(u[2]))
                        B.append(int(othermovies[other[0]][u[1]]))
                for x in A:
                    print("A:")
                    print(A)
                for y in B:
                    print("B:")
                    print(B)
                if(len(A) > 0 and len(B) > 0):
                    peardif = pearsonr(A,B)
                    dif, pval = peardif
                    if(np.ptp(dif) == 0):
                        PEARSONdiff.append(dif)
                        peard[other[0]]=dif
        contMID = {}
        for ii in peard:
            if(othermovies[ii].get(movieID, "none") != "none"):
                contMID[peard[ii]]= ii

        closestp = heapq.nlargest(K, contMID.keys())

        closePRate = []
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                closePRate.append(rowss.get(contMID[ctp])[2])
        above = 0;
        total = 0;
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                multiply = float(ctp) * float(rowss.get(contMID[ctp])[2])
                above = float(above + multiply);
                total = float(total + ctp);
        if(total != 0):
            PERDICT = float(above/total)
            print("pittrecsys.prediction =",PERDICT)
            if(actual != -1):
                PERDIF.append((float(actual)-PERDICT)**2)
###########################################################################################
#MAIN:
if (len(sys.argv) == 7 and sys.argv[1] == 'predict'):
    filename = sys.argv[2]
    K = int(sys.argv[3])
    algo = sys.argv[4]
    userID = sys.argv[5]
    movieID = sys.argv[6]
    print("pittrecsys.command =",sys.argv[1])
    print("pittrecsys.training =",filename)
    print("pittrecsys.algorithm =",algo)
    print("pittrecsys.k =",K)
    print("pittrecsys.userID =",userID)
    print("pittrecsys.movieID =",movieID)

    f = open(filename, 'r')
    content = f.read()
    f.close()

    for row in content.split("\n"):
        rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        if(len(row) > 0 and row.split()[1] == movieID):
            if(row.split()[0] != userID):
                sums = sums + int(row.split()[2])
                total = total + 1
                ave = sums / total

    #print("PRINT ROWS")
    foundhere = 0
    f = 0
    #print("CHECK USERID")
    while(len(rows[f]) > 0 and f < len(rows) and foundhere != 1):
        temp = rows[f][0].replace("'", "")
        #print(userID+"and"+ rows[f][0])
        if(userID == rows[f][0]):
            foundhere = 1
        f+=1
    #print("found here: ", foundhere)

    foundhere1 = 0
    f1 = 0
    #print("CHECK MOVIEID")
    while(len(rows[f1]) > 0 and f1 < len(rows) and foundhere1 != 1):
        temp = rows[f1][1].replace("'", "")
        #print(movieID+"and"+ rows[f1][1])
        if(movieID == rows[f1][1]):
            foundhere1 = 1
        f1+=1
    #print("found1 here: ", foundhere1)
    if(foundhere == 0):
        print("INVALID USER ID")
    else:
        print("VALID USER ID")
    if(foundhere1 == 0):
        print("INVALID MOVIE ID")
    else:
        print("VALID MOVIE ID")
    if(foundhere == 0 or foundhere1 == 0):
        print("DISCONTINUING")

    if (sys.argv[4] == 'average' and (foundhere != 0 and foundhere1 != 0)):
        print("pittrecsys.prediction =",ave)
#######################################################################
    elif (sys.argv[4] == 'euclid' and (foundhere != 0 and foundhere1 != 0)):
        euclid1(userID, movieID, K, filename, -1)
#######################################################################
    elif (sys.argv[4] == 'pearson' and (foundhere != 0 and foundhere1 != 0)):
        pearson();
        X = [2, 2, 3, 3, 4]
        Y = [2, 3, 2, 3, 4]
        PE1 = pearsonr(X, Y)
        Z = [2, 3, 3, 4, 4]
        T = [1, 1, 3, 2, 3]
        PE2 = pearsonr(Z, T)
        i = 0
        DIFFS = []

        othermovies = {}
        done = {}
        PEARSONdiff = []
        peard = {}
        pearsondict = {}
        specialmovies = {}
        for other in rows:
            if(len(other) > 0 and other[0] != userID and done.get(other[0],"NOPE") != "DONE"):
                othermovies[other[0]] = {}
                for o in rows:
                    if(len(o) > 0):
                        if(o[0] == other[0]):
                            othermovies[other[0]][o[1]] = o[2]
                done[other[0]] = "DONE"
                A = []
                B = []
                for u in userMovies:
                    if(othermovies[other[0]].get(u[1],"NOPE") != "NOPE"):
                        A.append(int(u[2]))
                        B.append(int(othermovies[other[0]][u[1]]))
                if(len(A) > 0 and len(B) > 0):
                    peardif = pearsonr(A,B)
                    dif, pval = peardif
                    if(np.ptp(dif) == 0):
                        PEARSONdiff.append(dif)
                        peard[other[0]]=dif
        contMID = {}
        for ii in peard:
            if(othermovies[ii].get(movieID, "none") != "none"):
                contMID[peard[ii]]= ii

        closestp = heapq.nlargest(K, contMID.keys())

        closePRate = []
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                closePRate.append(rowss.get(contMID[ctp])[2])
        above = 0;
        total = 0;
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                multiply = float(ctp) * float(rowss.get(contMID[ctp])[2])
                above = float(above + multiply);
                total = float(total + ctp);
        print("pittrecsys.prediction =",above/total)


    elif (sys.argv[4] == 'cosine' and (foundhere != 0 and foundhere1 != 0)):
        cosine1(userID, movieID, K, filename, -1);
elif (len(sys.argv) == 6 and sys.argv[1] == 'evaluate'):
    trainfile = sys.argv[2]
    K1 = int(sys.argv[3])
    algo = sys.argv[4]
    testfile = sys.argv[5]

    print("pittrecsys.command =",sys.argv[1])
    print("pittrecsys.training =",sys.argv[2])
    print("pittrecsys.testing =",sys.argv[5])
    print("pittrecsys.algorithm =",sys.argv[4])
    print("pittrecsys.k =",sys.argv[3])

    f = open(trainfile, 'r')
    traincont = f.read()
    f.close()
    TRAINING = {}
    TESTING = {}
    for tc in traincont.split("\n"):
        if(len(tc) > 0):
            if(TRAINING.get(tc.split()[0], "no") == "no"): #first one:
                moviedict = {}
                TRAINING[tc.split()[0]] = moviedict
                moviedict[tc.split()[1]] = tc.split()
            else:
                TRAINING[tc.split()[0]][tc.split()[1]] = tc.split()
    f = open(trainfile, 'r')
    testcont = f.read()
    f.close()
    for sc in testcont.split("\n"):
        if(len(sc) > 0):
            if(TESTING.get(sc.split()[0], "no") == "no"): #first one:
                moviedict1 = {}
                TESTING[sc.split()[0]] = moviedict1
                moviedict1[sc.split()[1]] = sc.split()
            else:
                TESTING[sc.split()[0]][sc.split()[1]] = sc.split()
    u = 101
    m = 24
    if(algo == 'average'):
        AVEDIFSQ = []
        rates = []
        N = 0
        for users in TESTING:
            for movies in TESTING[users]:
                for uss in TRAINING:
                    if(uss != users and TRAINING[uss].get(movies, "no") != "no"):
                        rates.append(int(TRAINING[uss].get(movies)[2]))
                sumrates = 0
                total = 0
                for rt in rates:
                    sumrates = sumrates + rt
                    total += 1
                    AVES = sumrates/total
                sqrtdif = (float(float(TESTING[users][movies][2]) - AVES))**2
                AVEDIFSQ.append(sqrtdif)
                N += 1
        SUMADSQ = 0
        for adq in AVEDIFSQ:
            SUMADSQ = SUMADSQ + AVEDIFSQ
        RMSEAVE = sqrt(SUMADSQ/N)
        print("pittrecsys.RMSE =",RMSAVE)
    if(algo == "euclid"):
        for users in TESTING:
            for movies in TESTING[users]:
                euclid1(users, movies, 20, trainfile, TESTING[users][movies][2])
        sumuu = 0
        for uu in EUDIF:
            sumuu = sumuu + uu
        RMSEU = sqrt(sumuu/len(EUDIF))
        print("pittrecsys.RMSE =",RMSEU)
    if(algo == "pearson"):
        for users in TESTING:
            for movies in TESTING[users]:
                pearson1(users, movies, 20, trainfile, TESTING[users][movies][2])
        sumr = 0
        for rr in PERDIF:
            sumr = sumr + rr
        RMSP = sqrt(sumr/len(PERDIF))
        print("pittrecsys.RMSE =",RMSP)
    if(algo == "cosine"):
        for users in TESTING:
            for movies in TESTING[users]:
                cosine1(users, movies, 20, trainfile, TESTING[users][movies][2])
        sume = 0
        for ee in COSDIF:
            sume = sume + ee
        RMSCOS = sqrt(sume/len(COSDIF))
        print("pittrecsys.RMSE =",RMSCOS)
else:
    print("Argument Invalid / Incomplete")
