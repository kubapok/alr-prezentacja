import tkinter as tk

state = 'broadcasting'
b_string = 'BROADCASTING NOW \n click to listen'
l_string = '  LISTENING NOW  \nclick to broadcast'

import client_logic


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.state_button = tk.Button(self)
        self.state_button["text"] = state
        self.state_button["command"] = None#self.change_state
        self.state_button.pack(side="top")
        self.state_button["height"] = 3
        self.state_button["width"] = 20
        self.state_button["bg"] = 'red'


        self.quit = tk.Button(self, text="QUIT", bg="brown4",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def change_state(self, command):
        state = command
        if state == 'listen':
            self.state_button["text"] = '  LISTENING NOW  \nclick to broadcast'
            self.state_button["bg"] = 'forest green'
            self.state_button["activebackground"]= 'green yellow'
        elif state == 'broadcast':
            self.state_button["text"] = b_string = 'BROADCASTING NOW \n click to listen'
            self.state_button["bg"] = 'red'
            self.state_button["activebackground"]= 'IndianRed1'
        else:
            print('sth bad happend')

root = tk.Tk()
root.minsize(width=300, height=300)
root.maxsize(width=300, height=300)
app = Application(master=root)


while True:
    command = client_logic.action('listen')
    app.change_state(command)
    app.update_idletasks()
    app.update()
