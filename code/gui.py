# -*- coding: utf-8 -*-
"""
Making a basic GUI for messing around with different image functions in openCV
Authors: Hamza and Nick
"""
import cv2 as cv
import numpy as np  #Not used yet
import math         #Not used yet
import tkinter as tk
import tkinter.filedialog
import Information as info
from PIL import Image, ImageTk


#Class that handles the creation of the window and its components
class App:
    original_image = None
    mod_image = None
    selected = None
    panel_a = None
    panel_b = None
    path = None
    info_pane = None
    scale_a = None
    scale_b = None
    cb_invert = None
    cb_invert_val = None
    save_btn = None
    scale_frame = None
    mod_frame = None
    og_frame = None
    edu_frame = None

    def __init__(self, master):
        #Formatting the window
        master.geometry('{}x{}'.format(1200, 600))
        #Making the window manually  resizable
        master.resizable(True, True)
        master.title('OpenCV')

        #Configuring columns
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2,weight=2)

        #Configuring rows
        #master.rowconfigure(2,weight=2)

        # Function list ###
        functions = [
            'Resize',
            'Rotate',
            'Canny Edge Detection',
            'Thresholding'
        ]

        self.selected = tk.StringVar()
        self.selected.set('Select a Function')

        # Frames ###
        self.scale_frame = tk.LabelFrame(master, text='Function Options', padx=5, pady=5)
        self.scale_frame.grid(column=0, row=2, sticky='nw', padx=5, pady=5)
        func_frame = tk.LabelFrame(master, text='OpenCV Functions', padx=5,pady=5)
        func_frame.grid(column=0,row=1,sticky='nw',padx=5,pady=5)
        self.mod_frame = tk.LabelFrame(master, text='Modified Image', padx=5, pady=5)
        self.mod_frame.grid(column=1, row=2, padx=5, pady=5)
        self.og_frame = tk.LabelFrame(master, text='Original Image', padx=5, pady=5)
        self.og_frame.grid(column=1, row=0, padx=5, pady=5)
        self.edu_frame = tk.LabelFrame(master, text='Information', padx=5, pady=5)
        self.edu_frame.grid(column=2, row=2,sticky='nw', padx=5, pady=5)
        
        # Options Menu ###
        #optionmenu needs the * pointer in front of functions list to read them all separately
        options = tk.OptionMenu(func_frame, self.selected, *functions)
        options.grid(column=0, row=0,sticky='nw', padx=5, pady=5)

        # Buttons ###
        #button to select image
        upload_btn = tk.Button(master, text='Select an image', command=self.select_image, width=17)
        upload_btn.grid(column=0, row=0, sticky='nw', padx=8, pady=8)
        #Button to load menu selection
        load_btn = tk.Button(func_frame, text='Load Module', command=self.load_module, width=17)
        load_btn.grid(column=1, row=0, sticky='n', padx=5, pady=5)
        
        # Scales ###
        self.scale_a = tk.Scale(self.scale_frame, label='Scale A', from_=0, to=100, orient='horizontal')
        self.scale_a.grid(column=0, row=0, padx=5, pady=5)
        self.scale_b = tk.Scale(self.scale_frame, label='Scale B', from_=0, to=100, orient='horizontal')
        self.scale_b.grid(column=0, row=1, padx=5, pady=5)
        
        # Checkboxes ###
        self.cb_invert = tk.Checkbutton(self.scale_frame, text='Invert', onvalue=1, offvalue=0)
        self.cb_invert.grid(column=0, row=5, padx=5, pady=5)

        # Labels ###
        self.info_pane = tk.Label(self.edu_frame, text='Information about the algorithm will appear here!',
                                  wraplength=360, justify='left')
        self.info_pane.pack()

###############################################################################

    #A function for destroying children in the scaleFrame
    def destroy_children(self):
        for widget in self.scale_frame.winfo_children():
            widget.destroy()
        for widget in self.edu_frame.winfo_children():
            widget.destroy()

###############################################################################

    # A Function that acts as an elif ladder for the drop-down menu
    def load_module(self):
        selection = self.selected.get()
        if selection == 'Canny Edge Detection':
            self.destroy_children()
            self.ready_canny()
            self.canny(self.scale_a.get())
        elif selection == 'Thresholding':
            self.destroy_children()
            self.ready_thresh()
            self.threshold(self.scale_b.get())
        elif selection == 'Resize':
            self.destroy_children()
            self.ready_resize()
            self.resize(self.scale_a.get())
        elif selection == 'Rotate':
            self.destroy_children()
            self.ready_rotate()
            self.rotate(self.scale_a.get())
        else:
            pass

#=============================================================================

    #Function that queries user for the photo to be modified
    def select_image(self):
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
            self.original_image = img
            #convert to rgb for Pillow to read
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            #filling the panels with the selected image
            self.update_image(img, True)

#=============================================================================

    #A function that updates the image, whether it is original or modified
    def update_image(self, image, is_original):
        #Converting image to tkinter friendly format
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        #filling the panels with the selected image
        if is_original:
            if self.panel_a is None:
                self.panel_a = tk.Label(self.og_frame, image=image)
                self.panel_a.image = image
                self.panel_a.pack()
            else:
                self.panel_a.configure(image=image)
                self.panel_a.image = image
        else: 
            if self.panel_b is None:
                self.panel_b = tk.Label(self.mod_frame, image=image)
                self.panel_b.image = image
                self.panel_b.pack()
            else:
                self.panel_b.configure(image=image)
                self.panel_b.image = image

#=============================================================================

    #Function to save a new original image
    def save_image(self):
        self.original_image = self.mod_image
        img = cv.cvtColor(self.mod_image, cv.COLOR_BGR2RGB)
        self.update_image(img, True)

#=============================================================================

    #Function to ready the resize module
    def ready_resize(self):
        self.scale_a = tk.Scale(self.scale_frame, label='Height', from_=1, to=200,
                                orient='horizontal', command=self.resize)
        self.scale_a.set(100)
        self.scale_a.grid(column=0, row=0, padx=5, pady=5)
        self.scale_b = tk.Scale(self.scale_frame, label='Width', from_=1, to=200,
                                orient='horizontal', command=self.resize)
        self.scale_b.set(100)
        self.scale_b.grid(column=0, row=1, padx=5, pady=5)
        self.save_btn = tk.Button(self.scale_frame, text='Save Photo', command=self.save_image, width=17)
        self.save_btn.grid(column=0, row=2, padx=5, pady=5)
        self.info_pane = tk.Label(self.edu_frame, text=info.get_resize(), wraplength=360, justify='left')
        self.info_pane.pack()
        
#=============================================================================

    #Function that resizes the original image and saves it. 
    def resize(self, value):
        #Get scale pct
        pct_height = int(self.scale_a.get())
        pct_width = int(self.scale_b.get())
        sd_height = int(self.original_image.shape[0] * pct_height / 100)
        sd_width = int(self.original_image.shape[1] * pct_width / 100)
        print(sd_height)
        img = cv.resize(self.original_image, (sd_width, sd_height))
        self.mod_image = img
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.update_image(img, False)
        
###############################################################################

    #Function that readies Scale values and attributes for Canny manipulation
    def ready_canny(self):
        #Setting new scale values and showing them
        self.scale_a = tk.Scale(self.scale_frame, label='Threshold', from_=0, to=100,
                                orient='horizontal', command=self.canny)
        self.scale_a.grid(column=0, row=0, padx=5, pady=5)
        self.info_pane = tk.Label(self.edu_frame, text=info.get_canny(), wraplength=360, justify='left')
        self.info_pane.pack()

#=============================================================================

    #Function that allows the user to Canny the image to the Canny algorithm's specifications
    def canny(self, value):
        value = int(value)
        #Pull the original image
        img = self.original_image.copy()
        #Grayscale for canny filter
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #blur using 3,3 kernel
        blur = cv.blur(gray, (3,3))
        #high threshold is 3 times higher than low, as suggest by Canny
        canny = cv.Canny(blur, value, value*3, 3)
        self.update_image(canny, False)
        
###############################################################################

    #Function to ready scaleFrame for Thresholding functions
    def ready_thresh(self):
        #Setting new scale values and showing them
        self.scale_a = tk.Scale(self.scale_frame, label='Thresh Value', from_=0, to=255,
                                orient='horizontal', command=self.threshold)
        self.scale_a.set(50)
        self.scale_a.grid(column=0, row=0, padx=5, pady=5)
        self.scale_b = tk.Scale(self.scale_frame, label='Max Value', from_=0, to=255,
                                orient='horizontal', command=self.threshold)
        self.scale_b.set(150)
        self.scale_b.grid(column=0, row=1, padx=5, pady=5)
        self.cb_invert_val = tk.IntVar()
        self.cb_invert = tk.Checkbutton(self.scale_frame, text='Invert', onvalue=1, offvalue=0,
                                        variable=self.cb_invert_val, command=self.threshold(self.cb_invert_val.get()))
        self.cb_invert.grid(column=0, row=2, padx=5, pady=5)
        self.info_pane = tk.Label(self.edu_frame, text=info.get_threshold(), wraplength=360, justify='left')
        self.info_pane.pack()
        
#=============================================================================

    #Function that allows the user to Thresh the image
    def threshold(self, value):
        #Pull original image
        img = self.original_image.copy()
        # convert to grayscale
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #Grab Scale values since passing all at once will not work well
        thresh_val = self.scale_a.get()
        max_val = self.scale_b.get()
        #inversion isn't throwing the command  when the box is checked but it does work when sliding
        if self.cb_invert_val.get() == 1:
            invert = cv.THRESH_BINARY_INV
        else:
            invert = cv.THRESH_BINARY
            
        ret, thresh = cv.threshold(gray,thresh_val, max_val, invert)
        self.update_image(thresh, False)

###############################################################################

    #Function to ready scaleFrame for rotation
    def ready_rotate(self):
        self.scale_a = tk.Scale(self.scale_frame, label='Rotation', from_=0, to=360,
                                orient='horizontal', command=self.rotate)
        self.scale_a.grid(column=0, row=0, padx=5, pady=5)
        self.save_btn = tk.Button(self.scale_frame, text='Save Photo', command=self.save_image, width=17)
        self.save_btn.grid(column=0, row=1, padx=5, pady=5)
        self.info_pane = tk.Label(self.edu_frame, text=info.get_rotate(), wraplength=360, justify='left')
        self.info_pane.pack()
        
#=============================================================================

    #Function to rotate image
    def rotate(self, value):
        img = self.original_image.copy()
        rotation = int(self.scale_a.get())
        height, width = img.shape[:2]
        matrix = cv.getRotationMatrix2D((width/2, height/2), rotation, 1)
        rotated = cv.warpAffine(img, matrix, (width, height))
        self.mod_image = rotated
        rotated = cv.cvtColor(rotated, cv.COLOR_BGR2RGB)
        self.update_image(rotated, False)

###############################################################################


#This is essentially the public static void Main() section of our program.
#Initialize tkinter window
root = tk.Tk()
app = App(root)

#Starts the Main Loop for continuously displaying the tkinter window
root.mainloop()
