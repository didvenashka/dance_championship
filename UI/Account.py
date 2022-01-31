from tkinter import *
from tkinter.messagebox import showwarning, showinfo
import StartClass
from ButyButton import HoverButton

class Window(Toplevel):
    def __init__(self, parent, get_con):
        super().__init__(parent)
        self.geometry('800x600')
        self.con = get_con
        self.window = parent
        self.activebg = "#f0f8ff"
        self.bg = "#f2f2f2"
        self.contentbg = "white"
        self.fg = "gray0"
        self.font = "Arial 20"
        self.font_sec = "Arial 16"
        self.font_thrd = "Arial 12"
        self.configure(bg="white")
        self.resizable(width=False, height=False)
        self.welcome_page()

    def welcome_page(self):
        self.label = Label(master=self, bg=self.contentbg, fg=self.fg, font=self.font_sec,
                           text='Добрый день! \nДля доступа в личный кабинет \nвойдите или зарегистрируйтесь.\n\n')
        self.label.place(relx=0.5, rely=0.5, anchor=S, y=-50)

        self.frame_chose = Frame(master=self, bg="white")
        self.chose_login_btn = HoverButton(master=self.frame_chose, text='Вход', bg=self.bg,
                                           activebackground=self.activebg,
                                           fg=self.fg, command=self.clicked_login_chose, font=self.font_thrd, width=14)
        self.chose_login_btn.grid(row=0, column=0, columnspan=2, sticky=SE, pady=5)
        self.chose_register_btn = HoverButton(master=self.frame_chose, text='Регистрация', bg=self.bg,
                                              activebackground=self.activebg,
                                              fg=self.fg, command=self.clicked_register_chose, font=self.font_thrd,
                                              width=14)
        self.chose_register_btn.grid(row=1, column=0, columnspan=2, sticky=SE, pady=5)
        self.frame_chose.place(relx=0.5, rely=0.5, anchor=CENTER)

    # --------------------------------------
    # ---------------LOGIN------------------
    # --------------------------------------

    def clicked_login_chose(self):
        self.clear_screen()
        self.frame_login = Frame(master=self, bg="white")

        self.login_text = Label(master=self.frame_login, text="Логин", bg=self.contentbg, fg=self.fg, font=self.font_thrd)
        self.login_entry = Entry(master=self.frame_login)
        self.login_text.grid(row=0, column=0, sticky=W, pady=5)
        self.login_entry.grid(row=0, column=1, sticky=N, pady=5)
        self.password_text = Label(master=self.frame_login, text="Пароль", bg=self.contentbg, fg=self.fg, font=self.font_thrd)
        self.password_entry = Entry(master=self.frame_login)
        self.password_text.grid(row=1, column=0, sticky=W)
        self.password_entry.grid(row=1, column=1, sticky=N)
        self.login_btn = HoverButton(master=self.frame_login, text='Вход', bg=self.bg, activebackground=self.activebg,
                                     fg=self.fg, command=self.login_clicked, font=self.font_thrd, width=14)
        self.login_btn.grid(row=2, column=0, columnspan=2, sticky=SE, pady=5)

        self.back_btn = HoverButton(master=self.frame_login, text='Назад', bg=self.bg, activebackground=self.activebg,
                                    fg=self.fg, command=self.back_clicked, font=self.font_thrd, width=14)
        self.back_btn.grid(row=3, column=0, columnspan=2, sticky=SE, pady=5)

        self.frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.label = Label(master=self, bg=self.contentbg, font=self.font_sec, text='Добро пожаловать', fg=self.fg)
        self.label.place(relx=0.5, rely=0.5, anchor=S, y=-110)

    def login_clicked(self, login="", password=""):
        if not login and not password:
            login = self.login_entry.get()
            password = self.password_entry.get()
        print("login clicked", login, password)
        id = self.con.execute(
            "select id from User where login = '" + login + "' and password = '" + password + "'").fetchone()
        print(id)
        if id:
            self.clear_screen()
            StartClass.start_page(self.con, self.window, id[0])
            self.destroy()
        else:
            warn = 'Проверьте правильность введеных данных'
            showwarning('Внимание', warn)

    # --------------------------------------
    # -------------REGISTER-----------------
    # --------------------------------------

    def clicked_register_chose(self):
        self.clear_screen()
        self.frame_register = Frame(master=self, bg=self.contentbg)

        self.login_text = Label(master=self.frame_register, text="Логин", bg=self.contentbg, fg=self.fg, font=self.font_thrd,
                                width=18, anchor=W)
        self.login_entry = Entry(master=self.frame_register)
        self.login_text.grid(row=0, column=0, sticky=W, pady=2)
        self.login_entry.grid(row=0, column=1, sticky=N, pady=2)
        self.password_text = Label(master=self.frame_register, text="Пароль", bg=self.contentbg, fg=self.fg, font=self.font_thrd,
                                   width=18, anchor=W)
        self.password_entry = Entry(master=self.frame_register)
        self.password_text.grid(row=1, column=0, sticky=W, pady=2)
        self.password_entry.grid(row=1, column=1, sticky=N, pady=2)
        self.confirm_password_text = Label(master=self.frame_register, text="Повторите пароль", bg=self.contentbg, fg=self.fg,
                                           font=self.font_thrd, width=18, anchor=W)
        self.confirm_password_entry = Entry(master=self.frame_register)
        self.confirm_password_text.grid(row=2, column=0, sticky=W, pady=2)
        self.confirm_password_entry.grid(row=2, column=1, sticky=N, pady=2)
        self.register_btn = HoverButton(master=self.frame_register, text='Регистрация', bg=self.bg, activebackground=self.activebg,
                                        fg=self.fg, command=self.register_clicked, font=self.font_thrd, width=14)
        self.register_btn.grid(row=3, column=0, columnspan=2, sticky=SE, pady=2)

        self.back_btn = HoverButton(master=self.frame_register, text='Назад', bg=self.bg, activebackground=self.activebg,
                                    fg=self.fg, command=self.back_clicked, font=self.font_thrd, width=14)
        self.back_btn.grid(row=4, column=0, columnspan=2, sticky=SE, pady=5)

        self.frame_register.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.label = Label(master=self, bg=self.contentbg, font=self.font_sec, text='Добро пожаловать', fg=self.fg)
        self.label.place(relx=0.5, rely=0.5, anchor=S, y=-110)

    def register_clicked(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        password_c = self.confirm_password_entry.get()
        if (self.con.cursor().execute("select exists(select * from user where login = '" + login + "')")).fetchone()[0]:
            warn = 'Логин занят'
            showwarning('Внимение', warn)
        elif password != password_c:
            warn = 'Пароли не совпадают'
            showwarning('Внимение', warn)
        elif len(login) < 4 :
            warn = 'Убедитесь, что длина логина больше 3 символов'
            showwarning('Внимение', warn)
        elif len(password) < 4 :
            warn = 'Убедитесь, что длина пароля больше 3 символов'
            showwarning('Внимение', warn)
        elif not login.isalnum() or not password.isalnum():
            warn = 'Пожалуйста используйте только буквы и цифры'
            showwarning('Внимение', warn)
        else:
            id = self.con.cursor().execute("select max(id) from user").fetchone()[0] + 1
            self.con.cursor().execute("insert into user values( " + str(id) + ", '" + login + "', '" + password +
                                      "', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")
            self.con.commit()
            info = 'Регистрация успешна.\nНе забудьте заполнить информацию в личном кабинете!'
            showinfo('Спасибо', info)

            self.clear_screen()
            StartClass.start_page(self.con, self.window, id)
            self.destroy()


    def clear_screen(self):
        for i in self.place_slaves():
            i.place_forget()

    def back_clicked(self):
        self.clear_screen()
        self.welcome_page()