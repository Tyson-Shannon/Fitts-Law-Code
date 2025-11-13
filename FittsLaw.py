'''
HCI CIS 482-01 Fall 2025
Minnesota State University, Mankato
Fitts' Law Project
Hugo Albanese, Tyson Shannon, Julissa Paramo
'''
import tkinter as tk
import random
import os
import time
import csv

# Global variable
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
current_index = 0
dimension_liste = []
counter_label = None
start_time = None
result_file = None
current_block = 0
circle_active = False
click_started_in_circle = False

error_count = 0

window = tk.Tk()
window.title("Fitts' Law Test")
window.state('zoomed')  # full screen mode
canvas = tk.Canvas(window, bg="white")
canvas.pack(fill="both", expand=True)

#TEST PAGE

def log_trial(hit):
    global result_file, dimension_liste, current_index, start_time, error_count

    if current_index == 0: # result should not be logged yet here
        return
        # When the circle is clic it stop the time, then we do the differences to have the time
    end_time = time.time()
    elapsed_time = (end_time-start_time) * 1000 # millisecondes conversion
 
    # We print the result in the file, maybe we have to change the syntax to have an easier export
    distance = dimension_liste[current_index - 1][0]
    size = dimension_liste[current_index - 1][1]
    direction = dimension_liste[current_index - 1][2]

    # write each data column
    with open(result_file, "a", newline="") as f:
        writer= csv.writer(f)
        writer.writerow([current_block + 1, current_index, distance, size, direction, f"{elapsed_time:.2f}", error_count, hit])    
    
    start_time = None # reset for next trial logging
    error_count = 0

def register_error(event):
    global error_count, circle_active, click_started_in_circle
    if not circle_active:
        return
    
    # Check that we clic the circle
    items_at_click = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in items_at_click:
        tags = canvas.gettags(item)
        if "circle" in tags:
            return  # C'est le cercle, pas une erreur
    
    # Here it's that we clic outside of the circle
    error_count += 1
    click_started_in_circle = False  # Reset because outside of the circle
    print(f"Error! Total errors: {error_count}")

canvas.bind("<ButtonPress-1>", register_error) 

# Function to create a unique file for the result
def create_unique_file(name, extension=".csv"):
    file_name = name + extension
    counter = 1

    # As long as the file exists, the counter is incremented
    while os.path.exists(file_name):
        file_name = f"{name}_{counter}{extension}"
        counter += 1

    # Create new file
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Block", "Trial", "Distance", "Size", "Direction", "Time (ms)", "Errors", "Hit"])
    return file_name

#triggers the log trial method if a circle is clicked and resets canvas
def Circle_Clicked(event=None):
    global circle_active
    if not circle_active:
        return
    log_trial(hit=True)
    print("Circle clicked!")
    canvas.delete("circle")
    circle_active = False

def on_circle_press(event):
    global click_started_in_circle
    click_started_in_circle = True
    print("Pressed in circle")

def on_circle_release(event):
    global click_started_in_circle, error_count
    if not click_started_in_circle:
        return
    
    # Check that the cursor is still in the circle at the moment of release.
    circle_items = canvas.find_withtag("circle")
    if circle_items:
        x1, y1, x2, y2 = canvas.coords(circle_items[0])
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            Circle_Clicked()
            print("Released in circle - VALID")
        else:
            error_count += 1
            print("Released outside circle - INVALID")
    
    click_started_in_circle = False

canvas.bind("<ButtonRelease-1>", on_circle_release)

# function to update the counter in the top of the page
def Update_Counter():
    global counter_label
    counter_text = f"Test Block : {current_block + 1}\nTrial {current_index + 1} / {len(dimension_liste)}"
    if counter_label is None:
        # Label creation for the first time
        counter_label = tk.Label(canvas, text=counter_text, font=("Arial", 16), bg="white")
        canvas.create_window(window.winfo_width()//2, 30, window=counter_label)
    else:
        # text update
        counter_label.config(text=counter_text)

#creates clickable circle of varying sizes, distances, and directions
def Create_Circle(midStart):
    global current_index, dimension_liste, start_time, current_block, circle_active

    # if the user did not click the circle
    if circle_active:
        canvas.delete("circle")
        circle_active = False
        log_trial(hit=False)

    if(current_index == 0):
        dimension_liste = [(8,8,"left"),(8,4,"left"),(8,2,"left"),(8,1,"left"),(16,8,"left"),(16,4,"left"),(16,2,"left"),(16,1,"left"),(32,8,"left"),(32,4,"left"),(32,2,"left"),(32,1,"left"),(64,8,"left"),(64,4,"left"),(64,2,"left"),(64,1,"left"),(8,8,"right"),(8,4,"right"),(8,2,"right"),(8,1,"right"),(16,8,"right"),(16,4,"right"),(16,2,"right"),(16,1,"right"),(32,8,"right"),(32,4,"right"),(32,2,"right"),(32,1,"right"),(64,8,"right"),(64,4,"right"),(64,2,"right"),(64,1,"right")]
        random.shuffle(dimension_liste)
    
    if current_index > len(dimension_liste) - 1:
        print("Test completed")
        current_index = 0
        current_block += 1
        return
    
    if current_block == 10: # stop the test after 10 blocks of 32 trials have been run , exit message + user can close the program
        canvas.delete("all")
        final_message = f"You have successfully completed all 10 test blocks.\nYour Results have been written to the \"{result_file}\" file for data collection.\nThank you!"
        completion_label = tk.Label(canvas,text=final_message, font=("Arial", 16), bg="white")
        canvas.create_window(window.winfo_width()/2, window.winfo_height()//2-50, window=completion_label)
        return
    # update counter
    
    Update_Counter() 

    #remove any previous circle buttons if needed
    canvas.delete("circle")

    # First : A, distance from the center
    # Second : W, circle width
    # Third : left or right
    size = dimension_liste[current_index][1]*10
    side = dimension_liste[current_index][2]
    offset = dimension_liste[current_index][0]*10

    current_index +=1

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
    #canvas.tag_bind(circle, "<Button-1>", lambda e: Circle_Clicked())
    canvas.tag_bind(circle, "<ButtonPress-1>", on_circle_press)
    #canvas.tag_bind(circle, "<ButtonRelease-1>", on_circle_release)
    canvas.itemconfig(circle, tags=("circle",))  #tag for easy deletion next time

    circle_active = True
    start_time = time.time()

#red button to create new circle and center mouse
def Run_Test():
    global midStart_window, result_file

    # creation of a new file for each test
    result_file = create_unique_file("Fitts_Law_results")

    midStart = tk.Button(canvas, text="X", bg="red", fg="white")
    midStart_window = canvas.create_window(
        window.winfo_width()//2, window.winfo_height()//2,
        window=midStart
    )
    midStart.config(command=lambda: Create_Circle(midStart))

#CONSENT PAGE

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
