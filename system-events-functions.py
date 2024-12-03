import re
import random
from argparse import ArgumentParser
import sys

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


    def summary (path):
        """ Displays a dictionary of the number of events then the user chooses a 
        review of an event type or a specific date to display events.
        Args:
            path(string): A path to the text file of event logs
        Side effects:
            prints dictionary, review, and time frames into the console.
        """
        events = ["Update", "Files", "Error", "Warning", "Security"]
        general_summ = {event: 0 for event in events}
        options = ["Review", "Time Frame"]
    
        with open(path, "r", encoding = "utf-8") as file:
            log_lines = [line.strip() for line in file]
            for line in log_lines:
                for event in events:
                    if event in line:
                        general_summ[event] += 1
  
        for event, num in general_summ.items():
            print(f"{event}: {num}")
    
        q1 = input("Enter a summary option (Review, Time Frame): ")

        if q1 not in options:
            print("Not an option")
            return

        if q1 == options[0]:
            q2 = input("Enter an event-type (Update, Files, Error, Warning, Security): ")

            if q2 not in events:
                print("Not an event type")
                return
        
            print(f"\nResults for {q1} - {q2}")
            for line in log_lines:
                if q2 in line:
                    print(line)
                
        if q1 == options[1]:
            m = [i for i in range(1,13)]
            d =  [i for i in range(1,32)]

            q3 = input("Enter a month (1-12): ")
            q3_int = int(q3)
            if q3_int not in m:
                print("Invalid month")
                return
        
            q4 = input("Enter a day (1-31): ")
            q4_int = int(q4)
            if q4_int not in d:
                print("Invalid day")
                return
            
            print(f"\nEvents from this date: {q3_int}-{q4_int}")
            for line in log_lines:
                date = line.split(" ")[0]
                month = date.split("-")[1]
                month_int = int(month)
                day = date.split("-")[2]
                day_int = int(day)
                if month_int == q3_int and day_int == q4_int:
                    print(line)
                
    def parse_args(arglist):
        """ Processes command line arguments. 
        Args:
            arglist (list of str): arguments from the command line.
    
        Returns:
            namespace: the parsed arguments, as a namespace.
        """
        parser = ArgumentParser()
        parser.add_argument("file", help="file containing the event logs")
        args = parser.parse_args(arglist)
        return args


    if __name__ == "__main__":
        args = parse_args(sys.argv[1:])
        summary(args.file)
             

    def extract_date_time(file_path):
        """
        Extracts the date and time from each event entry in a system event file
        
        Args: 
        file_path(str): The path to the system event file
        
        Returns:
        list of tuples: A list where each element is a tuple that contains
            the date and time of a system event
            
        Raises:
        FileNotFoundError: If the file cannot be found
        Exception: If an error happens during reading of the file or processing
        
        """
        regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})'
        extracted_dates_times = []
        
        try:
            with open(file_path, 'r') as f: 
                for line in f:
                    matches = re.findall(regex,line)
                    if matches:
                        for match in matches:
                            date_time = match. split()
                            date = date_time[0]
                            time = date_time[1]
                            extracted_dates_times.append ((date, time))
        except FileNotFoundError:
            raise FileNotFoundError("The file is not found")
        except Exception:
            raise Exception ("There is an error")
        return extracted_dates_times

                            
                            
                    
        
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

        

    def event_sequence(file_path):
        """A function to find the most common order of system events within the
        txt file.  
        
        Args: 
            file_path (str): name of the file that will be read to get the
                system events information for. 
        
        Returns:
            The top three most common sequences of events as strings. 
                Format: 
                "Top 3 most common sequences:"
                "event1, event2, event3"
                "event6, event3, event2"
                "event1, event2"
        
        Side effects: 
            Adds/modifies the keys and values of "count" dictionary (mutable)
                when seeing what sequences of events have occurred.  
        """
        
        # will include all the event descriptions/entries within the file to be
        # sorted afterwards
        entire_descriptions = []

        with open(file_path, "r", encoding="utf-8") as f: 
            regex = r"[^|]+(?=\s*$)"
            
            for line in f:
                # getting only the event description from the lines using the
                    # regular expression above
                matches = re.search(regex, line)
                
                # if matches the filtering criteria (meaning is the "event
                    # description")
                if matches: 
                    for match in matches: 
                        # get rid of whitespace from before first word of
                            # description starts
                        event_desc = match.strip()

                # adding event descriptions from each line to list that will
                    # hold all descriptions
                entire_descriptions.append(event_desc)
                
                    
        # count dictionary will keep track of how many times a certain sequence
            # appears in the following format:
            # sequence of events: number of times sequence has occured
            # {event 1, event 2, event 3: 4}
        count = {}
        
        # need to figure out what sequences exist within the file 
        
        # goes through each event description
        for event_desc in entire_descriptions:
             

            
            
            
            
            
            
            
            # if that sequence does not exist yet as a key, then add 1 to the 
                # current number of occurences
                # (eg: if "event1, event 2" is not a key)
            if individual_sequence in count:
            # if that sequence does exist already as a key, then add 1 to the 
                # current number of occurences
                count[individual_sequence] += 1
            # if the sequence does not exist as a key yet, set the number of
            # times it has occured to one (initalizes it)
            else: 
                count[individual_sequence] = 1
            
        # figuring out what are the most common sequences
                
        # sort sequences according to whichever ones have the highest number of 
            # occurences; list most common sequences at the top 
        ordered_sequences = sorted(max(individual_sequence), reverse = True)
        
        # getting the top three most common ones using slicing; gets everything
            # before the third index (meaning before the fourth most common
            # sequence, since ordered_sequences is going from highest occurrences
            # at the top of the list to lowest number of occurrences)
        most_common_sequences = ordered_sequences[:3]
        
        
        result_heading = ("Top 3 most common sequences:" + "\n")
        
        # creating empty string for all sequences to go into
        result_content = ""
        
        for individual_sequence in most_common_sequences:
            # if not all the top 3 sequences have been added, add a new line
                # before the next sequence
            if individual_sequence < 3:
                result_content.append(individual_sequence + "\n")
            else:
                # add last sequence
                result_content.append(individual_sequence)
                
        return result_heading, result_content