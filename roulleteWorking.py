import random 

# 
# Fast doubling Fibonacci algorithm (Python)
# 
# Copyright (c) 2015 Project Nayuki
# All rights reserved. Contact Nayuki for licensing.
# https://www.nayuki.io/page/fast-fibonacci-algorithms
# 

attempts = 1
draws = 1000000
deposit = 1000
maxLot = 10

initLot = 0.9
stepMultiply = 1.5
stepAdd = 0
winRatioFromLot = 1
winRatioFroNeutralNumbers = 3
playMartingale = False
playNotOnLoss = True
playOnWinOnly = False
playNotOnLosingStreak = False

# losingNumbers = list([0]) + list(range(19, 37)) # 1
# losingNumbers = list([0]) + list(range(25, 37)) # 2
# losingNumbers = list([0]) + list(range(31, 37)) # 5
# losingNumbers = list([0]) + list(range(35, 37)) # 17


winningNumbers = list(range(19, 24)) # 2
losingNumbers = list([0]) + list(range(25, 37)) # 2
print losingNumbers

keepMaxLot = False
resetOnMaxLot = True
errorOnMaxLot = False

prevDraw = -1
lastDraw = -1
lot = 0
winsInARoll = 0
goodDraws = 0
badDraws = 0


def main():
	global deposit, lastDraw, lot, maxLot

	wins = 0

	for att in range(1,attempts+1):
		try:
			oneAttempt()
			if deposit > 1000:
				wins += 1

			print "Attempt " + str(att) + "     deposit: " + str(deposit) + "     winrate: " + str((wins*100)/att) 
			# dumpAttempt()
			dumpStats()
			deposit = 1000
			lot = 0
			lastDraw = -1
			
		except ValueError as err:	
			dumpStats()
			deposit = 1000
			lot = 0
			lastDraw = -1
			print "Attempt " + str(att) + "     deposit: " + str(deposit)
			print(err)		
			



def oneAttempt():
	global draws, deposit, lastDraw, lot, maxLot

	while draws > 0:
		draws -= 1
		#print draw
		placeBet()
		# print "placed lot: " + str(lot)
		spinWheel()
		# print "number : " + str(lastDraw) + " win: " + str(isWin())
		cashIn()

		dump()


def placeBet():
	global lastDraw, initLot, maxLot, lot, playOnWinOnly, placeNotOnLosingStreak
	
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

	return validateNextLot()


def placeMartingale():
	global lastDraw, initLot, maxLot, lot

	if (isWin() == None):
		pass
	elif isWin() == False:
		stepUpBet()
	elif (isWin() == True):
		lot = initLot

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => lot: " + str(lot)
	return lot


def placeBetNotOnLosingStreak():
	global lastDraw, initLot, maxLot, lot

	if (isWin() == None):
		pass
	elif isWin() == False:
		lot = initLot
		if isPrevWin() == False:
			lot = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => lot: " + str(lot)
	return lot


def placeNotOnLoss():
	global lastDraw, initLot, maxLot, lot

	if (isWin() == None):
		stepUpBet()
	elif isWin() == False:
		lot = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => lot: " + str(lot)
	return lot


def placeBetOnWinOnly():
	global lastDraw, initLot, maxLot, lot

	if (isWin() == None):
		pass
	elif isWin() == False:
		lot = 0
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetOnWinOnly, isWin() was: " + str(isWin()) + " => lot: " + str(lot)
	return lot


def placeBetAlways():
	global lastDraw, initLot, maxLot, lot

	if (isWin() == None):
		pass
	elif isWin() == False:
		lot = initLot
	elif (isWin() == True):
		stepUpBet()

	# print "placeBetAlways, isWin() was: " + str(isWin()) + " => lot: " + str(lot)
	return lot

def stepUpBet():
	global lot, stepAdd, initLot
	if lot == 0:
		lot = initLot
	else:
		if stepMultiply > 0:
			if stepMultiply < 1:
				lot = lot + round(lot*stepMultiply,1)
			else:
				lot = round(lot*stepMultiply,1)
		if stepAdd > 0:
			lot += stepAdd
		#tmplot += round(1 - stepLot*winsInARoll,2)

def validateNextLot():
	global lastDraw, initLot, maxLot, lot

	# if lot > maxLot:
	# 	raise ValueError("max lot reached!")

	if lot == 0:
		pass
	elif lot < initLot:
		lot = initLot
	elif lot > maxLot:
		if keepMaxLot:
			lot = maxLot
		if resetOnMaxLot:
			lot = initLot
		if errorOnMaxLot:
			raise ValueError("max lot!")

	if lot > deposit:
		raise ValueError("no money, no honey!")

	return lot


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
	global deposit, lastDraw, lot, winsInARoll

	if lot == 0:
		return

	if (isWin() == True):
		deposit += lot/winRatioFromLot
		winsInARoll += 1
	elif (isWin() == False):
		deposit -= lot
		winsInARoll = 0
	else:
		deposit += lot/winRatioFroNeutralNumbers
		winsInARoll += 1
	
	deposit = round(deposit, 1)
	if deposit < 0:
		raise ValueError("all is lost!")


def dump():
	global deposit, lastDraw, lot
	print "draws: " + str(draws) + ", lastDraw: " + str(lastDraw) + ", win: " + str(isWin()) + ", lot: " + str(lot) + ", deposit: " + str(deposit) 

def dumpStats():
	global deposit, lastDraw, lot, goodDraws, badDraws
	print "deposit: " + str(deposit)  + ", goodDraws: " + str(goodDraws)   + ", badDraws: " + str(badDraws) 

def dumpAttempt():
	global deposit, lastDraw, lot
	print "deposit: " + str(deposit) 
















main()

