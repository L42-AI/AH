import customtkinter
import tkinter as tk

frame = customtkinter.CTk()

# Create a canvas to hold the contents of the frame
canvas = customtkinter.CTkCanvas(frame)

frame1 = customtkinter.CTkFrame(canvas, height=200, width=200, fg_color='red')
frame2 = customtkinter.CTkFrame(canvas, height=300, width=200, fg_color='green')
frame3 = customtkinter.CTkFrame(canvas, height=200, width=100, fg_color='blue')
frame4 = customtkinter.CTkFrame(canvas, height=150, width=150, fg_color='black')

frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()

# Create a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview, troughcolor="red")

# Pack the canvas and scrollbar into the frame
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Set the canvas scroll region to encompass the entire frame
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Set the canvas widget to handle vertical scrolling using the scrollbar
canvas.configure(yscrollcommand=scrollbar.set(first=1, last=20))

frame.mainloop()
