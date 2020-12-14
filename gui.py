from ursina import *
from gomoku import Board, Gomoku

app = Ursina()

window.borderless = False

w, h = 20, 20
camera.orthographic = True
camera.fov = 23
camera.position = (w//2, h//2)

player = Entity(name='1', color=color.azure)
cursor = Tooltip(player.name, color=player.color, origin=(0.6, 0.6), scale=2, enabled=True)
cursor.background.color = color.clear

board = Board(w=w, h=h)
game = Gomoku(board=board)

for y in range(h):
    for x in range(w):
        b = Button(parent=scene, position=(x, y))

        def on_click(b=b):
            current_player = game.current_player

            b.text = str(current_player)
            b.color = color.orange if current_player == 1 else color.azure
            b.collision = False

            game.put(x=int(b.position.x), y=int(b.position.y))

            won_player = game.check_won()

            if won_player > 0:
                end_session(won_player)

            game.next()

            cursor.text = str(game.current_player)
            cursor.color = color.orange if game.current_player == 1 else color.azure

        b.on_click = on_click

def end_session(won_player):
    destroy(cursor)
    Panel(z=1, scale=10, model='quad')
    t = Text(f'Player {won_player} won!', scale=3, origin=(0, 0), background=True)
    t.create_background(padding=(.5,.25), radius=Text.size/2)
    t.background.color = player.color.tint(-.2)

app.run()