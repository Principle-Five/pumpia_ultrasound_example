from pumpia.module_handling.module_collections import BaseCollection, OutputFrame
from pumpia.module_handling.in_outs.viewer_ios import DicomViewerIO
from pumpia.widgets.viewers import DicomViewer

from simple_ultrasound_collection.modules.region_module import RegionModule
from simple_ultrasound_collection.modules.measurement_calculator import Calculator


class SimpleUSTool(BaseCollection):
    version = (1, 0, 0)
    name = "Simple Ultrasound Tool"

    viewer = DicomViewerIO(row=0, column=0)

    region_module = RegionModule()
    calculator = Calculator()

    pixel_output = OutputFrame()
    region_output = OutputFrame()
    length_output = OutputFrame()
    area_output = OutputFrame()

    def load_outputs(self):
        self.pixel_output.register_output(self.region_module.pixel_width)
        self.pixel_output.register_output(self.region_module.pixel_height)

        self.region_output.register_output(self.region_module.region_xmin)
        self.region_output.register_output(self.region_module.region_xmax)
        self.region_output.register_output(self.region_module.region_ymin)
        self.region_output.register_output(self.region_module.region_ymax)
        self.region_output.register_output(self.region_module.region_width)
        self.region_output.register_output(self.region_module.region_height)

        self.length_output.register_output(self.calculator.x_length_pix)
        self.length_output.register_output(self.calculator.x_length_mm)
        self.length_output.register_output(self.calculator.y_length_pix)
        self.length_output.register_output(self.calculator.y_length_mm)
        self.length_output.register_output(self.calculator.total_length_mm)

        self.area_output.register_output(self.calculator.area_pix)
        self.area_output.register_output(self.calculator.area_mm)

    def on_image_load(self, viewer: DicomViewer) -> None:
        if viewer is self.viewer:
            if self.viewer.image is not None:
                image = self.viewer.image
                self.region_module.viewer.load_image(image)
                self.calculator.viewer.load_image(image)
