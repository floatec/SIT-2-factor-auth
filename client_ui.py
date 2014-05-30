from Tkinter import *
from stoplight import Stoplight

class ClientUI:
    def __init__(self, client):
        self.client = client
        self.window = Tk()
        self.window.geometry("600x200")

        # server response field
        self.server_response = StringVar()
        self.server_response.set('Please enter your username and password.')
        self.response_field = Entry(self.window, state="readonly", textvariable=self.server_response, width="70")
        self.response_field.pack()
        self.response_field.grid(row=0, column=1)
        # username field
        self.user_label = Label(self.window, text="User")
        self.user_label.grid(row=1)
        self.user_entry = Entry(self.window, width=70)
        self.user_entry.grid(row=1, column=1)
        # password field
        self.pwd_label = Label(self.window, text="Password")
        self.pwd_label.grid(row=2)
        self.pwd_entry = Entry(self.window, width=70, show='*')
        self.pwd_entry.bind("<Return>", lambda event: self.next())
        self.pwd_entry.grid(row=2, column=1)

        # tmp password
        self.second_pw = Label(self.window, text="2. Password")
        self.second_pw_entry = Entry(self.window, width="70", show='*')
        self.second_pw_entry.bind("<Return>", lambda event: self.send_2nd_pwd())
        self.button_send_pwd = Button(self.window, text='Send', command=self.send_2nd_pwd)
        self.second_factor = ''

        # stoplight
        self.stoplight = Stoplight('red')
        self.frame_stoplight = Frame(master=self.window, background='darkgray')
        self.frame_stoplight.place(x=500, y=20, width=40, height=100)
        # Label red light
        self.label_red = Label(master=self.frame_stoplight, background='gray')
        self.label_red.place(x=10, y=10, width=20, height=20)
        # yellow light
        self.label_yellow = Label(master=self.frame_stoplight, background='gray')
        self.label_yellow.place(x=10, y=40, width=20, height=20)
        # green  light
        self.label_green = Label(master=self.frame_stoplight, background='gray')
        self.label_green.place(x=10, y=70, width=20, height=20)
        # lamp display update
        (lamp_red, lamp_yellow, lamp_green) = self.stoplight.get_lamps()
        self.update_display(lamp_red, lamp_yellow, lamp_green)

        # buttons
        self.button_quit = Button(self.window, text='Quit', command=self.window.quit)
        self.button_quit.grid(row=3, column=0, sticky=W, pady=1)
        self.button_next = Button(self.window, text='next', command=self.next)
        self.button_next.grid(row=3, column=1, sticky=W, pady=1)

        self.window.mainloop()

    def next(self):
        username = self.user_entry.get()
        password = self.pwd_entry.get()
        success = self.client.login(username, password)
        if not success:
            self.button_next.destroy()
            self.server_response.set("Could not find user with this password. Quit and try again, please!")
            return

        self.button_next.destroy()

        #self.response_field = Entry(self.window, state="readonly", textvariable=self.server_response, width="70")
        #self.response_field.grid(row=0, column=1)
        self.server_response.set("Please enter a temporary password.")

        self.second_pw = Label(self.window, text="2. Password")
        self.second_pw.grid(row=1)
        #self.second_pw_entry = Entry(self.window, width="70", show='*')
        self.second_pw_entry.grid(row=1, column=1)

        self.update_display(False, True, False)
        #self.button_send_pwd = Button(self.window, text='Send', command=self.send_2nd_pwd))
        self.button_send_pwd.grid(row=2, column=1, sticky=W, pady=1)
        self.button_quit.grid(row=2, column=0, sticky=W, pady=1)
        self.user_label.destroy()
        self.user_entry.destroy()
        self.pwd_entry.destroy()
        self.pwd_label.destroy()

    def send_2nd_pwd(self):
        tmp_pwd = self.second_pw_entry.get()
        msg = self.client.send_tmp_pwd(tmp_pwd)
        if not msg:
            return
        self.server_response.set("Enter this code on our website using the temporary password: " + msg)
        self.response_field.update()
        self.button_send_pwd.destroy()
        self.second_pw_entry.destroy()
        self.second_pw.destroy()
        if self.client.wait_for_authentication():
            self.update_display(False, False, True)
            self.server_response.set("You have authenticated yourself successfully!")
        else:
            self.update_display(True, False, False)
            self.server_response.set("Authentication failed!")

    def update_display(self, lamp_red, lamp_yellow, lamp_green):
        if lamp_red:
            self.label_red.config(background='red')
        else:
            self.label_red.config(background='gray')
        if lamp_yellow:
            self.label_yellow.config(background='yellow')
        else:
            self.label_yellow.config(background='gray')
        if lamp_green:
            self.label_green.config(background='green')
        else:
            self.label_green.config(background='gray')