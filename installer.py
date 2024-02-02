import tkinter as tk
import tkinter.messagebox as messagebox
import os
import shutil

class Downloader:
    def __init__(self, download_directory, installation_directory):
        self.download_directory = download_directory
        self.installation_directory = installation_directory
        self.version = "0.0.3"

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

            messagebox.showinfo("Installation Complete", "Janex Personal Assistant has been installed successfully!")
        except Exception as e:
            messagebox.showerror("Installation Failed", f"An error occurred during installation: {str(e)}")

class App:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Janex Personal Assistant - Installer")
        width, height = 324, 168
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

        # Install button
        install_button = tk.Button(self.root, text="Install", command=self.install_action, bg="#01aaed", fg="#000000", justify="center")
        install_button.place(x=220, y=130, width=71, height=30)

        # Label
        label = tk.Label(self.root, text="Install your own Janex Personal Assistant", fg="#333333", justify="center")
        label.place(x=30, y=30, width=280, height=30)

    def install_action(self):
        directory = self.directory_entry.get()
        downloader = Downloader("~/Downloads", directory)
        downloader.download_and_extract()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
