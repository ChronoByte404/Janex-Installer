import tkinter as tk
import tkinter.messagebox as messagebox
import os
import shutil
import sys
import subprocess

class Downloader:
    def __init__(self, download_directory, installation_directory):
        self.download_directory = download_directory
        self.installation_directory = installation_directory
        self.version = "0.0.6"

    def install_dependencies(self):
        os.system("cd ~/.JanexAssistant && mkdir ./Settings && python3 -m pip install -r Setup/requirements.txt")

    def create_desktop_entry(self):
        os.system("cd ~ && wget https://github.com/ChronoByte404/Janex-Assistant/raw/main/BinaryFiles/Janex-Assistant.janex")
        subprocess.run(f"sudo chmod +x {os.environ['HOME']}/Janex-Assistant.janex", shell=True, check=True)
        desktop_entry = f'''[Desktop Entry]
Name=Janex Assistant
Exec="~/Janex-Assistant.janex"
Icon={os.path.join(self.installation_directory, 'images', 'icon.png')}
Type=Application
Categories=Utility;'''

        desktop_path = os.path.join(os.environ['HOME'], '.local', 'share', 'applications', 'Janex_Assistant.desktop')

        with open(desktop_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry)

        print(f"Desktop entry created at: {desktop_path}")

    def download_and_extract(self):
        try:
            if os.path.exists(self.installation_directory):
                print("Removing existing installation (excluding Settings folder).")
                for item in os.listdir(self.installation_directory):
                    if item != "Settings":
                        item_path = os.path.join(self.installation_directory, item)
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)

            print("Downloading zip.")
            os.system(f"cd {self.download_directory} && wget https://github.com/ChronoByte404/Janex-Assistant/archive/refs/tags/v{self.version}.zip -O Janex-Assistant.zip")

            print("Extracting zip.")
            os.system(f"unzip {self.download_directory}/Janex-Assistant.zip -d {self.download_directory}")

            print("Moving contents.")
            os.system(f"mkdir -p {self.installation_directory}")
            os.system(f"mv {self.download_directory}/Janex-Assistant-{self.version}/* {self.installation_directory}")

            print("Creating executable.")

            JanexAssistantInfo = ""

            messagebox.showinfo("Installation Complete", "Janex Personal Assistant has been installed successfully!")
            self.create_desktop_entry()  # Call to create desktop entry
            sys.exit()
        except Exception as e:
            messagebox.showerror("Installation Failed", f"An error occurred during installation: {str(e)}")

class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Janex Personal Assistant - Installer")
        width, height = 324, 228
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def create_widgets(self):
        # Entry widget for directory
        default_directory = '~/.JanexAssistant'
        self.directory_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.directory_entry.insert(tk.END, default_directory)
        self.directory_entry.place(x=30, y=90, width=260, height=30)

        # Entry widget for assistant name
        self.assistant_name_entry = tk.Entry(self.root, bg="#ffffff", fg="#333333", justify="center")
        self.assistant_name_entry.insert(tk.END, "Janex Assistant")
        self.assistant_name_entry.place(x=30, y=140, width=260, height=30)

        # Install button
        install_button = tk.Button(self.root, text="Install", command=self.install_action, bg="#01aaed", fg="#000000", justify="center")
        install_button.place(x=220, y=190, width=71, height=30)

        # Label
        label = tk.Label(self.root, text="Install your own Janex Personal Assistant", fg="#333333", justify="center")
        label.place(x=30, y=30, width=280, height=30)

    def install_action(self):
        directory = self.directory_entry.get()
        downloader = Downloader("~/Downloads", directory)
        downloader.download_and_extract()
        downloader.install_dependencies()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
