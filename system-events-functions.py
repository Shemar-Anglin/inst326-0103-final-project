import re
from argparse import ArgumentParser
import sys

class SystemEventsManager:
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
        
        
    def extract_date_time(self, file_path):
        """
        Extracts the date and time from each event entry in a system event file.

        Args: 
            file_path(str): The path to the system event file.
            
        Returns:
            list of tuples: A list where each element is a tuple that contains
                the date and time of a system event.
            
        Raises:
            FileNotFoundError: If the file cannot be found.
            Exception: If an error happens during reading of the file or processing.
            
        Side Effects:
            Prints the extracted dates and times to the console in the format:
                "Extracted Dates and Times:" outputs a list of (Date, Time) tuples
        """
        regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})'
        extracted_dates_times = []

        try:
            with open(file_path, 'r', encoding="utf-8") as f: 
                for line in f:
                    matches = re.findall(regex, line)
                    if matches:
                        for match in matches:
                            date_time = match.split()
                            date = date_time[0]
                            time = date_time[1]
                            extracted_dates_times.append((date, time))
        except FileNotFoundError:
            raise FileNotFoundError("The file is not found.")
        except Exception:
            raise Exception("There is an error.")

        print("Extracted Dates and Times:")
        for date, time in extracted_dates_times:
            print(f"(Date: {date}, Time: {time})")

        return extracted_dates_times

    def keyword_search(self, file_path):
        """
        Allows users to search for and view specific event types from 
        the txt file. This function prompts the user to input an event type 
        (e.g., Error, Warning) and a required keyword to filter event 
        descriptions. Then processes the file to display matching events with 
        their details, such as the date, event type, event ID, and description.
        It also tracks and displays events and keywords previously 
        viewed during the session.

        Args:
            file_path (str): Path to the txt file that contains system events.

        Side effects:  
            - Prompts the user for input (event type and keyword).
            - Reads and processes the log file to find matching events.
            - Prints matching event details (search results) to the console, 
              including event date, type, ID, and description.
            - Prints error messages to the console if the file is not found 
              or if an unexpected error occurs.
            - Prints previously searched keywords and events if the user opts 
              to view them.
            - Prints confirmation messages when an event is found or if no 
                events match the search criteria.
            - Prints instructions to the console to guide the user.
        
        Raises:
            FileNotFoundError: If the file is not found.
            Exception: If any other unexpected error occurs 
        """
        event_history = []  
        keyword_history = []  

        # Instructions for the user
        print("Welcome to keyword search. Please follow the prompts to search "
              "for specific event types and descriptions.")
        print(
    "You are required to enter a keyword to filter event descriptions.")
        print("Examples of keywords: 'saved', 'deleted', 'CPU', 'Game', "
              "'presentation'.")
        print("You also have the option to view previously searched events and"
              " keywords during the session.")

        while True:
            try:
                # Ask the user what kind of event they want to search for
                event_type = input(
                    "Enter the event type you want to search for "
                    "(e.g., Error, Update, Warning, Security, Files): "
                ).strip()

                # Ask the user for a keyword 
                while True:
                    keyword = input(
    "Enter keyword to filter descriptions:"
).strip()
                    if keyword:
                        break
                    else:
                        print("Keyword is required. Enter a valid keyword.")
                
                # Add the keyword to keyword history (avoid duplicates)
                if keyword not in keyword_history:
                    keyword_history.append(keyword)

                with open(file_path, 'r') as file:
                    event_found = False
                    print("\nSearch Results:")

                    for line in file:
                        parts = line.split('|')
                        
                        if (
                            len(parts) > 3 
                            and event_type.lower() in parts[1].strip().lower()
                        ):
                            # Extract the event details
                            date_time = parts[0].strip()  
                            event = parts[1].strip()  
                            event_id = parts[2].strip() 
                            description = parts[3].strip()  
                            
                            if keyword.lower() not in description.lower():
                                continue
                            event_details = (
    f"{date_time} | {event} | {event_id} | {description}"
)
                            # Print the matching event
                            print(f"\n{event_details}")
                            event_found = True
                            
                            # Add the event to the event history
                            if event_details not in event_history:
                                event_history.append(event_details)
                    print(
    "\nNo events found matching." if not event_found else ""
)

                # Ask the user if they want to see 
                # previously searched events and keywords
                view_history = input(
    "\nDo you want to view previously searched events and keywords? (yes/no): "
).strip().lower()
                if view_history == 'yes':
                    if keyword_history:
                        print("\nPreviously Searched Keywords:")
                        print(", ".join(keyword_history))
                    else:
                        print("\nNo previously searched keywords found")
                    
                    if event_history:
                        print("\nPreviously Viewed Events:")
                        for event in event_history:
                            print(event)
                    else:
                        print("\nNo previously viewed events found")
                    

                # Ask the user if they want to search again or exit
                continue_search = input(
                    "\nDo you want to search again? (yes/no): "
                ).strip().lower()
                if continue_search != 'yes':
                    print("Exiting search.")
                    break
            
            except FileNotFoundError:
                print(f"Error: The file '{file_path}' was not found.")
                break  
            except Exception as e:
                print(f"An error occurred: {e}")
                break  


def parse_args(arglist):
    """ Processes command line arguments. 
    Args:
    arglist (list of str): arguments from the command line.
    
Returns:
    namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("file_path", help="file containing the event logs")
    args = parser.parse_args(arglist)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    
    # create an instance of the temporaryName class
    temp_obj = temporaryName()  
    
    # calls extract_date_time 
    temp_obj.extract_date_time(args.file_path)

    # call keyword_search 
    temp_obj.keyword_search(args.file_path)

    
    def id_warning_patterns(file_path, pattern_length=3):
        """  
        Identifies patterns of warning events in the log file.

        Parameters:
            file_path (str): Path to the file.
            pattern_length (int): Number of warning events to form a pattern. Default is 3.

        Returns:
            dict: Patterns with occurrences greater than 1.
        """
            
        warning_patterns = {} # Dictionary to store patterns and their counts

        with open(file_path, 'r') as file:
            logs = file.readlines()

        event_sequence = []

        for line in logs:
            parts = [part.strip() for part in line.split('|')]
            if len(parts) < 4:
                continue

            event_type = parts[1]
            event_desc = parts[3]

            # Append to sequence if it's a "Warning" event
            if event_type == "Warning":
                event_sequence.append((event_type, event_desc))

            # Only check for patterns if we have enough warning patterns to account for.
            if len(event_sequence) >= pattern_length:

                # Create a pattern from the last 'pattern_length' warning events
                pattern = tuple(event_sequence[-pattern_length:])
                
                # Increase the count of pattern, initilizing if necessary 
                warning_patterns[pattern] = warning_patterns.get(pattern, 0) + 1
        
        # Use comprehension to filter patterns occurring more than once
        significant_patterns = {pattern: count for pattern, count in warning_patterns.items() if count > 1}
        return significant_patterns



    log_file_path = "spring2024_system_events.txt"
    pattern_length = 3

    # Call function with parsed arguments 
    patterns = id_warning_patterns(log_file_path, pattern_length=pattern_length)

    # Display patterns using sequence unpacking and f-strings
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
        The top three most common sequences of events as strings in tuples with
            the number of occurences listed after the sequences. 
                Format (note: is along the lines of what looking to output,
                numbers/sequences below are not exact): 
                    "Top 3 most common sequences:
                    (event1, event2, event3): 28
                    (event6, event3, event2): 16
                    (event1, event2): 15"
        
    Side effects: 
        Adds/modifies the keys and values of "count" dictionary (mutable) when
            seeing what sequences of events have occurred.  

    Attribution:
        The Python Software Foundation (2024) 4.3. The range() Function
            (Version 2) [Source code].
            https://umd.instructure.com/courses/1374047/assignments/syllabus.
        (link accessed/found through "4. More Control Flow Tools" link in
            "Prerequisite knowledge" module in Professor Aric Bill's INST326
            Fall 2024 syllabus)
        
        Used range() function under section 4.3 from following examples:
            Source code snippet 1:
                "list(range(5, 10))"
            Source code snippet 2: 
                "a = ['Mary', 'had', 'a', 'little', 'lamb']
                for i in range(len(a))"

        My modifications:
            "for len_of_sequence in range(2, len(entire_descriptions))" and
            "for start_point in
                range(0, len(entire_descriptions) - len_of_sequence)" - combined
                both source code snippets to include searching within a range
                for both regular numeric values (2) and the length of a list
                (len(entire_descriptions)).
            
        More information about why/how used source code in program in PDF documentation for final submission.
        """

        # will include all the event descriptions/entries within the file to be
            # sorted afterwards
        entire_descriptions = []

        
        with open(file_path, "r", encoding="utf-8") as f:
            # capturing group that matches one or more characters from the end
                # of line in the file that is not separator character (|) 
            regex = r"([^|]+)$"
            
            for line in f:
                matches = re.search(regex, line)
                
                # if matches the filtering criteria (meaning is the "event
                    # description")  
                if matches:
                    # gets entire match object and strips the whitespace, not
                        # including the spaces between words (before stripping,
                        # is exactly " System update completed" from regex)
                    event_desc = matches.group(0).strip()
                    entire_descriptions.append(event_desc)

        
        # empty dictionary for now, but will be in following the format later:
        # count = {
            # sequence1: number of times sequence has occurred
            # sequence2: number of times sequence has occurred
            # etc.}
        count = {}

        
        # goes through all possible sequence lengths that can occur until have
            # gone through all of the events in the file (range starts at 2
            # since at least two events need to be listed to be considered a
            # sequence)
                # (in other words: one event is not a sequence since it's by itself)
        for len_of_sequence in range(2, len(entire_descriptions)):

            
            # now actually going through each event sequence to see what events
                # different sequences can contain (like what events come after
                # each other)
            # starting at first event in list of event descriptions (index 0)
                # and iterates until the last line/event (minus the length of 
                # sequences we're trying to find) in order to prevent the the indexes
                # from going out of bounds
                    # (eg: if we have a list of 6 event_desc in
                    # entire_descriptions,
                        # entire_descriptions =
                            # [event1, event2, event3, event4, event5, event6]
                        # as the len_of_sequence = 2 and our start_point is 0,
                            # we will look at two events in a row during loop
                            # (event1 and event2), then (event2 and event3), etc.)
                        # when len_of_sequence = 3 and our start_point is 0, 
                            # will look at (event1, event2, event3), then
                            # (event2, event3, event4), etc.
                        
                        # "(len(entire_descriptions) - len of sequence)"  
                            # minusing len_of_sequence determines number of
                            # iterations that will go through when indexing
                            # through events
                        # going back to example with 6 events in
                            # entire_descriptions and inputting into
                            # "(len(entire_descriptions) - len of sequence)", 
                            
                            # 6 (num of events in list) - 2 (max # of events in
                                # individual sequence) = 4 (num of interations)
                        # will complete 4 iterations to find the sequences for
                            # those six numbers
                            # iterations = (event1,event2), (event2,event3) ...
                                            # iteration 0         iteration 1
                                            # (since start_point
                                                # is 0)
                        # (will end at finding (event 5, event 6) since length of
                            # list is 6 and next iteration would be (event6, event7)
                            # which does not exist)
            for start_point in range(0, len(entire_descriptions) -
                len_of_sequence):
                

                # need to put found sequences in tuples b/c tuples allow to use
                    # the sequences as keys in the "count" dictionary (which 
                    # then allows to look up number of occurences per sequence)
                #"[start_point:start_point + len_of_sequence]" - if start_point
                    # = 0, and len_of_sequence = 2, this determines the limit of
                    # the number of elements in the sequence we are looking at
                individual_sequence = tuple(entire_descriptions
                    [start_point:start_point + len_of_sequence])
                                                    # from eg: [0: 0 + 2]
                                                        # start at index 0 and
                                                        # go through events in
                                                        # range, excluding event/
                                                        # endpoint which we
                                                        # don't want to count
                                                        # eg: event1, event2,
                                                            # event3
                                                        # counts (event1,event2)
                                                            #    (index0,index1)
                                                        # but doesn't count
                                                            # event3
                                                            # (index2)
                                                        
                                                        
                # if that sequence already exists as a key, then add 1 to the
                    # current number of occurences
                    # (eg: if "event1, event 2" is not a key)
                if individual_sequence in count:
                    count[individual_sequence] += 1
                # if the sequence does not exist as a key yet, set the number of
                    # times it has occured to one
                    # (initalizes it/the count)
                else:
                    count[individual_sequence] = 1

            
            # "count.items()" - allows iteration over keys/val in "count" dict
            # "lambda x: x[1]" - looking at first index/sorting by number of
                # occurrences (index 0 = sequence itself)
            # "reverse = True" - sorts from descending order (most common sequences
                # at top)
        ordered_sequences = sorted(count.items(), key=lambda x: x[1],
                                   reverse=True)

            
            # getting the top three most common sequences using slicing; gets
                # everything before the third index
                # (meaning everything before the fourth most common sequence
                # since indexes start at 0)
        most_common_sequences = ordered_sequences[:3]

        result_heading = "Top 3 most common sequences:\n"
        result_content = ""

            # for each key/value pairs for the top 3 most common sequences,
        for individual_sequence, num_occurences in most_common_sequences:
                # add those pairs to what we're going to be outputting
            result_content += f"{individual_sequence}: {num_occurences}\n"
    
        return result_heading + result_content
    
    
    if __name__ == "__main__":
        file_path = "spring2024_system_events.txt"
        
        result = event_sequence(file_path)
        print(result)
    
    
    def main_menu(self, file_path, path):
        "temporary docstring"
        
        print("Welcome to Analyzing System Events!")
        
        print("Please select one of the functions to run:")
        print("1. manage_system_events") # Shemar's first and second func
                                         # included (has multiple functions)
        print("2. summary") # Cam's first function
        print("3. extract_date_time") # Neha's first function
        print("4. id_warning_patterns") # Stephany's first function
        print("5. keyword_search") # Neha's second func
        print("6. event_sequence") # Christie's first func
        
        print("7. name") # Cam's second func
        print("8. name") # Stephany's second func
        # this function itself is already Christie's second function, so that's
            # why it's not listed  

        
        # missing:
            # cam's second func name
            # stephany's second func name

        # if have time, try putting this func in a loop so that it can ask if want to run another function after one runs
        
        # get rid of any whitespace when user writes their input
        function_choice = input("Enter corresponding function number \
            (1, 2, 3, 4, 5, 6, 7, 8): ").strip().lower()
        
        if function_choice == "1":
            # run the corresponding function
            print("\n Function number 1/manage_system_events(): \n")
            self.manage_system_events(file_path)
        elif function_choice == "2":
            print("\n Function number 2/summary(): \n")
            self.summary(path)
        elif function_choice == "3":
            print("\n Function number 3/extract_date_time(): \n")
            self.extract_date_time(file_path)
        elif function_choice == "4":
            print("\n Function number 4/id_warning_patterns(): \n")        
            
            patterns = self.id_warning_patterns(file_path)

            # running what the function I am referencing (id_warning_patterns)
                # did to display the results of their own function
            # Original function portion:
            # Call function with parsed arguments 
            # patterns = id_warning_patterns(log_file_path,
                # pattern_length=pattern_length)
        
            # Display patterns using sequence unpacking and f-strings
            # for i, (pattern, count) in enumerate(patterns.items(), start=1):
            #     events = " -> ".join(f"{event[1]}" for event in pattern) 
            #     print(f"{i}. Pattern: {events} | Occurrences: {count}")
            
            for i, (pattern, count) in enumerate(patterns.items(), start=1):
                events = " -> ".join(f"{event[1]}" for event in pattern) 
                print(f"{i}. Pattern: {events} | Occurrences: {count}")

        
            
        elif function_choice == "5":
            self.keyword_search(file_path)
        elif function_choice == "6": 
            self.event_sequence(file_path)
        elif function_choice == "7":
            self.name1() # Cam's second func (need name)
        elif function_choice == "8":
            self.name2() # Stephany's second func (need name) 
        else: 
            print("Please enter a valid function number (1, 2, 3, 4, 5, 6, 7, 8).")


        file_path = "spring2024_system_events.txt"
        path = "spring2024_system_events.txt"

        example = temporaryName()
        example.main_menu(file_path, path)