from sdl2 import *

# 이벤트 체크 함수를 정의
# 상태 이벤트 e = (종류, 실제값)

def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e): # e 가 space_down 인지 판단 > 0 or 1
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def time_out(e): # e 가 time_out 인지 판단
    return e[0] == 'TIME_OUT'

def AutoRun_time_out(e): # e 가 AutoRun_time_out 인지 판단
    return e[0] == 'AUTORUN_TIME_OUT'

class StateMachine:
    def __init__(self, obj):
        self.obj = obj # 어떤 객체의 상태 머신인지 설정
        self.event_q = [] # 상태 이벤트를 보관할 큐

    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서, 그걸로 현재 상태를 정의
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')

    def update(self):
        self.cur_state.do(self.obj) # Idle.do()
        
        if self.event_q: # list는 요소가 존재하면 True
            e = self.event_q.pop(0) # 0 으로 설정하면 맨 앞에서 pop 수행
            # 현재 상태와 발생한 이벤트에 따라서 다음 상태를 결정 = 상태 변환 테이블
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    print(f'Enter into {next_state}')
                    self.cur_state.enter(self.obj, e) # 상태 변환 이유를 구분
                    return # event에 따른 상태 변환 완료
                
            # 이 시점에 왔다는 것은, event에 따른 전환에 실패.

    def draw(self):
        self.cur_state.draw(self.obj)

    def add_event(self, e):
        print(f'    DEBUG: add event {e}')
        self.event_q.append(e)

    def set_transitions(self, transitions):
        self.transitions = transitions