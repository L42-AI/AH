import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1100}x{580}")

        figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self)
        chart_type.get_tk_widget().pack()
        df = df[['First Column','Second Column']].groupby('First Column').sum()
        df.plot(kind='Chart Type such as bar', legend=True, ax=ax)
        ax.set_title('The Title for your chart')




# https://datatofish.com/matplotlib-charts-tkinter-gui/