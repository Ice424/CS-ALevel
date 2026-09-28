#Skeleton Program code for the AQA A Level Paper 1 Summer 2027 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

import math

def Main():
    Board = []
    Players = []
    Discard = []
    TurnsSinceMatch = 0
    WhoseTurn = 0
    MaxScore = 10
    FILE_EXTENSION = ".txt"
    FileName = input("Enter filename to load or just press Enter to play the default game: ") + FILE_EXTENSION
    UseDataFromFile = False
    if FileName != FILE_EXTENSION:
        UseDataFromFile, Board, Players, Discard, MaxScore, WhoseTurn, TurnsSinceMatch = LoadGame(FileName)   
        if UseDataFromFile == False:
            print("Setting up default game")
    if UseDataFromFile == False:
        Players.append(Player("Player 1", 0))
        Players.append(Player("Player 2", 0))
        for Count in range(1, 37):
            P = Pile(3, 0)
            P.Add(Tile("A", 1))
            P.Add(Tile("B", 2))
            P.Add(Tile("A", 1))
            Board.append(P)
    ThisGame = Game(Board, Players, Discard, WhoseTurn, MaxScore, TurnsSinceMatch)
    ThisGame.PlayGame()
    input()

def LoadGame(FileName):
    Board = []
    Players = []
    Discard = []
    MaxScore = 0
    WhoseTurn = 0
    TurnsSinceMatch = 0
    try:
        with open(FileName) as File:
            LineFromFile = File.readline()
            BoardSize = int(LineFromFile)
            for i in range(1, BoardSize + 1):
                LineFromFile = File.readline()
                Items = LineFromFile.split(",")
                PileSize = len(Items) // 2
                P = Pile(PileSize, int(Items[0]))
                for TileNo in range(len(Items) - 2, -1, -2):
                    P.Add(Tile(Items[TileNo], int(Items[TileNo + 1])))
                Board.append(P)
            LineFromFile = File.readline()
            NoOfPlayers = int(LineFromFile)
            for i in range (1, NoOfPlayers + 1):
                LineFromFile = File.readline()
                Items = LineFromFile.split(",")
                Players.append(Player(Items[0], int(Items[1])))
            LineFromFile = File.readline()
            Items = LineFromFile.split(",")
            for i in range(0, len(Items) - 1, 2):
                Discard.append(Tile(Items[i], int(Items[i + 1])))
            LineFromFile = File.readline()
            MaxScore = int(LineFromFile)
            LineFromFile = File.readline()
            WhoseTurn = int(LineFromFile)
            LineFromFile = File.readline()
            TurnsSinceMatch = int(LineFromFile)
    except:
        print("File not loaded")
        return False, Board, Players, Discard, MaxScore, WhoseTurn, TurnsSinceMatch
    return True, Board, Players, Discard, MaxScore, WhoseTurn, TurnsSinceMatch

class Game():
    def __init__(self, B, P, D, WT, MS, TSM):
        self.__Board = B
        self.__Players = P
        self.__Discard = D
        self.__WhoseTurn = WT
        self.__MaxScore = MS
        self.__TurnsSinceMatch = TSM
        self.__GameOver = False
        self.__GridSize = int(math.sqrt(len(self.__Board)))

    def PlayGame(self):
        while self.__GameOver == False:
            Choice = ""
            while Choice != "T":
                self.__DisplayMenu()
                Choice = self.__GetChoice()
                if Choice == "B":
                    self.__DisplayBoard()
                elif Choice == "D":
                    self.__DisplayDiscard()
                elif Choice == "S":
                    self.__DisplayScores()
            Pile1 = self.__ChoosePile()
            Pile2 = self.__ChoosePile()
            while Pile1 == Pile2:
                Pile2 = self.__ChoosePile()
            self.__TurnsSinceMatch += 1
            if self.__Board[Pile1].Empty() == False and self.__Board[Pile2].Empty() == False:
                if self.__Board[Pile1].GetSymbolOfTopTile() == self.__Board[Pile2].GetSymbolOfTopTile():
                    self.__TurnsSinceMatch = 0
                    Tile1 = self.__Board[Pile1].Remove()
                    Tile2 = self.__Board[Pile2].Remove()
                    self.__Discard.append(Tile1)
                    self.__Discard.append(Tile2)
                    ScoreIncrease = 0
                    ScoreIncrease += Tile1.GetPoints() + Tile2.GetPoints()
                    self.__Players[self.__WhoseTurn].ChangeScore(ScoreIncrease)
                    print(f"{self.__Players[self.__WhoseTurn].GetName()}, you had two matching {Tile1.GetSymbol()} tiles; your score has increased by {ScoreIncrease}")
                else:
                    print("You did not find a matching pair.")
                    print(f"The first pile you chose had a {self.__Board[Pile1].GetSymbolOfTopTile()}")
                    print(f"The second pile you chose had a {self.__Board[Pile2].GetSymbolOfTopTile()}")
            else:
                print("You chose an empty pile")
            print()
            self.__UpdateWhoseTurn()
            self.__GameOver = self.__MaxScoreReached() or self.__NoMoreTilesLeft()
        if self.__Players[0].GetScore() > self.__Players[1].GetScore():
            print(f"{self.__Players[0].GetName()} has won!")
        elif self.__Players[1].GetScore() > self.__Players[0].GetScore():
            print(f"{self.__Players[1].GetName()} has won!")

    def __DisplayScores(self):
        print()
        for P in self.__Players:
            print(f"{P.GetName()}: has a score of {P.GetScore()}")
        print()

    def __DisplayMenu(self):
        print()
        print()
        print("MENU")
        print("B. Display the board")
        print("D. Display the discard")
        print("T. Take turn")
        print("S. Display scores")
        print()

    def __GetChoice(self):
        Choice = input(f"{self.__Players[self.__WhoseTurn].GetName()}, enter your choice: ")
        return Choice

    def __DisplayBoard(self):
        for y in range (self.__GridSize, 0, -1):
            print(f"{y}|", end="")
            for x in range(1, self.__GridSize + 1):
                print(self.__Board[self.__GetIndex(x, y)].GetNumberOfTiles(), end="")
            print()
        print("  ", end="")
        for x in range(1, self.__GridSize + 1):
            print("-", end="")
        print()
        print("  ", end="")
        for x in range (1, self.__GridSize + 1):
            print(x, end="")
        print()

    def __DisplayDiscard(self):
        print()
        print()
        print("Discard: ", end="")
        if len(self.__Discard) == 0:
            print("Empty")
        else:
            print(self.__Discard[0].GetSymbol(), end="")
            Count = 1
            while Count < len(self.__Discard):
                print(f", {self.__Discard[Count].GetSymbol()}", end="")
                Count += 1
        print()
        print()

    def __ChoosePile(self):
        x = 0
        y = 0
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        return self.__GetIndex(x, y)

    def __GetIndex(self, x, y):
        return x - 1 + ((y - 1) * self.__GridSize)

    def __UpdateWhoseTurn(self):
        self.__WhoseTurn = (self.__WhoseTurn + 1) % len(self.__Players)

    def __NoMoreTilesLeft(self):
        for P in self.__Board:
            if P.Empty() == False:
                return False
        return True

    def __MaxScoreReached(self):
        for P in self.__Players:
            if P.GetScore() >= self.__MaxScore:
                return True
        return False

class Tile():
    def __init__(self, S, P):
        self._Symbol = S
        self._Points = P

    def GetPoints(self):
        return self._Points

    def GetSymbol(self):
        return self._Symbol

class Player():
    def __init__(self, N, S):
        self._Name = N
        self._Score = S

    def GetScore(self):
        return self._Score

    def GetName(self):
        return self._Name

    def ChangeScore(self, Change):
        self._Score += Change

class Pile():
    def __init__(self, M, B):
        self._Tiles = []
        self._Max = M
        self._Bonus = B

    def Add(self, T):
        if len(self._Tiles) < self._Max:
            self._Tiles.insert(0, T)

    def GetSymbolOfTopTile(self):
        return self._Tiles[0].GetSymbol()

    def Remove(self):
        Temp = self._Tiles[0]
        self._Tiles.pop(0)
        return Temp

    def Empty(self):
        if len(self._Tiles) == 0:
            return True
        else:
            return False

    def GetNumberOfTiles(self):
        return len(self._Tiles)

if __name__ == "__main__":
    Main()
