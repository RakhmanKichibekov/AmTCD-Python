import tkinter as tk
from tkinter import filedialog, messagebox
import configparser


class AmTCD(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Блокнот AmTCD")
        self.pack()
        self.create_widgets()
        self.filename = None
        self.text_widget = None
        self.create_widgets()

    def create_widgets(self):
        self.key_label = tk.Label(self, text="Личный ключ:", bg="darkolivegreen2")
        self.key_label.grid(row=0, column=0)
        self.key_entry = tk.Entry(self, show="*", bg="pale green")
        self.key_entry.grid(row=0, column=1)
        self.save_key_button = tk.Button(self, text="Сохранить ключ", command=self.save_key, bg="darkolivegreen1")
        self.save_key_button.grid(row=0, column=2)
        self.text_label = tk.Label(self, text="Текст:", bg="darkolivegreen2")
        self.text_label.grid(row=1, column=0)
        self.text_box = tk.Text(self, bg="pale green")
        self.text_box.grid(row=2, column=0, columnspan=3)
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0, bg="darkolivegreen1")
        filemenu.add_command(label="Создать файл", command=self.create_file)
        filemenu.add_command(label="Открыть файл", command=self.open_file)
        filemenu.add_command(label="Сохранить файл", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label='Выход', command=self.exit_application)
        menubar.add_cascade(label="Файл", menu=filemenu)
        menu2 = tk.Menu(menubar, tearoff=0, bg="darkolivegreen1")
        menubar.add_cascade(label="Правка", menu=menu2)
        menu2.add_command(label="Копировать", command=self.copy_text)
        menu2.add_command(label="Вставить", command=self.paste_text)
        menu2.add_separator()
        menu2.add_command(label="Параметры...", accelerator="Ctrl+S", command=self.change_theme)
        helpmenu = tk.Menu(menubar, tearoff=0, bg="darkolivegreen1")
        helpmenu.add_command(label="Справка", command=self.show_help)
        helpmenu.add_separator()
        helpmenu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Помощь", menu=helpmenu)

    def change_theme(self):
        theme_choice = tk.StringVar(self.master)
        theme_choice.set('default')
        themes = ['default', 'dark', 'light', 'blue']
        theme_menu = tk.OptionMenu(self.master, theme_choice, *themes)
        theme_menu.pack()
        ok_button = tk.Button(self.master, text='OK', command=lambda: self.set_theme(theme_choice.get())).pack()

    def set_theme(self, theme_name):
        if theme_name == 'default':
            self.master.configure(background='SystemButtonFace').text_widget.configure(bg='white', fg='black')
        elif theme_name == 'dark':
            self.master.configure(background='gray').text_widget.configure(bg='black', fg='white')
        elif theme_name == 'light':
            self.master.configure(background='white').text_widget.configure(bg='white', fg='black')
        elif theme_name == 'blue':
            self.master.configure(background='blue').text_widget.configure(bg='white', fg='black')

    def copy_text(self, event=None):
        selected_text = self.text_box.selection_get()
        if selected_text:
            self.master.clipboard_clear().clipboard_append(selected_text)

    def paste_text(self, event=None):
        self.text_box.insert(tk.INSERT, self.master.clipboard_get())

    def exit_application(self, event=None):
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.master.destroy()

    def create_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
        if filename:
            config = configparser.ConfigParser()
            config["main"] = {"keyopen": "", "mess": ""}
            with open(filename, "w") as f:
                config.write(f)

    def open_file(self):
        filename = filedialog.askopenfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
        if filename:
            config = configparser.ConfigParser()
            config.read(filename)
            self.text_box.delete("1.0", tk.END).insert("1.0", self.xor_encrypt(config["main"]["mess"],
                                                                               int(self.key_entry.get())))

    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
            if not self.filename:
                return
        ciphertext = self.xor_encrypt(self.text_box.get("1.0", tk.END), self.key_entry.get())
        with open(self.filename, "w") as f:
            f.write("[main]\nkeyopen = {}\nmess = {}".format(self.key_entry.get(), ciphertext))

    def show_help(self):
        help_text = "Данная программа позволяет создавать, открывать и сохранять файлы с зашифрованным текстом с помощью XOR-шифрования.\n\n Чтобы создать новый файл, выберите в меню Файл пункт Создать файл.\n\nЧтобы открыть уже существующий файл, выберите в меню Файл пункт Открыть файл и выберите нужный файл в диалоговом окне.\n\nЧтобы сохранить изменения в открытом файле, выберите в меню Файл пункт Сохранить файл.\n\n" \
                    "Перед использованием программы необходимо ввести личный ключ, который будет использоваться для шифрования и расшифрования текста. Личный ключ можно сохранить, нажав на кнопку Сохранить ключ.\n\n" \
                    "Автор: Рахман Кичибеков"
        self.help_window = tk.Toplevel(self.master).title("Справка")
        self.help_text_box = tk.Text(self.help_window, wrap=tk.WORD, state=tk.DISABLED,
                                     bg="darkolivegreen2").pack().configure(state=tk.NORMAL).insert(tk.END,
                                                                                                    help_text).configure(
            state=tk.DISABLED)

    def show_about(self):
        about_text = "Блокнот AmTCD\nВерсия: 1.0\n\nАвтор: Рахман Кичибеков"
        tk.messagebox.showinfo(title="О программе", message=about_text)

    def save_key(self):
        config = configparser.ConfigParser()
        config["main"] = {"keyuser": self.key_entry.get()}
        with open("AmTCD.ini", "w") as f:
            config.write(f)

    def xor_encrypt(self, plaintext, key):
        ciphertext = ""
        for i in range(len(plaintext)):
            char = plaintext[i]
            key_c = str(key)[i % len(str(key))]
            ciphertext += chr(ord(char) ^ ord(key_c))
        return ciphertext


root = tk.Tk()
app = AmTCD(master=root)
app.config(bg='darkolivegreen2')
app.mainloop()
