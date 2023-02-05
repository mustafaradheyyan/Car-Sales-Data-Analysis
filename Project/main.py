## Author: Mustafa Radheyyan
## Date: 02/02/2023
## Assignment: Cognixia JUMPro Python Project 3 - Queries

import car_sales.car_sales as cs

def print_dictionary_values(dictionary: dict):
    for key, value in dictionary.items():
        print(f"\n\n{key}:\n\n{value}\n\n")

def print_aggregate_value_result(aggregate_values):
    if aggregate_values:
        for dictionary in aggregate_values:
            for key in dictionary.keys():
                for calculations in dictionary[key]:
                    print_dictionary_values(calculations)

def main():
    car_sales = cs.CarSales()
    
    car_sales.clean_data()
    # car_sales.print_data()
    # car_sales.print_data_snippet()
    # car_sales.print_data_types()
    # print(car_sales.get_min_values())
    # print(car_sales.get_max_values())
    # print_aggregate_value_result(car_sales.group_by_id())
    # print_aggregate_value_result(car_sales.group_by_color_id())
    # car_sales.get_aggregate_values()
    # print(car_sales.lowest_avg_cost_color())
    # print(car_sales.highest_avg_cost_color())
    # print(car_sales.most_common_color_per_vehicle_type())
    # print_aggregate_value_result(car_sales.get_aggregate_values())
    # car_sales.get_boolean_values()
    # car_sales.get_boolean_values()
    # print(car_sales.sort_by_purchase_date())
    # car_sales.get_custom_query()
    # print(car_sales.min_cost_and_min_mileage(100000, 100000))
    # print(car_sales.max_cost_and_max_mileage(20000, 50000))
    
    print(car_sales.revenue_by_make())
    # print(car_sales.cost_per_miles())
    # print(car_sales.percent_of_cars_sold_above_mileage(100000))
    # print(car_sales.percent_of_cars_sold_below_mileage(100000))
    # print(car_sales.percent_of_cars_sold_between_mileage(50000, 100000))
    
    # car_sales.get_custom_query()
    # car_sales.get_custom_query()

if __name__ == "__main__":
    main()