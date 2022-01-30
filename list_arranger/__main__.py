from __init__ import Achivements_widget
from tkinter import *
def main():
    root=Tk()
    achivment=Achivements_widget(root)
    achivment.pack(fill=BOTH,expand=YES)
    Button(root,text="add task",command=achivment.add_item).pack()
    Button(root,text="get taskes",command=lambda:print(list(achivment.get_keys()))).pack()
    root.mainloop()
if __name__=="__main__":
    main()