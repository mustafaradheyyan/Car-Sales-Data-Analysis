## Author: Mustafa Radheyyan
## Date: 02/02/2023
## Assignment: Cognixia JUMPro Python Project 3 - Queries

import car_sales.car_sales as cs
import database.curd as dbc

def get_user_input() -> int:
    RETRY_STRING = "That is not a valid choice! (Must be an integer from 0-6)"
    
    while(True):
        try:
            user_choice = int(input("""
                            What do you want to do? (type 0-6, followed by enter)\n
                            0) Quit the Program
                            
         Car Sales Dataset  1) Exploration 2) Queries
                            
         Car Sales Database 3) CREATE      4) UPDATE
                            5) READ        6) DELETE\n
                            """))
        except ValueError:
            print(RETRY_STRING)
        else:
            if user_choice >= 0 and user_choice < 7: 
                break
            else:
                print(RETRY_STRING)
    return user_choice

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
    print(cs.DASH_SEPARATOR, "\nMinimum numerical values:", car_sales.get_min_values(), cs.DASH_SEPARATOR)
    print("Maximum numerical values:", car_sales.get_max_values(), cs.DASH_SEPARATOR)
    print("Lowest average cost color ID:", car_sales.lowest_avg_cost_color(), cs.DASH_SEPARATOR)
    print("Highest average cost color ID:", car_sales.highest_avg_cost_color(), cs.DASH_SEPARATOR)
    print("Most common color ID per vehicle type:", car_sales.most_common_color_per_vehicle_type(), cs.DASH_SEPARATOR)
    print("Most common color ID per vehicle make:", car_sales.most_common_color_per_vehicle_make(), cs.DASH_SEPARATOR)
    print("Most common color ID per category (example argument is 'Model'):", car_sales.most_common_color_per_category("Model"), cs.DASH_SEPARATOR)
    print("Result of querying minimum cost (100,000) and minimum mileage values (100,000):", car_sales.min_cost_and_min_mileage(100000, 100000), cs.DASH_SEPARATOR)
    print("Result of querying maximum cost (20,000) and maximum mileage (50,000) values:", car_sales.max_cost_and_max_mileage(20000, 50000), cs.DASH_SEPARATOR)
    print("Total revenue by vehicle make:", car_sales.total_revenue_by_make(), cs.DASH_SEPARATOR)
    print("Average cost of sale per mile of vehicle mileage:", car_sales.cost_per_mile_of_mileage(), cs.DASH_SEPARATOR)
    print("Percent of cars sold above mileage (example argument is 100,000 miles):", car_sales.percent_of_cars_sold_above_mileage(100000), cs.DASH_SEPARATOR)
    print("Percent of cars sold below mileage (example argument is 100,000 miles):", car_sales.percent_of_cars_sold_below_mileage(100000), cs.DASH_SEPARATOR)
    print("Percent of cars sold between mileage (example argument is between 50,000-100,000 miles):", car_sales.percent_of_cars_sold_between_mileage(50000, 100000), cs.DASH_SEPARATOR)

def main():
    car_sales = cs.CarSales()
    dbc.persist_dataset(car_sales.car_sales_df)
    car_sales.clean_data()
    
    while(True):
        user_choice = get_user_input()
        
        if user_choice == 1:
            post_cleaning_data_exploration(car_sales)
        elif user_choice == 2:
            queries(car_sales)
        elif user_choice == 3:
            dbc.add_data(car_sales.car_sales_columns_list)
        elif user_choice == 4:
            dbc.update_data(car_sales.car_sales_columns_list)
        elif user_choice == 5:
            dbc.read_data()
        elif user_choice == 6:
            dbc.delete_data()
        else:
            break

if __name__ == "__main__":
    dbc.open_connection()
    main()
    dbc.close_connection()