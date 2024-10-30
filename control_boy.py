from pico2d import *
import random
from grass import *
from boy import *

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type == SDL_KEYDOWN or SDL_KEYUP:
                boy.add_event(event) # input 이벤트를 boy 에게 전달하고 있다.

def reset_world():
    global running
    global grass
    global world
    global boy

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

# finalization code
close_canvas()