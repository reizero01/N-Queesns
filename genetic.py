from board import Board
import random
import copy


class Genetic:
    def __init__(self, board : Board):
        self.step = 0
        self.n_queen = len(board.map)
        self.total_pairs = 0
        for i in range(self.n_queen):
            self.total_pairs += i
        self.board = board
        self.state = []
        self.pair_H = []
        self.best_H = 0
        self.answer = ""

# Generate the four states for genetic method
    def get4States(self):
        for x in range (4):
            state = ""
            board = Board(self.n_queen)
            board.set_queens()
            for i in range (self.n_queen):
                for j in range (self.n_queen):
                    if (board.map[i][j] != 0):
                        state += str(j + 1)
            self.state.append(state)
        # print(self.state)

    def pairs_check(self):
        atk_pair = [0] * len(self.state)
        non_atk_pair = [0] * len(self.state)
        
        # Check attacking pair
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                for k in range(1, self.n_queen):    
                    if(j + k < 5):   
                        if(int(self.state[i][j+k]) == int(self.state[i][j]) + k or int(self.state[i][j+k]) == int(self.state[i][j]) - k):
                            atk_pair[i] += 1
                        if(self.state[i][j+k] == self.state[i][j]):
                            atk_pair[i] += 1
                    if(j - k >= 0):
                        if(int(self.state[i][j-k]) == int(self.state[i][j]) + k or int(self.state[i][j-k]) == int(self.state[i][j]) - k):
                            atk_pair[i] += 1
                        if(self.state[i][j-k] == self.state[i][j]):
                            atk_pair[i] += 1
            atk_pair[i] = atk_pair[i]/2
            non_atk_pair[i] = self.total_pairs - atk_pair[i]
        self.pair_H = non_atk_pair
        self.best_H = max(non_atk_pair)
        index = non_atk_pair.index(self.best_H)
        self.answer = self.state[index]
        # print(non_atk_pair)
        # print(self.answer)
    
    def selection(self):
        current_state = copy.deepcopy(self.state)
        current_best_H = sum(self.pair_H)
        current_pair_H = self.pair_H
        partical = []
        ran = []
        # Get the partial of H
        for i in range(len(current_pair_H)):
            partical.append(current_pair_H[i]/current_best_H)
        # print(partical)
        ran.append(partical[0])
        # Get the probability of each state
        for i in range(1, len(partical)):
            ran.append(ran[i-1] + partical[i])
        # print(ran)
    
        for j in range(len(self.state)):
            r = random.random()
            # print(r)
            if(ran[0] > r):
                self.state[j] = current_state[0]
            else:
                for i in range(1, len(ran)):
                    if(r > ran[i - 1] and r < ran[i]):
                        self.state[j] = current_state[i]
        # print(self.state)
    
    def cross_over(self):
        for i in range(0, len(self.state), 2):
            r = random.randint(1, self.n_queen - 1)
            # print(r)
            switch = self.state[i][r:len(self.state[i])]
            # print(switch)
            self.state[i] = self.state[i][0:r] + self.state[i+1][r:len(self.state[i])]
            self.state[i+1] = self.state[i+1][0:r] + switch
        # print(self.state)
    
    def mutation(self):
        for i in range(len(self.state)):
            r1 = random.randint(0, self.n_queen - 1)
            r2 = random.randint(0, self.n_queen)
            if(r2 > 0):
                self.state[i] = self.state[i][0:r1] + str(r2) + self.state[i][r1+1:]
        # print(self.state)

    def solve(self):
        self.get4States()
        while(1 > 0):
            self.pairs_check()
            if(self.best_H < self.total_pairs):
                self.selection()
                self.cross_over()
                self.mutation()
            else:
                for i in range(len(self.answer)):
                    self.board.map[i][int(self.answer[i])-1] = 1
                self.board.show()
                print("Steps: " + str(self.step))
                break
            self.step+=1


if __name__ == '__main__':
    home = Board(5)
    genetic = Genetic(home)
    genetic.solve()
