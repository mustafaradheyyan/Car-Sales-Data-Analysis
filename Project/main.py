## Author: Mustafa Radheyyan
## Date: 02/02/2023
## Assignment: Cognixia JUMPro Python Project 3 - Queries

import car_sales.car_sales as cs

def print_aggregate_value_result(aggregate_values):
    if aggregate_values:
        for dictionary in aggregate_values:
            for key, value in dictionary.items():
                for calculations in dictionary[key]:
                    for key, value in calculations.items():
                        print(f"\n\n{key}:\n\n{value}\n\n")

def main():
    car_sales = cs.CarSales()
    
    car_sales.clean_data()
    # car_sales.print_data()
    # car_sales.print_data_snippet()
    # car_sales.print_data_types()
    # print(car_sales.get_min_values())
    # print(car_sales.get_max_values())
    print_aggregate_value_result(car_sales.group_by_id())
    # print_aggregate_value_result(car_sales.get_aggregate_values())
    # car_sales.get_aggregate_values()
    # car_sales.get_boolean_values()
    # car_sales.get_boolean_values()
    # print(car_sales.sort_by_purchase_date())
    # car_sales.get_custom_query()
    # car_sales.get_custom_query()
    # car_sales.get_custom_query()

if __name__ == "__main__":
    main()