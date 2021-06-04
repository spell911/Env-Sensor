"""
_setup.py: Load and create dataframe for our streamline, etc. No need to edit.

"""
from _cons import PATH_TO_DATA

import numpy as np
import pandas as pd


try:
    # Set warn_bad_lines to issue warnings about bad records
    records = pd.read_csv(PATH_TO_DATA,
                          nrows=None,
                          error_bad_lines=False,
                          warn_bad_lines=True)

    # Separate data by device
    device_00 = records.loc[records['device'] == '00:0f:00:70:91:0a']
    device_1c = records.loc[records['device'] == '1c:bf:ce:15:ec:4d']
    device_b8 = records.loc[records['device'] == 'b8:27:eb:bf:9d:51']

    # Prep variables for export
    ex_vars = [device_00, device_1c, device_b8]

except pd.io.common.CParserError:
    print("Your data contained rows that could not be parsed.")


def print_info(df):
    """ print important infomation of data frame

    Args:
        df (dataframe): The dataframe we want to see the infomations.
    """
    # Get duplicates across all columns
    duplicates = df.duplicated()
    print(df[duplicates])
    # Print the head of the df data
    print(df.head())
    # Print information about df
    print(df.info())
    # Print the shape of df
    print(df.shape)
    # Print a description of df
    print(df.describe())

    pass


if __name__ == '__main__':
    print_info(records)
