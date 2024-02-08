def part1():

    # Import necessary Fiji classes
    from ij import IJ
    from ij import ImagePlus
    from inra.ijpb.label.conncomp import FloodFillRegionComponentsLabeling3D
    from inra.ijpb.label import LabelImages
    from inra.ijpb.plugins import AnalyzeRegions3D
    import os

    # Set the path to your 3D TIFF images
    image_folder = "/home/shaswati/Documents/PSF/40x-1.4-banana"

    
    # Process each 3D TIFF image in the folder
    for file_name in os.listdir(image_folder):
        full_path = os.path.join(image_folder, file_name)
        if file_name.lower().endswith(".tif"):
            if "mask" in file_name:
                continue
            # Open the 3D image
            image = IJ.openImage(full_path)

            IJ.run(image, "Subtract Background...", "rolling=50 stack")
            image.show()
            rsl_good = image.getTitle()

            lapresult = IJ.getImage()

            mask = lapresult.duplicate()
            lapresult.close()

            # ImageConverter.setDoScaling(True)
            IJ.setAutoThreshold(mask, "Default dark stack")
            IJ.run(mask, "Convert to Mask", "Background=dark")
            mask.getProcessor().invert()
            
            # Use FloodFillRegionComponentsLabeling3D (FFRC) to label the connected components
            ffrcl = FloodFillRegionComponentsLabeling3D(26, 16)
            labeled_image = ffrcl.computeLabels(mask.getStack(), 255)  # 26-connectivity and 16-bit image
           
            # Use LabelImages to remove border regions
            LabelImages.removeBorderLabels(labeled_image)

            # Analyze regions using AnalyzeRegions3D
            clean_image = ImagePlus("PSF_rsl", labeled_image)
            IJ.saveAs(clean_image, "Tiff", os.path.join(image_folder, rsl_good + "_mask.tif"))
            analyze_regions = AnalyzeRegions3D()
            rsl = analyze_regions.process(clean_image)
            rsl.saveAs(os.path.join(image_folder, rsl_good + ".csv"))

            
            # Close all images
            IJ.run("Close All")

def main():