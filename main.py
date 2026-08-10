# main.py
from helpers_new import sanctuaryStations, phototransQuery, seastarsQuery, createOutputJSON, writeOutputJSON

# --- Load stations; change the stationsFile being read into inputJSON function in order to switch sanctuaries ---
stationsFile_MBNMS = 'https://www.researchworkspace.com/files/44959120/marine_photoplot_sites_mbnms.json'
stationsFile_CINMS = 'JSON-inputs/marine_sites_cinms.json'
stationsFile_OCNMS = 'JSON-inputs/marine_sites_ocnms.json'
inputJSON = sanctuaryStations(stationsFile_OCNMS)
print('inputJSON finished reading: ',inputJSON)

# --- Ask user for input ---
sourceDataName = input("Enter source data (MARINe Transects / MARINe Photoplots / MARINe Seastars): ")
targetAssemblage = input("Enter target assemblage (e.g., Mytilus): ")
speciesName = input("Enter species name (e.g., Mytilus californianus): ")

# --- Set constant variables ---
timeFormat = "YYYY"

# --- Branching logic depending on type of MARINe dataset ---
if sourceDataName == "MARINe Transects":
    #dataFile = "https://www.researchworkspace.com/file/45117911/transects_ingest_20251209.csv"
    dataFile = 'csv_inputs/transects_ingest_20251209.csv'
    sourceDataURL = "Not Publicly Available Yet"
    variableUnit = "Percent Cover"
    variable = "organismQuantity"
    aggFunction = "mean"
    df = phototransQuery(dataFile, targetAssemblage, speciesName)

elif sourceDataName == "MARINe Photoplots":
    #dataFile = "https://researchworkspace.com/files/45117169/photoplots_ingest_20251209.csv"
    dataFile = 'csv_inputs/photoplots_ingest_20251209.csv'
    sourceDataURL = "Not Publicly Available Yet"
    variableUnit = "Percent Cover"
    variable = "organismQuantity"
    aggFunction = "mean"
    df = phototransQuery(dataFile, targetAssemblage, speciesName)

elif sourceDataName == "MARINe Seastars":
    #dataFile = "https://www.researchworkspace.com/file/45134907/seastars_ingest_08042025.csv"
    dataFile = 'csv_inputs/MARINE_LTM_seastarkat_count_occurrence_v5_20251210.csv'
    sourceDataURL = "Not Publicly Available Yet"
    variableUnit = "% of Maximum Percent Cover"
    variable = "organismQuantity"
    aggFunction = "sum"
    df = seastarsQuery(dataFile, speciesName)

else:
    raise ValueError("Invalid source data name entered!")

# --- Process output ---
outputJSON, pivot_df = createOutputJSON(
                    inputJSON, df, variable, variableUnit, timeFormat, 
                    targetAssemblage, speciesName, sourceDataName, sourceDataURL, aggFunction
)
writeOutputJSON(outputJSON)


