import tkinter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import Normalize
import nibabel as nib
import numpy as np
import os

from services import DicomReader

matplotlib.use('TkAgg')


class MRIPlotComponent:
    _base_image_path = ""
    _base_image_data = None
    _image_min_max = (0, 1)
    _axial_pos = 0
    _sagittal_pos = 0
    _coronal_pos = 0
    _plot_canvas = None
    _plot_artists = []

    def __init__(self, root):
        self.root = root
        self._plot_canvas, self._plot_axes = plt.subplots(nrows=1, ncols=1)
        canvas = FigureCanvasTkAgg(self._plot_canvas, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        canvas.mpl_connect('close_event', self._handle_close)

    def set_image_paths(self, image_path):
        self._base_image_path = image_path
        self.display_images()

    def display_images(self):
        if self._base_image_path != "":
            _, file_extension = os.path.splitext(self._base_image_path)

            if file_extension == ".nii":
                self._base_image_data, _ = load_mri_image(self._base_image_path)
                self._image_min_max = (self._base_image_data.min(), self._base_image_data.max())
                print(self._base_image_data.shape)
                self._axial_pos = self._base_image_data.shape[0] // 2
                self._sagittal_pos = self._base_image_data.shape[1] // 2
                self._coronal_pos = self._base_image_data.shape[2] // 2
                self._display_current_frame()
            else:
                dataset = DicomReader.read_file(self._base_image_path)
                DicomReader.print_file_details(dataset)
                DicomReader.show_image(dataset)
        else:
            self._base_image_data = None
            self._display_current_frame()

    def _display_current_frame(self):
        slices = [self._base_image_data[self._axial_pos, :, :]]
        self._plot_artists = [None]
        for i, slice in enumerate(slices):
            self._plot_axes.clear()
            self._plot_artists[i] = self._plot_axes.imshow(slice.T,
                                                           cmap="gray",
                                                           origin="lower",
                                                           norm=Normalize(vmax=self._image_min_max[1],
                                                                          vmin=self._image_min_max[0]),
                                                           picker=True)
        self._plot_canvas.canvas.draw()

    def _move_slice(self, axial_delta, saggital_delta, coronal_delta):
        self._axial_pos = self._axial_pos + axial_delta
        self._axial_pos = self._axial_pos % self._base_image_data.shape[0]
        self._sagittal_pos = self._sagittal_pos + saggital_delta
        self._sagittal_pos = self._sagittal_pos % self._base_image_data.shape[1]
        self._coronal_pos = self._coronal_pos + coronal_delta
        self._coronal_pos = self._coronal_pos % self._base_image_data.shape[2]

    def save_nifti_image(img_data, affine, img_path):
        img = nib.Nifti1Image(img_data, affine)
        img.to_filename(img_path)
        nib.save(img, img_path)

    def load_and_prepare_nifti_image(path):
        image_data, _ = load_mri_image(path)
        image_data = image_data * (255.0 / image_data.max())
        image_data = image_data.astype(np.uint8)
        image_data = np.expand_dims(image_data, axis=-1)
        return image_data

    def get_path_for_saving(extension):
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=extension)
        if f is None:
            return None
        else:
            return f.name

    def _handle_close(self):
        plt.close('all')


def load_mri_image(img_path):
    proxy_img = nib.load(img_path)
    canonical_img = nib.as_closest_canonical(proxy_img)
    image_data = canonical_img.get_fdata()
    return image_data, canonical_img.affine

