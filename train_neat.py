import multiprocessing as mp
import pickle
import os

import neat

from gomoku import *

runs_per_net = 5
w, h = 10, 10
max_generation = 50

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        fitness = 0
        board = Board(w=w, h=h)
        game = Gomoku(board=board)
        game.next() # first random place

        for i in range(w * h - 1):
            player = game.current_player

            # 1: current player, -1: opposite player, 0: space available
            inputs = game.board.board.copy()
            inputs[(inputs != player) & (inputs != 0)] = -1
            inputs[(inputs == player) & (inputs != 0)] = 1
            inputs = inputs.astype(np.float32).flatten()

            # 1: space available, 0: unavailable
            # spaces = game.board.board.copy()
            # spaces[spaces == 0] = 10
            # spaces[spaces != 10] = 0
            # spaces[spaces == 10] = 1

            action = np.array(net.activate(inputs), np.float32).reshape((board.h, board.w))
            x, y = np.unravel_index(np.argmax(action), action.shape)
            # x, y = np.clip(net.activate(inputs), 0, 9).astype(np.int)

            if game.board.board[y][x] == 0:
                game.next(x=x, y=y)
                fitness += 2
            else:
                game.next()
                fitness -= 1

            won_player = game.check_won()

            if won_player > 0:
                fitness += 50
                break

        fitnesses.append(fitness)

    return min(fitnesses)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    'config'
)

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
pop.add_reporter(neat.StdOutReporter(True))

# winner = pop.run(eval_genomes)
pe = neat.ParallelEvaluator(mp.cpu_count(), eval_genome)
winner = pop.run(pe.evaluate, n=max_generation)

os.makedirs('result', exist_ok=True)
with open('result/winner', 'wb') as f:
    pickle.dump(winner, f)

print(winner)