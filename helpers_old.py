import pandas as pd
import json
import os
import requests

def sanctuaryStations(jsonFile):
    response = requests.get(jsonFile)
    data = response.json()
    return data
    
def phototransQuery(dataFile, targetAssemblage, speciesName):
    df = pd.read_csv(dataFile)
    df = df[df['graph_target_assemblage'] == targetAssemblage]
    df = df[df['scientificName'] == speciesName]
    df = df[["locality", "eventDate_mid", "organismQuantity"]]
    df['eventDate_mid']= pd.to_datetime(df["eventDate_mid"])
    print('Successfully created dataframe based on query...')

    return df

def seastarsQuery(dataFile, speciesName):
    df = pd.read_csv(dataFile)
    df = df[df['scientificName'] == speciesName]
    df = df[["locality", "eventDate_mid", "individualCount"]]
    df["eventDate_mid"]= pd.to_datetime(df["eventDate_mid"])
    print('Successfully created dataframe based on query...')

    return df

def createOutputJSON(inputJSON, df, variable, variableUnit, timeFormat, 
                     targetAssemblage, speciesName, sourceDataName, sourceDataURL, aggFunction):
    
    variable = variable
    variableUnit = variableUnit 
    timeFormat = "%Y"
    targetAssemblage = targetAssemblage  
    speciesName = speciesName 
    sourceDataName = sourceDataName
    aggFunction = aggFunction

    metadata = {
            "sanctuaryName": inputJSON.get("Sanctuary", "Unknown"),
            "sourceDataName": sourceDataName,
            "sourceDataURL": sourceDataURL,
            "metadataCreatorName": inputJSON.get("metadataCreatorName", "Unknown"),
            "metadataCreatorEmail": inputJSON.get("metadataCreatorEmail", "Unknown"),
            "variableUnit": variableUnit,
            "timeFormat": timeFormat,
            "targetAssemblage": targetAssemblage,
            "indicatorSpecies": speciesName

    }

    # Step 1: Collapse to one row per year per station
    df["Year"] = df["eventDate_mid"].dt.year
    grouped = df.groupby(["Year", "locality"], as_index=False)[variable].agg(aggFunction)

    # Step 2: Create pivot table with years as index
    pivot_df = grouped.pivot_table(
        index="Year",
        columns="locality",
        values=variable
    ).sort_index()
    
    # Step 3: Build master year list
    master_years = pivot_df.index.tolist()
    master_years_str = [str(y) for y in master_years]

    # Step 4: Build data dictionary
    data = {
        "Date": master_years_str
    }

    for station in inputJSON["stationNames"]:
        if station in pivot_df.columns:
            values = pivot_df[station].tolist()
            values = [round(val, 2) if pd.notnull(val) else None for val in values]
            data[station] = values
        else:
            data[station] = [None] * len(master_years)
            
    # Step 5: Calculate mean across stations for each year
    stations_in_input = [s for s in inputJSON["stationNames"] if s in pivot_df.columns]
    mean_vals = pivot_df[stations_in_input].mean(axis=1, skipna=True).round(2).tolist()
    mean_vals = [val if not pd.isna(val) else None for val in mean_vals]
    data["meanValues"] = mean_vals
    
    # Step 6: Calculate standard deviations across stations for each year
    std_vals = pivot_df[stations_in_input].std(axis=1, skipna=True, ddof=0).round(2).tolist()
    std_vals = [val if not pd.isna(val) else None for val in std_vals]
    data["standardDeviationValues"] = std_vals

    
    # Step 7: Calculate the total number of stations that don't have NaNs used to derive the mean/std values
    station_counts = pivot_df[stations_in_input].notna().sum(axis=1).tolist()
    data["stationCounts"] = station_counts
    
    
    outputJSON = {
        "metadata": metadata,
        "data": data
    }

    return outputJSON, pivot_df


def writeOutputJSON(outputJSON, save = True):
    if save == True:
        with open(f"JSON-outputs/{outputJSON['metadata']['sanctuaryName']}_MARINe_{outputJSON['metadata']['sourceDataName']}.split(' ')[1]_{outputJSON['metadata']['targetAssemblage']}.json", "w") as file:
            json.dump(outputJSON, file, indent=4)
        
    print(f"Successfully saved JSON file as {file}") 