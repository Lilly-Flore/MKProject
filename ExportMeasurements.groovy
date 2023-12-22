/*
 * @author Lilly-Flore Celma
 */

import qupath.lib.gui.tools.MeasurementExporter
import qupath.lib.objects.PathDetectionObject

// Get the list of all images in the current project
def project = getProject()
def imagesToExport = project.getImageList()

// Separate each measurement value in the output file with a tab ("\t")
def separator = "\t"

// Choose the columns that will be included in the export
// Note: if 'columnsToInclude' is empty, all columns will be included
def columnsToInclude = new String[]{"Image", "Object ID", "Name", "Number of nuclei", 
                                    "Area µm^2", "Nuclei Area µm^2: Mean", "Area Ratio %",
                                    "Max diameter µm", "Nuclei diameter µm: Mean Max", "Diameter Ratio %: Max",
                                    "Min diameter µm", "Nuclei diameter µm: Mean Min", "Diameter Ratio %: Min", 
                                    "Circularity", "Nuclei Circularity µm: Mean", "Circularity Ratio %",
                                    "Hematoxylin: Mean", "Hematoxylin: Min", "Hematoxylin: Max", "Hematoxylin: Std.Dev.",
                                    "Nuclei Hematoxylin: Min", "Nuclei Hematoxylin: Max", "Nuclei Hematoxylin: Mean", "Nuclei Hematoxylin: Std.Dev."
                                    }
print(columnsToInclude)
// Choose the type of objects that the export will process
// Other possibilities include:
//    1. PathAnnotationObject
//    2. PathCellObject
//    3. PathRootObject
// Note: import statements should then be modified accordingly
def exportType = PathDetectionObject.class

// Choose your *full* output path
def outputPath = "/home/big/Desktop/MarrowBone/MKProject/Common/measurements.tsv"
def outputFile = new File(outputPath)

// Create the measurementExporter and start the export
def exporter  = new MeasurementExporter()
                  .imageList(imagesToExport)            // Images from which measurements will be exported
                  .separator(separator)                 // Character that separates values
                  .includeOnlyColumns(columnsToInclude) // Columns are case-sensitive
                  .exportType(exportType)               // Type of objects to export
                  .filter(obj -> obj.getPathClass() == getPathClass("MK")) //|| obj.getPathClass() == getPathClass("nuclei"))
                  .exportMeasurements(outputFile)        // Start the export process

print("Done!")