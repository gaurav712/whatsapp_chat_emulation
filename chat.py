import sys
import math
import curses
import textwrap

## GLOBALS

perspective = ""

CURRENT_ROW = 0
MAX_ROWS = 0
MAX_COLUMNS = 0
DIALOGUE_PADDING = "                              "
WRAP_AT = 40

## FUNCTIONS

# To print to stderr
def perror(msg):
    print(msg, file=sys.stderr)

# Check if string is in Date Format i.e. dd/mm/yy
def is_date(text):
    if (text[:2].isnumeric() and text[2] == '/' and text[3:5].isnumeric() and
        text[5] == '/' and text[6:8].isnumeric()):
        return True
    return False

# Check if string is in Time Format i.e. hh:mm aa
def is_time(text):
    text = text.split()
    text = text[0].split(':')

    if (text[0].isnumeric() and text[1].isnumeric()):
        return True
    
    return False

# Check if its a marker i.e line where a new dialogue starts
def is_a_marker(text):

    # The line should be in the format "dd/mm/yy, hh:mm aa". Verify it contains a ','
    if text.find(',') == -1:
        return False

    # Verify that it doesn't have multiple commas
    # later

    # Now that it has a ',', verify that it has date and time on both ends
    splitted_marker = text.split(',')

    if is_date(splitted_marker[0]) and is_time(splitted_marker[1]):
        return True

    return False

# Merges a list of strings to make it a single string
def list_to_string(my_list):
    my_str = ""
    for elems in my_list:
        my_str += elems
    return my_str

# Fetches the speaker for the dialogue
def split_speaker_and_dialogue(line):

    speaker = ((line.split(':'))[0]).strip()
    dialogue = list_to_string((line.split(':'))[1:])

    return speaker, dialogue

# Calculates the number of lines a string needs to fit in
def get_num_of_lines(dialogue):

    count = 0

    # return math.ceil((len(text) % maxcol))

    for text in dialogue:
        if len(text) > MAX_COLUMNS:
            count += math.ceil((len(text) % MAX_COLUMNS))
        else:
            count += 1
    
    return count

# Makes a list of all the dialogues, padded, and ready to print
def make_list(dialogues):

    final_list = []

    # Get the perspective if not provided by default
    # Check contidion TBD
    # perspective, dialogues[0][0] = split_speaker_and_dialogue(dialogues[0][0])
    perspective = 'Anjali'
    
    for dialogue in dialogues:

        # Check perspective
        if ((dialogue[0]).split(':'))[0].strip() == perspective:
            padding = DIALOGUE_PADDING
        else:
            padding = ""
        
        for line in dialogue:
            # current_line = padding + line

            line = textwrap.wrap(line, WRAP_AT)

            for index in range(len(line)):
                line[index] = padding + line[index]

            final_list += line

    return final_list

def represent_dialogues(scr, dialogues):
    
    scr.scrollok(1)

    MAX_ROWS = (scr.getmaxyx())[0]
    MAX_COLUMNS = (scr.getmaxyx())[1]

    list_to_print = make_list(dialogues)

    del dialogues

    for lines in list_to_print:
        scr.addstr(lines + '\n')
    
    # scr.addstr('\n\n')

    # Print dialogues
    # for dialogue in dialogues:

    #     if dialogue[0].find(':') == -1:
    #         continue

    #     speaker, dialogue[0] = split_speaker_and_dialogue(dialogue[0])
    #     lines = list_to_string(dialogue)

    #     scr.addstr(speaker + ':\n')
    #     scr.addstr(lines + '\n')


    scr.refresh()

    while True:
        key = scr.getch()

        if key == 81:
            break
        elif key == curses.KEY_UP:
            scr.scroll(-1)
        elif key == curses.KEY_DOWN:
            scr.scroll(1)


dialogues = [[]]

# Check arguments
arguments = sys.argv
if len(arguments) != 2:
    # perror("USAGE:\n\t" + arguments[0] + "-f path_to_file -p perspective\n")
    perror("USAGE:\n\t" + arguments[0] + " path_to_file\n")
    exit(1)

# Set Perspective according to -p flag
# perspective = ""

# Open the file
chat_file = open(arguments[1], "rt")

chat = chat_file.read().split('\n')

# Close the file
chat_file.close()

# It's starting from -1 because it'll add an empty list in dialogues[[]] in the begining.
# Change it to 0 and you'll know what I mean
# current_elem = -1
current_elem = 0

for line in chat:

    chat_line = ""

    # Search for '-', because it might be a marker line
    if line.find('-') != -1:

        # Its probably a marker line
        if is_a_marker((line.split('-'))[0]):
            temp_list = []
            dialogues.append(temp_list)
            current_elem += 1
            chat_line = list_to_string((line.split('-'))[1:])
        else:
            chat_line = line
    else:
        chat_line = line
        
    dialogues[current_elem].append(chat_line)

# There are empty lists on both ends, so trimming 'em off
dialogues = dialogues[1:-1]

# It's representation time!
# print(dialogues)

# Calling in a wrapper to avoid exceptions
curses.wrapper(represent_dialogues, dialogues)
