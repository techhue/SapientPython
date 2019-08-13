import pickle
import sys
class TicTacToe:

	
	def __init__(self,choices=[],playerOneTurn=True,winner=False,boardDim=3,game="newGame"):
		if game == "newGame" :
			self.choices = choices
			self.playerOneTurn = playerOneTurn
			self.winner = winner	
			self.boardDim = boardDim
			self.initialiseParameters(self.boardDim)
		else:
			f1 = open("TicTacToesavefile",'r+b')
			data = pickle.load(f1)
			self.choices = data[0]
			self.playerOneTurn = data[1]
			self.winner = data[2]
			self.boardDim = data[3]
			f1.close()
			self.simulateGame(self.choices,self.playerOneTurn,self.winner,self.boardDim)
	
	def initialiseParameters(self,boardDim):
		print("Enter the side of board\n")
		self.boardDim = int(input(">> "))
		self.initialiseBoard(self.choices,self.boardDim)
		

	def initialiseBoard(self,choices,boardDim):
		for x in range (0,self.boardDim*self.boardDim):
			self.choices.append(str(x+1))
		self.simulateGame(self.choices,self.playerOneTurn,self.winner,self.boardDim)

	def printBoard(self,choices,boardDim):
		print("\nCurrent Board\n")
		for row in range(self.boardDim):
			s = ""
			for column in range(self.boardDim):
				s= s + '{:>3}'.format((self.choices[((row)*self.boardDim)+column])) + ' '
#				s = s + self.choices[((row)*self.boardDim)+column] + ' '
			print(s)
			print("\n")
	
	def simulateGame(self,choices,playerOneTurn,winner,boardDim):
		flag = 0
		while not self.winner and flag<(self.boardDim*self.boardDim) :
			self.printBoard(choices,boardDim)
			print("\nPress Q to exit and S to save:\n")
			if self.playerOneTurn :
				print("Player 1:")
			else:
				print("Player 2:")

			choice = input(">> ")
	
			if choice == "q":
				sys.exit()			
			elif choice == "s":
				saveData = [choices,playerOneTurn,winner,boardDim]
				f = open('TicTacToesavefile','w+b')
				pickle.dump(saveData,f)
				f.close()
				sys.exit()
			else:
				choice = int(choice)
				if self.choices[choice-1] == 'X' or self.choices[choice-1] == 'O':
					print("illegal move,please try again")
					continue

			if self.playerOneTurn:
				self.choices[choice-1] = 'X'
			else :
				self.choices[choice-1] = 'O'
	
			self.playerOneTurn = not self.playerOneTurn

 
			
			for x in range (0,self.boardDim) :
				y = x*self.boardDim
				
				if(len(set(self.choices[y:y+self.boardDim]))==1):
					self.winner = True
					self.printBoard(choices,boardDim)
				
				if(len(set(self.choices[x::self.boardDim]))==1):
					self.winner = True
					self.printBoard(choices,boardDim)
				
				if(len(set(self.choices[0::self.boardDim+1]))==1):	
					self.winner = True
					self.printBoard(choices,boardDim)
			
			flag= flag+1
		if flag == self.boardDim * self.boardDim:
			print("\nMatch Tied\n")
		else:
			print ("Player" + str(int(self.playerOneTurn + 1)) + "wins!\n")



if __name__ == "__main__":
	print("Welcome to TicTacToe Game:")
	print("--------------------------------")
	print("        made by Ajay            ")
	print("\n \n Press the appropriate digit\n ")
	print("1 - New Game \n2 - Saved Game \n")
	choiceGame = int(input(">> "))
	if choiceGame == 1:
		g1 = TicTacToe()
	else:
		g1 = TicTacToe(game="oldGame")
