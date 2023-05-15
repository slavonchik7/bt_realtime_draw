
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import SubplotParams
import functools
import math
import time
import serial
from ctypes import c_short
import sys
import struct




NUM_CHANNELS = 4    # число каналов, которые следует вывести
OX_NUM_POINTS = 100  #Число точек по оси Ox
REFRESH_RATE = 0.001  # частота обновления графиков (считывания с порта) milisecond

FILL_COLOR = 'b'  # цвет, которым означает наличие данных на графике
EMPTY_COLOR = 'w'  # цвет, которым означает отсутствие данных на графике

GRAPHS_SCALE = 0.45 # масштаб графиков на главном окне, чем меньше, тем ближе они будут расположены

SERIAL_NAME             = "COM10"
SERIAL_DATA_SIZE        = NUM_CHANNELS * 2
SERIAL_BLOCK_SIZE       = SERIAL_DATA_SIZE + 2



SERIAL_PCKT_HDR_HBYTE   = 0x10
SERIAL_PCKT_HDR_LBYTE   = 0x2
SERIAL_PCKT_HDR         = struct.unpack('h' * 1, bytes([SERIAL_PCKT_HDR_HBYTE, SERIAL_PCKT_HDR_LBYTE]))

# класс хранит информацию о точке на графике
class DrawPoint:
    def __init__(self, x_val, y_val, clr):
        self.x = x_val
        self.y = y_val
        self.color = clr

# класс хранит информацию о графике для канала
class ComChannel:
    
    OX_NAME = 'Ox'
    OY_NAME = 'Oy'

    OX_MAX = 4096
    OX_MIN = 0
    
    OY_MAX = 4096
    OY_MIN = 0


    def __init__(self, sfig, name, nrows, ncols, index, npoints):

        self.ox_values = list(range(0, self.OX_MAX))
        self.axs = sfig.add_subplot(nrows, ncols, index)
        self.name = name
        self.np = npoints
        self.data = [0] * self.OX_MAX

    def update(self, addpoints):
        del self.data[:len(addpoints)]
        self.data += addpoints
        self.__refresh_plt()

    def __refresh_plt(self):
        
        # очищаю график в текущем subplot
        self.axs.clear()
        
        # устанавливаю требуемы настройки
        self.axs.set_xlabel(self.OX_NAME)
        self.axs.set_ylabel(self.OY_NAME)
        self.axs.set_title(self.name)
        self.axs.set_xlim(self.OX_MIN, self.OX_MAX)
        self.axs.set_ylim(self.OY_MIN, self.OY_MAX)
        #print("x: " + str(len(self.ox_values)) + "y: " + str(len(self.data)))
        self.axs.plot(self.ox_values, self.data, color=FILL_COLOR)


def upper_square(num):
	# наибольший ближайший квадрат числа
	# беру корень от num и округляю до верхнего целого

	return math.ceil(math.sqrt(num))

def get_optimal_vertical_cell(num_graph):
	up_sq_num = upper_square(num_graph)

	# нахожу количество делений по вертикали
	for i in range(1, up_sq_num + 1):
		if i * up_sq_num >= num_graph:
			return i

def get_optimal_horizontal_cell(num_graph):
	# количество делений по горизонтали
	return upper_square(num_graph)



def serial_sync(srl):
    while (True):
        b = srl.read(1)
        if len(b) != 0:
            if int.from_bytes(b, sys.byteorder) == SERIAL_PCKT_HDR_HBYTE:
                b = srl.read(1)
                if len(b) != 0:
                    if int.from_bytes(b, sys.byteorder) == SERIAL_PCKT_HDR_LBYTE:
                        return bytes([SERIAL_PCKT_HDR_HBYTE, SERIAL_PCKT_HDR_LBYTE]) + srl.read(SERIAL_DATA_SIZE)

def serial_packet_read(srl):
    while (True):
        b = srl.read(1)
        if len(b) == 0:
            return  b
        else:
            if int.from_bytes(b, sys.byteorder) == SERIAL_PCKT_HDR_HBYTE:
                b = srl.read(1)
                if len(b) == 0:
                    return b
                else:
                    if int.from_bytes(b, sys.byteorder) == SERIAL_PCKT_HDR_LBYTE:
                        return srl.read(SERIAL_DATA_SIZE)


def byte_to_short(bytes):
    # преобрахование списка char в список short

    dbsize = int(len(bytes) / 2)
    arrsh = (c_short * dbsize)()
    
    for i in range(dbsize):
        arrsh[i] = (bytes[i*2]) | (bytes[i*2+1] << 8)

    return list(arrsh)

def serial_nread(srl, size):
    data = bytes([])
    while (size != 0):
        tmp = srl.read(size)
        data += tmp
        size -= len(tmp)

    return data

def serial_nread_sync(srl, size):

    data = serial_sync(srl)
    size -= len(data)
    #print("sync: " + str(len(data)))

    return data + serial_nread(srl, size)


def proc_serial_draw(frame, chnllist, srl):


    # читаю данные
    #data = byte_to_short(serial_packet_read(srl))
    #data = serial_packet_read(srl)
    #print("OK")
    packets_num = 300
    buf_size = SERIAL_BLOCK_SIZE * (packets_num)
    #data = srl.read(buf_size)

    data = serial_nread_sync(srl, buf_size)
    #packets_num = int(len(data) / SERIAL_BLOCK_SIZE)
    print(str(len(data)) + " | " + str(len(data) / SERIAL_BLOCK_SIZE) + " | " + str(len(data) / 2))
    data = list(struct.unpack('h' * int(len(data) / 2), data))
    #print("OK")
    #print("short data len "  + str(len(data)))

    #time.sleep(1)
    #print(data)
    #print(byte_to_short(data))
    #print(struct.unpack('h' * int(len(data) / 2), data)) #преобразовываю к типу short

    chlen = len(channels)
    newpoints = [[] for k in range(chlen)]

    for i in range(packets_num):
        for j in range(chlen):
            newpoints[j].append(data[i * int(SERIAL_BLOCK_SIZE / 2) + (j + 1)])
            #print(data[i * int(SERIAL_BLOCK_SIZE / 2) + (j + 1)])

    # добавляю точки ко всем графикам
    for i in range(chlen):
        chnllist[i].update(newpoints[i])

    #print("OK")


if __name__ == '__main__':

	# получаю разбиение графиков
    num_ver_cell = get_optimal_vertical_cell(NUM_CHANNELS)  
    num_hor_cell = get_optimal_horizontal_cell(NUM_CHANNELS)

    # создание основного окна графика 
    fig = plt.figure(subplotpars=SubplotParams(wspace=GRAPHS_SCALE, hspace=GRAPHS_SCALE))

    # открытие и настройка порта
    #print("start sync")
    ser = serial.Serial(SERIAL_NAME, baudrate=115200, timeout=0.1)
    serial_sync(ser)
    #print("sync OK")

    # заполенение информации о графиках каналов
    channels = []
    for i in range(1, NUM_CHANNELS + 1):
        channels.append(ComChannel(fig, "Channel " + str(i), num_hor_cell, num_ver_cell, i, OX_NUM_POINTS))

    """
    while(True):

        proc_serial_draw(0, channels, ser)
        time.sleep(1)
    """
    # запуск основного икла программы
    anim = animation.FuncAnimation(fig, functools.partial(proc_serial_draw, chnllist=channels, srl=ser), interval=REFRESH_RATE)
    plt.show()
