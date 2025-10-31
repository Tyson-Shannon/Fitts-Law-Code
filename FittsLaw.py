'''
HCI CIS 482-01 Fall 2025
Minnesota State University, Mankato
Fitts' Law Project
Hugo Albanese, Tyson Shannon, Julissa Paramo
'''

import tkinter as tk
import random

window = tk.Tk()

window.title("Fitts' Law Test")
window.state('zoomed')
canvas = tk.Canvas(window, bg="white")
canvas.pack(fill="both", expand=True)

#TEST PAGE

#deals with data after circle is clicked
def Circle_Clicked():
    print("Circle clicked!")
    canvas.delete("circle")

#creates clickable circle of varying sizes, distances, and directions
def Create_Circle(midStart):
    #--alter for test criteria later--
    
    #remove any previous circle buttons if needed
    canvas.delete("circle")

    #random size between 30–100 pixels
    size = random.randint(30, 100)

    #randomly choose left or right
    side = random.choice(["left", "right"])
    offset = 100  #distance in pixels from the centerof midStart to center of circle

    #get midStart's coordinates
    midStart.update_idletasks()
    start_x = midStart.winfo_x() + midStart.winfo_width() // 2
    start_y = midStart.winfo_y() + midStart.winfo_height() // 2

    #calculate circle position
    if side == "left":
        x = start_x - offset
    else:
        x = start_x + offset
    y = start_y

    #draw a circle
    circle = canvas.create_oval(
        x - size//2, y - size//2,
        x + size//2, y + size//2,
        fill="blue", outline=""
    )
    #detect clicks on circle
    canvas.tag_bind(circle, "<Button-1>", lambda e: Circle_Clicked())
    canvas.itemconfig(circle, tags=("circle",))  #tag for easy deletion next time

#red button to create new circle and center mouse
def Run_Test():
    global midStart_window
    midStart = tk.Button(canvas, text="X", bg="red", fg="white")
    midStart_window = canvas.create_window(
        window.winfo_width()//2, window.winfo_height()//2,
        window=midStart
    )
    midStart.config(command=lambda: Create_Circle(midStart))

#CONSENT PAGE

consentWords = """
Potential Risks 
The risks of participation are no greater than those experienced during daily life. Although the 
likelihood of discomfort is very unlikely, you are free to withdraw from participation at any 
point. 
Potential Benefits 
There are no tangible benefits of participation in this research. You might find that experiencing 
the intervention promotes a more positive outlook on your work life. However, the findings of 
this research could positively inform leadership practices. 
Compensation 
You will not receive any compensation for participation in this research. 
Voluntary Nature of the Study 
You are free to withdraw your consent to participate at any time. Your decision whether to 
participate will not affect your relationship with Minnesota State University, Mankato, and 
refusal to participate will involve no penalty or loss of benefits. 
Confidentiality 
All information obtained in this research project will be kept confidential by the research team and 
our professor. All information will be stored on this device and shared with our course professor. 
Your name will not be recorded. All other materials will be coded to protect your identity. All 
information will be deleted after submission and grading of this project.
"""

def I_Consent():
    canvas.delete(consentLabel_window)
    canvas.delete(consentButton_window)
    Run_Test()

def Show_Consent():
    global consentLabel_window, consentButton_window
    consentLabel = tk.Label(canvas, text=consentWords, wraplength=900, font=("Arial", 14))
    consentButton = tk.Button(canvas, text="I consent and agree to participate", command=I_Consent)
    #place in the center
    consentLabel_window = canvas.create_window(window.winfo_width()//2, window.winfo_height()//2 - 150, window=consentLabel)
    consentButton_window = canvas.create_window(window.winfo_width()//2, window.winfo_height()//2 + 150, window=consentButton)

#delay until window is rendered
window.after(100, Show_Consent)


window.mainloop()