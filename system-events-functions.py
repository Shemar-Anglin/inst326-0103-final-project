"""temporary script docstring"""

import re

class temporaryName:
    """temporary class docstring"""
    
    def function_one():
        """This is Shemar's function meant to do something in some way"""
        
        x = 1
        y = 2
        z = x + y
        
        
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
        
    def function_four():
        """ This function is Stephany's and what is does is calculate the number of events.
        Args:
            It does sosmething
        Returns:
            an integer
        """
        pass

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