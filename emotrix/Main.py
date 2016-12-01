import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from RawData import RawData
from HeadsetEmotiv import HeadsetEmotiv

fig1 = plt.figure(1)
ax1 = fig1.add_subplot(1,1,1)
raw = RawData('user2.csv')
blocks = raw.get_blocks_data()

class Main(object):
    def __init__(self):
        self.he = HeadsetEmotiv(5)

    def animate(self, i):
        ax1.clear()
        ax1.plot(self.he.f3.getAll(), "r")
        ax1.plot(self.he.f4.getAll(), "b")
        ax1.plot(self.he.af3.getAll(), "y")
        ax1.plot(self.he.af4.getAll(), "k")


    def show(self):
        self.he.start()
        ani = animation.FuncAnimation(fig1, self.animate, interval=10)
        plt.show()


main = Main()
main.show()

