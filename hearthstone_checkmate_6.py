import random
import pygame
from sys import exit
from pygal import Bar

class Minion:
    def __init__(self,attack,health):
        self.a_h=[]
        self.a_h.append(attack)
        self.a_h.append(health)
        self.live=True
        self.poison=False
        self.shield=False
        self.taunt=False
    def attack(self,opponent_minions,random_num):
        seek=0
        taunt_num=0
        for minion in opponent_minions:
            if minion.taunt and minion.live:
                taunt_num+=1
        if taunt_num==0:
            for num in range(0,7):
                if opponent_minions[num].live:
                    seek+=1
                    if seek==random_num:
                        opponent_num=num
                        break
        else:
            random_num=random.randint(1,taunt_num)
            for num in range(0,7):
                if opponent_minions[num].taunt and opponent_minions[num].live:
                    seek+=1
                    if seek==random_num:
                        opponent_num=num
                        break
        print(str(self.a_h)+'->'+str(opponent_minions[opponent_num].a_h))
        if self.shield:
            self.shield=False
        else:
            self.a_h[1]-=opponent_minions[opponent_num].a_h[0]
        if opponent_minions[opponent_num].shield:
            opponent_minions[opponent_num].shield=False
        else:
            opponent_minions[opponent_num].a_h[1]-=self.a_h[0]

class Poison_Minion(Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.poison=True
        
class Shield_Minion(Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.shield=True
        
class Taunt_Minion(Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.taunt=True
        
class Poison_Shield_Minion(Poison_Minion,Shield_Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.poison=True
        self.shield=True
    
class Poison_Taunt_Minion(Poison_Minion,Taunt_Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.poison=True
        self.taunt=True
    
class Shield_Taunt_Minion(Taunt_Minion,Shield_Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.shield=True
        self.taunt=True

class Poison_Shield_Taunt_Minion(Poison_Minion,Shield_Minion,Taunt_Minion):
    def __init__(self,attack,health):
        super().__init__(attack,health)
        self.poison=True
        self.shield=True
        self.taunt=True

def check_event():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()

def poison_attack_addition(a,b):
    health_max=0
    for minion in a:
        if minion.a_h[1]>health_max:
            health_max=minion.a_h[1]
    for minion in b:
        if minion.a_h[1]>health_max:
            health_max=minion.a_h[1]
    for minion in a:
        if minion.poison:
            minion.a_h[0]=health_max
    for minion in b:
        if minion.poison:
            minion.a_h[0]=health_max

def get_random(a_b_alive_num,a,b,x):
    num=0
    for minion in a:
        if minion.a_h[1]<=0:
            minion.live=False
        else:
            num+=1
    a_b_alive_num[0]=num
    num=0
    for minion in b:
        if minion.a_h[1]<=0:
            minion.live=False
        else:
            num+=1
    a_b_alive_num[1]=num
    if a_b_alive_num[0]==0 or a_b_alive_num[1]==0:
        return -1
    else:
        if x=='a':
            return random.randint(1,a_b_alive_num[0])
        elif x=='b':
            return random.randint(1,a_b_alive_num[1])
        else:
            return 0

def check(
        board_a=[[100,100,'n'],[5,5,'p'],[4,4,'s'],[3,3,'st'],[2,2,'p'],[7,700,'pt'],[6,6,'pst']],
        board_b=[[5,5,'p'],[2,2,'p'],[4,4,'s'],[100,100,'n'],[3,3,'st'],[7,700,'pt'],[6,6,'pst']],
        ):
    #strings discribing minions
    '''
          'n' -> nomal
          'p' -> poison
          's' -> shield
          't' -> taunt
         'ps' -> poison & shield
         'pt' -> poison & taunt
         'st' -> shield & taunt
        'pst' -> poison & shield & taunt
    '''
    a=[]
    b=[]
    for x in range(0,7):
        minion_list=board_a[x]
        if minion_list[2]=='n':
            a.append(Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='p':
            a.append(Poison_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='s':
            a.append(Shield_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='t':
            a.append(Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='ps':
            a.append(Poison_Shield_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='pt':
            a.append(Poison_Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='st':
            a.append(Shield_Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='pst':
            a.append(Poison_Shield_Taunt_Minion(minion_list[0],minion_list[1]))
    for x in range(0,7):
        minion_list=board_b[x]
        if minion_list[2]=='n':
            b.append(Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='p':
            b.append(Poison_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='s':
            b.append(Shield_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='t':
            b.append(Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='ps':
            b.append(Poison_Shield_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='pt':
            b.append(Poison_Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='st':
            b.append(Shield_Taunt_Minion(minion_list[0],minion_list[1]))
        elif minion_list[2]=='pst':
            b.append(Poison_Shield_Taunt_Minion(minion_list[0],minion_list[1]))

    a_b_alive_num=[len(a),len(b)]
    a_b_fighter_num=[0,0]
    poison_attack_addition(a,b)

    while True:
        random_num=get_random(a_b_alive_num,a,b,'b')
        if random_num==-1:
            break
        a[a_b_fighter_num[0]].attack(b,random_num)
        random_num=get_random(a_b_alive_num,a,b,'c')
        if random_num==-1:
            break
        a_b_fighter_num[0]+=1
            
        if a_b_fighter_num[0]>=7:
            a_b_fighter_num[0]=0
        while b[a_b_fighter_num[1]].live==False:
            a_b_fighter_num[1]+=1
            if a_b_fighter_num[1]>=7:
                a_b_fighter_num[1]=0
        random_num=get_random(a_b_alive_num,a,b,'a')
        if random_num==-1:
            break
        b[a_b_fighter_num[1]].attack(a,random_num)
        random_num=get_random(a_b_alive_num,a,b,'c')
        if random_num==-1:
            break
        a_b_fighter_num[1]+=1
        if a_b_fighter_num[1]>=7:
            a_b_fighter_num[1]=0
        while a[a_b_fighter_num[0]].live==False:
            a_b_fighter_num[0]+=1
            if a_b_fighter_num[0]>=7:
                a_b_fighter_num[0]=0

    if a_b_alive_num[0]>0:
        print('a win!')
        return a_b_alive_num[0]*1
    elif a_b_alive_num[1]>0:
        print('b win!')
        return a_b_alive_num[1]*(-1)
    else:
        print('tie!')
        return 0

pygame.init()
screen=pygame.display.set_mode((600,120))
pygame.display.set_caption('progress')
rect=pygame.Rect(10,10,0,100)
result=[0 for num in range(0,15)]
for num in range(0,7000):
    check_event()
    rect.width=int(580*(num+1)/7000)
    pygame.draw.rect(screen,(255,255,255),rect)
    result[check()+7]+=1
    pygame.display.update()
    
hist=Bar()
hist.title='a:[[100,100,n],[5,5,p],[4,4,s],[3,3,st],[2,2,p],[7,700,pt],[6,6,pst]]\n'+'b:[[5,5,p],[2,2,p],[4,4,s],[100,100,n],[3,3,st],[7,700,pt],[6,6,pst]]'

hist.add('result',result)
hist.render_to_file('result_1.svg')
    
