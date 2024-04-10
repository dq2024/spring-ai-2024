import numpy as np
import random

'''
Task: Given a probability distribution p over the values from 1 to p.length, choose a
random value. Use the algorithm in the assignment. If you want to test this, pick some test value of p;
and write a driver that runs it 1000 times, and keep a tally of how many times each value was reached.
The frequencies of the different values should more or less correspond to the original distribution p. If
you are doing the assignment in Python, you can just use the library function random.choices().
'''
def chooseFromDist(p):
    return random.choices(list(range(len(p))), weights = p, k = 1)[0]

'''
Task: Simulate the rolling of NDice dice with NSides sides.
'''
def rollDice(NDice, NSides):
    return [random.randint(1, NSides) for i in range(NDice)]    

'''
Task: Pick the number of dice to roll, given the parameters, following the formulas in the assignment. 
You should work out what the numbers fk and pk are for some particular value of the above parameters, 
and then make sure that you are calculating them correctly.
'''
def chooseDice(score, oppScore, LoseCount, WinCount, NDice, M):
    K = NDice 
    fk = np.zeros(K)
    pk = np.zeros(K)

    for k in range(0, K):
        wins = WinCount[score, oppScore, k + 1]
        losses = LoseCount[score, oppScore, k + 1]
        total = wins + losses
        if total > 0:
            fk[k - 1] = (wins / total)
        else:
            fk[k - 1] = 0.5
    
    k_best = np.argmax(fk)  
    sum = np.sum(fk) - fk[k_best]
    wins = WinCount[score, oppScore, :]
    losses = LoseCount[oppScore, oppScore, :]
    totalGames = np.sum(wins + losses)
    
    for k in range(0, K):
        if k == k_best:            
            pk[k] = (totalGames * fk[k] + M) / (totalGames * fk[k] + K * M)
        else:
            pk[k] = (1 - pk[k_best]) * (totalGames * fk[k] + M) / (sum * totalGames + (K - 1) * M)

    return chooseFromDist(pk) + 1

'''
Task: Play 1 game with the above parameters. The output is new values of LoseCount and WinCount. 
You should keep track of the trace of the game as it proceeds (the sequence of score, number of 
dice rolled, and outcome of the roll), and then make sure that the changes to LoseCount and 
WinCount correspond to the trace.
'''
def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    trace = []  
    playerScores = [0, 0]
    p = 0   
    victory = False

    while True:
        numDice = chooseDice(playerScores[p], playerScores[1 - p], LoseCount, WinCount, NDice, M)
        rolls = rollDice(numDice, NSides)
        rollsSum = sum(rolls)
        playerScores[p] += rollsSum
        trace.append((playerScores[p] - rollsSum, playerScores[1 - p], numDice))
        
        if playerScores[p] >= LTarget and playerScores[p] <= UTarget:
            victory = True
            break
        elif playerScores[p] > UTarget:
            break

        p = 1 - p

    for score, oppScore, numDice in trace:
        triple = (score, oppScore, numDice)
        if victory:
            WinCount[triple] = WinCount[triple] + 1
        else:
            LoseCount[triple] = LoseCount[triple] + 1

    return trace, WinCount, LoseCount

'''
Task: Given the final state of the arrays, extract the best move in
each state and the probability of winning if you make that move
'''
def extractAnswer(WinCount, LoseCount, LTarget):
    play = np.zeros((LTarget, LTarget))
    prob = np.zeros((LTarget, LTarget))

    for score in range(0, LTarget):
        for oppScore in range(LTarget):
            wins = WinCount[score, oppScore, 1:]
            losses = LoseCount[score, oppScore, 1:]
            counts = wins + losses

            probs = [0] * (len(WinCount[score, oppScore]) - 1)

            for i in range(1, len(WinCount[score, oppScore])):
                if counts[i - 1] == 0:  
                    probs[i - 1] = 0
                else:
                    probs[i - 1] = WinCount[score, oppScore, i] / counts[i - 1]
            
            updatedProbs = []
            for x in probs:
                if x != x: 
                    updatedProbs.append(0)  
                else:
                    updatedProbs.append(x)  

            k_best = np.argmax(updatedProbs) + 1

            play[score, oppScore] = k_best
            prob[score, oppScore] = updatedProbs[k_best - 1]

            if updatedProbs[k_best - 1] > 0:
                play[score, oppScore] = k_best
            else:
                play[score, oppScore] = 0

    return play, prob

'''
Task: Top-level function. Once all the other pieces are working, this is four or five lines of code. 
Initialize LoseCount and WinCount to arrays of 0, play the game NGames times, and then extract the 
answer from the final state of WinCount and LoseCount.
'''
def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    WinCount = np.zeros((LTarget, LTarget, NDice + 1))
    LoseCount = np.zeros((LTarget, LTarget, NDice + 1)) 

    for i in range(NGames):
        trace, WinCount, LoseCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
    
    return extractAnswer(WinCount, LoseCount, LTarget)

def main():
    NDice = 2
    NSides = 2
    LTarget = 4
    UTarget = 4
    NGames = 100000
    M = 100

    play, prob = prog3(NDice, NSides, LTarget, UTarget, NGames, M)
    print("\nRun 1: \nPlay")
    for x in play:
        print(x)
    print("\nProb")
    print(prob)

    play, prob = prog3(NDice, NSides, LTarget, UTarget, NGames, M)
    print("\nRun 2: \nPlay")
    for x in play:
        print(x)
    print("\nProb")
    print(prob)

    play, prob = prog3(NDice, NSides, LTarget, UTarget, NGames, M)
    print("\nRun 3: \nPlay")
    for x in play:
        print(x)
    print("\nProb")
    print(prob)
        
main()
