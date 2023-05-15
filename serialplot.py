import matplotlib.pyplot as plt
import matplotlib.animation as animation
from socket import *



VERTICAL_CELL   = 2
HORIZONTAL_CELL = 2

class Channel:
    
    def __init__(self, sfig, ox_num, nrows, ncols, index):
        self.data = [0] * ox_num
        self.axs = sfig.add_subplot(nrows, ncols, index)



OX_POINTS_NUM = 50
CHANNELS_NUM = 4
OX_RANGE = [0, OX_POINTS_NUM]
OY_RANGE = [0, 2**12]

ox_values = [i for i in range(OX_POINTS_NUM)]

channel_plts = []
channel_data = []
channel_axs  = []

#plt.ion()
fig = plt.figure()

for i in range(1, CHANNELS_NUM + 1):
    channel_data.append([0] * OX_POINTS_NUM) # cоздание списка на 0 элементов
    #plt.subplot(CHANNELS_NUM, CHANNELS_NUM, i)
    #a = fig.add_subplot(HORIZONTAL_CELL, VERTICAL_CELL, i)
    
    channel_axs.append(fig.add_subplot(HORIZONTAL_CELL, VERTICAL_CELL, i))
    #l, = plt.plot([0] * OX_POINTS_NUM)
    #channel_plts.append(l) # размещение графика канала в определённой части главного окна 


#plt.show()

udp_listen = socket(AF_INET, SOCK_DGRAM)
udp_listen.bind(("127.0.0.1", 4000))




def animat(arg):
    data = open('stock.txt', 'r').read()
    lines = data.split('\n')
    print(lines)
    xs = []
    ys = []

    for line in lines:
        x, y = line.split(',')
        xs.append(float(x))
        ys.append(float(y))

    #ax.clear()
    #ax.plot(xs, ys)

    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.title('Graphic realtime')


def read_block_data():
    
    msg = udp_listen.recvfrom(254)[0]
    chars = msg.decode()
    vlist = chars.split()

    return vlist

def proc_serial_draw(arg):

    values = read_block_data()
    for i in range(CHANNELS_NUM):
        channel_data[i].append(float(values[i]))
        del channel_data[i][0]

        channel_axs[i].clear()
        channel_axs[i].plot(ox_values, channel_data[i])
        
        #channel_plts[i].set_xdata([0] * OX_POINTS_NUM)
        #channel_plts[i].set_ydata([channel_data])
        #channel_plts[i].ylim([0, 1])
    
    #plt.ylim([0, 1])    
    #plt.draw()

    return



if __name__ == '__main__':
    anim = animation.FuncAnimation(fig, proc_serial_draw, interval=10)
    plt.show()























#==================================================================

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from socket import *






udp_listen = socket(AF_INET, SOCK_DGRAM)
udp_listen.bind(("127.0.0.1", 4000))





VERTICAL_CELL   = 2
HORIZONTAL_CELL = 2

NUM_CHANNELS = 4
OX_NUM_POINTS = 100

channels = []
fig = plt.figure()
ox_values = [i for i in range(OX_NUM_POINTS)]


class ComChannel:
    
    def __init__(self, sfig, name, nrows, ncols, index):
        self.data = [0] * OX_NUM_POINTS
        #self.axs = sfig.add_subplot(nrows, ncols, index)
        
        #axs = sfig.add_subplot(nrows, ncols, index)

        self.axs = sfig.add_subplot(nrows, ncols, index)
        self.cfig = sfig
        self.name = name
        self.nrows = nrows
        self.ncols = ncols
        self.pos = index
       # self.cplt = plt.plot()
        
        self.__refresh_plt()
        

    
    def update(self, y_val):
        self.data.append(y_val)
        del self.data[0]
    
    
    def __refresh_plt(self):
      #  self.cplt.remove()
        self.axs = self.cfig.add_subplot(self.nrows, self.ncols, self.pos)
        self.axs.remove()
        self.axs.plot(ox_values, self.data)
       # self.cplt.title(self.name)
        .xlabel("oX")
        self.cplt.ylabel("oY")
        self.cplt.grid(True)




#==================================================================