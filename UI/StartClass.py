import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.messagebox import askyesno
from ButyButton import HoverButton, HoverMenuButton
import Account
from PIL import Image, ImageTk


class start_page(Tk):

    def __init__(self, get_con, get_window, ID=-1):
        self.window = get_window
        self.con = get_con
        self.ID = ID
        self.activebg = "#f0f8ff"
        self.bg = "#f2f2f2"
        self.contentbg = "white"
        self.fg = "gray0"
        self.font = "Arial 16"
        self.font_sec = "Arial 14"
        self.font_thrd = "Arial 12"
        self.clear_screen(self.window)
        self.name = self.con.cursor().execute("select name from User where id = " + str(ID)).fetchone()
        if self.name:
            self.name = self.name[0]
        self.name_label = Label(self.window, text=self.name, font="Arial 10", bg=self.contentbg)
        self.name_label.place(relx=0.937, rely=0.05, anchor=SE)

        self.content = Frame(self.window, bg=self.contentbg, width=self.window.winfo_width(),
                             height=self.window.winfo_height())
        self.main()

        # ---------------------------------------------
        # --------------------МЕНЮ---------------------
        # ---------------------------------------------

        self.menuButton = HoverMenuButton(self.window, text="Меню", activebackground=self.activebg,
                                          direction=LEFT, bg=self.bg)
        self.menuButton.menu = Menu(self.menuButton, tearoff=0, activebackground=self.activebg,
                                    activeforeground=self.fg)
        self.menuButton["menu"] = self.menuButton.menu

        self.menuButton.menu.add_command(label="Главная", command=self.main)
        self.menuButton.menu.add_command(label="Рейтинг", command=self.rating)

        if self.ID < 0:
            self.menuButton.menu.add_command(label="Вход", command=self.login)
            self.menuButton.place(relx=0.9, rely=0.05)
        else:
            self.menuButton.menu.add_command(label="Личный кабинет", command=lambda id=self.ID: self.personal_acc(id))
            self.menuButton.menu.add_command(label="Список стилей", command=self.style_list)
            self.menuButton.menu.add_command(label="Выход", command=self.exit)
            self.menuButton.place(relx=0.9, rely=0.05)


        # -------------------------------------------------------
        # -------------------------------------------------------
        # -----------------------РЕЙТИНГ-------------------------
        # -------------------------------------------------------
        # -------------------------------------------------------

    def rating(self):
        self.clear_screen(self.content)

        def change_stylies():
            values = self.con.cursor().execute(
                'select distinct name, id from Style join Style_Team_Champ on Style.id = id_style '
                'where id_champ = ' + str(self.year_choice.current())).fetchall()
            self.values_dict = {}
            self.values_dict.clear()
            for i in range(len(values)):
                self.values_dict[values[i][0]] = values[i][1]
                values[i] = values[i][0]

            self.style_choice["values"] = values
            self.style_choice.set("")
            if self.style_choice["values"]:
                self.style_choice.current(0)
                self.stage_choice.current(0)
                rate_list()

        def change_stylies_event(event):
            change_stylies()

        # ---------------------------------------------
        # ------------ВЫБОР ГОДА ЧЕМПИОНАТА------------
        # ---------------------------------------------

        self.years = tuple(self.con.cursor().execute('select year from championship').fetchall())
        self.year_choice = Combobox(self.content, values=self.years, state='readonly')
        self.year_choice.bind("<<ComboboxSelected>>", change_stylies_event)
        self.year_choice.place(relx=0.1, rely=0.1)
        self.year_choice.current(len(self.years) - 1)

        def rate_list():
            try:
                self.team_rate_list = []
                self.team_rate_list = self.con.cursor().execute('select id_team, name, avg(mark) from Ratings '
                                                                'join Team on id_team = id '
                                                                'where id_champ = ' + str(self.year_choice.current()) +
                                                                ' and id_style = ' + str(
                    self.values_dict[self.style_choice.get()]) +
                                                                ' and stage = ' + str(self.stage_choice.current()) +
                                                                ' group by id_team order by 3 desc').fetchall()

                rate_draw()
            except KeyError:
                for i in self.rate_list_frame_pack.pack_slaves():
                    i.pack_forget()

        def rate_list_event(event):
            rate_list()

        self.style_choice = Combobox(self.content, values=[], state='readonly')
        self.style_choice.bind("<<ComboboxSelected>>", rate_list_event)
        self.style_choice.place(relx=0.1, rely=0.15)

        self.stage_choice = Combobox(self.content, values=["отборочный тур", "финал"], state='readonly')
        self.stage_choice.bind("<<ComboboxSelected>>", rate_list_event)
        self.stage_choice.place(relx=0.1, rely=0.2)
        self.team_rate_list = []
        self.rate_list_teams = []
        self.rate_list_frame = Frame(master=self.content)
        self.rate_list_frame_pack = Frame(master=self.rate_list_frame)

        def rate_draw():
            print(self.team_rate_list)
            width = 400
            height = 200
            for i in self.rate_list_frame_pack.pack_slaves():
                i.pack_forget()
            self.rate_list_frame_scroll = self.canvas_scroll(width, height, self.rate_list_frame_pack)
            self.rate_list_teams = []
            for i in range(len(self.team_rate_list)):
                self.rate_list_teams.append(
                    [Label(master=self.rate_list_frame_scroll, text=str(i + 1), bg=self.contentbg, width=4),
                     Label(master=self.rate_list_frame_scroll, text=self.team_rate_list[i][1].rjust(30),
                           bg=self.contentbg, width=30),
                     Label(master=self.rate_list_frame_scroll, text=self.team_rate_list[i][2], bg=self.contentbg,
                           width=4, anchor=E)])

            for i in range(len(self.rate_list_teams)):
                self.rate_list_teams[i][0].grid(row=i, column=0)
                self.rate_list_teams[i][1].grid(row=i, column=1)
                self.rate_list_teams[i][2].grid(row=i, column=2)
            self.rate_list_frame_pack.pack()
            self.rate_list_frame.place(relx=0.3, rely=0.1)

        change_stylies()
        rate_draw()
        self.content.place(x=0, y=0)

        # -------------------------------------------------------
        # -------------------------------------------------------
        # -------------------ГЛАВНАЯ СТРАНИЦА--------------------
        # -------------------------------------------------------
        # -------------------------------------------------------

    def main(self):
        self.clear_screen(self.content)
        self.last_chemp_description = Text(self.content, height=7, width=70, font=self.font, wrap=WORD, bd=0)
        self.last_chemp_description.insert(1.0, self.con.cursor().execute(
            "select description from Championship order by year DESC").fetchone()[0])
        self.last_chemp_description.configure(state="disabled")
        self.last_chemp_description.place(relx=0.02, rely=0.1)
        self.canvas = tkinter.Canvas(self.window, height=400, width=1256)
        self.image = Image.open("../IMAGES/img.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.place(x=0, y=410, anchor='nw')

        def block_create(year_local, style_local, block):
            block_frame = Frame(self.content, bg=self.contentbg)
            champ_label = Label(block_frame, text=str(year_local) + " " + style_local, bg=self.contentbg,
                                font=self.font_sec)
            champ_label.grid(row=0, column=0, columnspan=3)
            for i in range(3):
                Label(block_frame, text=str(i + 1), width=2, bg=self.contentbg, font=self.font_thrd).grid(row=i + 1,
                                                                                                         column=0)
                Label(block_frame, text=block[i][1], width=18, bg=self.contentbg, font=self.font_thrd).grid(row=i + 1,
                                                                                                           column=1)
                Label(block_frame, text=str(block[i][2]), width=2, bg=self.contentbg, font=self.font_thrd).grid(
                    row=i + 1, column=2)
            return block_frame

        def block(ID_champ, ID_style):
            return self.con.cursor().execute('select id_team, name, avg(mark) from Ratings '
                                             'join Team on id_team = id '
                                             'where id_champ = ' + str(ID_champ) +
                                             ' and id_style = ' + str(ID_style) +
                                             ' and stage = 1'
                                             ' group by id_team order by 3 desc ').fetchmany(3)

        firstblock = block(0, 1)
        print(firstblock)
        year = self.con.cursor().execute('select year from Championship where id = 0').fetchone()
        style = self.con.cursor().execute('select name from Style where id = 1').fetchone()
        self.firstblock_frame = block_create(year[0], style[0], firstblock)
        self.firstblock_frame.place(relx=0.02, rely=0.3)

        secondblock = block(0, 2)
        year = self.con.cursor().execute('select year from Championship where id = 0').fetchone()
        style = self.con.cursor().execute('select name from Style where id = 2').fetchone()
        self.firstblock_frame = block_create(year[0], style[0], secondblock)
        self.firstblock_frame.place(relx=0.25, rely=0.3)

        thirdblock = block(1, 3)
        year = self.con.cursor().execute('select year from Championship where id = 1').fetchone()
        style = self.con.cursor().execute('select name from Style where id = 3').fetchone()
        self.firstblock_frame = block_create(year[0], style[0], thirdblock)
        self.firstblock_frame.place(relx=0.55, rely=0.3)

        fourblock = block(2, 0)
        year = self.con.cursor().execute('select year from Championship where id = 2').fetchone()
        style = self.con.cursor().execute('select name from Style where id = 0').fetchone()
        self.firstblock_frame = block_create(year[0], style[0], fourblock)
        self.firstblock_frame.place(relx=0.78, rely=0.3)

        self.content.place(x=0, y=0)

    def personal_acc(self, id):
        self.clear_screen(self.content)

        name = self.con.cursor().execute("select name from User where id = " + str(self.ID)).fetchone()[0]
        name_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=30, height=1)
        if name:
            name_label.insert(1.0, name)
        name_label.configure(state='disabled')
        name_label.place(relx=0.05, rely=0.1)
        name_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='Имя (фамилия)')
        name_labe.place(relx=0.05, rely=0.055)

        email = self.con.cursor().execute("select email from User where id = " + str(self.ID)).fetchone()[0]
        email_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=30, height=1)
        if email:
            email_label.insert(1.0, email)
        email_label.configure(state='disabled')
        email_label.place(relx=0.05, rely=0.2)
        email_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='Почта')
        email_labe.place(relx=0.05, rely=0.155)

        phone = self.con.cursor().execute("select phone from User where id = " + str(self.ID)).fetchone()[0]
        phone_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=30, height=1)
        if phone:
            phone_label.insert(1.0, phone)
        phone_label.configure(state='disabled')
        phone_label.place(relx=0.05, rely=0.3)
        phone_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='Телефон')
        phone_labe.place(relx=0.05, rely=0.255)

        descr = self.con.cursor().execute("select description from User where id = " + str(self.ID)).fetchone()[0]
        descr_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=40, height=4, wrap=WORD)
        if descr:
            descr_label.insert(1.0, descr)
        descr_label.configure(state='disabled')
        descr_label.place(relx=0.45, rely=0.1)
        descr_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='О себе')
        descr_labe.place(relx=0.45, rely=0.055)

        age = self.con.cursor().execute("select age from User where id = " + str(self.ID)).fetchone()[0]
        age_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=8, height=1, wrap=WORD)
        if age:
            age_label.insert(1.0, age)
        age_label.configure(state='disabled')
        age_label.place(relx=0.05, rely=0.4)
        age_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='Возраст')
        age_labe.place(relx=0.05, rely=0.355)

        country = self.con.cursor().execute("select country from User where id = " + str(self.ID)).fetchone()[0]
        country_label = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=18, height=1, wrap=WORD)
        if country:
            country_label.insert(1.0, country)
        country_label.configure(state='disabled')
        country_label.place(relx=0.15, rely=0.4)
        country_labe = Label(master=self.content, font=self.font_sec, bg=self.contentbg, text='Страна')
        country_labe.place(relx=0.15, rely=0.355)

        def change():
            name_label.configure(state='normal')
            email_label.configure(state='normal')
            phone_label.configure(state='normal')
            descr_label.configure(state='normal')
            age_label.configure(state='normal')
            country_label.configure(state='normal')

        def save():
            name_label.configure(state='disabled')
            email_label.configure(state='disabled')
            phone_label.configure(state='disabled')
            descr_label.configure(state='disabled')
            age_label.configure(state='disabled')
            country_label.configure(state='disabled')

        changeButt = HoverButton(master=self.content, text='Изменить\nинформацию', bg=self.bg,
                                 activebackground=self.activebg,
                                 fg=self.fg, command=change, font=self.font_sec, width=14)
        changeButt.place(relx=0.45, rely=0.3)

        self.content.place(x=0, y=0)

    def style_list(self):
        self.clear_screen(self.content)
        styleGrid = Frame(self.content)
        styleList = self.con.cursor().execute('select id, name, description from style').fetchall()
        self.current_style = 0

        styleName = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=38, height=1, wrap=WORD)
        styleName.place(relx=0.5, rely=0.1)
        styleDesc = Text(master=self.content, font=self.font_sec, bg=self.contentbg, width=38, height=4, wrap=WORD)
        styleDesc.place(relx=0.5, rely=0.2)

        def another_style(K=-1):
            styleName.delete(1.0, END)
            styleDesc.delete(1.0, END)
            if K == -1:
                styleName.insert(1.0, 'Название')
                styleDesc.insert(1.0, 'Описание стиля')
                self.current_style = -(len(styleList))
            else:
                styleName.insert(1.0, styleList[K][1])
                styleDesc.insert(1.0, styleList[K][2])
                self.current_style = K

        def del_style():
            if self.current_style >= 0:
                self.con.cursor().execute(
                    'delete from ratings where id_style = ' + str(styleList[self.current_style][0]))
                self.con.cursor().execute(
                    'delete from style_team_champ where id_style = ' + str(styleList[self.current_style][0]))
                self.con.cursor().execute('delete from style where id = ' + str(styleList[self.current_style][0]))
                self.con.commit()
            self.style_list()

        def change_style():
            if self.current_style >= 0:
                self.con.cursor().execute("update style set name = '" + styleName.get(1.0, END)[:-1] + "', "
                                                                                                       "description = '" + styleDesc.get(
                    1.0, END)[:-1] + "' where id = "
                                          + str(styleList[self.current_style][0]))
            else:
                self.con.cursor().execute("insert into style values(" + str(-self.current_style) + ", '"
                                          + styleName.get(1.0, END)[:-1] + "', '" + styleDesc.get(1.0, END)[:-1] + "')")
            self.con.commit()
            self.style_list()

        style_btns = []
        for i in range(len(styleList)):
            style_btns.append(
                HoverButton(master=styleGrid, text=styleList[i][1], bg=self.bg, activebackground=self.activebg,
                            fg=self.fg, command=lambda K=i: another_style(K), font=self.font_thrd, width=40, height=1))
        style_btns.append(
            HoverButton(master=styleGrid, text='Добавить стиль', bg=self.bg, activebackground=self.activebg,
                        fg=self.fg, command=another_style, font=self.font_thrd, width=40, height=1))
        for i in range(len(styleList) + 1):
            style_btns[i].grid(row=i, column=0)

        another_style(0)
        styleGrid.place(relx=0.1, rely=0.1)
        DelButton = HoverButton(master=self.content, text='Удалить', bg=self.bg, activebackground=self.activebg,
                                fg=self.fg, command=del_style, font=self.font_thrd, width=14, height=2)
        ChangeButton = HoverButton(master=self.content, text='Сохранить\nИзменения', bg=self.bg,
                                   activebackground=self.activebg,
                                   fg=self.fg, command=change_style, font=self.font_thrd, width=14, height=2)
        DelButton.place(relx=0.5, rely=0.42)
        ChangeButton.place(relx=0.65, rely=0.42)

        self.content.place(x=0, y=0)

    def login(self):
        window = Account.Window(self.window, self.con)
        window.grab_set()

    def exit(self):
        exit_bool = askyesno(" ", "Вы действительно хотите выйти? ")
        if exit_bool:
            start_page(self.con, self.window)
        else:
            return

    #

    def clear_screen(self, screen):
        for i in screen.place_slaves():
            i.place_forget()

    def canvas_scroll(self, Width, Height, FRAME):

        def current_scroll(event):
            canvas_current.configure(scrollregion=canvas_current.bbox("all"), width=Width, height=Height)

        for i in FRAME.pack_slaves():
            i.pack_forget()
        canvas_current = Canvas(FRAME, bg=self.contentbg, highlightthickness=0)
        current_list = Frame(canvas_current, bg=self.contentbg)
        current_scrollbar = Scrollbar(FRAME, orient="vertical", command=canvas_current.yview)
        canvas_current.configure(yscrollcommand=current_scrollbar.set)
        current_scrollbar.pack(side='right', fill='y')
        canvas_current.pack(side='left')
        canvas_current.create_window((0, 0), window=current_list, anchor='nw')
        current_list.bind("<Configure>", current_scroll)
        return current_list
