from math import sqrt

from pumpia.module_handling.in_outs.viewer_ios import DicomViewerIO
from pumpia.module_handling.modules import BaseModule
from pumpia.module_handling.in_outs.simple import (FloatOutput,
                                                   IntInput,
                                                   FloatInput)
from pumpia.file_handling.dicom_tags import USTags
from pumpia.file_handling.dicom_structures import Series, Instance


class Calculator(BaseModule):
    viewer = DicomViewerIO(row=0,
                           column=0,
                           allow_drag_drop=False)

    pixel_width = FloatOutput(verbose_name="Pixel Width (mm)")
    pixel_height = FloatOutput(verbose_name="Pixel Height (mm)")

    x_length_pix = IntInput(verbose_name="x Length (pixels)")
    y_length_pix = IntInput(verbose_name="y Length (pixels)")
    area_pix = FloatInput(verbose_name="Area (pixels^2)")

    x_length_mm = FloatOutput(verbose_name="x Length (mm)")
    y_length_mm = FloatOutput(verbose_name="y Length (mm)")
    total_length_mm = FloatOutput(verbose_name="Total Length (mm)")
    area_mm = FloatOutput(verbose_name="Area (mm^2)")

    def load_commands(self):
        self.register_command("Convert Measurements", self.calculate)

    def set_values(self, image: Series | Instance):
        self.pixel_width.value = 10 * float(
            image.get_tag(USTags.PhysicalDeltaX))  # type: ignore
        self.pixel_height.value = 10 * float(
            image.get_tag(USTags.PhysicalDeltaY))  # type: ignore

    def calculate(self):
        image = self.viewer.image
        if image is not None:
            self.set_values(image)
            self.x_length_mm.value = (self.pixel_width.value
                                      * self.x_length_pix.value)
            self.y_length_mm.value = (self.pixel_height.value
                                      * self.y_length_pix.value)
            self.total_length_mm.value = sqrt((self.x_length_mm.value**2
                                               + self.y_length_mm.value**2))
            self.area_mm.value = (self.area_pix.value
                                  * self.pixel_height.value
                                  * self.pixel_width.value)
