## Author: Mustafa Radheyyan
## Date: 02/02/2023
## Assignment: Cognixia JUMPro Python Project 3 - Queries

import pandas as pd

class DataCleaner():
    def convert_columns_to_date(self, data_frame: pd.DataFrame):
        for column in data_frame.columns:
            if "Date" in str(column):
                data_frame[column] = pd.to_datetime(data_frame[column])

    def remove_single_value_columns(self, data_frame: pd.DataFrame):
        saved_values = []
        for column in data_frame.columns:
            if "ID" not in str(column) and data_frame[column].min() == data_frame[column].max():
                saved_values.append({column: data_frame[column].min()})
                self.drop_columns(data_frame, column)
        return saved_values

    def drop_columns(self, data_frame: pd.DataFrame, column_names):
        data_frame.drop(columns=[column_names], inplace=True)

    def drop_null_rows(self, data_frame: pd.DataFrame, column_names):
        data_frame.dropna(subset=column_names, inplace=True)