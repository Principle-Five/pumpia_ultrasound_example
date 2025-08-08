from pumpia.module_handling.modules import BaseModule
from pumpia.module_handling.in_outs.viewer_ios import DicomViewerIO
from pumpia.widgets.viewers import DicomViewer
from pumpia.module_handling.in_outs.simple import FloatOutput, IntOutput
from pumpia.module_handling.in_outs.roi_ios import InputRectangleROI, BaseInputROI
from pumpia.image_handling.roi_structures import RectangleROI
from pumpia.file_handling.dicom_tags import USTags


class RegionModule(BaseModule):
    viewer = DicomViewerIO(row=0,
                           column=0,
                           allow_drag_drop=False,
                           allow_drawing_rois=False,
                           allow_changing_rois=False)
    region_roi = InputRectangleROI(allow_manual_draw=False)

    pixel_width = FloatOutput(verbose_name="Pixel Width (mm)")
    pixel_height = FloatOutput(verbose_name="Pixel Height (mm)")

    region_xmin = IntOutput()
    region_xmax = IntOutput()
    region_ymin = IntOutput()
    region_ymax = IntOutput()

    region_width = FloatOutput(verbose_name="Region Width (mm)")
    region_height = FloatOutput(verbose_name="Region Height (mm)")

    def link_rois_viewers(self):
        self.region_roi.viewer = self.viewer

    def post_roi_register(self, roi_input: BaseInputROI):
        if (roi_input.roi is not None
            and self.manager is not None
                and roi_input in self.rois):
            self.manager.add_roi(roi_input.roi)

    def load_commands(self):
        self.register_command("Draw Region Boundary", self.draw_region_boundary)

    def on_image_load(self, viewer: DicomViewer) -> None:
        if viewer is self.viewer:
            image = self.viewer.image
            if image is not None:
                self.region_xmin.value = int(
                    image.get_tag(USTags.RegionLocationMinX0))  # type: ignore
                self.region_xmax.value = int(
                    image.get_tag(USTags.RegionLocationMaxX1))  # type: ignore
                self.region_ymin.value = int(
                    image.get_tag(USTags.RegionLocationMinY0))  # type: ignore
                self.region_ymax.value = int(
                    image.get_tag(USTags.RegionLocationMaxY1))  # type: ignore

                self.pixel_width.value = 10 * float(
                    image.get_tag(USTags.PhysicalDeltaX))  # type: ignore
                self.pixel_height.value = 10 * float(
                    image.get_tag(USTags.PhysicalDeltaY))  # type: ignore

                self.region_width.value = (self.pixel_width.value
                                           * (self.region_xmax.value
                                              - self.region_xmin.value))
                self.region_height.value = (self.pixel_height.value
                                            * (self.region_ymax.value
                                               - self.region_ymin.value))

    def draw_region_boundary(self) -> None:
        image = self.viewer.image
        if image is not None:
            self.region_roi.register_roi(RectangleROI(image,
                                                      self.region_xmin.value,
                                                      self.region_ymin.value,
                                                      (self.region_xmax.value
                                                       - self.region_xmin.value),
                                                      (self.region_ymax.value
                                                       - self.region_ymin.value),
                                                      slice_num=self.viewer.current_slice),
                                         update_viewers=True)
