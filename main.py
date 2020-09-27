import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2 
import sys
import numpy
import os

stage = 0


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.Frame() 
        self.openButton()
        self.quitButton()
        self.textBox()
        self.start_button()
        self.next_button()
        self.back_button()

    def Frame(self): #สร้าง Frame ขึ้นมา
        self.MainFrame = tk.Frame(root, width=1000, height=700, borderwidth=5)
        self.LabelFrame = tk.Frame(self.MainFrame, width=300, height=700, relief='raised', borderwidth=5)
        self.openFrame = tk.Frame(self.LabelFrame,width=300, height=300)
        self.textboxFrame = tk.Frame(self.LabelFrame,width=300, height=400)
        self.imageFrame = tk.Frame(self.MainFrame, width=700, height=700, borderwidth=5)
        for frame in [self.MainFrame, self.LabelFrame, self.imageFrame]:
            frame.pack(side = "left")
            frame.pack_propagate(0)
        for frame in [self.openFrame,self.textboxFrame]:
            frame.pack(side = "top")
            frame.pack_propagate(0)

    def openButton(self):
        self.openButton= tk.Button(self.openFrame,text="Open Image",command = self.openButton_command)
        self.openButton.pack( side = "top")

    def openButton_command(self):
        global img
        global filename
        global stage
        self.printout("Opening Image...")
        filename = askopenfilename()
        stage = 0
        try:
            img.pack_forget()
            self.load_img = Image.open(filename)
            self.resized_img = self.load_img.resize((690,690))
            self.render = ImageTk.PhotoImage(self.resized_img)
            img = tk.Label(self.imageFrame, image=self.render)
            img.image = self.render
            img.pack()
            self.printout("Image opened!")

        except:
            self.load_img = Image.open(filename)
            self.resized_img = self.load_img.resize((690,690))
            self.render = ImageTk.PhotoImage(self.resized_img)
            img = tk.Label(self.imageFrame, image=self.render)
            img.image = self.render
            img.pack()
            self.printout("Image opened!")

    def quitButton(self):
        self.quit_button = tk.Button(self.openFrame,text ="Quit", command = self.master.destroy)
        self.quit_button.pack(side = "bottom")

    def textBox(self):
        self.textBox = tk.Text(self.textboxFrame,state = "disabled")
        self.textBox.pack()
        self.pl = PrintLogger(self.textBox)
        sys.stdout = self.pl

    def start_button(self):
        
        self.start_button = tk.Button(self.openFrame,text = "Start",command= self.start)
        self.start_button.pack(side = "top")
      

    def start(self):
        global filename
        global blur
        try:
            self.src = cv2.imread(filename,0)
            if numpy.shape(self.src) == ():
                self.printout("fail")
            else:
                blur = cv2.GaussianBlur(self.src,(5,5),0)
                try:
                    os.remove("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/1.jpg")
                except:
                    pass
                cv2.imwrite("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/1.jpg",blur)
                self.printout("blur save")

                gray = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)

                try:
                    os.remove("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/2.jpg")
                except:
                    pass
                cv2.imwrite("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/2.jpg",gray)
                self.printout("gray save")

                invert = cv2.bitwise_not(gray)

                try:
                    os.remove("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/3.jpg")
                except:
                    pass
                cv2.imwrite("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/3.jpg",invert)
                self.printout("invert save")

                kernel = numpy.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], numpy.uint8)
                gray = cv2.dilate(invert, kernel)
                self.image = gray
                try:
                    os.remove("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/4.jpg")
                except:
                    pass
                cv2.imwrite("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/4.jpg", gray)
                self.printout("dilate save")
        except:
            self.printout("Please open the image first")

    def next_button(self):
        self.next_button = tk.Button(self.openFrame,text = ">>",command= self.next_command)
        self.next_button.pack(side ="right")

    def next_command(self):
        global stage
        global img
        try:
            if stage >3:
                stage = 0
            stage +=1
            img.pack_forget()
            self.load_img = Image.open("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/{}.jpg".format(stage))
            self.resized_img = self.load_img.resize((690,690))
            self.render = ImageTk.PhotoImage(self.resized_img)
            img = tk.Label(self.imageFrame, image=self.render)
            img.image = self.render
            img.pack()
            self.printout("Image {} Opened".format(stage))
        except:
            self.printout("Please open the image first")


    def back_button(self):
        self.back_button = tk.Button(self.openFrame,text = "<<",command= self.back_command)
        self.back_button.pack(side ="left")

    def back_command(self):
        global stage
        global img
        try:
            if stage <=1:
                stage =5
            stage -=1
            img.pack_forget()
            self.load_img = Image.open("C:/Users/VAHAH/Desktop/project/sudoku solver/StagesIMG/{}.jpg".format(stage))
            self.resized_img = self.load_img.resize((690,690))
            self.render = ImageTk.PhotoImage(self.resized_img)
            img = tk.Label(self.imageFrame, image=self.render)
            img.image = self.render
            img.pack()
            self.printout("Image {} Opened".format(stage))
        except:
            self.printout("Please open the image first")


    def printout(self,text):
        self.textBox.configure(state = "normal")
        print(text)
        self.textBox.configure(state = "disabled")
        
class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass


root = tk.Tk()
App = Application(root)
root.geometry("1000x700")
root.resizable(0,0)
App.mainloop()
# import tkinter as tk
# import sys

# class PrintLogger(): # create file like object
#     def __init__(self, textbox): # pass reference to text widget
#         self.textbox = textbox # keep ref

#     def write(self, text):
#         self.textbox.insert(tk.END, text) # write text to textbox
#             # could also scroll to end of textbox here to make sure always visible

#     def flush(self): # needed for file like object
#         pass

# if __name__ == '__main__':
#     def do_something():
#         print('i did something')
#         root.after(1000, do_something)

#     root = tk.Tk()
#     t = tk.Text()
#     t.pack()
#     # create instance of file like object
#     pl = PrintLogger(t)

#     # replace sys.stdout with our object
#     sys.stdout = pl

#     root.after(1000, do_something)
#     root.mainloop()

# img.pack_forget()
# blur = cv.GaussianBlur(self.src,(5,5),0)
# b,g,r= cv.split(blur)
# self.img_blur = cv.merge((r,g,b))
# self.img_blur = Image.fromarray(self.img_blur)
# self.img_blur = self.img_blur.resize((690,690))
# self.render = ImageTk.PhotoImage(image=self.img_blur)
# img = tk.Label(self.imageFrame,image=self.render)
# img.image = self.render
# img.pack()
# self.printout("Blured!")