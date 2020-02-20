import random
import time

colors=[]

red=(211, 47, 47)
colors.append(red)

pink=(194, 24, 91)
colors.append(pink)

purple=(123, 31, 162)
colors.append(purple)

deep_purple=(81, 45, 168)
colors.append(deep_purple)

indigo=(48, 63, 159)
colors.append(indigo)

blue=(25, 118, 210)
colors.append(blue)

light_blue=(2, 136, 209)
colors.append(light_blue)

cyan=(0, 151, 167)
colors.append(cyan)

teal=(0, 121, 107)
colors.append(teal)

green=(56, 142, 60)
colors.append(green)

light_green=(104, 159, 56)
lime=(175, 180, 43)
yellow=(255,235,59)
amber=(255,160,0)
orange=(245,124,0)
deep_orange=(230,74,25)
brown=(93,64,55)
gray=(97,97,97)
blue_gray=(69,90,100)
black=(0,0,0)
white=(255,255,255)
c2=[light_green,lime,yellow,amber,orange,deep_orange,brown,gray,blue_gray,black,white]
colors=colors+c2
def random_color():
    num=random.randint(0,len(colors)-2)
    return colors[num]

