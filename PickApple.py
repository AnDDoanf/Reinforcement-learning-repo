from turtle import Turtle, Screen
import numpy as np
import random

learning_rate = 0.1
discount_factor = 0.6


screen = Screen()
vi_tri =[(-225,225),(-75,225),(75,225),(225,225),
         (-225,75),(-75,75),(75,75),(225,75),
         (-225,-75),(-75,-75),(75,-75),(225,-75),
         (-225,-225),(-75,-225),(75,-225),(225,-225)]

tuong = []
tao = []
# Q_table = np.zeros((16,4))
Q_table =  np.array([[ 0.00000000e+00,  5.92227325e-01,  0.00000000e+00,  5.87600720e-02],
            [ 0.00000000e+00,  0.00000000e+00,  5.94889523e-03,  2.63408932e-01],
            [ 0.00000000e+00,  8.83836656e-02,  7.35474938e-03,  1.09322682e+00],
            [ 0.00000000e+00,  3.66476395e+00,  5.12851716e-02,  0.00000000e+00],
            [ 6.40459493e-01,  7.56193088e-02,  0.00000000e+00,  0.00000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
            [ 4.73519257e-02,  1.28762497e+00,  0.00000000e+00,  5.06513875e-02],
            [ 3.90149083e-02,  0.00000000e+00,  2.85966726e-01,  0.00000000e+00],
            [ 9.77767230e-01,  1.94940546e-02,  0.00000000e+00,  4.20676528e-03],
            [ 0.00000000e+00, -3.91100579e+00,  2.11449881e-01,  2.61307690e-03],
            [ 5.83873456e-02,  3.48731733e-04,  3.48557636e+00,  0.00000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
            [ 3.66744468e-01,  0.00000000e+00,  0.00000000e+00, -2.52802435e+00],
            [ 1.29114176e+00,  0.00000000e+00,  1.02105889e-04,  6.28074082e-05],
            [ 1.72592871e-01,  0.00000000e+00, -5.00000000e-01,  0.00000000e+00],
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]])
#chon vi tri cho khi
monkey = Turtle("arrow")
monkey.color("brown")
monkey.penup()
monkey.goto(vi_tri[12])

#chon vi tri cho su tu
lion = Turtle("square")
lion.penup()
lion.goto(vi_tri[13])


draw = Turtle("circle")
draw.color("red")
draw.hideturtle()
draw.speed(0)
draw.pencolor("black")
# ve ban do
for a in range (4):
    draw.penup()
    draw.goto(-300,-300 + a* 150)
    draw.pendown()
    for i in range (4):
        for j in range (4):
            draw.forward(150)
            draw.left(90)
        draw.forward(150)
#ô không đi được
def KhongDiDuoc (o):
    draw.penup()
    draw.goto(vi_tri[o])
    draw.backward(75)
    draw.left(90)
    draw.forward(75)
    draw.right(90)
    draw.fillcolor("black")
    draw.begin_fill()
    for _ in range(4):
        draw.forward(150)
        draw.right(90)
    draw.end_fill()
    tuong.append(o)
    

#ô có phần thưởng
def QuaTao (o):
    draw.penup()
    draw.goto(vi_tri[o])
    draw.dot(50, "red")
    tao.append(o)
    

KhongDiDuoc(5)
KhongDiDuoc(11)

def DiLen():
    monkey.goto(monkey.pos() + (0,150))
def DiXuong():
    monkey.goto(monkey.pos() + (0,-150))
def SangTrai():
    monkey.goto(monkey.pos() + (-150,0))
def SangPhai():
    monkey.goto(monkey.pos() + (150,0))

#chon hanh dong
def choose_action(state):
    
    actions = []
    if (vi_tri[state][0] + 150 ) <= 300 and (state + 1) not in tuong:
        actions.append(3)
    if (vi_tri[state][0] - 150 ) >= -300 and (state - 1) not in tuong:
        actions.append(2)
    if (vi_tri[state][1] - 150 ) >= -300 and (state + 4) not in tuong:
        actions.append(1)
    if (vi_tri[state][1] + 150 ) <= 300 and (state - 4) not in tuong:
        actions.append(0)
        
    if random.uniform(0, 1) < 0.1:
        action = random.choice(actions)
    else:
        max_q_value = np.max(Q_table[state][actions])
        valid_actions = [action for action in actions if Q_table[state][action] == max_q_value]
        action = random.choice(valid_actions)
    return action

#cap nhap trang thai
def get_next_state(state, action):
    if action == 0:
        DiLen()
        state -= 4
    if action == 1:
        DiXuong()
        state += 4
    if action == 2:
        SangTrai()
        state -=1
    if action == 3:
        SangPhai()
        state +=1
    return state

def get_reward(state, prev_state):
    if state in tao:
        return 5
    if state == 13:
        return -5
    # elif state == prev_state:
    #     return -1
    else:
        return 0

# cap nhap Q_talbe
def update_Q(state, action, next_state, reward):
    Q_table[state][action] = (1 - learning_rate) * Q_table[state][action] + learning_rate * (reward + discount_factor * np.max(Q_table[next_state]))
    print(Q_table)
    print('\n')

tong_so_tao = 0
state = 12
prev_state = 0
for i in range (20):
   QuaTao(7)
   QuaTao(0)
   QuaTao(9)
   state = 12
   monkey.goto(vi_tri[12])
   tong_so_tao = 0
   
   while tong_so_tao != 3:
       action = choose_action(state)
       next_state = get_next_state(state, action)
       #nhat tao

    #    reward = get_reward(next_state, prev_state)
       if next_state in tao:
           tong_so_tao +=1
           draw.goto(vi_tri[next_state])
           draw.dot(50,"white")
           tao.remove(next_state)
    #    update_Q(state, action, next_state, reward)
       pev_state = state
       state = next_state

screen.exitonclick()