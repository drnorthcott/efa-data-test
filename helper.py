"""helper.py - A group of helper functions for processing energy data.

Daniel Northcott 2024
"""
import numpy as np
import pandas as pd
import os

# Recorded in Snag, Yukon in 1947
THE_COLDEST_TEMPERATURE_IN_NORTH_AMERICA_DEG_C = -63.0


def import_csv_files(file_path, file_names):
    """Import a list of csv files at a certain path to a signal pandas DataFrame.
    
    Arguments:
    file_path -- A single file path string where all of the filenames reside
    file_names -- A list of file names as strings

    Returns: A dataframe prepended by input_file (the file_name of the data source for that row),
             file_row (integer row number from the file having a zero length column name, if present)
             and all the other columns from the csv file. Data is sorted by timestamp, input_file, file_row
    """

    # Import all signals files
    df = pd.DataFrame()
    for file in file_names:
        temp_df = pd.read_csv(os.path.join(file_path, file))

        # Here I attempt to save the original file indexes and reference to file name
        # in case I need them
        temp_df = temp_df.rename(columns={"Unnamed: 0": "file_row"})
        temp_df.insert(0, "input_file", [file for row in range(len(temp_df.index))])

        # Append to accumulate all the files into one dataframe
        df = df.append(temp_df)

    df = df.sort_values(by=['timestamp', 'input_file', 'file_row']).reset_index()

    return df


def _limit_temp_deg_c_minimum(signal_name, signal_value):
    """Checks applies sensible limits to all TempDegC signals and applies np.Nan as needed.
    """
    if "TempDegC" in signal_name:
        if signal_value < THE_COLDEST_TEMPERATURE_IN_NORTH_AMERICA_DEG_C:
            signal_value = np.nan
    return signal_value


def clean_temperature_data(data):
    """Applies a sensible limit to cold temperatures. Only for TempDegC signals.

    Arguments:
    data -- A dataframe with at minimum columns signal_name and VALUE

    Returns: An updated dataframe with temperature limits applied.
    """

    data['VALUE'] = data.apply(lambda x: _limit_temp_deg_c_minimum(x['signal_name'], x['VALUE']), axis=1)
    
    return data