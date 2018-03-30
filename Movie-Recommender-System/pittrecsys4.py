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
#possible = [1.0, 0.5, 0.333, 0.25, 0.2, 0.167]
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
    print("TESTING COSINE")
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
    print("COSrow DONE")

    userMoves = [COSrow[userID]]
    print("userM")
    print(userMoves)

    collectSim = []
    collectSimRate = []

    for us in COSrow:
        if(us != userID):
            otherMoves = [COSrow[us]]
            A1 = []
            B1 = []
            for moves in COSrow[userID]:
                #print(moves)
                if(COSrow[us].get(moves, "no") != "no"):
                    print("MoveID:", COSrow[us].get(moves))
                    A1.append(float(COSrow[userID][moves][2]))
                    print("Appending A:",COSrow[userID][moves][2])
                    B1.append(float(COSrow[us].get(moves)[2]))
                    print("Appending B:",COSrow[us].get(moves)[2])
            if(len(A1) > 0 or len(B1) > 0):
                print("A1:")
                print(A1)
                print("B1:")
                print(B1)
                ABOVE1 = 0;
                indB = 0
                for ii in A1:
                    ABOVE1 = ABOVE1 + (ii*B1[indB])
                    #print("Cur Above1:",ABOVE1)
                    indB += 1
                SQRa = 0
                SQRb = 0
                for iii in A1:
                    SQRa = SQRa + (iii**2)
                    #print("Cur SQRa:",SQRa)
                for bbb in A1:
                    SQRb = SQRb + (bbb**2)
                ACTSQA = sqrt(SQRa)
                ACTSQB = sqrt(SQRb)
                MULT = ACTSQA*ACTSQB

                if(MULT != 0):
                    COSINESIM = float(ABOVE1/MULT)
                    print("COSINE SIM:",COSINESIM)
                    if(COSrow[us].get(movieID, "no") != "no"):
                        print("MOVIEID:",movieID)
                        print(COSrow[us].get(movieID))
                        simrate = float(COSINESIM * float(COSrow[us][movieID][2]))
                        print("SIMRATE:",simrate)
                        collectSim.append(COSINESIM)
                        collectSimRate.append(simrate)
                else:
                    print("DIVISION BY 0")

    sumcsim = 0
    sumcsimrate = 0

    for csim in collectSim:
        sumcsim = float(sumcsim + csim)
    print("csim:",csim)
    for csimr in collectSimRate:
        sumcsimrate = float(sumcsimrate + csimr)
    print("csimrate:",sumcsimrate)

    COSpredict = float(sumcsimrate / sumcsim)
    #print("CosPredict:",COSpredict)
    print("pittrecsys.prediction =",COSpredict)
    COS.append(COSpredict)
    if(actual != -1):
        COSDIF.append((float(actual)-COSpredict)**2)
        print("COSDIF:",(float(actual)-COSpredict)**2)


####################################################################################################
def euclid1(UID, MID, kk, trainf, actual):
    userID = str(UID)
    movieID = str(MID)
    K = kk
    print(userID, movieID, K)
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
    print("EUrow DONE")
    #print(EUrow)
    EUSERMOV = EUrow[UID]
    SIMIS = {}
    for euser in EUrow:
        rateDif = []
        if(euser != userID):
            difsq = []
            for mov in EUSERMOV:
                if(EUrow[euser].get(mov,"no") != "no"):
                    print("mov",mov)
                    temp = (float(EUrow[euser][mov][2]) - float(EUrow[userID][mov][2]))**2
                    print("temp",temp)
                    difsq.append(temp)
            sumdf = 0
            for ds in difsq:
                sumdf = sumdf + ds
            eudis = sqrt(sumdf)
            print("EU DIST for",userID, euser, "is",eudis)
            simi = 1/(1+eudis)
            print("simim",simi)
            if(EUrow[euser].get(movieID,"no") != "no"):
                SIMIS[simi] = euser
            #closestp = heapq.nlargest(K, contMID.keys())
    CLOSESTSIM = heapq.nlargest(K, SIMIS.keys())
    print("CLOSE SIM")
    print(CLOSESTSIM)

    sumweighted = 0
    sumweight = 0
    for cp in CLOSESTSIM:
        if(EUrow[str(SIMIS[cp])].get(movieID,"no") != "no"):
            print(cp)
            rateus = EUrow[str(SIMIS[cp])][movieID][2]
            print("rating by euser:",rateus)
            mull = float(rateus)*cp
            print("weighted:",mull)
            sumweighted = sumweighted + mull
            sumweight = sumweight + cp
        else:
            print(cp, SIMIS[cp], )
            print("nooo")
    print(sumweighted, sumweight)
    EUPREDICT = sumweighted/sumweight
    #print("EUCLIDIAN PREDICTION:", EUPREDICT)
    print("pittrecsys.prediction =",EUPREDICT)
    if(actual != -1):
    #print(COSrow[userID][movieID])
        EUDIF.append((float(actual)-EUPREDICT)**2)
        print("EUDIF:",(float(actual)-EUPREDICT)**2)
###########################################################################################
#PEARSON ALGORITHM
def pearson1(UID, MID, kk, trainf, testf):
        userID = str(UID)
        movieID = str(MID)
        K = kk
        print(userID, movieID, K)
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
        for some in userMovies:
            print(some)
            print("hehe")
        print("Movies rated by userID")
        f = open(trainf, 'r')
        content = f.read()
        f.close()
        print("trainfs opened", trainf)
        print(content)
        print(userID, movieID)

        sums = 0;
        total = 0;
        ave = 0;
        print("Ratings for MovieID =",movieID)

        print("nih")
        for row in content.split("\n"):
            rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        #FILLING userMovies
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        #GETTING AVERAGE
        if(len(row) > 0 and row.split()[1] == movieID):
            print(row)
            if(row.split()[0] != userID):
                print(sums)
                sums = sums + int(row.split()[2])
                total = total + 1
                ave = sums / total

        rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        #FILLING userMovies
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        #GETTING AVERAGE
        if(len(row) > 0 and row.split()[1] == movieID):
            print(row)
            if(row.split()[0] != userID):
                print(sums)
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
                print("rowsss")
                print(other)
                #othermovies[other[0]] = []
                othermovies[other[0]] = {}
                for o in rows:
                    if(len(o) > 0):
                        if(o[0] == other[0]):
                            othermovies[other[0]][o[1]] = o[2]
                print("OTHERMOVIES for",other[0])
                print("WORKS!")
                for om in othermovies[other[0]]:
                    print(om)
                done[other[0]] = "DONE"
                A = []
                B = []
                for u in userMovies:
                    #print("lookkk",u[1])
                    #if(othermovies.get(u[1], "NOPE") != "NOPE"):
                    if(othermovies[other[0]].get(u[1],"NOPE") != "NOPE"):
                        print("The movie",u[1],"exists")
                        A.append(int(u[2]))
                        B.append(int(othermovies[other[0]][u[1]]))
                        print("Appended A:",u[2],"B:",othermovies[other[0]][u[1]])
                        #if(u[1] == MovieID):
                        #    specialmovies[]
                #for x in A:
                print("A:")
                print(A)
                #for y in B:
                print("B:")
                print(B)
                peardif = pearsonr(A,B)
                dif, pval = peardif
                if(np.ptp(dif) == 0):
                    PEARSONdiff.append(dif)
                    peard[other[0]]=dif
                    #pearsondict[str(dif)]:
                print("PEARSONR DIFF:",peardif)
        #for pdif in PEARSONdiff:
        #print(pdif)
        print(PEARSONdiff)
        #THE ONE THAT HAS MOVIE ID
        print("peard is")
        print(peard)
        contMID = {}
        print("inputting")
        for ii in peard:
            if(othermovies[ii].get(movieID, "none") != "none"):
                print(peard[ii], ii)
                contMID[peard[ii]]= ii
        print("conttt1")
        print(contMID)

        closestp = heapq.nlargest(K, contMID.keys())
        print("CLOSEST PEARSON")
        print(closestp)

        closePRate = []
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                print(ctp, contMID[ctp])
                print(rowss.get(contMID[ctp]))
                closePRate.append(rowss.get(contMID[ctp])[2])
        print("FINAL")
        print(closePRate)
        above = 0;
        total = 0;
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                multiply = float(ctp) * float(rowss.get(contMID[ctp])[2])
                print(multiply)
                above = float(above + multiply);
                total = float(total + ctp);
        print("PEARSON RESULT:")
        if(total != 0):
            PERDICT = float(above/total)
            print(PERDICT)
    if(actual != -1):
        PERDIF.append((float(actual)-PERDICT)**2)
        print("PERDIF:",(float(actual)-PERDICT)**2)
###########################################################################################
#MAIN:
if (len(sys.argv) == 7 and sys.argv[1] == 'predict'):
    print("Predicting..")
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
    #print("pittrecsys.prediction =",sys.argv[1])

    f = open(filename, 'r')
    content = f.read()
    f.close()
    #ADDITIONAL VARIABLES:
    """
    sums = 0
    total = 0
    rows = [] #MAKE DATA ACCESS EASIER & FASTER
    rowss = {}
    userMovies = [] #movies rated by user other than we predict
    userMovDict = []
    Edistance = {} #pair of userID compared with and the Euclid distance
    """
    ###
    print("Ratings for MovieID =",movieID)
    for row in content.split("\n"):
        #print("all")
        if(len(row) > 0):
            if(row.split()[0] == userID and row.split()[1] == movieID):
                print(row)
                #print("here!")
        #print(row)
        rows.append(row.split())
        if(len(row) > 0):
            rowss[row.split()[1]] = row.split()
        #FILLING userMovies
        if(len(row) > 0 and row.split()[0] == userID):
            userMovies.append(row.split())
            tempD = {row.split()[1]:row.split()}
            userMovDict.append(tempD)
        #GETTING AVERAGE
        if(len(row) > 0 and row.split()[1] == movieID):
            print(row)
            if(row.split()[0] != userID):
                sums = sums + int(row.split()[2])
                total = total + 1
                ave = sums / total
    #print("Sum:",sums)
    #print("Total:",total)
    #print("Average:",ave)
    for things in rows:
        print(things)
    ###
    if (sys.argv[4] == 'average'):
        print("pittrecsys.prediction =",ave)
    #######################################################################
    elif (sys.argv[4] == 'euclid'):
        euclid1(userID, movieID, K, filename, -1)
#######################################################################
    elif (sys.argv[4] == 'pearson'):
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
        for some in userMovies:
            print(some)
            print("hehe")
        print("Movies rated by userID")

        othermovies = {}
        done = {}
        PEARSONdiff = []
        peard = {}
        pearsondict = {}
        specialmovies = {}
        for other in rows:
            if(len(other) > 0 and other[0] != userID and done.get(other[0],"NOPE") != "DONE"):
                print("rowsss")
                print(other)
                #othermovies[other[0]] = []
                othermovies[other[0]] = {}
                for o in rows:
                    if(len(o) > 0):
                        if(o[0] == other[0]):
                            othermovies[other[0]][o[1]] = o[2]
                print("OTHERMOVIES for",other[0])
                print("WORKS!")
                for om in othermovies[other[0]]:
                    print(om)
                done[other[0]] = "DONE"
                A = []
                B = []
                for u in userMovies:
                    #print("lookkk",u[1])
                    #if(othermovies.get(u[1], "NOPE") != "NOPE"):
                    if(othermovies[other[0]].get(u[1],"NOPE") != "NOPE"):
                        print("The movie",u[1],"exists")
                        A.append(int(u[2]))
                        B.append(int(othermovies[other[0]][u[1]]))
                        print("Appended A:",u[2],"B:",othermovies[other[0]][u[1]])
                        #if(u[1] == MovieID):
                        #    specialmovies[]
                #for x in A:
                print("A:")
                print(A)
                #for y in B:
                print("B:")
                print(B)
                peardif = pearsonr(A,B)
                dif, pval = peardif
                if(np.ptp(dif) == 0):
                    PEARSONdiff.append(dif)
                    peard[other[0]]=dif
                    #pearsondict[str(dif)]:
                print("PEARSONR DIFF:",peardif)
        #for pdif in PEARSONdiff:
        #print(pdif)
        print(PEARSONdiff)
        #THE ONE THAT HAS MOVIE ID
        print("peard is")
        print(peard)
        contMID = {}
        print("inputting")
        for ii in peard:
            if(othermovies[ii].get(movieID, "none") != "none"):
                #contMID[ii] = peard[ii]
                #print(peard[ii])
                #print(peard[0])
                print(peard[ii], ii)
                contMID[peard[ii]]= ii
        print("conttt1")
        print(contMID)

        closestp = heapq.nlargest(K, contMID.keys())
        print("CLOSEST PEARSON")
        print(closestp)

        closePRate = []
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                print(ctp, contMID[ctp])
                print(rowss.get(contMID[ctp]))
                closePRate.append(rowss.get(contMID[ctp])[2])
        print("FINAL")
        print(closePRate)
        above = 0;
        total = 0;
        for ctp in closestp:
            if(contMID.get(ctp, "noo") != "noo"):
                multiply = float(ctp) * float(rowss.get(contMID[ctp])[2])
                print(multiply)
                above = float(above + multiply);
                total = float(total + ctp);
        print("PEARSON RESULT:")
        print(float(above/total))

    elif (sys.argv[4] == 'cosine'):
        cosine1(userID, movieID, K, filename, -1);
elif (len(sys.argv) == 6 and sys.argv[1] == 'evaluate'):
    print("Evaluating...")
    trainfile = sys.argv[2]
    K1 = int(sys.argv[3])
    algo = sys.argv[4]
    testfile = sys.argv[5]

    print("pittrecsys.command =",sys.argv[1])
    print("pittrecsys.training =",sys.argv[2])
    print("pittrecsys.testing =",sys.argv[5])
    print("pittrecsys.algorithm =",sys.argv[4])
    print("pittrecsys.k =",sys.argv[3])
    #print("pittrecsys.RMSE =",0)

    f = open(trainfile, 'r')
    traincont = f.read()
    f.close()
    TRAINING = {}
    TESTING = {}
    print(trainfile, "CONTENT:")
    for tc in traincont.split("\n"):
        #print(tc.split())
        if(len(tc) > 0):
            if(TRAINING.get(tc.split()[0], "no") == "no"): #first one:
                moviedict = {}
                TRAINING[tc.split()[0]] = moviedict
                moviedict[tc.split()[1]] = tc.split()
            else:
                TRAINING[tc.split()[0]][tc.split()[1]] = tc.split()
    print("TRAINING DONE")
    #print(TRAINING)
    f = open(trainfile, 'r')
    testcont = f.read()
    f.close()
    print(testfile, "CONTENT:")
    for sc in testcont.split("\n"):
        #print(sc.split())
        if(len(sc) > 0):
            if(TESTING.get(sc.split()[0], "no") == "no"): #first one:
                moviedict1 = {}
                TESTING[sc.split()[0]] = moviedict1
                moviedict1[sc.split()[1]] = sc.split()
            else:
                TESTING[sc.split()[0]][sc.split()[1]] = sc.split()
    print("TESTING DONE")
    u = 101
    m = 24
    if(algo == 'average'):
        AVEDIFSQ = []
        rates = []
        N = 0
        print("AVE!")
        for users in TESTING:
            for movies in TESTING[users]:
                for uss in TRAINING:
                    if(uss != users and TRAINING[uss].get(movies, "no") != "no"):
                        print("Appending..",uss, int(TRAINING[uss].get(movies)[2]))
                        rates.append(int(TRAINING[uss].get(movies)[2]))
                sumrates = 0
                total = 0
                for rt in rates:
                    sumrates = sumrates + rt
                    total += 1
                    AVES = sumrates/total
                print("AVE for",users,movies,"is",AVES)
                sqrtdif = (float(float(TESTING[users][movies][2]) - AVES))**2
                AVEDIFSQ.append(sqrtdif)
                print("Appended:",sqrtdif)
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
        print("TEST PEARSON1")
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
