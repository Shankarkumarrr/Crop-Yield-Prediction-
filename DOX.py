import numpy as np
import random as rn
import time


def vectorAttack(SearchAgents_no, na):
    c = 1
    vAttack = []
    while (c <= na):
        idx = round(1 + (SearchAgents_no - 1) * np.rand())
        if ~findrep(idx, vAttack):
            vAttack[c] = idx
            c = c + 1
    return vAttack


def survival_rate(fit, min, max):
    o = np.zeros((fit.shape[1]))
    for i in range(fit.shape[1]):
        o[i] = (max - fit[i]) / (max - min)
    return o


def getBinary():
    if np.rand() < 0.5:
        val = 0
    else:
        val = 1
    return val


def findrep(val, vector):  # return 1= repeated  0= not repeated
    band = 0
    for i in range(vector.shape[1]):
        if val == vector[i]:
            band = 1
            break
    return band


def Attack(SearchAgents_no, na, Positions, r):
    sumatory = 0
    vAttack = vectorAttack(SearchAgents_no, na)
    for j in range(vAttack.shape[1]):
        sumatory = sumatory + Positions[vAttack(j), :] - Positions[r, :]
    sumatory = sumatory / na


def DOX(Positions, objfun, LB, UB, Max_iter):
    SearchAgents_no, dim = Positions.shape[0], Positions.shape[1]
    lb = LB[0, :]
    ub = UB[1, :]
    P = 0.5  # Hunting or Scavenger?  rate.Seesection3.0.4, P and Qparametersanalysis
    Q = 0.7  # Group attack or persecution?
    beta1 = -2 + 4 * np.rand()  # -2 < beta < 2 Used in Eq. 2,
    beta2 = -1 + 2 * np.rand()  # -1 < beta2 < 1  Used in Eq. 2, 3, and 4
    naIni = 2  # minimum number  of dingoes  that  will  attack

    naEnd = SearchAgents_no / naIni  # maximum number of  dingoes  that  will  attack
    na = round(naIni + (
                naEnd - naIni) * np.rand())  # number  of dingoes that will attack, used in Attack.m Section  2.2 .1: Group attack
    # Positions = initialization(SearchAgents_no, dim, ub, lb)
    Fitness = np.zeros((SearchAgents_no))
    for i in range(SearchAgents_no):
        Fitness[i] = objfun(Positions[i, :])  # get fitness

    vMin, minIdx = min(Fitness)  # the  min fitness value vMin and the  position minIdx
    theBestVct = Positions[minIdx, :]  # the best vector
    vMax, maxIdx = max(Fitness)  # the max fitness value vMax and the position maxIdx
    Convergence_curve = np.zeros((Max_iter))
    Convergence_curve[0] = vMin
    survival = survival_rate(Fitness, vMin, vMax)  # Section  2.2 .4 Dingoes'survival rates
    v = - np.zeros((SearchAgents_no))

    ct = time.time()
    # Main loop
    for t in range(Max_iter):
        for r in range(SearchAgents_no):
            sumatory = 0
            if np.rand() < P:  # If Hunting?
                sumatory = Attack(SearchAgents_no, na, Positions, r)  # Section 2.2.1, Strategy1: Part of  Eq .2
                if np.rand() < Q:  # If group attack?
                    v[r, :] = beta1 * sumatory - theBestVct;  # Strategy 1: Eq .2
                else:  # Persecution
                    r1 = round(1 + (SearchAgents_no - 1) * np.rand())  #
                    v[r, :] = theBestVct + beta1 * (np.exp(beta2)) * (
                    (Positions[r1, :] - Positions[r, :]))  # Section  2.2 .2, Strategy 2: Eq .3
            else:  # Scavenger
                r1 = np.round(1 + (SearchAgents_no - 1) * np.rand())
                v[r, :] = (np.exp(beta2) * Positions[r1, :] - ((-1) ^ getBinary()) * Positions[r,
                                                                                     :]) / 2  # Section2.2.3, Strategy3: Eq.4

            if survival[r] <= 0.3:  # Section 2.2.4, Algorithm 3 - Survival procedure
                band = 1
                while band:
                    r1 = round(1 + (SearchAgents_no - 1) * np.rand())
                    r2 = round(1 + (SearchAgents_no - 1) * np.rand())
                    if r1 != r2:
                        band = 0

                v[r, :] = theBestVct + (Positions[r1, :] - ((-1) ^ getBinary()) * Positions[r2, :]) / 2  # Section 2.2 .4, Strategy 4: Eq .6

            # Return  back  the search  agents  that    go  beyond   the  boundaries  of the  search  space.
            Flag4ub = v[r, :] > ub
            Flag4lb = v[r, :] < lb
            v[r, :] = (v[r, :] * (~(Flag4ub + Flag4lb))) + ub * Flag4ub + lb * Flag4lb  # Evaluate new solutions
            Fnew = objfun(v[r, :])  # get fitness
            # Update if the  solution improves
            if Fnew <= Fitness[r]:
                Positions[r, :] = v[r, :]
                Fitness[r] = Fnew
            if Fnew <= vMin:
                theBestVct = v[r, :]
                vMin = Fnew

        Convergence_curve[t] = vMin
        vMax, maxIdx = max(Fitness)
        survival = survival_rate(Fitness, vMin, vMax)  # Section  2.2 .4 Dingoes 'survival rates
    ct = time.time() - ct

    return vMin, theBestVct, Convergence_curve, time

