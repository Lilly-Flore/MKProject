selectObjectsByClassification(null);
addShapeMeasurements("AREA", "LENGTH", "CIRCULARITY", "SOLIDITY", "MAX_DIAMETER", "MIN_DIAMETER", "NUCLEUS_CELL_RATIO")

def px = getCurrentServer().getPixelCalibration().getAveragedPixelSizeMicrons()

// Only select the MK it.getName()?.contains("LF") }
def pathObjects = QP.getDetectionObjects().findAll { it.getPathClass() ==  getPathClass("MK")} /*getAnnotationObjects().findAll  { 
                    !(it.getPathClass() ==  getPathClass("Training") ||    
                    it.getPathClass() ==  getPathClass("Validation"))
                    }*/

pathObjects.each{ o ->
    def children = o.getChildObjects()
    def num_nuclei = 0.0
    
    if(children != null) {
        num_nuclei = children.size() as double 
        o.measurements['Number of nuclei'] = num_nuclei
    }   
    
    def nuc_area_px = children.collect{ it.getROI().getArea() }?.sum() / num_nuclei
    def nuc_min_diam_px = children.collect{ it.measurements['Min diameter µm'] }?.sum() / num_nuclei
    def nuc_max_diam_px = children.collect{ it.measurements['Max diameter µm'] }?.sum() / num_nuclei
    def nuc_circ_px = children.collect{ it.measurements['Circularity'] }?.sum() / num_nuclei
    def nuc_min_hema = children.collect{ it.measurements['Hematoxylin: Min'] }?.sum() / num_nuclei
    def nuc_max_hema = children.collect{ it.measurements['Hematoxylin: Max'] }?.sum() / num_nuclei
    def nuc_mean_hema = children.collect{ it.measurements['Hematoxylin: Mean'] }?.sum() / num_nuclei
    def nuc_std_hema = children.collect{ it.measurements['Hematoxylin: Std.Dev.'] }?.sum() / num_nuclei
    //print(nuc_max_diam_px)
    
    
    if(nuc_area_px != null) {
        // Calculate area ratio
        def area_ratio = nuc_area_px / o.getROI().getArea() * 100
        o.measurements['Area Ratio %'] = area_ratio
        o.measurements['Nuclei Area '+GeneralTools.micrometerSymbol()+'^2: Mean' ] = nuc_area_px * px * px
    }
    if(nuc_min_diam_px != null) {
        // Calculate min diameter ratio
        def min_diam_ratio = nuc_min_diam_px / o.measurements['Min diameter µm'] * 100
        o.measurements['Diameter Ratio %: Min'] = min_diam_ratio
        o.measurements['Nuclei diameter '+GeneralTools.micrometerSymbol()+ ': Mean Min' ] = nuc_min_diam_px //* px * px   
    }
    if(nuc_max_diam_px != null) {
        // Calculate max diameter ratio
        def max_diam_ratio = nuc_max_diam_px / o.measurements['Max diameter µm'] * 100
        o.measurements['Diameter Ratio %: Max'] = max_diam_ratio
        o.measurements['Nuclei diameter '+GeneralTools.micrometerSymbol()+ ': Mean Max' ] = nuc_max_diam_px * px * px      
    }    
    if(nuc_max_diam_px != null) {
        // Calculate circularity ratio
        def circ_ratio = nuc_circ_px / o.measurements['Circularity'] * 100
        o.measurements['Circularity Ratio %'] = circ_ratio
        o.measurements['Nuclei Circularity '+GeneralTools.micrometerSymbol()+ ': Mean' ] = nuc_circ_px * px * px
    }
    if(nuc_min_hema != null) {
        o.measurements['Nuclei Hematoxylin: Min'] = nuc_min_hema
    }
    if(nuc_max_hema != null) {
        o.measurements['Nuclei Hematoxylin: Max'] = nuc_max_hema
    }
    if(nuc_mean_hema != null) {
        o.measurements['Nuclei Hematoxylin: Mean'] = nuc_max_hema
    }
    if(nuc_std_hema != null) {
        o.measurements['Nuclei Hematoxylin: Std.Dev.'] = nuc_max_hema
    }
}
println('Done!')