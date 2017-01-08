import tkinter as tk





class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.state = 'listen'
        self.request_state = 'listen'
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.state_button = tk.Button(self)
        self.state_button["text"] = self.state
        self.state_button["command"] = self.change_state_request
        self.state_button.pack(side="top")
        self.state_button["height"] = 3
        self.state_button["width"] = 20
        self.state_button["bg"] = 'red'


        self.quit = tk.Button(self, text="QUIT", bg="brown4",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def change_state_request(self,):
        print('AAAAAAA\n'*20)
        if self.state == 'listen':
            self.request_state = 'broadcast'
        elif self.state == 'broadcast':
            self.request_state = 'listen'
        else:
            print(self.request_state)
            assert False


    def set_state(self, command):
        if command == 'listen':
            self.state = 'listen'
            self.state_button["text"] = '  LISTENING NOW  \nclick to broadcast'
            self.state_button["bg"] = 'forest green'
            self.state_button["activebackground"]= 'green yellow'
        elif command == 'broadcast':
            self.state = 'broadcast'
            self.state_button["text"] = b_string = 'BROADCASTING NOW \n click to listen'
            self.state_button["bg"] = 'red'
            self.state_button["activebackground"]= 'IndianRed1'
        else:
            print('sth bad happend')
            assert False

root = tk.Tk()
root.minsize(width=300, height=300)
root.maxsize(width=300, height=300)
app = Application(master=root)


import client_logic
while True:
    print('I want to ', app.request_state)
    command = client_logic.action(app.request_state)
    app.request_state = command
    app.state = command
    app.set_state(command)
    app.update_idletasks()
    app.update()
