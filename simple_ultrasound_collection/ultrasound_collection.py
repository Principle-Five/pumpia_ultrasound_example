from pumpia.module_handling.module_collections import BaseCollection, OutputFrame
from pumpia.module_handling.in_outs.viewer_ios import DicomViewerIO
from pumpia.widgets.viewers import DicomViewer

from simple_ultrasound_collection.modules.region_module import RegionModule


class SimpleUSCollection(BaseCollection):
    name = "Simple Ultrasound Module"

    viewer = DicomViewerIO(row=0, column=0)

    region_module = RegionModule()

    pixel_output = OutputFrame()
    region_output = OutputFrame()
    calculator_output = OutputFrame()

    def load_outputs(self):
        self.pixel_output.register_output(self.region_module.pixel_width)
        self.pixel_output.register_output(self.region_module.pixel_height)

        self.region_output.register_output(self.region_module.region_xmin)
        self.region_output.register_output(self.region_module.region_xmax)
        self.region_output.register_output(self.region_module.region_ymin)
        self.region_output.register_output(self.region_module.region_ymax)
        self.region_output.register_output(self.region_module.region_width)
        self.region_output.register_output(self.region_module.region_height)

    def on_image_load(self, viewer: DicomViewer) -> None:
        if viewer is self.viewer:
            if self.viewer.image is not None:
                image = self.viewer.image
                self.region_module.viewer.load_image(image)
