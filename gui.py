from ursina import *
import numpy as np
from tensorflow.keras.models import load_model
from gomoku import Board, Gomoku

model = load_model('models/20201213_202430.h5')

app = Ursina()

window.borderless = False

w, h = 20, 20
camera.orthographic = True
camera.fov = 23
camera.position = (w//2, h//2)

player = Entity(name='1', color=color.orange)
cursor = Tooltip(player.name, color=player.color, origin=(0.6, 0.6), scale=2, enabled=True)
cursor.background.color = color.clear

board = Board(w=w, h=h)
board_buttons = [[None for x in range(w)] for y in range(h)]
game = Gomoku(board=board)

for y in range(h):
    for x in range(w):
        b = Button(parent=scene, position=(x, y)) # start from bottom left
        board_buttons[y][x] = b

        def on_click(b=b):
            # player turn
            b.text = '1'
            b.color = color.orange
            b.collision = False

            game.put(x=int(b.position.x), y=int(h - b.position.y - 1)) # start from top left

            won_player = game.check_won()

            if won_player > 0:
                end_session(won_player)

            game.next()

            # cpu turn
            input = game.board.board.copy()
            input[(input != 1) & (input != 0)] = -1
            input[(input == 1) & (input != 0)] = 1
            input = np.expand_dims(input, axis=(0, -1)).astype(np.float32)

            output = model.predict(input).squeeze()
            output = output.reshape((h, w))
            output_y, output_x = np.unravel_index(np.argmax(output), output.shape)

            game.put(x=output_x, y=output_y)
            
            board_buttons[h - output_y - 1][output_x].text = '2'
            board_buttons[h - output_y - 1][output_x].color = color.azure
            board_buttons[h - output_y - 1][output_x].collision = False

            won_player = game.check_won()

            if won_player > 0:
                end_session(won_player)

            game.next()

            print(game.board)

        b.on_click = on_click

def end_session(won_player):
    destroy(cursor)
    Panel(z=1, scale=10, model='quad')
    t = Text(f'Player {won_player} won!', scale=3, origin=(0, 0), background=True)
    t.create_background(padding=(.5,.25), radius=Text.size/2)

app.run()