import os
import tkinter as tk
from tkinter import scrolledtext, filedialog

def about():
    tk.messagebox.showinfo("About", "Minecraft Mod List App\nCreated by Lilly 💖")

def exit_app():
    root.destroy()
    
def export_list():
    # Get the current text in the ScrolledText widget
    mods_text = text_area.get("1.0", tk.END)

    if not mods_text.strip():  # If the list is empty, do nothing
        return

    # Open a file dialog to choose the save location and filename
    file_path = filedialog.asksaveasfilename(
        title="Export Mods List",
        initialdir=".",  # Start in the current directory
        defaultextension=".txt",  # Set the default extension as .txt
        filetypes=[("Text files", "*.txt")]  # Only allow text files to be saved
    )

    if not file_path:  # User cancelled the dialog
        return

    # Save the mod list to a text file
    with open(file_path, "w") as f:
        f.write(mods_text)

def list_mods():
    # Open a file dialog to choose the mod folder
    mod_folder = filedialog.askdirectory(title="Select Minecraft Mods Folder")

    if not mod_folder:
        return  # User cancelled the dialog

    mods = [f for f in os.listdir(mod_folder) if f.endswith(".jar")]

    text_area.delete("1.0", tk.END)
    for mod in mods:
        text_area.insert(tk.END, mod + "\n")
        
def compare_lists():
    # Open a file dialog to choose the first mod list text file
    mod_file1 = filedialog.askopenfilename(
        title="Select First Mod List Text File",
        initialdir=".",  # Start in the current directory
        filetypes=[("Text files", "*.txt")]  # Only allow text files to be selected
    )

    if not mod_file1:
        return

    # Open a file dialog to choose the second mod list text file
    mod_file2 = filedialog.askopenfilename(
        title="Select Second Mod List Text File",
        initialdir=".",  # Start in the current directory
        filetypes=[("Text files", "*.txt")]  # Only allow text files to be selected
    )

    if not mod_file2:
        return

    # Read the mods from both text files and convert them to sets for faster lookup
    with open(mod_file1, "r") as f1, open(mod_file2, "r") as f2:
        mod_set1 = set(line.strip() for line in f1)
        mod_set2 = set(line.strip() for line in f2)

    # Initialize counters for mods found in both and missing from one
    found_in_both = 0
    only_in_file1 = 0
    only_in_file2 = 0

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "Alright, sweet cheeks! Let's see how these two mod lists stack up!\n\n")

    for mod in sorted(mod_set1 | mod_set2):
        if mod in mod_set1 and mod in mod_set2:
            text_area.insert(tk.END, f"🎉 {mod}: Found in both files! We're off to a great start, babe!\n")
            found_in_both += 1
        elif mod in mod_set1:
            text_area.insert(tk.END, f"😓 {mod}: Only in {os.path.basename(mod_file1)}. Bummer, but we'll find its match soon enough, yeah?\n")
            only_in_file1 += 1
        else:  # mod is only in the second file
            text_area.insert(tk.END, f"😮 {mod}: Only in {os.path.basename(mod_file2)}. Well, well, well! Let's hope its friend shows up soon!\n")
            only_in_file2 += 1

    text_area.insert(tk.END, f"\n\nSo far, we've found {found_in_both} mods in both files and {only_in_file1 + only_in_file2} that are only in one file. Now let's see who's been naughty and not playing nice with sharing!\n\n")

    text_area.insert(tk.END, f"😒 Mods that are only in {os.path.basename(mod_file1)}:\n")

    # Display mods unique to the first file
    for mod in sorted(mod_set1 - mod_set2):
        text_area.insert(tk.END, f"- 🚫 {mod}\n")
    if not (mod_set1 - mod_set2):
        text_area.insert(tk.END, "😏 None! Both files are playing nice so far!\n")

    text_area.insert(tk.END, f"\nAnd now for the mods that are only in {os.path.basename(mod_file2)}:\n")

    # Display mods unique to the second file
    for mod in sorted(mod_set2 - mod_set1):
        text_area.insert(tk.END, f"- 😲 {mod}\n")
    if not (mod_set2 - mod_set1):
        text_area.insert(tk.END, "🤗 None!\n")

    text_area.insert(tk.END, f"\n\nSo, in total, we've found {found_in_both} mods that both of you should have and {only_in_file1 + only_in_file2} mods that one of you is missing out on! 🤗")

    

# Create the main window
root = tk.Tk()
root.title("Minecraft Mod List")
root.geometry("400x350")  # Set a fixed size for the window

# Create a menu bar
menu_bar = tk.Menu(root)

# Create "File" and "Help" menus with their respective commands
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Exit", command=exit_app)
help_menu = tk.Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About...", command=about)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Create a frame to hold the buttons and text area
frame = tk.Frame(root)

# Create a ScrolledText widget with increased height and width to display the list of mods
text_area = scrolledtext.ScrolledText(frame, width=120, height=40)
text_area.pack(padx=10, pady=5)

# Create a "List Mods" button that opens the file dialog
list_button = tk.Button(
    frame,
    text="List Mods",
    command=list_mods,
)
list_button.pack(padx=5, pady=5)

compare_button = tk.Button(
    frame,
    text="Compare List",
    command=compare_lists,
)
compare_button.pack(padx=5, pady=5)

frame.pack()

file_menu.add_command(label="Export List...", command=export_list)


# Run the application's main loop
root.mainloop()
