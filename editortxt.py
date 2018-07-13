                                                #TEXT EDITOR


#IMPORT MODULE
from PIL import ImageTk
from tkinter import *
import os
import tkinter.filedialog
import tkinter.messagebox
from tkcolorpicker import askcolor



#CREATE A ROOT WINDOW AND GIVE TITLE TO THE WINDOW.
root = Tk()
TITLE = "Text Editor"
root.title(TITLE)
file_name = None
root.geometry('450x350')


#FUNCTIONALITY OF TEXT.
def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


#THEME FUNCTIONALITY.
def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(background=background_color, fg=foreground_color)



#ROOT ICON.
root.iconbitmap('icons_pi6_icon.ico')

# ICONS FOR MENU.

#1. FOR FILE MENU ICONS.
new_file_icon = PhotoImage(file='pics/new_file.gif')
open_file_icon = PhotoImage(file='pics/open_file.gif')
save_file_icon = PhotoImage(file='pics/save.gif')

#2. FOR EDIT MENU ICONS.
cut_icon = PhotoImage(file='pics/cut.gif')
copy_icon = PhotoImage(file='pics/copy.gif')
paste_icon = PhotoImage(file='pics/paste.gif')
undo_icon = PhotoImage(file='pics/undo.gif')
redo_icon = PhotoImage(file='pics/redo.gif')
find_icon = PhotoImage(file='pics/find_text.gif')


# FUNCTIONALITY OF FILE MENU.

#1.NEW FILE
def new_file(event=None):
    root.title("Text Editor")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()

#2.OPEN FILE
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),
                                                                    ("HTML", "*.html"), ("CSS", "*.css"),
                                                                    ("JavaScript", "*.js")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name),TITLE))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())

    on_content_changed()


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass

		
#3. SAVE AS FILE

def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),
                                                                      ("HTML", "*.html")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name),TITLE))
    return "break"

#4 SAVE FILE
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

#3.EXIT
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Exit", "Are you sure want to exit?"):
        root.destroy()

#MENU CODE.
menu_bar = Menu(root)
                         #FILE MENU
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', image=new_file_icon, underline=0,command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0,command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0,command=save)
file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', compound='left', underline=0, command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', underline=0, command=exit_editor)




  # EDIT MENU

#FUNCTIONALITY OF EDIT MENU.

#1.CUT 
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"

#2.COPY
def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return "break"

#3.PASTE
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"

#4.UNDO
def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"

#5.REDO
def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return "break"


                                    #EDIT MENU

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left', image=cut_icon, underline=0, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', image=copy_icon, underline=0, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left', image=paste_icon, underline=0,command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound='left', image=undo_icon, underline=0, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', image=redo_icon, underline=0, command=redo)


#SHOW CURSOR
def show_cursor():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()

                                       #VIEW MENU

view_menu = Menu(menu_bar, tearoff=0)
view_menu.add_command(label='statusbar')
view_menu.add_separator()
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor)
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)

themes_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='View', menu=view_menu)


# FUNCTIONALITY OF ABOUT MENU

#1.ABOUT
def display_about(event=None):
    tkinter.messagebox.showinfo(
        "About",TITLE + "\n A python alternative to editor.")

#2.HELP
def display_help(event=None):
    tkinter.messagebox.showinfo("Help", "This is similar to other editors.",icon='question')

#3.EXIT
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Exit", "Are you sure want to exit?"):
        root.destroy()

#ABOUT MENU
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About', underline=0, command=display_about)
about_menu.add_command(label='Help', underline=0, command=display_help)
about_menu.add_separator()
about_menu.add_command(label='Exit', underline=0, command=exit_editor)



#CONFIG ROOT WINDOW.
root.config(menu=menu_bar)


#FUNCTIONALITY OF LINE NUMBERS

#GET LINE NUMBER.
def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

#CONTENT CHANGES
def on_content_changed(event=None):
    update_line_numbers()
    update_cursor()

#UPDATE LINE NUMBER
def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')
	
	
#FUNCTIONALITY OF CURSOR.

#SHOW CURSOR
def show_cursor():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()

#UPDATE CURSOR
def update_cursor(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

#  CREATE SHORTCUT BAR
shortcut_bar = Frame(root, height=25)
shortcut_bar.pack(expand='no', fill='x')

# ADDING ICONS ON SHORTCUT BAR.
icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='pics/{}.gif'.format(icon))#.zoom(2, 2)
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, height=35, width=35, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')

line_number_bar = Text(root, width=3, padx=3, takefocus=0, fg='black', border=0, background='#ffa500', state='disabled',
                       wrap='none')
line_number_bar.pack(side='left', fill='y')

# CONTENT TEXT AND SCROLL BAR WIGDETS
content_text = Text(root, wrap='word')
content_text.pack(expand='yes', fill='both')

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

# CURSOR LABEL.
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')


# HANDLING BINDING.

content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-y>', redo)
content_text.bind('<KeyPress-F1>', display_help)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='ivory2')
content_text.focus_set()

#CLOSE WINDOW.

root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()
