# Processing data from CeNCOOS to National Marine Sanctuary Condition Reports
(NOTE: This code was created by Marine Lebrec for CeNCOOS)
This project converts ecological monitoring data stored in **Darwin Core (DwC) CSV format** into a **standardized JSON format** that can be more readily used by Sanctuary staff in their **Web Condition Reports (CRs)**.  <br><br>
The example used in this repository uses data from the Multi-Agency Rocky Intertidal Network (MARINe) which has been processed into Darwin Core and published to GBIF/OBIS, and the CalOOS Data Portal. <br><br>
The workflow takes user inputs about the data (e.g. the dataset name, indicator species), cleans and aggregates data, and outputs JSONs that align with reporting needs such as **mean values, standard deviations, and station counts across years**.

## 📂 Project Structure
```
CeNCOOS-to-Sanctuary-CR/
│
├── helpers_new.py # Helper functions (data loading, processing, output writing)
├── main.py # Driver script that prompts user for inputs and runs workflow
├── JSON_outputs/ # Folder for generated JSON outputs for each indicator, separated out by Sanctuary
├── JSON_inputs/ # Folder for input JSON files that contain information about what stations to query for a given Sanctuary
└── README.md # This file
```

## ⚙️ Workflow

1. **User selects input parameters**  
   When you run `main.py`, the script prompts you to provide:  
   - **Stations file** (JSON describing stations for a sanctuary)  
   - **Source dataset** (`MARINe Transects`, `MARINe Photoplots`, or `MARINe Seastars`)  
   - **Target assemblage** (e.g., `Mytilus`)  
   - **Indicator species** (e.g., `Mytilus californianus`)

2. **CSV ingestion**  
   The corresponding CSV file (Darwin Core format) is read and filtered to only include relevant assemblages/species.

3. **Data processing**  
   The pipeline:  
   - Groups data by **year** and **station**  
   - Builds pivot tables of values  
   - Calculates **mean**, **standard deviation**, and **station counts** across stations per year  
   - Assembles results into a JSON with a **metadata block**  

4. **JSON output**  
   Results are saved to the `JSON_outputs/` folder, with filenames based on sanctuary name, dataset, and assemblage.  

