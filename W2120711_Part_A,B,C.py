import csv

# Task A: Input Validation
def validate_date_input():
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")
        except ValueError:
            print("Integer required.")
    
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format mm: "))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - values must be in the range 1 to 12.")
        except ValueError:
            print("Integer required.")
    
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format yyyy: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required.")
    
    return day, month, year

def validate_continue_input():
    while True:
        user_input = input("Do you want to select a data file for a different date? Y/N: ").strip().upper()
        if user_input in ['Y', 'N']:
            return user_input
        else:
            print("Please enter 'Y' or 'N'.")

# Task B: Processed Outcomes
def process_csv_data(file_path):
    outcomes = {
        'total_vehicles': 0,
        'total_trucks': 0,
        'total_electric_vehicles': 0,
        'two_wheeled_vehicles': 0,
        'buses_north_elm_avenue': 0,
        'vehicles_both_junctions_no_turn': 0,  # Updated description
        'over_speed_limit': 0,
        'elm_avenue_vehicles': 0,
        'hanley_highway_vehicles': 0,
        'peak_hour_vehicles_hanley': 0,
        'peak_times_hanley': [],
        'rain_hours': set(),
        'total_bicycles': 0,  # Count total bicycles
        'average_bicycles_per_hour': 0, # Placeholder for average calculation
        'scooters_elm_avenue': 0,  # Count scooters at Elm Avenue
        'percentage_scooters_elm_avenue': 0  # Placeholder for scooter percentage
    }

    hourly_vehicles_hanley = {f'{hour:02d}:00-{hour+1:02d}:00': 0 for hour in range(24)}

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            outcomes['total_vehicles'] += 1

            if row['VehicleType'] == 'Bicycle':
                outcomes['total_bicycles'] += 1
            

            if row['travel_Direction_in'] == row['travel_Direction_out']:
                outcomes['vehicles_both_junctions_no_turn'] += 1
                
            if 'rain' in row['Weather_Conditions'].strip().lower():
                hour = row['timeOfDay'].split(':')[0]
                outcomes['rain_hours'].add(hour)  # Add hour to the set

            
            if row['elctricHybrid'].strip().lower() == 'true':
                outcomes['total_electric_vehicles'] += 1
            
            if row['VehicleType'] == 'Truck':
                outcomes['total_trucks'] += 1
            
            if row['VehicleType'] in ['Bicycle', 'Motorcycle', 'Scooter']:
                outcomes['two_wheeled_vehicles'] += 1
                
            if row['JunctionName'] == 'Elm Avenue/Rabbit Road' and row['VehicleType'] == 'Scooter':
                outcomes['scooters_elm_avenue'] += 1
            
            if (row['JunctionName'] == 'Elm Avenue/Rabbit Road' and 
                row['VehicleType'] == 'Buss' and 
                row['travel_Direction_out'] == 'N'):
                outcomes['buses_north_elm_avenue'] += 1
            
            if int(row['VehicleSpeed']) > int(row['JunctionSpeedLimit']):
                outcomes['over_speed_limit'] += 1

            if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                outcomes['elm_avenue_vehicles'] += 1
            elif row['JunctionName'] == 'Hanley Highway/Westway':
                outcomes['hanley_highway_vehicles'] += 1
                hour = int(row['timeOfDay'].split(':')[0])
                hourly_vehicles_hanley[f'{hour:02d}:00-{hour+1:02d}:00'] += 1

        outcomes['peak_hour_vehicles_hanley'] = max(hourly_vehicles_hanley.values())
        outcomes['peak_times_hanley'] = [
            time for time, count in hourly_vehicles_hanley.items()
            if count == outcomes['peak_hour_vehicles_hanley']
        ]
    outcomes['rain_hours'] = len(outcomes['rain_hours'])
    # Calculate average bicycles per hour if bicycles are recorded
    if outcomes['total_bicycles'] > 0:
        outcomes['average_bicycles_per_hour'] = round(outcomes['total_bicycles'] / 24)

    # Calculate percentage of scooters at Elm Avenue
    if outcomes['elm_avenue_vehicles'] > 0:
        outcomes['percentage_scooters_elm_avenue'] = round(
            (outcomes['scooters_elm_avenue'] / outcomes['elm_avenue_vehicles']) * 100
        )
    return outcomes


# Task C: Save Results
def save_results_to_file(outcomes, file_name="results.txt", selected_file=""):
    with open(file_name, 'a') as file:
        file.write(f"data file selected is {selected_file}\n")
        file.write(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}\n")
        file.write(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}\n")
        file.write(f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}\n")
        file.write(f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}\n")
        file.write(f"The total number of Buses leaving Elm Avenue/Rabbit Road North is {outcomes['buses_north_elm_avenue']}\n")
        file.write(f"The total number of vehicles through both junctions not turning left or right is {outcomes['vehicles_both_junctions_no_turn']}\n")
        file.write(f"The percentage of vehicles recorded that are trucks for this date is {round(outcomes['total_trucks'] / outcomes['total_vehicles'] * 100)}%\n")
        file.write(f"The average number of bicycles per hour is {outcomes['average_bicycles_per_hour']}\n")
        file.write(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['over_speed_limit']}\n")
        file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['elm_avenue_vehicles']}\n")
        file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['hanley_highway_vehicles']}\n")
        file.write(f"{outcomes['percentage_scooters_elm_avenue']}% of vehicles recorded through Elm Avenue/Rabbit Road that are scooters. \n")  
        file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_vehicles_hanley']}\n")
        file.write(f"The most vehicles through Hanley Highway/Westway were recorded between {', '.join(outcomes['peak_times_hanley'])}\n")
        file.write(f"The number of hours of rain for this date is {outcomes['rain_hours']}\n")
        
        file.write('-' * 50 + '\n')
        



def main():
    base_path = "C:/Users/Akil/Documents/IIT/1 Year/Programming/Tutorial/CW part A,B,C/"

    while True:
        day, month, year = validate_date_input()
        file_name = f"traffic_data{day:02d}{month:02d}{year} (1).csv"
        full_file_path = base_path+file_name
        
        try:
            outcomes = process_csv_data(full_file_path)
            save_results_to_file(outcomes, selected_file=file_name)

            # Printing the output directly to the console
            print("-" * 50)
            print(f"data file selected is {file_name}")
            print(f"The total number of vehicles recorded for this date is {outcomes['total_vehicles']}")
            print(f"The total number of trucks recorded for this date is {outcomes['total_trucks']}")
            print(f"The total number of electric vehicles for this date is {outcomes['total_electric_vehicles']}")
            print(f"The total number of two-wheeled vehicles for this date is {outcomes['two_wheeled_vehicles']}")
            print(f"The total number of Buses leaving Elm Avenue/Rabbit Road North is {outcomes['buses_north_elm_avenue']}")
            print(f"The total number of vehicles through both junctions not turning left or right is {outcomes['vehicles_both_junctions_no_turn']}")
            print(f"The percentage of vehicles recorded that are trucks for this date is {round(outcomes['total_trucks'] / outcomes['total_vehicles'] * 100)}%")
            print(f"The average number of bicycles per hour is {outcomes['average_bicycles_per_hour']}")
            print(f"{outcomes['percentage_scooters_elm_avenue']}% of vehicles recorded through Elm Avenue/Rabbit Road that are scooters.")
            print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['over_speed_limit']}")
            print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['elm_avenue_vehicles']}")
            print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['hanley_highway_vehicles']}")
            print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['peak_hour_vehicles_hanley']}")
            print(f"The most vehicles through Hanley Highway/Westway were recorded between {', '.join(outcomes['peak_times_hanley'])}")
            print(f"The number of hours of rain for this date is {outcomes['rain_hours']}")
            print("-" * 50)
            
        except FileNotFoundError:
            print(f"File {file_name} not found. Please check the file.")
        
        if validate_continue_input() == 'N':
            print("End of run.")
            break

if __name__ == "__main__":
    main()
