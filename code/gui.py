# -*- coding: utf-8 -*-
"""
Making a basic GUI for messing around with different image functions in openCV
Authors: Hamza and Nick
"""
import cv2 as cv
import numpy as np #Not used yet
import math        #Not used yet
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk

#Class that handles the creation of the window and its components
class App:
    originalImage = None
    modImage = None
    selected = None
    panelA = None
    panelB = None
    path = None
    scaleA = None
    scaleB = None
    cbInvert = None
    cbInvertVal = None
    saveBtn = None
    scaleFrame = None
    modFrame = None
    ogFrame = None
    
    
    def __init__(self, root):
        #Formatting the window
        root.geometry('{}x{}'.format(1200, 600))
        #Making the window manually  resizable
        root.resizable(True, True)
        root.title('OpenCV')

        #Configuring columns
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)

        ### Function list###
        functions = [
            'Resize',
            'Canny Edge Detection',
            'Thresholding'
        ]

        self.selected = tk.StringVar()
        self.selected.set('Select a Function')

        ### Frames ###
        self.scaleFrame = tk.LabelFrame(root, text='Function Options', padx=5,pady=5)
        self.scaleFrame.grid(column=0,row=2,sticky='nw',padx=5,pady=5)
        funcFrame = tk.LabelFrame(root, text='OpenCV Functions', padx=5,pady=5)
        funcFrame.grid(column=0,row=1,sticky='nw',padx=5,pady=5)
        self.modFrame = tk.LabelFrame(root,  text='Modified Image', padx=5,pady=5)
        self.modFrame.grid(column=1,row=2,padx=5,pady=5)
        self.ogFrame = tk.LabelFrame(root,  text='Original Image', padx=5,pady=5)
        self.ogFrame.grid(column=1,row=0,padx=5,pady=5)
        
        ### Options Menu ###
        #optionmenu needs the * pointer in front of functions list to read them all seperately
        options = tk.OptionMenu(funcFrame, self.selected, *functions)
        options.grid(column=0, row=0,sticky='nw', padx = 5, pady = 5)

        ### Buttons ###
        #button to select image
        uploadBtn = tk.Button(root, text='Select an image', command=self.selectImage, width = 17)
        uploadBtn.grid(column=0, row=0,sticky='nw',padx=8, pady=8)
        #Button to load menu selection
        loadBtn = tk.Button(funcFrame, text='Load Module', command=self.loadModule, width=17)
        loadBtn.grid(column=1,row=0,sticky='n',padx=5,pady=5)
        
        ### Scales ###
        self.scaleA = tk.Scale(self.scaleFrame, label='Scale A',from_=0,to=100,orient='horizontal')
        self.scaleA.grid(column=0,row=0,padx=5,pady=5)
        self.scaleB = tk.Scale(self.scaleFrame, label='Scale B', from_=0, to=100, orient='horizontal')
        self.scaleB.grid(column=0,row=1,padx=5,pady=5)
        
        ### Checkboxes ###
        self.cbInvert = tk.Checkbutton(self.scaleFrame, text='Invert', onvalue=1, offvalue=0)
        self.cbInvert.grid(column=0,row=5,padx=5,pady=5)

###############################################################################

    #A nothing function for trackbar creation
    #Can be deleted. Was only used for openCV trackbars, not tk scales
    def destroyChildren(self):
        for widget in self.scaleFrame.winfo_children():
            widget.destroy()        

###############################################################################

    # A Function that acts as an elif ladder for the drop-down menu
    def loadModule(self):
        selection = self.selected.get()
        if selection == 'Canny Edge Detection':
            self.destroyChildren()
            self.readyCanny()
            self.canny(self.scaleA.get())
        elif selection == 'Thresholding':
            self.destroyChildren()
            self.readyThresh()
            self.threshold(self.scaleB.get())
        elif selection == 'Resize':
            self.destroyChildren()
            self.readyResize()
            self.resize(self.scaleA.get())
        else:
            pass

#=============================================================================

    #Function that queries user for the photo to be modified
    def selectImage(self):
        #choosing the  path
        self.path = tkinter.filedialog.askopenfilename()
        if len(self.path) > 0:
            #reading the image from the chosen path
            img = cv.imread(self.path)

            #scaledown
            scale_percent = 60
            scaledown_height = int(img.shape[0] * scale_percent/100)
            scaledown_width = int(img.shape[1] * scale_percent/100)
            img = cv.resize(img, (scaledown_width, scaledown_height))
            self.originalImage = img
            #convert to rgb for Pillow to read
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            #filling the panels with the selected image
            self.updateImage(img, True)

#=============================================================================

    #A function that updates the image, whether it is original or modified
    def updateImage(self, image, isOriginal):
        #Converting image to tkinter friendly format
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        #filling the panels with the selected image
        if isOriginal:
            if self.panelA is None:
                self.panelA = tk.Label(self.ogFrame, image=image)
                self.panelA.image = image
                self.panelA.pack()
                self.panelA.grid(column=1,row=0,padx=5,pady=5)
            else:
                self.panelA.configure(image = image)
                self.panelA.image = image
        else: #PanelB isnt used yet because openCV currently creates all the new windows
            if self.panelB is None:
                self.panelB = tk.Label(self.modFrame, image=image)
                self.panelB.image = image
                self.panelB.pack()
                self.modFrame.grid(column=1,row=2,padx=5,pady=5)
            else:
                self.panelB.configure(image = image)
                self.panelB.image = image

#=============================================================================

    #Function to save a new original image
    def saveImage(self):
        self.originalImage = cv.cvtColor(self.modImage, cv.COLOR_BGR2RGB)
        self.updateImage(self.originalImage, True)

#=============================================================================

    #Function to ready the resize module
    def readyResize(self):
        self.scaleA = tk.Scale(self.scaleFrame, label='Height',from_=1, to=200, orient='horizontal', command=self.resize)
        self.scaleA.set(60)
        self.scaleA.grid(column=0,row=0,padx=5,pady=5)
        self.scaleB = tk.Scale(self.scaleFrame, label='Width', from_=1, to=200, orient='horizontal', command=self.resize)
        self.scaleB.set(30)
        self.scaleB.grid(column=0,row=1,padx=5,pady=5)
        self.saveBtn = tk.Button(self.scaleFrame, text='Save Photo', command=self.saveImage, width=17)
        self.saveBtn.grid(column=0, row=2, padx=5,pady=5)
        self.scaleFrame.grid(column=0,row=2,sticky='nw',padx=5,pady=5)
        
#=============================================================================

    #Function that resizes the original image and saves it. 
    def resize(self, value):
        #Get scale pct
        pctHeight = int(self.scaleA.get())
        pctWidth = int(self.scaleB.get())
        sdHeight = int(self.originalImage.shape[0] * pctHeight/100)
        sdWidth = int(self.originalImage.shape[1] * pctWidth/100)
        print(sdHeight)
        img = cv.resize(self.originalImage, (sdWidth, sdHeight))
        self.modImage = img
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.updateImage(img, False)
        
###############################################################################

    #Function that readies Scale values and attributes for Canny manipulation
    def readyCanny(self):
        #Setting new scale values and showing them
        self.scaleA = tk.Scale(self.scaleFrame, label='Threshold', from_=0, to=100, orient='horizontal', command=self.canny)
        self.scaleA.grid(column=0,row=0,padx=5,pady=5)
        self.scaleFrame.grid(column=0,row=2,sticky='nw',padx=5,pady=5)

#=============================================================================

    #Function that allows the user to Canny the image to the Canny algorithm's specifications
    def canny(self, value):
        value = int(value)
        #Pull the original image
        img = self.originalImage.copy()
        #Grayscale for canny filter
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #blur using 3,3 kernel
        blur = cv.blur(gray, (3,3))
        #high threshold is 3 times higher than low, as suggest by Canny
        canny = cv.Canny(blur, value, value*3, 3)
        self.updateImage(canny, False)
        
###############################################################################

    #Function to ready scaleFrame for Thresholding functions
    def readyThresh(self):
        #Setting new scale values and showing them
        self.scaleA = tk.Scale(self.scaleFrame, label='Thresh Value', from_=0, to=255, orient='horizontal', command=self.threshold)
        self.scaleA.set(50)
        self.scaleA.grid(column=0,row=0,padx=5,pady=5)
        self.scaleB = tk.Scale(self.scaleFrame, label='Max Value', from_=0,to=255, orient='horizontal', command=self.threshold)
        self.scaleB.set(150)
        self.scaleB.grid(column=0,row=1,padx=5,pady=5)
        self.cbInvertVal = tk.IntVar()
        self.cbInvert = tk.Checkbutton(self.scaleFrame, text='Invert', onvalue=1, offvalue=0, variable=self.cbInvertVal, command=self.threshold)
        self.cbInvert.grid(column=0,row=2,padx=5,pady=5)
        self.scaleFrame.grid(column=0,row=2,sticky='nw',padx=5,pady=5)
        
#=============================================================================

    #Function that allows the user to Thresh the image
    def threshold(self, value):
        #Pull original image
        img = self.originalImage
        # convert to grayscale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #Grab Scale values since passing all at once will not work well
        threshVal = self.scaleA.get()
        maxVal = self.scaleB.get()
        #inversion isnt throwing the command  when the box is checked but it does work when sliding
        if self.cbInvertVal.get() == 1:
            invert = cv.THRESH_BINARY_INV
        else:
            invert = cv.THRESH_BINARY
            
        ret, thresh = cv.threshold(gray,threshVal, maxVal, invert)
        self.updateImage(thresh, False)

###############################################################################

#This is essentially the public static void Main() section of our program.
#Initialize tkinter window
root = tk.Tk()
app = App(root)

#Starts the Main Loop for continuously displaying the tkinter window
root.mainloop()