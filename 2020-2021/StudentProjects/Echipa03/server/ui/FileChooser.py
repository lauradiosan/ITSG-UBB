import tkinter as tk
import tkinter.filedialog

from services.MRIPlotComponent import MRIPlotComponent


class FileChooser:
    IMG_CHANNELS = 3

    def __init__(self, master):
        self.root = master
        self.root.geometry("700x450")
        self.root.resizable(1, 1)
        self.root.title("ITSG Medical Image Assistent")
        self._menu_file = [("Upload image", self._on_load_image)]
        self._menus = [("File", self._menu_file)]
        self.image_path = ""
        self.label_path = ""
        self.plot_canvas = MRIPlotComponent(self.root)

    def _init_menus(self):
        self.menubar = tk.Menu(self.root)
        for menuName, options in self._menus:
            file_menu = tk.Menu(self.menubar, tearoff=0)
            for subMenuName, action in options:
                if action is not None:
                    file_menu.add_command(label=subMenuName, command=action)
                else:
                    file_menu.add_separator()
            self.menubar.add_cascade(label=menuName, menu=file_menu)
        self.root.config(menu=self.menubar)

    def _on_load_image(self):
        self.image_path = tk.filedialog.askopenfilename(parent=self.root, initialdir="/", title="Select image file")
        print(self.image_path)
        if ".nrrd" in str(self.image_path):
            self.convert_to_NIfTI(self.image_path)
        if self.image_path != "":
            self._display_image()

    def _display_image(self):
        self.plot_canvas.set_image_paths(self.image_path)

    def show(self):
        # Initialize the menu bar
        self._init_menus()
