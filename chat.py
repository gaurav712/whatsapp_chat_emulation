import sys
import math
import curses
import textwrap
import gi
from optparse import OptionParser
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

## GLOBALS
perspective = ""

# Classes

class ChatBubble(Gtk.Label):

    def __init__(self, left, dialogue, list_box):

        # Make a box container for the label
        self.box = Gtk.Box()

        # Making the label itself
        # self.label = Gtk.Label(label = dialogue)
        self.label = Gtk.Label()
        self.label.set_markup(dialogue)
        self.label.set_selectable(Gtk.SelectionMode.NONE)
        self.label.set_line_wrap(True)

        # Set perspective for proper look and alignment
        if left:
            self.label.set_name("non_persp_dialogue")
            self.label.set_xalign(0)
            self.label.set_margin_end(100)
            # Add label to the box
            self.box.pack_start(self.label, False, False, 5)
        else:
            self.label.set_name("persp_dialogue")
            self.label.set_xalign(1)
            self.label.set_margin_start(100)
            # Add label to the box
            self.box.pack_end(self.label, False, False, 5)
        
        # Make a ListBox row and add the box
        self.list_box_row = Gtk.ListBoxRow()
        self.list_box_row.add(self.box)

        # Add the row to the list
        list_box.add(self.list_box_row)


class MainWindow(Gtk.Window):

    def __init__(self, dialogues):

        Gtk.Window.__init__(self, title="WhatsApp Chat Emulation")

        # Set window default size
        self.set_size_request(560,640)

        # To make the content scrollable
        self.scrolled_window = Gtk.ScrolledWindow()

        # Load CSS
        self.css = b"""
                #non_persp_dialogue {   background-color: #303030; color: #ffffff; border-radius: 5px; padding: 5px }
                #persp_dialogue {  background-color: #075e54; color: #ffffff; border-radius: 5px; padding: 5px }
                """
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(self.css)
        self.context = Gtk.StyleContext()
        self.screen = Gdk.Screen.get_default()
        self.context.add_provider_for_screen(self.screen, self.css_provider,
                                            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # ListBox for storing all the labels
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        for elem in dialogues:

            # Ignore if it's not a dialogue
            if elem[0].find(':') == -1:
                continue
            
            self.speaker, self.dialogue = split_speaker_and_dialogue(elem)

            # Just skip those <Media omitted> texts
            if self.dialogue.find('<Media omitted>') != -1:
                continue

            # Now create those chat bubbles
            if self.speaker == perspective:
                self.left = False
            else:
                self.left = True
            ChatBubble(self.left,  ('<b>' + self.speaker + '</b>\n' + self.dialogue), self.list_box)
        
        # Add the list_box to scrollable window and the later to the main window
        self.scrolled_window.add(self.list_box)
        self.add(self.scrolled_window)


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

    for elem in my_list:
        my_str += elem + '\n'

    return my_str.strip()

# Fetches the speaker for the dialogue
def split_speaker_and_dialogue(dialogue):

    speaker = ((dialogue[0].split(':'))[0]).strip()
    dialogue[0] = list_to_string((dialogue[0].split(':'))[1:])
    dialogue = list_to_string(dialogue)

    return speaker , dialogue


############ MAIN ################

# To store dialogues
dialogues = [[]]

# Check arguments
arguments = sys.argv
if len(arguments) != 5:
    perror("USAGE:\n\t" + arguments[0] + " -f path_to_file -p perspective\n")
    exit(1)

# Parse arguments
parser = OptionParser()

parser.add_option("-f", dest="filename", help="file to use", metavar="FILE")
parser.add_option("-p", dest="perspective", help="the perspective for the conversation", metavar="PERSP")

(options, arguments) = parser.parse_args()

# Set Perspective according to -p flag
# perspective = arguments[4]
perspective = options.perspective

# Open the file
# chat_file = open(arguments[2], "rt")
chat_file = open(options.filename, "rt")

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

# It's representation time! Drawing windows
window = MainWindow(dialogues)
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
