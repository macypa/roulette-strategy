import random
import sys


# 
# Fast doubling Fibonacci algorithm (Python)
# 
# Copyright (c) 2015 Project Nayuki
# All rights reserved. Contact Nayuki for licensing.
# https://www.nayuki.io/page/fast-fibonacci-algorithms
# 

total = len(sys.argv)
cmdargs = str(sys.argv)

print "total " + str(total)
print "cmdargs " + str(cmdargs)

if len(sys.argv)>1:
	attempts = int(sys.argv[1])
else:
	attempts = 1

if len(sys.argv)>2:
	draws = int(sys.argv[2])
else:
	draws = 100

if len(sys.argv)>3:
	drawnDiff = int(sys.argv[3])
else:
	drawnDiff = 5



deposit = 1000
maxBet = 10

useBetSteps = False
betSteps = [0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4] # / (3x18, 1x0)
# betSteps = [1.7, 1, 1.5, 2.0, 3.5, 4, 4.5, 7.2, 8.1] # / (9x18, 1x8)
# betSteps = [0.5, 1, 1.5, 2.0, 3.5, 4, 4.5, 7.2, 8.1] # / (3x18, 2x3)
# betSteps = [0.9, 1.8, 2.7, 3.6, 4.5, 5.4, 6.3, 7.2, 8.1] # / (5x12, 4x2)
# betSteps = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0] # / (3x18, 1x4) 
#betSteps = [0.9, 1.4, 2.1, 3.2, 4.8, 7.2] # always work but it's not applicable in our case, not every number is divisible on 3 / (2x18, 1x6)

zero = list([0])
redNumbers = list([1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36])
blackNumbers = list([2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35])

oddNumbers = list([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35])
evenNumbers = list([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36])

# numbers1to18 = list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
# numbers19to36 = list([19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36])
numbers1to18 = list(range(1, 19))
numbers19to36 = list(range(19, 37))

# numbers1st12 = list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
# numbers2nd12 = list([13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
# numbers3rd12 = list([25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36])
numbers1st12 = list(range(1, 13))
numbers2nd12 = list(range(13, 25))
numbers3rd12 = list(range(25, 37))

numbers1stLine = list([3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36])
numbers2ndLine = list([2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35])
numbers3rdLine = list([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34])


winningNumbers = redNumbers
losingNumbers = zero + blackNumbers

numbersDrawn = list([])

redNumbersDrawn = 0
blackNumbersDrawn = 0

initBet = 0.1
stepMultiply = 0
stepAdd = 0

winRatioFromBet = 1
winRatioFroNeutralNumbers = 1
winAddFromBet = 0
winAddFroNeutralNumbers = 0

playMartingale = False
playNotOnLoss = False
playOnWinOnly = False
playNotOnLosingStreak = False

# losingNumbers = list([0]) + list(range(19, 37)) # 1
# losingNumbers = list([0]) + list(range(25, 37)) # 2
# losingNumbers = list([0]) + list(range(31, 37)) # 5
# losingNumbers = list([0]) + list(range(35, 37)) # 17
# winningNumbers = list(range(19, 24)) # 2
# losingNumbers = list([0]) + list(range(25, 37)) # 2


keepmaxBet = False
resetOnmaxBet = True
errorOnmaxBet = False

prevDraw = -1
lastDraw = -1
bet = 0
winsInARoll = 0
goodDraws = 0
badDraws = 0


def main():
	global deposit, lastDraw, bet, maxBet

	wins = 0

	for att in range(1,attempts+1):
		try:
			oneAttempt()
			if deposit > 1000:
				wins += 1

			print "Attempt " + str(att) + "     deposit: " + str(deposit) + "     winrate: " + str((wins*100)/att) + "  ..... redNumbersDrawn: " + str(redNumbersDrawn) + ", blackNumbersDrawn: " + str(blackNumbersDrawn)
			# dumpAttempt()
			# dumpStats()
			init()
			
		except ValueError as err:	
			# dumpStats()
			print "Attempt " + str(att) + "     deposit: " + str(deposit) + "  ..... redNumbersDrawn: " + str(redNumbersDrawn) + ", blackNumbersDrawn: " + str(blackNumbersDrawn)
			print(err)
			init()
			
def init():
	global deposit, prevDraw, lastDraw, bet, winsInARoll, goodDraws, badDraws, redNumbersDrawn, blackNumbersDrawn

	deposit = 1000
	prevDraw = -1
	lastDraw = -1
	bet = 0
	winsInARoll = 0
	goodDraws = 0
	badDraws = 0
	redNumbersDrawn = 0
	blackNumbersDrawn = 0


def oneAttempt():
	global deposit, lastDraw, bet, maxBet, draws

	attemptDraws = draws
	while attemptDraws > 0:
		attemptDraws -= 1
		#print draw
		updateStatistics()
		placeBet()
		# print "placed bet: " + str(bet)
		spinWheel()
		# print "number : " + str(lastDraw) + " win: " + str(isWin())
		cashIn()

		if attempts == 1:
			dump(attemptDraws)



def updateStatistics():
	global redNumbersDrawn, blackNumbersDrawn
	numbersDrawn.append(lastDraw)

	if lastDraw in redNumbers:
		redNumbersDrawn += 1
	elif lastDraw in blackNumbers:
		blackNumbersDrawn += 1


def placeBet():
	global lastDraw, initBet, maxBet, bet, playOnWinOnly, placeNotOnLosingStreak, winningNumbers, losingNumbers

	if redNumbersDrawn > blackNumbersDrawn+drawnDiff:
		winningNumbers = blackNumbers
		losingNumbers = zero + redNumbers
	elif blackNumbersDrawn > redNumbersDrawn+drawnDiff:
		winningNumbers = redNumbers
		losingNumbers = zero + blackNumbers
	else:
		bet = 0
		return
	
	if playMartingale:
		placeMartingale()
	elif playNotOnLoss:
		placeNotOnLoss()
	elif playOnWinOnly:
		placeBetOnWinOnly()
	elif playNotOnLosingStreak:
		placeBetNotOnLosingStreak()
	else:
		placeBetAlways()

	return validateNextbet()


def placeMartingale():
	global lastDraw, initBet, maxBet, bet

	if (isWin() == None):
		bet = initBet
	elif isWin() == False:
		stepUpBet()
	elif (isWin() == True):
		bet = initBet

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => bet: " + str(bet)
	return bet


def placeBetNotOnLosingStreak():
	global lastDraw, initBet, maxBet, bet

	if (isWin() == None):
		stepUpBet()
	elif isWin() == False:
		bet = initBet
		if isPrevWin() == False:
			bet = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => bet: " + str(bet)
	return bet


def placeNotOnLoss():
	global lastDraw, initBet, maxBet, bet

	if (isWin() == None):
		stepUpBet()
	elif isWin() == False:
		bet = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => bet: " + str(bet)
	return bet


def placeBetOnWinOnly():
	global lastDraw, initBet, maxBet, bet

	if (isWin() == None):
		stepUpBet()
	elif isWin() == False:
		bet = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => bet: " + str(bet)
	return bet


def placeBetAlways():
	global lastDraw, initBet, maxBet, bet

	if (isWin() == None):
		stepUpBet()
	elif isWin() == False:
		bet = initBet
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetAlways, isWin() was: " + str(isWin()) + " => bet: " + str(bet)
	return bet

def stepUpBet():
	global bet, stepAdd, initBet
	if bet == 0:
		bet = initBet
	else:
		bet = nextStepUp()
		#tmpbet += round(1 - stepbet*winsInARoll,2)


def nextStepUp():
	global bet, stepAdd, initBet, betSteps

	if useBetSteps:
		bet = nextBetStep()		
	else:
		if stepMultiply > 0:
			if stepMultiply < 1:
				bet = bet + round(bet*stepMultiply,1)
			else:
				bet = round(bet*stepMultiply,1)
		if stepAdd > 0:
			bet += stepAdd

	return bet

def nextBetStep():
	global lastDraw, initBet, maxBet, bet, betSteps

	try:
		betStepsIter = iter(betSteps)
		for step in betStepsIter:
			if step == bet:
				bet = next(betStepsIter)
	except StopIteration:
		return initBet
	return bet

def validateNextbet():
	global lastDraw, initBet, maxBet, bet

	# if bet > maxBet:
	# 	raise ValueError("max bet reached!")

	if bet == 0:
		pass
	elif bet < initBet:
		bet = initBet
	elif bet > maxBet:
		if keepmaxBet:
			bet = maxBet
		if resetOnmaxBet:
			bet = initBet
		if errorOnmaxBet:
			raise ValueError("max bet!")

	if bet > deposit:
		raise ValueError("no money, no honey!")

	return bet


def spinWheel():
	global lastDraw, prevDraw, goodDraws, badDraws
	prevDraw = lastDraw
	lastDraw = random.choice(range(0, 37))
	if isWin() == False:
		badDraws += 1
	else:
		goodDraws += 1
	return lastDraw

def isWin():
	if lastDraw in winningNumbers:
		return True
	elif lastDraw in losingNumbers:
		return False
	else:
		return None


def isPrevWin():	
	if lastDraw in winningNumbers:
		return True
	elif prevDraw in losingNumbers:
		return False
	else:
		return None


# def getLosingNumbers():
# 	return list([0]) + list(range(25, 37))


def cashIn():
	global deposit, lastDraw, bet, winsInARoll

	if bet == 0:
		return

	if (isWin() == True):
		if winRatioFromBet > 0:
			deposit += round(bet*winRatioFromBet,1)
		# if winAddFromBet > 0:
		# 	deposit += winAddFromBet
		winsInARoll += 1
	elif (isWin() == False):
		deposit -= bet
		winsInARoll = 0
	else:
		if winRatioFroNeutralNumbers > 0:
			deposit += round(bet*winRatioFroNeutralNumbers,1)
		# if winAddFroNeutralNumbers > 0:
		# 	deposit += winAddFroNeutralNumbers
		winsInARoll += 1
	
	deposit = round(deposit, 1)
	if deposit < 0:
		raise ValueError("all is lost!")

def dump():
	dump(draws)

def dump(drawNumber):
	global deposit, lastDraw, bet
	print "drawNumber: " + str(drawNumber) + ", lastDraw: " + str(lastDraw) + ", win: " + str(isWin()) + ", bet: " + str(bet) + ", profit: " + str(-bet if isWin() == False else round(bet*winRatioFromBet,1) if isWin() == True else round(bet*winRatioFroNeutralNumbers,1)) + ", deposit: " + str(deposit) + "  ..... redNumbersDrawn: " + str(redNumbersDrawn) + ", blackNumbersDrawn: " + str(blackNumbersDrawn)

def dumpStats():
	global deposit, lastDraw, bet, goodDraws, badDraws
	print "deposit: " + str(deposit)  + ", goodDraws: " + str(goodDraws)   + ", badDraws: " + str(badDraws) + "  ..... redNumbersDrawn: " + str(redNumbersDrawn) + ", blackNumbersDrawn: " + str(blackNumbersDrawn)

def dumpAttempt():
	global deposit, lastDraw, bet
	print "deposit: " + str(deposit) 





main()
