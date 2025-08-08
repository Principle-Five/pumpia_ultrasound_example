# Simple Ultrasound Tool
A simple tool for showing ultrasound images and demonstrating key features of ultrasound DICOMs.

# Usage

Users should make themselves familiar with the [PumpIA user interface](https://principle-five.github.io/pumpia/usage/user_interface.html)

To run the program:
1. Clone the repository
2. Use an environment manager to install the requirements from [`requirements.txt`](https://github.com/Principle-Five/pumpia_ultrasound_example/blob/main/requirements.txt) or install the requirements using the command `pip install -r requirements.txt` when in the repository directory
3. Run the [`simple_us_tool_v1_0_0.py`](https://github.com/Principle-Five/pumpia_ultrasound_example/blob/main/simple_us_tool_v1_0_0.py) script

Alternatively the [releases](https://github.com/Principle-Five/pumpia_ultrasound_example/releases) contain the script packaged as an executable and zip, either one might work depending on your antivirus settings.

# Key DICOM Tags

This program uses the following DICOM tags:
- `RegionLocationMinX0`
- `RegionLocationMaxX1`
- `RegionLocationMinY0`
- `RegionLocationMaxY1`
- `PhysicalDeltaX`
- `PhysicalDeltaY`

These are all inside the `SequenceOfUltrasoundRegions` tag which contains information about ultrasound regions (see [page 8 here](https://www.dicomstandard.org/News-dir/ftsup/docs/sups/sup84.pdf) for more information). One image can contain multiple regions for example if it is a duplex image with B-mode and pulsed doppler. Tags such as `RegionSpatialFormat` contain informaion on what is contained in each region, however they are often coded. The [Innolitics DICOM Browser](https://dicom.innolitics.com/ciods/ultrasound-image/us-region-calibration/00186011/00186012) is useful for finding what the codes mean. It should be noted that a region may not cover the expected area, for example a B-mode region often doesn't hug the picture and can include surrounding information such as rulers.

Within this program the first region stored is used to get the relevant information, this may not be the desired region if there are multiple in the image. All the processing for this is done in the [`regions module`](https://github.com/Principle-Five/pumpia_ultrasound_example/blob/main/simple_ultrasound_collection/modules/region_module.py) function `set_values`.

The `PixelSpacing` tag can also provide information about the pixel size, however it is not included in every Ultrasound image. Where it is include the `PixelSpacing` tag units are mm, however `PhysicalDeltaX` and `PhysicalDeltaY` units are cm (where they refer to a 2D image). Care should be taken to ensure units are converted as needed.

# The Program

It should be noted that some ultrasound series contain images with different pixel sizes and regions, therefore the 3 tabs described below may not be fully coherent.

## Main Page
This contains a summary of the other two tabs on the right hand side.

Drag series or instances into the viewer on this page to view them. You cannot drag and drop into the other viewers.

The buttons "copy horizontal/vertical" in this page can be used to copy values to clipboard.

## Region Module
Press the "Draw Region Boundary" button to populate the information for the first region in the image in the viewer, and draw the region on the image shown.

The number of regions in the image is also provided to demonstrate how different images can have a different amount depending on content.

## Calculator
This contains a simple calculator for converting between measurements in pixel units - like those provided in the measurements of ROIs - and real world values. The values are calculated using the button "Convert Measurements". This uses the information from the DICOM header for the image shown on the viewer.
