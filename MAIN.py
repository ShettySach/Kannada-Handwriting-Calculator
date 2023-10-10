#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
from keras.models import load_model
import cv2
import numpy as np

# Import libraries


# In[2]:


model=tf.keras.models.load_model('model_V2.h5')

# Load model


# In[3]:


kan=['೦','೧','೨','೩','೪','೫','೬','೭','೮','೯']

def eng2kan(s):
    r = ""
    for i in s:
        if i.isnumeric():
            r += kan[int(i)]
        else:
            r += i
    return r

eng2kan("0 1 2 3 4 5 6 7 8 9")


# In[4]:


def testing(img):
    img=cv2.bitwise_not(img)
    img=cv2.resize(img,(28,28))
    img=img.reshape(1,28,28,1)
    img=img.astype('float32')
    img=img/255.0

    return model.predict(img)

# Testing function


# In[5]:


width = 3500
height = 750

# Canvas height and width can be adjusted here


# In[6]:


def img_change():
    labimg = Image.open('Contours.png')
    labimg = ctk.CTkImage(dark_image = labimg, size = (width//5,height//5))
    image_label.configure(image=labimg)
    image_label.image = labimg
    
# Function to change image


# In[7]:


def num_to_sym(x):
    if x == 10:
        return '+'
    if x == 11:
        return '-'
    if x == 12:
        return '*'
    if x == 13:
        return '/'
    if x == 14:
        return '('
    if x == 15:
        return ')'
    if x == 16:
        return '.'
    else:
        return str(x)
    
# Function to change numbers to symbols
# The prediction returns 0-9 for numbers and 10-16 for symbols


# In[8]:


def solve_exp(preds):
    ans = ""
    for ind, acc in preds:
        ans += ind
        print(num_to_sym(ind) + " " + str(acc))
        
    try:
        eval(ans)
        fin = eval(ans)
        fin = str(float(f"{fin:.4f}"))
    
        txt.delete('1.0', ctk.END) # Delete prev expression
        sol.delete('1.0', ctk.END) # Delete prev calculations
    
        txt.insert(ctk.INSERT, "{}    [ {} ]".format(eng2kan(ans), ans))
        sol.insert(ctk.INSERT, "= {}    [ {} ]".format(eng2kan(fin), fin))
        
    except Exception:
        txt.delete('1.0', ctk.END) # Delete prev expression
        sol.delete('1.0', ctk.END) # Delete prev calculations
    
        txt.insert(ctk.INSERT, "{}".format(ans))
        sol.insert(ctk.INSERT, "Invalid expression")



# Function to print solution from expression string      


# In[9]:


red = (0, 0, 225)
green = (0, 230, 0)
blue = (225, 0, 0)

#colors


# In[10]:


import os

directory = os.getcwd()
imsave = directory+"\\imgs\\"

print("Images used by CNN to predict individual numbers are stored here: " + imsave)


# In[11]:


def mod():
    # Save canvas as image and read 
    image1.save('image.png')
    img = cv2.imread('image.png')

    # Add padding around the original image
    pad = 5
    h, w = img.shape[:2]
    im2 = ~(np.ones((h + pad * 2, w + pad * 2, 3), dtype=np.uint8))
    im2[pad:pad + h, pad:pad + w] = img[:]
    img = im2

    # Blur it to remove noise
    img = cv2.GaussianBlur(img, (5, 5), 5)

    # Gray and B/W version
    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw = cv2.threshold(im, 200, 255, cv2.THRESH_BINARY)[1]

    # Find contours (only external) and sort them by X position, left to right
    bw = cv2.bitwise_not(bw)
    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0] + cv2.boundingRect(x)[2])

    i = 0    
    preds = []
    
    
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        i = i + 1
        # Crop the region of interest
        cropped_img = im[y:y + h, x:x + w]

        # Case of '1' (add padding)
        if abs(h) > 1.25 * abs(w):
            pad = 3*(h//w)**3
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=255)

        # Case of '-' add padding)
        if abs(w) > 1.1 * abs(h):
            pad = 3*(w//h)**3
            cropped_img = cv2.copyMakeBorder(cropped_img, pad, pad, 0, 0, cv2.BORDER_CONSTANT, value=255)

        # Resize the cropped image to 28x28 pixels
        resized_img = cv2.resize(cropped_img, (28, 28))
        # Add 2-pixel padding
        padded_img = cv2.copyMakeBorder(resized_img, 6, 6, 6, 6, cv2.BORDER_CONSTANT, value=255)
        # Save individual contour images
        cv2.imwrite(imsave+'img_' + str(i) + '.png', padded_img)

        # Predict the image
        predi = testing(padded_img)
        ind = np.argmax(predi[0]) # Index of prediction
        acc = predi[0][ind]*100   # Accuracy of prediction
        acc = float(f"{acc:.2f}")
        
        preds.append((num_to_sym(ind), acc)) # Append to preds list

        # Draw rectangle borders, number/symbol and corresponding accuracy
        cv2.rectangle(img, (x, y), (x + w, y + h), green, 7)

        if y < 80:
            yim = y + h + 85
        else:
            yim = y - 25

        cv2.putText(img, f"{num_to_sym(ind)}", (x, yim), cv2.FONT_HERSHEY_SIMPLEX, 3, blue, 10)
        cv2.putText(img, f"{acc}%", (x+75, yim), cv2.FONT_HERSHEY_DUPLEX, 1.75, red, 3)

    cv2.imwrite('Contours.png', img)
    img_change()

    solve_exp(preds)


# In[12]:


def paint(event):
    d = 15
    x1, y1 = (event.x - d), (event.y - d)
    x2, y2 = (event.x + d), (event.y + d)
    canv.create_oval(x1, y1, x2, y2, fill="black",width=25)
    draw.line([x1, y1, x2, y2],fill="black",width=35)
    
    # Brush thickness, size etc. can be adjusted here


# In[13]:


def clear():
    canv.delete('all')
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255, 0))
    txt.delete('1.0', ctk.END)
    sol.delete('1.0', ctk.END)
        
    # Clears the canvas


# In[14]:


from PIL import ImageTk, Image, ImageDraw
import PIL
import customtkinter as ctk

# Canvas and GUI


# In[16]:


root = ctk.CTk()
root.resizable(0, 0)
root.title('HANDWRITING CALCULATOR')

# Canvas for drawing numbers
canv = ctk.CTkCanvas(root, width=width, height=height, bg='white')
canv.grid(row=0, column=0, columnspan=2, padx=10, pady=17)
canv.bind("<B1-Motion>", paint)

white = (255, 255, 255)
image1 = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image1)

your_font = "Bahnschrift" #You can change the font here

# Text boxes
text_font = ctk.CTkFont(family=your_font, size=25)
txt = ctk.CTkTextbox(root, exportselection=0,
              padx=10, pady=10, height=height//10, width=width//5, font=text_font)
txt.grid(row=2, column=0, padx=0, pady=3)

sol_font = ctk.CTkFont(family=your_font, size=30, weight = "bold")
sol = ctk.CTkTextbox(root, exportselection=0,
              padx=10, pady=10, height=height//10, width=width//5, font=sol_font, text_color='#3085ff')
sol.grid(row=3, column=0, padx=0, pady=3)

# Image box
labimg = Image.open("Blank.png")
labimg = ctk.CTkImage(dark_image = labimg, size = (width//5,height//5)) 

image_label = ctk.CTkLabel(root, image=labimg, text="")
image_label.grid(row=2, column=1, padx=10, pady=5, rowspan = 2)

# Buttons
button_font = ctk.CTkFont(family=your_font, size=15)
Pred = ctk.CTkButton(root, text="Calculate", command=mod, fg_color = '#0056C4', hover_color='#007dfe',font = button_font,
                    height = height//22.5)
Clr = ctk.CTkButton(root, text="Clear", command=clear, fg_color = '#B50000', hover_color='#dd0000', font = button_font,
                    height = height//22.5)

Pred.grid(row=1, column=0, padx=5, pady=1, sticky='ew')
Clr.grid(row=1, column=1, padx=5, pady=1, sticky='ew')

root.mainloop()

