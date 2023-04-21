import tkinter as tk

#Game Tree node
class Node:
    def __init__(self, number = 0):
        #number currently equal to
        self.number = number

        #child values for division
        self.two = None
        self.three = None
        self.four = None
        self.five = None
        
        #node state -1 = not leaf, 0 = draw, 1 = win
        self.state = -1
        
class GameWindow:
    def __init__(self) -> None:
        #Init main window for the game
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry("1000x600")
        
        #Field for initial number of the game
        self.inputNumberValidation = (self.mainWindow.register(self.verifyValue), '%P')
        self.playNumberField = tk.Entry(self.mainWindow, validate = "key", validatecommand = self.inputNumberValidation)
        self.playNumberField.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.playNumberFieldLabel = tk.Label(self.mainWindow, text = "Initial number: ")
        self.playNumberFieldLabel.grid(row = 1, column = 0, padx = 15, pady = 15)

        #Field for the number to win the game
        self.winNumberField = tk.Entry(self.mainWindow, validate = "key", validatecommand = self.inputNumberValidation)
        self.winNumberField.grid(row = 2, column = 1, padx = 15, pady = 15)

        self.winNumberFieldLabel = tk.Label(self.mainWindow, text = "Winning number: ")
        self.winNumberFieldLabel.grid(row = 2, column = 0, padx = 15, pady = 15)

        #Who won
        self.winnner = tk.Label(self.mainWindow, text = "Winner: ")
        self.winnner.grid(row = 3, column = 0, padx = 15, pady = 15)

        self.winnnerName = tk.Label(self.mainWindow, text = "")
        self.winnnerName.grid(row = 3, column = 1, padx = 15, pady = 15)
        
        #Creating start button
        self.startBut = tk.Button(self.mainWindow, text = "Start", width = 5, height = 5, command = self.startGame, state = "normal")
        self.startBut.grid(row=1, column=3, padx=15, pady=15)

        self.restartBut = tk.Button(self.mainWindow, text = "Restart", width = 5, height = 5, command = self.restartGame, state = "normal")
        self.restartBut.grid(row=1, column=4, padx=15, pady=15)

        #Choose who starts the game (makes first move)
        self.starting = tk.IntVar()

        #If 0 then max level, if 1 then minimize
        self.computerMaxOrMin = 0

        self.choiceLabel = tk.Label(self.mainWindow, text = "Choose who makes the first move: ")
        self.choiceLabel.grid(row = 2, column = 3)

        self.humanStarts = tk.Radiobutton(self.mainWindow, text = "Human", variable = self.starting, value = 0)
        self.humanStarts.grid(row = 3, column = 3, padx=15, pady=5)

        self.computerStarts = tk.Radiobutton(self.mainWindow, text = "Compter", variable = self.starting, value = 1)
        self.computerStarts.grid(row = 4, column = 3, padx=15, pady=5)

        #Label for the playing number changing in real time
        self.playNumberText = tk.Label(self.mainWindow, text = "0", font=("Arial", 50), bg="gray", fg="blue")
        self.playNumberText.grid(row = 5, column = 3, padx = 0, pady = 0)

        #Division buttons label
        self.divideButtonLabel = tk.Label(self.mainWindow, text = "Click number to divide: ")
        self.divideButtonLabel.grid(row=6, column=1, padx=15, pady=15)

        #Creating divide by 2 button
        self.divideBy2 = tk.Button(self.mainWindow, text = "2", width = 5, height = 5, command = self.divideBy2, state = "disabled")
        self.divideBy2.grid(row=6, column=2, padx=5, pady=10)

        #Creating divide by 3 button
        self.divideBy3 = tk.Button(self.mainWindow, text = "3", width = 5, height = 5, command = self.divideBy3, state = "disabled")
        self.divideBy3.grid(row=6, column=3, padx=5, pady=10)

        #Creating divide by 4 button
        self.divideBy4 = tk.Button(self.mainWindow, text = "4", width = 5, height = 5, command = self.divideBy4, state = "disabled")
        self.divideBy4.grid(row=6, column=4, padx=5, pady=10)

        #Creating divide by 5 button
        self.divideBy5 = tk.Button(self.mainWindow, text = "5", width = 5, height = 5, command = self.divideBy5, state = "disabled")
        self.divideBy5.grid(row=6, column=5, padx=5, pady=10)

        #Game Tree root node
        self.root = Node(int(self.playNumberText.cget("text")))

        self.mainWindow.mainloop()
    
    def verifyValue(self, value):
        if not value:
            return True
        
        try:
            int(value)
            return True
        
        except ValueError:
            return False
    
    #Starting the game
    def startGame(self):
        playNumberInt = int(self.playNumberField.get())
        winNumberInt = int(self.winNumberField.get())
        if(playNumberInt <= winNumberInt or playNumberInt <= 0 or winNumberInt <= 0):
            self.restartGame()
            return

        self.playNumberField.config(state = "disabled")
        self.winNumberField.config(state = "disabled")
        self.startBut.config(state = "disabled")
        self.humanStarts.config(state = "disabled")
        self.computerStarts.config(state = "disabled")
        self.winnnerName.config(text = "")
        
        self.unfreezeUI()

        self.playNumberText.config(text = self.playNumberField.get())
        self.root.number = int(self.playNumberText.cget("text"))
        self.buildTree(self.root)
        self.playNumber = int(self.playNumberField.get())

        if int(self.starting.get()) == 0:
            self.unfreezeUI()
            self.computerMaxOrMin = 1
        else:
            self.computerMaxOrMin = 0
            self.computerMove(self.computerMaxOrMin)
    
    #Restarting the game
    def restartGame(self):
        self.playNumberField.delete(0, tk.END)
        self.winNumberField.delete(0, tk.END)
        self.playNumberField.config(state = "normal")
        self.winNumberField.config(state = "normal")
        self.startBut.config(state = "normal")
        self.humanStarts.config(state = "normal")
        self.computerStarts.config(state = "normal")
        self.playNumberText.config(text="0")
        self.winnnerName.config(text = "")
        self.root = Node(int(self.playNumberText.cget("text")))
        self.freezeUI()
    
    #Disabling buttons so computer can make the move
    def freezeUI(self):
        self.divideBy2.config(state = "disabled")
        self.divideBy3.config(state = "disabled")
        self.divideBy4.config(state = "disabled")
        self.divideBy5.config(state = "disabled")
    
    #Enabling buttons so human can make the move
    def unfreezeUI(self):
        self.divideBy2.config(state = "normal")
        self.divideBy3.config(state = "normal")
        self.divideBy4.config(state = "normal")
        self.divideBy5.config(state = "normal")

    def isWin(self, player): #player is either 0 or 1
        number = int(self.playNumberText.cget("text"))
        if number == int(self.winNumberField.get()):
            self.gameResult(player)
            return True
        elif not self.isValid:
            self.gameResult(-1)
            return True
        else:
            return False
        
    def isValid(self) -> bool:
        number = int(self.playNumberText.cget("text"))
        if number % 2 != 0 and number % 3 != 0 and number % 4 != 0 and number % 5 != 0 and number > int(self.winNumberField.get()) or number < int(self.winNumberField.get()):
            return False
        return True

    def isLegalMove(self, number, divisor):
        if number % divisor == 0:
            return True
        return False
    
    

    def divideBy2(self):
        asInt = int(self.playNumberText.cget("text"))

        if not self.isValid():
            self.gameResult(-1)
            return
        
        if self.isLegalMove(asInt, 2):
            asInt = asInt // 2
            self.playNumberText.config(text = str(asInt))
            if self.isWin(0):
                return
            self.root = self.root.two
            self.computerMove(self.computerMaxOrMin)
        

    def divideBy3(self):
        asInt = int(self.playNumberText.cget("text"))

        if not self.isValid():
            self.gameResult(-1)
            return
        
        if self.isLegalMove(asInt, 3):
            asInt = asInt // 3
            self.playNumberText.config(text = str(asInt))
            if self.isWin(0):
                return
            self.root = self.root.three
            self.computerMove(self.computerMaxOrMin)


    def divideBy4(self):
        asInt = int(self.playNumberText.cget("text"))

        if not self.isValid():
            self.gameResult(-1)
            return
        
        if self.isLegalMove(asInt, 4):
            asInt = asInt // 4
            self.playNumberText.config(text = str(asInt))
            if self.isWin(0):
                return
            self.root = self.root.four
            self.computerMove(self.computerMaxOrMin)
    
    def divideBy5(self):
        asInt = int(self.playNumberText.cget("text"))

        if not self.isValid():
            self.gameResult(-1)
            return
        
        if self.isLegalMove(asInt, 5):
            asInt = asInt // 5
            self.playNumberText.config(text = str(asInt))
            if self.isWin(0):
                return
            self.root = self.root.five
            self.computerMove(self.computerMaxOrMin)
    

    def gameResult(self, winner):
        if winner == 0:
            self.winnnerName.config(text = "Human! \nPress restart to start new game.")
            return
        elif winner == 1:
            self.winnnerName.config(text = "Computer! \nPress restart to start new game.")
            return
        else:
            self.winnnerName.config(text = "Draw! \nPress restart to start new game.")
            return

    def isDivisible(self, number):
        if number % 2 != 0 and number % 3 != 0 and number % 4 != 0 and number % 5 != 0:
            return False
        return True

    #Recursively building tree
    def buildTree(self, node, step = 0):
        winNum = int(self.winNumberField.get())

        if not node:
            return

        if node.number == winNum:
            node.state = step + 1 #win
            return
        if node.number < winNum:
            node.state = 0 #draw
            return
        if not self.isDivisible(node.number):
            node.state = 0 #draw
            return
        
        if node.number % 2 == 0:
            node.two = Node(node.number//2)
            self.buildTree(node.two, step + 1)

        if node.number % 3 == 0:
            node.three = Node(node.number//3)
            self.buildTree(node.three, step + 1)

        if node.number % 4 == 0:
            node.four = Node(node.number//4)
            self.buildTree(node.four, step + 1)

        if node.number % 5 == 0:
            node.five = Node(node.number//5)
            self.buildTree(node.five, step + 1)


    def miniMax(self, node, level):
        #If state is either 0 or 1, then we have leaf nodes
        #This means we have draw or win
        if node.state != -1:
            return node.state #returns 0 or 1

        #If we are maximizing then we have to find the largest score of its children nodes
        if level == 1: #maximize
            maxScore = float('-inf')
            if node.two:
                maxScore = max(maxScore, self.miniMax(node.two, 0))
            if node.three:
                maxScore = max(maxScore, self.miniMax(node.three, 0))
            if node.four:
                maxScore = max(maxScore, self.miniMax(node.four, 0))
            if node.five:
                maxScore = max(maxScore, self.miniMax(node.five, 0))
            return maxScore
        
        #If we are minimizing then we have to find the lowest score of its children nodes
        else: #minimize
            minScore = float('inf')
            if node.two:
                minScore = min(minScore, self.miniMax(node.two, 1))
            if node.three:
                minScore = min(minScore, self.miniMax(node.three, 1))
            if node.four:
                minScore = min(minScore, self.miniMax(node.four, 1))
            if node.five:
                minScore = min(minScore, self.miniMax(node.five, 1))
            return minScore

    def findBestMove(self, node, level):
        if level == 0:
            bestScore = float('inf')
        else:
            bestScore = float('-inf')
        bestNode = None
        bestMove = 0

        if not self.isValid():
            return 0

        #Looking for the node with maximum current score
        if node.two:
            currentScore = self.miniMax(node.two, 1 - level)
            if level == 1 and currentScore > bestScore:
                bestScore = currentScore
                bestNode = node.two
                bestMove = 2
            elif level == 0 and currentScore < bestScore:
                bestScore = currentScore
                bestNode = node.two
                bestMove = 2

        if node.three:
            currentScore = self.miniMax(node.three, 1 - level)
            if level == 1 and currentScore > bestScore:
                bestScore = currentScore
                bestNode = node.three
                bestMove = 3
            elif level == 0 and currentScore < bestScore:
                bestScore = currentScore
                bestNode = node.three
                bestMove = 3

        if node.four:
            currentScore = self.miniMax(node.four, 1 - level)
            if level == 1 and currentScore > bestScore:
                bestScore = currentScore
                bestNode = node.four
                bestMove = 4
            elif level == 0 and currentScore < bestScore:
                bestScore = currentScore
                bestNode = node.four
                bestMove = 4

        if node.five:
            currentScore = self.miniMax(node.five, 1 - level)
            if level == 1 and currentScore > bestScore:
                bestScore = currentScore
                bestNode = node.five
                bestMove = 5
            elif level == 0 and currentScore < bestScore:
                bestScore = currentScore
                bestNode = node.five
                bestMove = 5

        return bestMove

    #Calling this function for computer move
    def computerMove(self, level):
        self.freezeUI()
        
        compMove = self.findBestMove(self.root, level)

        if compMove == 0:
            self.gameResult(-1)
            return
        else:
            currentNumber = int(self.playNumberText.cget("text"))
            currentNumber = currentNumber // compMove
            self.playNumberText.config(text = str(currentNumber))

            self.isWin(1)
            
            if compMove == 2:
                self.root = self.root.two
            elif compMove == 3:
                self.root = self.root.three
            elif compMove == 4:
                self.root = self.root.four
            elif compMove == 5:
                self.root = self.root.five
            
        print("Computer move: ", compMove)
        self.unfreezeUI()

class StartGame():
    def __init__(self) -> None:
        gameWindow = GameWindow()



startGame = StartGame()
