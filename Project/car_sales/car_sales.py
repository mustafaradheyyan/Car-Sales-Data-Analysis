import pandas as pd
from pathlib import Path
from data_cleaner.data_cleaner import DataCleaner

DASH_SEPARATOR = "\n" + ("-" * 50)
NUMERICAL_DTYPES = ["int64", "float"]

class CarSales():
    car_sales_file_path = Path("car_sales/car_sales_table.csv")
    data_cleaner = DataCleaner()
    
    def __init__(self):
        """Read csv and set StockID as the index column (checked to be unique key)
        """
        self.car_sales_df = pd.read_csv(self.car_sales_file_path, index_col="StockID")
        self.car_sales_single_values = []
    
    def clean_data(self):
        """
        - Drop any rows which have a null value in the "CostPrice" column
        - Convert columns with "Date" in name to the datetime data type
        - Change British English spelling to American English spelling
        - Remove columns with only one value and save it to an object variable
        - Print columns removed, if any
        """
        self.data_cleaner.drop_null_rows(self.car_sales_df, ["CostPrice"])
        self.data_cleaner.convert_columns_to_date(self.car_sales_df)
        self.car_sales_df["VehicleType"].replace("Saloon", "Sedan", inplace=True)
        self.car_sales_single_values = self.data_cleaner.remove_single_value_columns(self.car_sales_df)
        print("\nData Cleaned!", f"Single value column{'s'[:len(self.car_sales_single_values)^1]} removed: {self.car_sales_single_values}" if self.car_sales_single_values else "", DASH_SEPARATOR)
    
    ## Pre-Cleaning Data Exploration (I learned that the PurchaseDate column only has a single value)
    def sort_by_column(self, column_name):
        return self.car_sales_df.sort_values(by=[column_name])
    
    def sort_by_purchase_date(self):
        return self.sort_by_column("PurchaseDate")
    
    ## Post-Cleaning Data Exploration (Looking at the table data types and group by calculation tables on every applicable column)
    def print_data(self): print(f"Car Sales Table!{DASH_SEPARATOR}\n{self.car_sales_df}")
    
    def print_data_snippet(self):
        min_index, max_index = 30, 40
        print(f"\nRows {min_index + 1}-{max_index} of Car Sales Table!{DASH_SEPARATOR}\n{self.car_sales_df[min_index:max_index]}")
    
    def print_data_types(self): 
        print(f"\nData Types of Car Sales Table!{DASH_SEPARATOR}\n")
        self.car_sales_df.info()
    
    def get_non_id_columns(self):
        return [column for column in self.car_sales_df.columns if "ID" not in str(column)]
    
    
    def get_aggregate_color_id(self):
        """
        Get various aggregation group by calculations for the ColorID column
        """
        column = "ColorID"
        return [{column: [
            {"min": self.car_sales_df.groupby([column])[self.get_non_id_columns()].min(numeric_only=True)},
            {"max": self.car_sales_df.groupby([column])[self.get_non_id_columns()].max(numeric_only=True)},
            {"mean": self.car_sales_df.groupby([column])[self.get_non_id_columns()].mean(numeric_only=True)},
            {"median": self.car_sales_df.groupby([column])[self.get_non_id_columns()].median(numeric_only=True)},
            {"mode": self.car_sales_df.groupby([column])[self.get_non_id_columns()].agg(lambda x: x.value_counts().index[0])},
            {"sum": self.car_sales_df.groupby([column])[self.get_non_id_columns()].sum(numeric_only=True)},
            ]}]
    
    def get_df_without_id_columns(self):
        id_columns = [column for column in self.car_sales_df.columns if "ID" in str(column)]
        return self.car_sales_df.drop(columns=id_columns)
      
    def get_aggregate_non_int_columns(self):
        """
        Get various aggregation group by calculations for the non-numeric columns, excluding ColorID column in result set
        """
        car_sales_df_no_id = self.get_df_without_id_columns()
        
        return [{column: [
            {"min": car_sales_df_no_id.groupby([column]).min(numeric_only=True)},
            {"max": car_sales_df_no_id.groupby([column]).max(numeric_only=True)},
            {"mean": car_sales_df_no_id.groupby([column]).mean(numeric_only=True)},
            {"median": car_sales_df_no_id.groupby([column]).median(numeric_only=True)},
            {"mode": car_sales_df_no_id.groupby([column]).agg(lambda x: x.value_counts().index[0])},
            {"sum": car_sales_df_no_id.groupby([column]).sum(numeric_only=True)},
            ]} for column in car_sales_df_no_id.columns if car_sales_df_no_id[column].dtype not in NUMERICAL_DTYPES]
    
    ## Query Helper Methods
    def combine_cost_columns(self):
        """
        Summing the various (3) columns that have a cost aspect, into one "Cost" column
        """
        cost_columns = [column for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column) and "Mileage" not in str(column)]
        car_sales_df_copy = self.car_sales_df.copy()
        car_sales_df_copy.drop(columns=cost_columns, inplace=True)
        car_sales_df_copy["Cost"] = 0
        for column in cost_columns:
            car_sales_df_copy["Cost"] += self.car_sales_df[column]
        return car_sales_df_copy
     
    ## Queries
    def get_min_values(self):
        """
        Getting the minimum values for numerical columns that are not key(ID)-based columns
        """
        return [{column: self.car_sales_df[column].min()} for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column)]
        
    def get_max_values(self):
        """
        Getting the maximum values for numerical columns that are not key(ID)-based columns
        """
        return [{column: self.car_sales_df[column].max()} for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column)]
    
    def lowest_avg_cost_color(self):
        """
        Grouping by ColorID, and finding the color ID with the lowest average cost.
        Returns a dictionary of the color ID with the lowest average cost as the key, and the lowest average cost as the value
        """
        car_sales_df_cost = self.combine_cost_columns()
        color_sales_by_cost_df = car_sales_df_cost.groupby(["ColorID"])["Cost"].mean(numeric_only=True).reset_index(name="AvgCost")
        lowest_average_cost_color_index = color_sales_by_cost_df["AvgCost"].idxmin()
        return {color_sales_by_cost_df.loc[lowest_average_cost_color_index, "ColorID"]: round(color_sales_by_cost_df.loc[lowest_average_cost_color_index, "AvgCost"], 2)}
    
    def highest_avg_cost_color(self):
        """
        Grouping by ColorID, and finding the color ID with the highest average cost.
        Returns a dictionary of the color ID with the highest average cost as the key, and the highest average cost as the value
        """
        car_sales_df_cost = self.combine_cost_columns()
        color_sales_by_cost_df = car_sales_df_cost.groupby(["ColorID"])["Cost"].mean(numeric_only=True).reset_index(name="AvgCost")
        highest_average_cost_color_index = color_sales_by_cost_df["AvgCost"].idxmax()
        return {color_sales_by_cost_df.loc[highest_average_cost_color_index, "ColorID"]: round(color_sales_by_cost_df.loc[highest_average_cost_color_index, "AvgCost"], 2)}
    
    def most_common_color_per_vehicle_type(self):
        """
        Grouping by VehicleType and ColorID, and finding the count of each group of vehicle type and color.
        Then the list is sorted from highest to lowest, and the duplicate values from the VehicleType column are dropped
        (drop_duplicate keeps the first occurrence and deletes the rest), so that only the rows with the most common color per vehicle type remain.
        Returns a dictionary with the vehicle type as the key and the color ID as the value.
        """
        car_sales_vehicle_type_color_count = self.car_sales_df.groupby(["VehicleType","ColorID"]).size().sort_values(ascending=False).reset_index(name="count").drop_duplicates(subset='VehicleType')
        return dict(zip(car_sales_vehicle_type_color_count["VehicleType"], car_sales_vehicle_type_color_count["ColorID"]))
    
    def most_common_color_per_vehicle_make(self):
        """
        Grouping by Make and ColorID, and finding the count of each group of vehicle type and color.
        Then the list is sorted from highest to lowest, and the duplicate values from the Make column are dropped
        (drop_duplicate keeps the first occurrence and deletes the rest), so that only the rows with the most common color per vehicle make remain.
        Returns a dictionary with the make as the key and the color ID as the value.
        """
        car_sales_vehicle_type_color_count = self.car_sales_df.groupby(["Make","ColorID"]).size().sort_values(ascending=False).reset_index(name="count").drop_duplicates(subset='Make')
        return dict(zip(car_sales_vehicle_type_color_count["Make"], car_sales_vehicle_type_color_count["ColorID"]))
    
    def most_common_color_per_category(self, category):
        """
        Grouping by the 'category' argument and ColorID, and finding the count of each group of 'category' and color.
        Then the list is sorted from highest to lowest, and the duplicate values from the 'category' column are dropped
        (drop_duplicate keeps the first occurrence and deletes the rest), so that only the rows with the most common color per category remain.
        Returns a dictionary with the category as the key and the color ID as the value.
        """
        car_sales_vehicle_type_color_count = self.car_sales_df.groupby([category,"ColorID"]).size().sort_values(ascending=False).reset_index(name="count").drop_duplicates(subset=category)
        return dict(zip(car_sales_vehicle_type_color_count[category], car_sales_vehicle_type_color_count["ColorID"]))
    
    def min_cost_and_min_mileage(self, cost_of_car, mileage_of_car):
        """
        Finds the rows with the minimum cost as the 'cost_of_car' argument, and the minimum mileage as the 'mileage_of_car' argument.
        Returns a dictionary with the StockID of the car sales that match this condition.
        """
        car_sales_df_cost = self.combine_cost_columns()
        car_sales_cost_vs_mileage = car_sales_df_cost.loc[(car_sales_df_cost["Cost"] >= cost_of_car) & (car_sales_df_cost["Mileage"] >= mileage_of_car)]
        return {"StockID": car_sales_cost_vs_mileage.index.tolist()}
    
    def max_cost_and_max_mileage(self, cost_of_car, mileage_of_car):
        """
        Finds the rows with the maximum cost as the 'cost_of_car' argument, and the maximum mileage as the 'mileage_of_car' argument.
        Returns a dictionary with the StockID of the car sales that match this condition.
        """
        car_sales_df_cost = self.combine_cost_columns()
        car_sales_cost_vs_mileage = car_sales_df_cost.loc[(car_sales_df_cost["Cost"] <= cost_of_car) & (car_sales_df_cost["Mileage"] <= mileage_of_car)]
        return {"StockID": car_sales_cost_vs_mileage.index.tolist()}
    
    def total_revenue_by_make(self):
        """
        Uses a combined cost car sales table, a table with combined cost columns into one "Cost" column, and groups the table by the "Make" column.
        Then the "Cost" column is summed up for each group of "Make" column values, and the summed up values are sorted from highest to lowest.
        Returns a dictionary with the make as the key and the total revenue as the value.
        """
        car_sales_df_cost = self.combine_cost_columns()
        car_sales_revenue_make = car_sales_df_cost.groupby(["Make"])["Cost"].sum().sort_values(ascending=False).reset_index(name="TotalRevenue")
        return dict(zip(car_sales_revenue_make["Make"], car_sales_revenue_make["TotalRevenue"]))
        
    def cost_per_mile_of_mileage(self):
        """
        Uses a combined cost car sales table, a table with combined cost columns into one "Cost" column, and divides the "Cost" column
        """
        car_sales_df_cost = self.combine_cost_columns()
        return round((car_sales_df_cost["Cost"] / car_sales_df_cost["Mileage"]).mean(), 2)
    
    def percent_of_cars_sold_above_mileage(self, mileage):
        return round(((len(self.car_sales_df.loc[(self.car_sales_df["Mileage"] >= mileage)]) / len(self.car_sales_df)) * 100), 2)
        
    def percent_of_cars_sold_below_mileage(self, mileage):
        return round(((len(self.car_sales_df.loc[(self.car_sales_df["Mileage"] <= mileage)]) / len(self.car_sales_df)) * 100), 2)
    
    def percent_of_cars_sold_between_mileage(self, mileage_low, mileage_high):
        return round(((len(self.car_sales_df.loc[(self.car_sales_df["Mileage"] >= mileage_low) & (self.car_sales_df["Mileage"] <= mileage_high)]) / len(self.car_sales_df)) * 100), 2)