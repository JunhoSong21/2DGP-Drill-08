from pico2d import *
from state_machine import *

class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif AutoRun_time_out(e):
            if boy.dir == 1:
                boy.face_dir = 1
                boy.action = 3
            elif boy.dir == -1:
                boy.dir = -1
                boy.action = 2

        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == 1:
            boy.dir = 1
        elif boy.face_dir == -1:
            boy.dir = -1

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1: # 오른쪽 바라보는 상태에서 Sleep
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100)
            
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100)
class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir = 1
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0

        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        if boy.x >= 780:
            boy.x = 780
        elif boy.x <= 20:
            boy.x = 20
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == 1:
            boy.dir = 1
            boy.action = 1
        elif boy.face_dir == -1:
            boy.dir = -1
            boy.action = 0

        boy.wait_time = get_time()
        boy.frame = 0

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 10
        if boy.x >= 780:
            boy.dir = -1
            boy.action = 0
            boy.x = 780
        elif boy.x <= 20:
            boy.dir = 1
            boy.action = 1
            boy.x = 20
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.wait_time > 5:
            boy.state_machine.add_event(('AUTORUN_TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y + 10, 150, 150)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle) # 초기 상태 Sleep 으로 설정
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_down: AutoRun},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, a_down: AutoRun},
                AutoRun: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, AutoRun_time_out: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle, a_down: AutoRun}
            }
        )

    def update(self):
        self.state_machine.update()

    def add_event(self, event):
        # event : 입력 이벤트 key, mouse...
        # state_machine에게는 튜플로 만들어진 이벤트로 넘겨주어야 함
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()