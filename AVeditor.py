

import tkinter as tk
import os
from lxml import etree

room_numbers = []
# index=0
rooms = []  # room class objects
# XMLParser = etree.XMLParser(remove_blank_text=True)


class Room:
        def __init__(self):
                self.name = ""
                self.number = None
                self.vid_switcher_output_num = 0
                self.has_local_rec = 0
                self.rec_has_vol_fb = 0
                self.rec_input_command_delay = 0
                self.rec_has_dist_audio = 0
                self.audio_zone_number = ""
                self.audio_has_vol_fb = None
                self.vid_vol_through_dist_audio = None
                self.LiftScenarioNum = None
                self.OpenWithOnCmdNum = None
                self.CloseWithOffCmdNum = None
                self.LiftButtonNames = []
                self.LiftPulseTimes = []
               

####FUNCTION DEFINITIONS#######
def read_xml():
        tree = etree.parse('roomAVDistribution.xml')
        root = tree.getroot()
        index = int(listbox.curselection()[0])
        roomz = root.find('rooms')
        room = roomz.find('room[@number="%s"]' % (index+1))
        print(room.get('name'))
        
        # lists = filter(lambda x: 'Room' in x.get('name'), rooms.findall(".//room[@name]"))
        # print(lists)
        # for room in rooms:
                # print(room.tag, room.attrib)#tag is just the element name
        
        
def write_xml():
        tree = etree.parse('roomAVDistribution.xml')
        root = tree.getroot()
        index = int(listbox.curselection()[0])
        roomz = root.find('rooms')
        room = roomz.find('room[@number="%s"]' % (index+1))  # move to the right room
        room.set('name', rooms[index].Name)  # update the room name
        config = room.find('configuration')  # move to the configuration section
        config.set('videoSwitcherOutputNum', rooms[index].vid_switcher_output_num)
        # LOCAL AVR SECTION####
        rec = config.find('receiver') # move to the local AVR section
        rec.set('hasReceiver', str(rooms[index].has_local_rec))
        rec.set('receiverHasVolFB', str(rooms[index].rec_has_vol_fb))
        rec.set('receiverInputDelay', rooms[index].rec_input_command_delay)
        rec.set('musicThroughReceiver', str(rooms[index].rec_has_dist_audio))
        # MUSIC#######
        music = config.find('music')
        music.set('musicZoneNum', rooms[index].audio_zone_number)
        music.set('musicHasVolFB', str(rooms[index].audio_has_vol_fb))
        music.set('videoVolThroughDistAudio', str(rooms[index].vid_vol_through_dist_audio))
        # WRITE TO THE FILE######
        tree.write('roomAVDistribution.xml')
        print('ok')
         
                
def add_room_button():
        room_number = lowest_open_room_number()
        listbox.insert(room_number-1, room_number)
        room_numbers.insert(room_number-1, room_number)
        rooms.insert(room_number-1, Room())
        rooms[room_number-1].number = room_number
        print('added room# %d' % room_number)
        print('room_numbers %s' % room_numbers)


def room_button_click(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        roomNameField.set(rooms[index].Name)
        vidSwitchField.set(rooms[index].vid_switcher_output_num)
        localRX.set(rooms[index].has_local_rec)
        local_rx_visible()
        value = w.get(index)
        
        print ('You selected item %d: "%s"' % (index, value))
       
        
def remove_button():
        index = int(listbox.curselection()[0])
        print('removed index %d' % (index))
        listbox.delete(index)
        del rooms[index]
        del room_numbers[index]  # removes by index
        if index > 0:
                listbox.selection_set(index-1)  # update the listbox selection
        else:
                listbox.selection_set(0)
        # room_numbers.remove(currentListSelection)#removes by value
        
        
def move_up():
        a = lowest_open_room_number()
        print(a)


def move_down():
        print(index)


def update_room(): 
        index = int(listbox.curselection()[0])
        if index >= 0:
                listbox.delete(index)
                rooms[index].name = roomNameTextField.get()
                rooms[index].vid_switcher_output_num = vidSwitchTextField.get()
                rooms[index].has_local_rec = localRX.get()
                rooms[index].rec_has_vol_fb = localRXVolFb.get()
                rooms[index].rec_input_command_delay = recInputDelayTextField.get()
                rooms[index].rec_has_dist_audio = localRXDistAudio.get()
                rooms[index].audio_zone_number = audioZoneField.get()
                rooms[index].audio_has_vol_fb = audioZoneVolFb.get()
                rooms[index].vid_vol_through_dist_audio = vidVolDist.get()
                listbox.insert(index, str(index+1) + " " + rooms[index].Name)
                print(rooms[index].Name)
        listbox.selection_set(index)


def print_button_list():
        print(rooms)


def lowest_open_room_number():
        if not room_numbers:
                return 1
        else:
                return next(i for i, e in enumerate(sorted(room_numbers) + [ None ], 1) if i != e)


def print_room_list():
        print(room_numbers)


def yview(self, *args):
        apply(listbox.yview, args)
        
        
def local_rx_visible():
        rx_is_visible = localRX.get()
        if rx_is_visible:
                recFrame.grid()
        else:
                recFrame.grid_remove()
             
                
def lift_visible():
        lift_is_visible = liftVis.get()
        if lift_is_visible:
                liftFrame.grid()
        else:
                liftFrame.grid_remove()
 
                
def sleep_visible():
        sleep_is_visible = sleepVis.get()
        if sleep_is_visible:
                sleepFrame.grid()
        else:
                sleepFrame.grid_remove()


def surround_visible():
        surround_is_visible = surroundVis.get()
        if surround_is_visible:
                surroundFrame.grid()
        else:
                surroundFrame.grid_remove()
# END FUNCTION DEFINITIONS #######                


# START UI #######################
root = tk.Tk()
root.title("ACS Room Video Editor v0.1")

# FRAMES
# frame1 top left
frame1 = tk.Frame(root, width=200, height=300, borderwidth=1, relief="groove")
frame1.grid(row=0, column=0, sticky=tk.N)
frameRight = tk.Frame(root, width=300, height=300, borderwidth=1, relief="groove")
frameRight.grid(row=0, column=1, sticky=tk.N)
frame2 = tk.Frame(root, width=300, height=300)
frame2.grid(row=1, column=0)
recFrame = tk.Frame(frameRight, borderwidth=1, relief="groove")
recFrame.grid(row=3, column=0, columnspan=2)
recFrame.grid_remove()
liftFrame = tk.Frame(frameRight, borderwidth=1, relief="groove")
liftFrame.grid(row=11, column=0, columnspan=2)
liftFrame.grid_remove()
sleepFrame = tk.Frame(frameRight, borderwidth=1, relief="groove")
sleepFrame.grid(row=13, column=0, columnspan=2)
sleepFrame.grid_remove()
surroundFrame = tk.Frame(frameRight, borderwidth=1, relief="groove")
surroundFrame.grid(row=16, column=0, columnspan=2)
surroundFrame.grid_remove()

####FRAME1 WIDGETS
add_room = tk.Button(frame1, text="add a room", width=15, command=add_room_button)
add_room.pack(pady =20, padx =20)


listbox = tk.Listbox(frame1, exportselection=0)
listbox.bind('<<ListboxSelect>>', room_button_click)
listbox.pack(side=tk.LEFT, fill=tk.Y)
scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)


####FRAME2 WIDGETS LOWER LEFT
delete_room = tk.Button(frame2, text="remove room", width=10, command=remove_button).grid(row=0, column=1)
read_xmlButton = tk.Button(frame2, text="read xml", width=7, command=read_xml).grid(row=0, column=0)
write_xmlButton = tk.Button(frame2, text="write xml", width=7, command=write_xml).grid(row=0, column=2)

####RIGHT FRAME WIDGETS
roomNameLabel = tk.Label(frameRight, text="Room Name:").grid(row=0, column=0, sticky=tk.E)
roomNameField = tk.StringVar()
roomNameTextField = tk.Entry(frameRight, textvariable=roomNameField)
roomNameTextField.grid(row=0, column=1)

vidSwitchLabel = tk.Label(frameRight, text="Video switcher output number:").grid(row=1, column=0, sticky=tk.E)
vidSwitchField = tk.StringVar()
vidSwitchTextField = tk.Entry(frameRight, width=3, textvariable=vidSwitchField)
vidSwitchTextField.grid(row=1, column=1, sticky=tk.W)

#Local Receiver
localRecLabel = tk.Label(frameRight, text="Does this room have a local receiver?").grid(row=2, column=0, sticky=tk.E)
localRX = tk.IntVar()
localRX.set(0)
tk.Radiobutton(frameRight, text="Yes", variable=localRX, command=local_rx_visible, value=1).grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=localRX, command=local_rx_visible, value=0).grid(row=2, column=1)

localRecVolLabel = tk.Label(recFrame, text="Does this receiver have volume feedback?")
localRecVolLabel.grid(row=0, column=0, sticky=tk.E)
localRXVolFb = tk.IntVar()
tk.Radiobutton(recFrame, text="Yes", variable=localRXVolFb, value=True).grid(row=0, column=1, sticky=tk.W)
tk.Radiobutton(recFrame, text="No", variable=localRXVolFb, value=False).grid(row=0, column=2)

localRecInputDelay = tk.Label(recFrame, text="Receiver input command delay (seconds) after power on:")
localRecInputDelay.grid(row=1, column=0, sticky=tk.E)
recInputDelayTextField = tk.Entry(recFrame, width=3)
recInputDelayTextField.grid(row=1, column=1, sticky=tk.W)

distAudioRecLabel = tk.Label(recFrame, text="Will distributed audio be sent to this receiver?").grid(row=2, column=0, sticky=tk.E)
localRXDistAudio = tk.IntVar()
tk.Radiobutton(recFrame, text="Yes", variable=localRXDistAudio, value=True).grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(recFrame, text="No", variable=localRXDistAudio, value=False).grid(row=2, column=2)
#End Local Receiver

#Music Zone#
audioZoneLabel = tk.Label(frameRight, text="Which audio zone number is this room?")
audioZoneLabel.grid(row=4, column=0, sticky=tk.E)
audioZoneField = tk.Entry(frameRight, width=3)
audioZoneField.grid(row=4, column=1, sticky=tk.W)

audioZoneVolLabel = tk.Label(frameRight, text="Does this audio zone have volume feedback?")
audioZoneVolLabel.grid(row=5, column=0, sticky=tk.E)
audioZoneVolFb = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=audioZoneVolFb, value=True).grid(row=5, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=audioZoneVolFb, value=False).grid(row=5, column=1)

vidVolLabel = tk.Label(frameRight, text="Will the video volume play through the distributed audio system?")
vidVolLabel.grid(row=6, column=0, sticky=tk.E)
vidVolDist = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=vidVolDist, value=True).grid(row=6, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=vidVolDist, value=False).grid(row=6, column=1)
#End Music Zone

#Display
displayInputDelay = tk.Label(frameRight, text="Display input command delay (seconds) after power on:")
displayInputDelay.grid(row=7, column=0, sticky=tk.E)
displayInputDelayTextField = tk.Entry(frameRight, width=3)
displayInputDelayTextField.grid(row=7, column=1, sticky=tk.W)

displayVolLabel = tk.Label(frameRight, text="Does this display have volume feedback?")
displayVolLabel.grid(row=8, column=0, sticky=tk.E)
displayVol = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=displayVol, value=True).grid(row=8, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=displayVol, value=False).grid(row=8, column=1)
#End Display

####Lift########
liftLabel = tk.Label(frameRight, text="Does the display in this room have a lift?")
liftLabel.grid(row=9, column=0, sticky=tk.E)
liftVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=liftVis, command=lift_visible, value=True).grid(row=9, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=liftVis, command=lift_visible, value=False).grid(row=9, column=1)

liftScenario = tk.Label(liftFrame, text="Enter the lift page scenario number:")
liftScenario.grid(row=1, column=0, sticky=tk.E)
liftScenarioTextField = tk.Entry(liftFrame, width=3)
liftScenarioTextField.grid(row=1, column=1, sticky=tk.W)

liftOpenCmdLabel = tk.Label(liftFrame, text="Which command number opens the lift?")
liftOpenCmdLabel.grid(row=2, column=0, sticky=tk.E)
liftOpenCmdTextField = tk.Entry(liftFrame, width=3)
liftOpenCmdTextField.grid(row=2, column=1, sticky=tk.W)

liftCloseCmdLabel = tk.Label(liftFrame, text="Which command number closes the lift?")
liftCloseCmdLabel.grid(row=3, column=0, sticky=tk.E)
liftCloseCmdTextField = tk.Entry(liftFrame, width=3)
liftCloseCmdTextField.grid(row=3, column=1, sticky=tk.W)

liftNamesLabel = tk.Label(liftFrame, text="Enter each of the lift button command numbers, names and pulse times:")
liftNamesLabel.grid(row=4, column=0, sticky=tk.E)
liftCmdTextField1 = tk.Entry(liftFrame, width=2)
liftCmdTextField1.grid(row=4, column=1, sticky=tk.W)
liftCmdTextField2 = tk.Entry(liftFrame, width=2)
liftCmdTextField2.grid(row=5, column=1, sticky=tk.W)
liftCmdTextField3 = tk.Entry(liftFrame, width=2)
liftCmdTextField3.grid(row=6, column=1, sticky=tk.W)
liftCmdTextField4 = tk.Entry(liftFrame, width=2)
liftCmdTextField4.grid(row=7, column=1, sticky=tk.W)
liftCmdTextField5 = tk.Entry(liftFrame, width=2)
liftCmdTextField5.grid(row=8, column=1, sticky=tk.W)
liftNameTextField1 = tk.Entry(liftFrame, width=8)
liftNameTextField1.grid(row=4, column=2, sticky=tk.W)
liftNameTextField2 = tk.Entry(liftFrame, width=8)
liftNameTextField2.grid(row=5, column=2, sticky=tk.W)
liftNameTextField3 = tk.Entry(liftFrame, width=8)
liftNameTextField3.grid(row=6, column=2, sticky=tk.W)
liftNameTextField4 = tk.Entry(liftFrame, width=8)
liftNameTextField4.grid(row=7, column=2, sticky=tk.W)
liftNameTextField5 = tk.Entry(liftFrame, width=8)
liftNameTextField5.grid(row=8, column=2, sticky=tk.W)
pulseTimeTextField1 = tk.Entry(liftFrame, width=4)
pulseTimeTextField1.grid(row=4, column=3, sticky=tk.W)
pulseTimeTextField2 = tk.Entry(liftFrame, width=4)
pulseTimeTextField2.grid(row=5, column=3, sticky=tk.W)
pulseTimeTextField3 = tk.Entry(liftFrame, width=4)
pulseTimeTextField3.grid(row=6, column=3, sticky=tk.W)
pulseTimeTextField4 = tk.Entry(liftFrame, width=4)
pulseTimeTextField4.grid(row=7, column=3, sticky=tk.W)
pulseTimeTextField5 = tk.Entry(liftFrame, width=4)
pulseTimeTextField5.grid(row=8, column=3, sticky=tk.W)
#########End Lift######

####Sleep Timer#########
sleepLabel = tk.Label(frameRight, text="Will this room have a sleep timer?")
sleepLabel.grid(row=12, column=0, sticky=tk.E)
sleepVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=sleepVis, command=sleep_visible, value=True).grid(row=12, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=sleepVis, command=sleep_visible, value=False).grid(row=12, column=1)

sleepScenario = tk.Label(sleepFrame, text="Enter the sleep page scenario number:")
sleepScenario.grid(row=1, column=0, sticky=tk.E)
sleepScenarioTextField = tk.Entry(sleepFrame, width=3)
sleepScenarioTextField.grid(row=1, column=1, sticky=tk.W)

sleepButtonText = tk.Label(sleepFrame, text="Enter the label for the sleep button:")
sleepButtonText.grid(row=2, column=0, sticky=tk.E)
sleepButtonTextField = tk.Entry(sleepFrame, width=8)
sleepButtonTextField.grid(row=2, column=1, sticky=tk.W)

sleepTimerText = tk.Label(sleepFrame, text="Enter the label for each of the sleep buttons followed by the timer length in minutes:")
sleepTimerText.grid(row=4, column=0, sticky=tk.E)
sleepButtonTextField1 = tk.Entry(sleepFrame, width=8)
sleepButtonTextField1.grid(row=4, column=1, sticky=tk.W)
sleepButtonTextField2 = tk.Entry(sleepFrame, width=8)
sleepButtonTextField2.grid(row=5, column=1, sticky=tk.W)
sleepButtonTextField3 = tk.Entry(sleepFrame, width=8)
sleepButtonTextField3.grid(row=6, column=1, sticky=tk.W)
sleepButtonTextField4 = tk.Entry(sleepFrame, width=8)
sleepButtonTextField4.grid(row=7, column=1, sticky=tk.W)
sleepTimeTextField1 = tk.Entry(sleepFrame, width=3)
sleepTimeTextField1.grid(row=4, column=2, sticky=tk.W)
sleepTimeTextField2 = tk.Entry(sleepFrame, width=3)
sleepTimeTextField2.grid(row=5, column=2, sticky=tk.W)
sleepTimeTextField3 = tk.Entry(sleepFrame, width=3)
sleepTimeTextField3.grid(row=6, column=2, sticky=tk.W)
sleepTimeTextField4 = tk.Entry(sleepFrame, width=3)
sleepTimeTextField4.grid(row=7, column=2, sticky=tk.W)
# End Sleep Timer #######

# Surround / Video Formats #######
surroundLabel = tk.Label(frameRight, text="Will this room have surround or video format selections?")
surroundLabel.grid(row=15, column=0, sticky=tk.E)
surroundVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=surroundVis, command=surround_visible, value=True).grid(row=15, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=surroundVis, command=surround_visible, value=False).grid(row=15, column=1)

surroundScenario = tk.Label(surroundFrame, text="Enter the surround/format page scenario number:")
surroundScenario.grid(row=1, column=0, sticky=tk.E)
surroundScenarioTextField = tk.Entry(surroundFrame, width=3)
surroundScenarioTextField.grid(row=1, column=1, sticky=tk.W)

surroundButtonText = tk.Label(surroundFrame, text="Enter the label for the format button:")
surroundButtonText.grid(row=2, column=0, sticky=tk.E)
surroundButtonTextField = tk.Entry(surroundFrame, width=8)
surroundButtonTextField.grid(row=2, column=1, sticky=tk.W)

surroundText = tk.Label(surroundFrame, text="Enter the command number for each of the format buttons followed by their names:")
surroundText.grid(row=4, column=0, sticky=tk.E)


update = tk.Button(frameRight, text="update room", width=15, command=update_room).grid(row=30, column=0)
printBtns = tk.Button(frameRight, text="print buttons", width=15, command=print_button_list).grid(row=31, column=0)
printRooms = tk.Button(frameRight, text="print Rooms", width=15, command=print_room_list).grid(row=32, column=0)


root.mainloop()

# END
