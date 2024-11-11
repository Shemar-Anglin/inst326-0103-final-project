import re
import random
import argsparse


class temporaryName:
    """temporary class docstring"""
    
    def manage_system_events(file_path, change_log_file=None):
        """Manages system events through a series of nested functions that allow
        users to add events, and records the changes in a log.

        Args:
            file_path (str): the path to the file where system events are logged
            change_log_file (str, optional): The path to the file where changes 
                are recorded. Default is None.
        Nested Functions:
            get_last_event_information: Retrieves the details of the last event
                from theevents txt file.
            format_given_date_and_time: changes date and time into a standard
                format.
            change_log_record: records the changes that are made and is saved in 
                a separate file.
            add_system_event: Handles user input to ad system events and up date
                the change log.

        Side Effects:
            Continuous loop to prompt the user to enter the requested 
                information.
            Reads the given txt file and writes to the given txt files when
                neccessary.
        
        """
        
        event_categories = {
            "Error":["Represents errors that occur on the system.",
                    "EX: Appllication \"XYX\" failed to start"
            ],
            "Warning":["Indicates warning conditions.",
                    "EX: Temperature warning: CPU overheating."
                
            ],
            "Update":["Represents instances of updates made on the system.",
                    "EX: Driver update for graphics card completed"
            ],
            "Security":["Security events that occured on the system",
                        "EX: Unauthorized login attempt"   
            ]
        }
        
        def get_last_event_information():
            """Retrieves the last date, time, and ID of the last event.

            Raises:
                FileNotFoundError: If teh specified file is not found.

            Returns:
                Opens and reads the event file to extract information.
            """
            
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                    final_entry = lines[-1].strip().split(" | ")
                    final_date_time = final_entry[0]
                    final_id_of_final_line = final_entry[2]
                    
                    return final_date_time, final_id_of_final_line
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"File \"{file_path}\" not found. Try again."
                )
                
        def format_given_date_and_time(date, time):
            """Formats the provided date and time into a standard 
                'YYYY-MM-DD HH:MM:00' format.

            Args:
                date (str): The date that is in MMDDYYYY format.
                time (str): The time that is in HHMM format.

            Raises:
                ValueError: If the date or time is invalid and/or not in the
                    expected ranges.

            Returns:
                str: The formattedd date and time as one simple string.
            """
            
            if len(date) != 8 or len(time) != 4:
                raise ValueError("INVALID DATE AND/OR TIME FORMAT!\n")
            else:
                month, day, year = date[:2], date[2:4], date[4:]
                hour, minute = time[:2], time[2:]

                if not (0 <= int(hour) < 24 and 0 <= int(minute) < 60):
                    raise ValueError(
                        "INVALID TIME! Hour must be 00-23, minute 00-59.\n"
                    )
                formatted_date = f"{year}-{month}-{day}"
                formatted_time = f"{hour}:{minute}:00"
                return formatted_date + " " + formatted_time
            
        def change_log_record(
            user_name, change_type, priority_level, description
        ):
            """Records every change that is made in by the user, the type of
                change, the prority level, and the description of the events.

            Args:
                user_name (str): The name of the user that is making the change.
                change_type (str): Type of change being made.
                priority_level (stf): The priority level of the event.
                description (str): Short description of the change being made.
                
            Side Effects:
                Appends a new entry to the  change log file and/or creates that
                    file if it does not exist.
            """
            
            if change_log_file is None:
                change_log_file_path = "default_system_made_change_log.txt"
            else:
                change_log_file_path = change_log_file
            
            try:
                with open(change_log_file_path, 'r') as log_file:
                    lines = log_file.readlines()
                    log_number = len(lines) + 1
            except FileNotFoundError:
                with open(change_log_file_path, 'w') as log_file:
                    pass
                log_number = 1
                
            with open(change_log_file_path, 'a') as log_file:
                new_entry = (
                    f"{log_number}. | {user_name} | {change_type} | "
                    f"{priority_level} | {description}\n"
                )
                log_file.write(new_entry)
        
        def add_system_event():
            """Prompts the user to ass a new system event, calls on the other
            functions to validate and format inputs, and writes the event
            details to the event file and updates the change log.
            
            Raises:
                ValueError: If the date and time inputs are not in the correct
                    format.
                Exception: For unprecedented errors.
                
            Side Effects:
                Prompts the user for input.
                Validates and formats the input from the user
                Writes the details of the events to the event file
                Updates the change log for every addition that occurs
            """
            
            try:
                date = input("Enter today's date (MMDDYYYY): \n").strip()
                time = input(
                    "Enter the current military time (HHMM): \n"
                ).strip()
                formatted_date_and_time = format_given_date_and_time(date, time)

                while True:
                    event_type = input(
                        f"Enter category: {list(event_categories.keys())}: "
                    ).strip().capitalize()
                    
                    if event_type in event_categories:
                        break
                    print(
                        "Invalid category. Choose predefined categories: "
                        f"{list(event_categories.keys())}\n"
                    )

                while True:
                    priority = input(
                        "What is the priority level (High/Low): \n"
                    ).strip().capitalize()

                    if priority in ["High", "Low"]:
                        break
                    print(
                        "Invalid priority level, enter \"High\" or \"Low\"\n"
                    )
                    
                event_description = input(
                    "Enter a short description of the event: \n"
                ).strip()
                user_name = input("Enter your name (for records): \n").strip()
                
                _, last_id = get_last_event_information()
                next_event_id_number = int(last_id[2:]) + 1
                next_event_id = f"ID{next_event_id_number}"
                
                new_event = (
                    f"{formatted_date_and_time} | {event_type} | "
                    f"{next_event_id} | {event_description}"
                )
                
                with open(file_path, 'a') as file:
                    file.write(new_event + "\n")
                print("SUCCESS! The event has been added\n")
                
                change_log_record(
                    user_name, "Add Event", priority, 
                    f"Added '{event_type}' Event"
                )
                
            except ValueError as i:
                print(f"Input Error: {i}")
            except Exception as e:
                print(f"An unexpected error has occured: {e}")
        
        while True:
            try:
                print(
                    "Choose an option:\n1. Add an event of your own\n2. Exit\n"
                )

                choice = input("Enter your choice (1/2): ").strip()
                
                if choice not in ["1", "2"]:
                    raise ValueError(
                        "Invalid choice! Please enter '1' or '2'.\n"
                    )

                if choice == '1':
                    add_system_event()
                elif choice == '2':
                    print("Exiting the program. Goodbye!")
                    break
            except ValueError as e:
                print(e)
            
            
        pass

    def summary(self):
        """ Cam's function allows users to see a summary of events that can be customized.
        Args:
            coming soon...
        Side effects:
            prints user's customized summary into the console.
        """
        pass

    def function_three():
        """This is Neha's function
        
        Side effects:
        
        Returns:
        """
        abc = "123"
        pass
        
    def id_warning_patterns(file_path, pattern_length=3):
        """  Identifies patterns of warning events in the log file.
        Parameters:
            file_path (str): Path to the file.
            pattern_length (int): Number of warning events to form a pattern. Default is 3.
        Returns:
            dict: Patterns with occurrences greater than 1.
        """
        warning_patterns = {}  

    with open(file_path, 'r') as file:
        logs = file.readlines()

    event_sequence = []

    for line in logs:
        parts = [part.strip() for part in line.split('|')]
        if len(parts) < 4:
            continue

        event_type = parts[1]
        event_desc = parts[3]

        if event_type == "Warning":
            event_sequence.append((event_type, event_desc))

        if len(event_sequence) >= pattern_length:
            
            pattern = tuple(event_sequence[-pattern_length:])

            warning_patterns[pattern] = warning_patterns.get(pattern, 0) + 1

    significant_patterns = {pattern: count for pattern, count in warning_patterns.items() if count > 1}
    return significant_patterns

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify recurring warning patterns in a log file.")
    parser.add_argument("log_file", type=str, help="Path to the log file")
    parser.add_argument("--pattern_length", type=int, default=3, help="Number of warning events to form a pattern (default is 3)")
    
    args = parser.parse_args()

    patterns = id_warning_patterns(args.log_file, pattern_length=args.pattern_length)

    for i, (pattern, count) in enumerate(patterns.items(), start=1):
        events = " -> ".join(f"{event[1]}" for event in pattern) 
        print(f"{i}. Pattern: {events} | Occurrences: {count}")

        

    def function_five():
        """This is Christie's function."""
        
        temp_dict = {}
