import Tkinter
from Main import Main

def funcion():
    main = Main()
    main.show()

root = Tkinter.Tk()
boton = Tkinter.Button(root, text="Ver", command=funcion)
boton.pack()
root.mainloop()