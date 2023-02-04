import pandas as pd
from pathlib import Path
from data_cleaner.data_cleaner import DataCleaner

DASH_SEPARATOR = "\n" + ("-" * (178 * 2)) + "\n"
NUMERICAL_DTYPES = ["int64", "float"]

class CarSales():
    car_sales_file_path = Path("car_sales/car_sales_table.csv")
    car_sales_df = pd.read_csv(car_sales_file_path)
    car_sales_single_values = []
    
    def __init__(self):
        self.data_cleaner = DataCleaner()
        
    def print_data(self): print(f"Car Sales Table!{DASH_SEPARATOR}{self.car_sales_df}")
    
    def print_data_snippet(self): print(f"\nFirst 5 Rows of Car Sales Table!{DASH_SEPARATOR}{self.car_sales_df.head()}")
    
    def print_data_types(self): 
        print(f"\nData Types of Car Sales Table!{DASH_SEPARATOR}")
        self.car_sales_df.info()
        
    def clean_data(self):
        self.data_cleaner.drop_null_rows(self.car_sales_df, ["CostPrice"])
        self.data_cleaner.convert_columns_to_date(self.car_sales_df)
        self.car_sales_df["VehicleType"].replace("Saloon", "Sedan", inplace=True)
        self.car_sales_single_values = self.data_cleaner.remove_single_value_columns(self.car_sales_df)
        print(f"\nData Cleaned!{DASH_SEPARATOR}")
    
    def sort_by_column(self, column_name):
        return self.car_sales_df.sort_values(by=[column_name])
    
    def sort_by_purchase_date(self):
        return self.sort_by_column("PurchaseDate")
       
    def get_min_values(self):
        return [{column: self.car_sales_df[column].min()} for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column)]
        
    def get_max_values(self):
        return [{column: self.car_sales_df[column].max()} for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column)]
    
    def group_by_id(self):
        return [{column: [
            {"min": self.car_sales_df.groupby([column]).min(numeric_only=True)},
            {"max": self.car_sales_df.groupby([column]).max(numeric_only=True)},
            {"mean": self.car_sales_df.groupby([column]).mean(numeric_only=True)},
            {"median": self.car_sales_df.groupby([column]).median(numeric_only=True)},
            {"mode": self.car_sales_df.groupby([column]).agg(lambda x: x.value_counts().index[0])},
            {"sum": self.car_sales_df.groupby([column])[self.get_non_id_columns()].sum(numeric_only=True)},
            ]} for column in self.car_sales_df.columns if "ID" in str(column)]
    
    def group_by_color_id(self):
        column = "ColorID"
        return [{column: [
            {"min": self.car_sales_df.groupby([column])[self.get_non_id_columns()].min(numeric_only=True)},
            {"max": self.car_sales_df.groupby([column])[self.get_non_id_columns()].max(numeric_only=True)},
            {"mean": self.car_sales_df.groupby([column])[self.get_non_id_columns()].mean(numeric_only=True)},
            {"median": self.car_sales_df.groupby([column])[self.get_non_id_columns()].median(numeric_only=True)},
            {"mode": self.car_sales_df.groupby([column])[self.get_non_id_columns()].agg(lambda x: x.value_counts().index[0])},
            {"sum": self.car_sales_df.groupby([column])[self.get_non_id_columns()].sum(numeric_only=True)},
            ]}]
    
    def lowest_avg_cost_color(self):
        color_sales_by_cost_df = self.car_sales_df.groupby(["ColorID"])[self.get_cost_columns()].mean(numeric_only=True).sum(axis=1).sort_values()
        return {color_sales_by_cost_df.index[0]: color_sales_by_cost_df.iloc[0]}
    
    def highest_avg_cost_color(self):
        color_sales_by_cost_df = self.car_sales_df.groupby(["ColorID"])[self.get_cost_columns()].mean(numeric_only=True).sum(axis=1).sort_values(ascending=False)
        return {color_sales_by_cost_df.index[0]: color_sales_by_cost_df.iloc[0]}
    
    def most_common_color_per_vehicle_type(self):
        return self.car_sales_df.groupby(["VehicleType","ColorID"]).size()
    
    def get_cost_columns(self):
        return [column for column in self.car_sales_df.columns if self.car_sales_df[column].dtype in NUMERICAL_DTYPES and "ID" not in str(column) and "Mileage" not in str(column)]
    
    def get_non_id_columns(self):
        return [column for column in self.car_sales_df.columns if "ID" not in str(column)]
    
    def get_df_without_id_columns(self):
        id_columns = [column for column in self.car_sales_df.columns if "ID" in str(column)]
        return self.car_sales_df.drop(columns=id_columns)
        
    def get_aggregate_values(self):
        car_sales_df_no_id = self.get_df_without_id_columns()
        
        return [{column: [
            {"min": car_sales_df_no_id.groupby([column]).min(numeric_only=True)},
            {"max": car_sales_df_no_id.groupby([column]).max(numeric_only=True)},
            {"mean": car_sales_df_no_id.groupby([column]).mean(numeric_only=True)},
            {"median": car_sales_df_no_id.groupby([column]).median(numeric_only=True)},
            {"mode": car_sales_df_no_id.groupby([column]).agg(lambda x: x.value_counts().index[0])},
            {"sum": car_sales_df_no_id.groupby([column]).sum(numeric_only=True)},
            ]} for column in car_sales_df_no_id.columns if car_sales_df_no_id[column].dtype not in NUMERICAL_DTYPES]
        
    # def get_aggregate_values(self): pass
    def get_boolean_values(self): pass
    def get_boolean_values(self): pass
    def get_custom_query(self): pass
    def get_custom_query(self): pass
    def get_custom_query(self): pass