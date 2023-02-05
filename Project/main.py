## Author: Mustafa Radheyyan
## Date: 02/02/2023
## Assignment: Cognixia JUMPro Python Project 3 - Queries

import car_sales.car_sales as cs
import database.curd as dbc

def print_dictionary_values(dictionary: dict):
    for key, value in dictionary.items():
        print(f"\n\n{key}:\n\n{value}\n\n")

def print_aggregate_value_result(aggregate_values, *args):
    if aggregate_values:
        for dictionary in aggregate_values:
            for key in dictionary.keys():
                for calculations in dictionary[key]:
                    print_dictionary_values(calculations)
    print(*args)

def post_cleaning_data_exploration(car_sales: cs.CarSales):
    car_sales.print_data()
    car_sales.print_data_snippet()
    car_sales.print_data_types()
    print_aggregate_value_result(car_sales.get_aggregate_color_id(), cs.DASH_SEPARATOR)
    print_aggregate_value_result(car_sales.get_aggregate_non_int_columns(), cs.DASH_SEPARATOR)

def queries(car_sales: cs.CarSales):
    print(car_sales.get_min_values(), cs.DASH_SEPARATOR)
    print(car_sales.get_max_values(), cs.DASH_SEPARATOR)
    print(car_sales.lowest_avg_cost_color(), cs.DASH_SEPARATOR)
    print(car_sales.highest_avg_cost_color(), cs.DASH_SEPARATOR)
    print(car_sales.most_common_color_per_vehicle_type(), cs.DASH_SEPARATOR)
    print(car_sales.most_common_color_per_vehicle_make(), cs.DASH_SEPARATOR)
    print(car_sales.most_common_color_per_category("Model"), cs.DASH_SEPARATOR)
    print(car_sales.min_cost_and_min_mileage(100000, 100000), cs.DASH_SEPARATOR)
    print(car_sales.max_cost_and_max_mileage(20000, 50000), cs.DASH_SEPARATOR)
    print(car_sales.total_revenue_by_make(), cs.DASH_SEPARATOR)
    print(car_sales.cost_per_mile_of_mileage(), cs.DASH_SEPARATOR)
    print(car_sales.percent_of_cars_sold_above_mileage(100000), cs.DASH_SEPARATOR)
    print(car_sales.percent_of_cars_sold_below_mileage(100000), cs.DASH_SEPARATOR)
    print(car_sales.percent_of_cars_sold_between_mileage(50000, 100000), cs.DASH_SEPARATOR)

def main():
    car_sales = cs.CarSales()
    dbc.persist_dataset(car_sales.car_sales_df)
    car_sales.clean_data()
    
    while(True):
        try:
            user_choice = int(input("""
                            What do you want to do?
                            
                            1) View Post Cleaning Data Exploration
                            2) View Data Queries
                            3) Add Data to Car Sales Database Table
                            4) Update Data from Car Sales Database Table
                            5) Read Data from Car Sales Database Table
                            6) Delete Data from Car Sales Database Table
                            """))
        except ValueError:
            print("That is not a valid choice! (Must be an integer from 1-6)")
        else:
            if user_choice > 0 and user_choice < 7: 
                break
            else:
                print("That is not a valid choice! (Must be an integer from 1-6)")
    if user_choice == 1:
        post_cleaning_data_exploration(car_sales)
    elif user_choice == 2:
        queries(car_sales)
    elif user_choice == 3:
        dbc.add_data()
    elif user_choice == 4:
        dbc.update_data()
    elif user_choice == 5:
        dbc.read_data()
    elif user_choice == 6:
        dbc.delete_data()

if __name__ == "__main__":
    dbc.open_connection()
    main()
    dbc.close_connection()