

import tkinter as tk
# import os
from lxml import etree

room_numbers = []
rooms = []  # room class objects


class Room:
        def __init__(self):
                self.name = ""
                self.number = None
                self.vid_switcher_output_num = 0
                self.send_to_speakers = 0
                self.has_local_rec = 0
                self.rec_has_vol_fb = 0
                self.rec_input_command_delay = 0
                self.rec_has_dist_audio = 0
                self.music_zone_number = 0
                self.music_has_vol_fb = 0
                self.vid_vol_through_dist_audio = 0
                self.display_input_delay = 5
                self.display_has_vol_fb = 0
                self.lift_scenario_num = "0"
                self.lift_open_with_on_cmd_num = 0
                self.lift_close_with_off_cmd_num = 0
                self.lift_button_cmd_num = [0, 0, 0, 0, 0]
                self.lift_button_names = [" ", " ", " ", " ", " "]
                self.lift_pulse_times = [0, 0, 0, 0, 0]
                self.sleep_scenario_num = "0"
                self.sleep_button_text = " "
                self.sleep_button_names = [" ", " ", " ", " ", " "]
                self.sleep_button_lengths = [0, 0, 0, 0, 0]
                self.format_scenario_num = "0"
                self.format_button_text = " "
                self.format_button_cmd_num = [0, 0, 0, 0, 0]
                self.format_button_names = [" ", " ", " ", " ", " "]
                self.video_sources = []
                self.video_source_display_inputs = []
                self.video_source_receiver_inputs = []
                self.video_source_alt_switcher_inputs = []
                self.music_sources = []
                self.music_source_receiver_inputs = []
               

# FUNCTION DEFINITIONS#######
def read_xml():
        tree = etree.parse('roomAVDistribution.xml')
        root = tree.getroot()
        roomz = root.find('rooms')
        ii = 0
        for room in roomz.findall('room'):

                if ii+1 not in room_numbers:
                        print('added room %s' % ii)
                        rooms.insert(ii, Room())
                        room_numbers.insert(ii, ii+1)
                        roomListBox.insert(ii, str(ii+1) + " " + room.get('name'))
                else:
                        roomListBox.delete(ii)
                        roomListBox.insert(ii, str(ii + 1) + " " + room.get('name'))
                print(ii)
                rooms[ii].name = room.get('name')
                config = room.find('configuration')
                rooms[ii].vid_switcher_output_num = config.get('videoSwitcherOutputNum')
                rooms[ii].send_to_speakers = config.get('sendToSpeakers')
                # LOCAL AVR SECTION ###
                rec = config.find('receiver')
                rooms[ii].has_local_rec = rec.get('hasReceiver')
                rooms[ii].rec_has_vol_fb = rec.get('receiverHasVolFB')
                rooms[ii].rec_input_command_delay = rec.get('receiverInputDelay')
                rooms[ii].rec_has_dist_audio = rec.get('musicThroughReceiver')
                # MUSIC #####
                music = config.find('music')
                rooms[ii].music_zone_number = music.get('musicZoneNum')
                rooms[ii].music_has_vol_fb = music.get('musicHasVolFB')
                rooms[ii].vid_vol_through_dist_audio = music.get('videoVolThroughDistAudio')
                # DISPLAY ####
                display = config.find('display')
                rooms[ii].display_input_delay = display.get('displayInputDelay')
                rooms[ii].display_has_vol_fb = display.get('tvHasVolFB')
                # LIFT ####
                lift = room.find('lift')
                rooms[ii].lift_scenario_num = lift.get('liftScenarioNum')
                rooms[ii].lift_open_with_on_cmd_num = lift.get('openWithOnCmdNum')
                rooms[ii].lift_close_with_off_cmd_num = lift.get('closeWithOffCmdNum')
                x = 0
                for lift_button in lift.findall('liftButton'):
                        rooms[ii].lift_button_cmd_num[x] = lift_button.get('cmdNum')
                        rooms[ii].lift_button_names[x] = lift_button.get('Name')
                        rooms[ii].lift_pulse_times[x] = lift_button.get('pulseTime')
                        x += 1
                sleep = room.find('sleep')
                rooms[ii].sleep_scenario_num = sleep.get('sleepScenarioNum')
                rooms[ii].sleep_button_text = sleep.get('sleepButtonText')
                x = 0
                for sleep_button in sleep.findall('sleepButton'):
                        rooms[ii].sleep_button_names[x] = sleep_button.get('Name')
                        rooms[ii].sleep_button_lengths[x] = sleep_button.get('length')
                        x += 1
                # FORMAT ####
                vid_format = room.find('format')
                rooms[ii].format_scenario_num = vid_format.get('formatScenarioNum')
                rooms[ii].format_button_text = vid_format.get('formatButtonText')
                x = 0
                for format_button in vid_format.findall('formatButton'):
                        rooms[ii].format_button_cmd_num[x] = format_button.get('cmdNum')
                        rooms[ii].format_button_names[x] = format_button.get('Name')
                ii += 1

        print(room.get('name'))
        print(config.get('videoSwitcherOutputNum'))
        print(rec.get('hasReceiver'))
        
        # lists = filter(lambda x: 'Room' in x.get('name'), rooms.findall(".//room[@name]"))
        # print(lists)
        # for room in rooms:
                # print(room.tag, room.attrib)#tag is just the element name
        
        
def write_xml():
        tree = etree.parse('roomAVDistribution.xml')
        root = tree.getroot()
        index = int(roomListBox.curselection()[0])
        roomz = root.find('rooms')
        room = roomz.find('room[@number="%s"]' % (index+1))  # move to the right room
        room.set('name', rooms[index].name)  # update the room name
        config = room.find('configuration')  # move to the configuration section
        config.set('videoSwitcherOutputNum', rooms[index].vid_switcher_output_num)
        # LOCAL AVR SECTION ####
        rec = config.find('receiver') # move to the local AVR section
        rec.set('hasReceiver', str(rooms[index].has_local_rec))
        rec.set('receiverHasVolFB', str(rooms[index].rec_has_vol_fb))
        rec.set('receiverInputDelay', rooms[index].rec_input_command_delay)
        rec.set('musicThroughReceiver', str(rooms[index].rec_has_dist_audio))
        # MUSIC #######
        music = config.find('music')
        music.set('musicZoneNum', rooms[index].music_zone_number)
        music.set('musicHasVolFB', str(rooms[index].music_has_vol_fb))
        music.set('videoVolThroughDistAudio', str(rooms[index].vid_vol_through_dist_audio))
        # DISPLAY ######
        display = config.find('display')
        display.set('displayInputDelay', rooms[index].display_input_delay)
        display.set('tvHasVolFB', str(rooms[index].display_has_vol_fb))
        # LIFT ####
        lift = room.find('lift')
        lift.set('liftScenarioNum', rooms[index].lift_scenario_num)
        lift.set('openWithOnCmdNum', rooms[index].lift_open_with_on_cmd_num)
        lift.set('closeWithOffCmdNum', str(rooms[index].lift_close_with_off_cmd_num))

        x = 0
        for lift_button in lift.findall('liftButton'):
                lift_button.set('cmdNum', rooms[index].lift_button_cmd_num[x])
                lift_button.set('Name', rooms[index].lift_button_names[x])
                lift_button.set('pulseTime', rooms[index].lift_pulse_times[x])
                x += 1
        # SLEEP ####
        sleep = room.find('sleep')
        sleep.set('sleepScenarioNum', rooms[index].sleep_scenario_num)
        sleep.set('sleepButtonText', rooms[index].sleep_button_text)
        x = 0
        for sleep_button in sleep.findall('sleepButton'):
                sleep_button.set('Name', rooms[index].sleep_button_names[x])
                sleep_button.set('length', rooms[index].sleep_button_lengths[x])
                x += 1
        # FORMAT ####
        vid_format = room.find('format')
        vid_format.set('formatScenarioNum', rooms[index].format_scenario_num)
        vid_format.set('formatButtonText', rooms[index].format_button_text)
        x = 0
        for format_button in vid_format.findall('formatButton'):
                format_button.set('cmdNum', rooms[index].format_button_cmd_num[x])
                format_button.set('Name', rooms[index].format_button_names[x])
            
        # WRITE TO THE FILE######
        tree.write('roomAVDistribution.xml')
        print('ok')
         
                
def add_room_button():
        room_number = lowest_open_room_number()
        roomListBox.insert(room_number-1, room_number)
        room_numbers.insert(room_number-1, room_number)
        rooms.insert(room_number-1, Room())
        rooms[room_number-1].number = room_number
        print('added room# %d' % room_number)
        print('room_numbers %s' % room_numbers)


def room_button_click(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        roomNameField.set(rooms[index].name)
        vidSwitchField.set(rooms[index].vid_switcher_output_num)
        localRX.set(rooms[index].has_local_rec)
        local_rx_visible()
        localRXVolFb.set(rooms[index].rec_has_vol_fb)
        recInputDelay.set(rooms[index].rec_input_command_delay)
        localRXDistAudio.set(rooms[index].rec_has_dist_audio)
        audioZoneNum.set(rooms[index].music_zone_number)
        audioZoneVolFb.set(rooms[index].music_has_vol_fb)
        vidVolDist.set(rooms[index].vid_vol_through_dist_audio)
        displayInputCmdDelay.set(rooms[index].display_input_delay)
        displayVol.set(rooms[index].display_has_vol_fb)
        if int(rooms[index].lift_scenario_num) > 0:
                liftVis.set(1)
        else:
                liftVis.set(0)
        lift_visible()
        liftScenarioNum.set(rooms[index].lift_scenario_num)
        liftOpenCmd.set(rooms[index].lift_open_with_on_cmd_num)
        liftCloseCmd.set(rooms[index].lift_close_with_off_cmd_num)
        for x in range(0, 5):
                liftBtnCmds[x].set(rooms[index].lift_button_cmd_num[x])
                liftBtnNames[x].set(rooms[index].lift_button_names[x])
                liftBtnTimes[x].set(rooms[index].lift_pulse_times[x])

        if int(rooms[index].sleep_scenario_num) > 0:
                sleepVis.set(1)
        else:
                sleepVis.set(0)
        sleep_visible()
        sleepScenarioNum.set(rooms[index].sleep_scenario_num)
        sleepButtonName.set(rooms[index].sleep_button_text)
        for x in range(0, 4):
                sleepBtnNames[x].set(rooms[index].sleep_button_names[x])
                sleepTimes[x].set(rooms[index].sleep_button_lengths[x])

        if int(rooms[index].format_scenario_num) > 0:
                formatVis.set(1)
        else:
                formatVis.set(0)
        surround_visible()
        surroundScenarioNum.set(rooms[index].format_scenario_num)
        surroundButtonName.set(rooms[index].format_button_text)
        for x in range(0, 4):
                formatBtnNames[x].set(rooms[index].format_button_names[x])
                formatCmds[x].set(rooms[index].format_button_cmd_num[x])

        value = w.get(index)
        
        print('You selected item %d: "%s"' % (index, value))

def vsrc_button_click(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        
def remove_button():
        index = int(roomListBox.curselection()[0])
        print('removed index %d' % (index))
        roomListBox.delete(index)
        del rooms[index]  # delete class instance
        del room_numbers[index]  # removes by index
        if index > 0:
                roomListBox.selection_set(index-1)  # update the roomListBox selection
        else:
                roomListBox.selection_set(0)
        # room_numbers.remove(currentListSelection)#removes by value


def update_room(): 
        index = int(roomListBox.curselection()[0])
        if index >= 0:
                roomListBox.delete(index)
                rooms[index].name = roomNameTextField.get()
                rooms[index].vid_switcher_output_num = vidSwitchTextField.get()
                rooms[index].has_local_rec = localRX.get()
                if rooms[index].has_local_rec:
                        rooms[index].rec_has_vol_fb = localRXVolFb.get()
                        rooms[index].rec_input_command_delay = recInputDelayTextField.get()
                        rooms[index].rec_has_dist_audio = localRXDistAudio.get()
                else:
                        rooms[index].rec_has_vol_fb = 0
                        rooms[index].rec_has_dist_audio = 0
                rooms[index].music_zone_number = audioZoneField.get()
                rooms[index].music_has_vol_fb = audioZoneVolFb.get()
                rooms[index].vid_vol_through_dist_audio = vidVolDist.get()
                rooms[index].display_input_delay = displayInputDelayTextField.get()
                rooms[index].display_has_vol_fb = displayVol.get()
                if liftVis:
                        rooms[index].lift_scenario_num = lift_scenario_text_field.get()
                        rooms[index].lift_open_with_on_cmd_num = liftOpenCmdTextField.get()
                        rooms[index].lift_close_with_off_cmd_num = liftCloseCmdTextField.get()
                        for i in range(0, 5):
                                rooms[index].lift_button_cmd_num[i] = liftCmdText[i].get()
                                rooms[index].lift_button_names[i] = liftNameText[i].get()
                                rooms[index].lift_pulse_times[i] = liftPulseTimeText[i].get()
                else:
                        rooms[index].lift_scenario_num = 0
                if sleepVis:
                        rooms[index].sleep_scenario_num = sleepScenarioTextField.get()
                        rooms[index].sleep_button_text = sleepButtonTextField.get()
                        for i in range(0, 4):
                                rooms[index].sleep_button_names[i] = sleepNamesText[i].get()
                                rooms[index].sleep_button_lengths[i] = sleepTimesText[i].get()
                else:
                        rooms[index].sleep_scenario_num = 0
                if formatVis:
                        rooms[index].format_scenario_num = surroundScenarioTextField.get()
                        rooms[index].format_button_text = surroundButtonTextField.get()
                        for i in range(0, 4):
                                rooms[index].format_button_cmd_num[i] = formatCmdsText[i].get()
                                rooms[index].format_button_names[i] = formatBtnNamesText[i].get()
                else:
                        rooms[index].format_scenario_num = 0

                roomListBox.insert(index, str(index+1) + " " + rooms[index].name)
                print(rooms[index].name)
        roomListBox.selection_set(index)


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
        apply(roomListBox.yview, args)
        
        
def local_rx_visible():
        rx_is_visible = localRX.get()
        if rx_is_visible:
                recFrame.grid()
        else:
                recFrame.grid_remove()
        frameRight.update_idletasks()
        vidConfigCanvas.config(scrollregion=vidConfigCanvas.bbox('all'))


def lift_visible():
        lift_is_visible = liftVis.get()

        if lift_is_visible:
                liftFrame.grid()
        else:
                liftFrame.grid_remove()
        frameRight.update_idletasks()
        vidConfigCanvas.config(scrollregion=vidConfigCanvas.bbox('all'))

                
def sleep_visible():
        sleep_is_visible = sleepVis.get()
        if sleep_is_visible:
                sleepFrame.grid()
        else:
                sleepFrame.grid_remove()
        frameRight.update_idletasks()
        vidConfigCanvas.config(scrollregion=vidConfigCanvas.bbox('all'))


def surround_visible():
        surround_is_visible = formatVis.get()
        if surround_is_visible:
                formatFrame.grid()
        else:
                formatFrame.grid_remove()
        frameRight.update_idletasks()
        vidConfigCanvas.config(scrollregion=vidConfigCanvas.bbox('all'))


def canvas_scroll_config(event):
        frameRight.update_idletasks()
        vidConfigCanvas.config(scrollregion=vidConfigCanvas.bbox('all'))


# END FUNCTION DEFINITIONS #######                


# START UI #######################
root = tk.Tk()
root.title("ACS Room Video Editor v0.1")

# region FRAMES
# roomListFrame top left
vidConfigCanvas = tk.Canvas(root)
roomListFrame = tk.Frame(root, width=100, height=300, borderwidth=1, relief="groove")
roomListFrame.grid(row=0, column=0, sticky=tk.N+tk.W, pady=20, padx=20)
vsrcListFrame = tk.Frame(root, width=100, height=300, borderwidth=1, relief="groove")
vsrcListFrame.grid(row=1, column=0, sticky=tk.N, pady=20, padx=20)
frameRight = tk.Frame(vidConfigCanvas, borderwidth=1, relief="groove")
frameRight.grid(row=0, column=0, sticky=tk.N+tk.S)
frame2 = tk.Frame(root, width=300, height=300)
frame2.grid(row=2, column=0)

recFrame = tk.Frame(frameRight, borderwidth=3, relief="groove")
recFrame.grid(row=3, column=0, columnspan=2)
recFrame.grid_remove()
liftFrame = tk.Frame(frameRight, borderwidth=3, relief="groove")
liftFrame.grid(row=11, column=0, columnspan=2)
liftFrame.grid_remove()
sleepFrame = tk.Frame(frameRight, borderwidth=3, relief="groove")
sleepFrame.grid(row=13, column=0, columnspan=2)
sleepFrame.grid_remove()
formatFrame = tk.Frame(frameRight, borderwidth=3, relief="groove")
formatFrame.grid(row=16, column=0, columnspan=2)
formatFrame.grid_remove()
# endregion

# region roomListFrame WIDGETS
add_room = tk.Button(roomListFrame, text="add a room", width=15, command=add_room_button).grid(row=0, column=0)

# Room roomListBox
roomListBox = tk.Listbox(roomListFrame, exportselection=0)
roomListBox.grid(row=1, column=0)
roomListBox.bind('<<ListboxSelect>>', room_button_click)
scrollbar = tk.Scrollbar(roomListFrame, orient=tk.VERTICAL, command=roomListBox.yview)
scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)
roomListBox.config(yscrollcommand=scrollbar.set)

delete_room = tk.Button(roomListFrame, text="remove room", width=10, command=remove_button).grid(row=2, column=0)

vidConfigCanvas.grid(row=0, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
vidConfigScrollBar = tk.Scrollbar(root, orient=tk.VERTICAL, command=vidConfigCanvas.yview)
vidConfigScrollBar.grid(row=0, column=5, rowspan=2, sticky=tk.N+tk.S)
vidConfigScrollBar.configure(command=vidConfigCanvas.yview)
vidConfigCanvas.config(yscrollcommand=vidConfigScrollBar.set, width=750, height=500)
vidConfigCanvas.bind('<Configure>', canvas_scroll_config)
vidConfigCanvas.create_window(0, 0, anchor=tk.NW, window=frameRight)
# endregion

# region FRAME2 WIDGETS LOWER LEFT
add_vsrc_button = tk.Button(vsrcListFrame, text="add video source").grid(row=0, column=0)
vsrcListBox = tk.Listbox(vsrcListFrame, exportselection=0)
vsrcListBox.grid(row=1, column=0)
vsrcListBox.bind('<<ListboxSelect>>', vsrc_button_click)
remove_vsrc_button = tk.Button(vsrcListFrame, text="remove video source").grid(row=2, column=0)
read_xmlButton = tk.Button(frame2, text="read xml", width=7, pady=50, command=read_xml).grid(row=5, column=0)
write_xmlButton = tk.Button(frame2, text="write xml", width=7, command=write_xml).grid(row=5, column=2)
# endregion

# region RIGHT FRAME WIDGETS
roomNameLabel = tk.Label(frameRight, text="Room Name:").grid(row=0, column=0, sticky=tk.E)
roomNameField = tk.StringVar()
roomNameTextField = tk.Entry(frameRight, textvariable=roomNameField)
roomNameTextField.grid(row=0, column=1, sticky=tk.W)

vidSwitchLabel = tk.Label(frameRight, text="Video switcher output number:").grid(row=1, column=0, sticky=tk.E)
vidSwitchField = tk.StringVar()
vidSwitchTextField = tk.Entry(frameRight, width=3, textvariable=vidSwitchField)
vidSwitchTextField.grid(row=1, column=1, sticky=tk.W)
# endregion

# region Local Receiver
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
recInputDelay = tk.StringVar()
recInputDelayTextField = tk.Entry(recFrame, width=3, textvariable=recInputDelay)
recInputDelayTextField.grid(row=1, column=1, sticky=tk.W)

distAudioRecLabel = tk.Label(recFrame, text="Will distributed audio be sent to this receiver?").grid(row=2, column=0, sticky=tk.E)
localRXDistAudio = tk.IntVar()
tk.Radiobutton(recFrame, text="Yes", variable=localRXDistAudio, value=True).grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(recFrame, text="No", variable=localRXDistAudio, value=False).grid(row=2, column=2)
# endregion

# region Music Zone#
audioZoneLabel = tk.Label(frameRight, text="Which audio zone number is this room?")
audioZoneLabel.grid(row=4, column=0, sticky=tk.E)
audioZoneNum = tk.StringVar()
audioZoneField = tk.Entry(frameRight, width=3, textvariable=audioZoneNum)
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
# endregion

# region Display
displayInputDelay = tk.Label(frameRight, text="Display input command delay (seconds) after power on:")
displayInputDelay.grid(row=7, column=0, sticky=tk.E)
displayInputCmdDelay = tk.StringVar()
displayInputDelayTextField = tk.Entry(frameRight, width=3, textvariable=displayInputCmdDelay)
displayInputDelayTextField.grid(row=7, column=1, sticky=tk.W)

displayVolLabel = tk.Label(frameRight, text="Does this display have volume feedback?")
displayVolLabel.grid(row=8, column=0, sticky=tk.E)
displayVol = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=displayVol, value=True).grid(row=8, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=displayVol, value=False).grid(row=8, column=1)
# endregion

# region Lift
liftLabel = tk.Label(frameRight, text="Does the display in this room have a lift?")
liftLabel.grid(row=9, column=0, sticky=tk.E)
liftVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=liftVis, command=lift_visible, value=True).grid(row=9, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=liftVis, command=lift_visible, value=False).grid(row=9, column=1)

lift_scenario = tk.Label(liftFrame, text="Enter the lift page scenario number:")
lift_scenario.grid(row=1, column=0, sticky=tk.E)
liftScenarioNum = tk.StringVar()
lift_scenario_text_field = tk.Entry(liftFrame, width=3, textvariable=liftScenarioNum)
lift_scenario_text_field.grid(row=1, column=1, sticky=tk.W)

liftOpenCmdLabel = tk.Label(liftFrame, text="Which command number opens the lift?")
liftOpenCmdLabel.grid(row=2, column=0, sticky=tk.E)
liftOpenCmd = tk.StringVar()
liftOpenCmdTextField = tk.Entry(liftFrame, width=3, textvariable=liftOpenCmd)
liftOpenCmdTextField.grid(row=2, column=1, sticky=tk.W)

liftCloseCmdLabel = tk.Label(liftFrame, text="Which command number closes the lift?")
liftCloseCmdLabel.grid(row=3, column=0, sticky=tk.E)
liftCloseCmd = tk.StringVar()
liftCloseCmdTextField = tk.Entry(liftFrame, width=3, textvariable=liftCloseCmd)
liftCloseCmdTextField.grid(row=3, column=1, sticky=tk.W)

liftNamesLabel = tk.Label(liftFrame, text="Enter each of the lift button command numbers, names and pulse times:")
liftNamesLabel.grid(row=4, column=0, sticky=tk.E)

liftBtnCmds = []
liftCmdText = []

liftBtnNames = []
liftNameText = []

liftBtnTimes = []
liftPulseTimeText = []
for i in range(0, 5):
        liftCmd = tk.StringVar()
        liftBtnCmds.append(liftCmd)
        liftCmdTextField = tk.Entry(liftFrame, width=2, textvariable=liftBtnCmds[i])
        liftCmdText.append(liftCmdTextField)
        liftCmdText[i].grid(row=i+4, column=1, sticky=tk.W)

        liftBtnName = tk.StringVar()
        liftBtnNames.append(liftBtnName)
        liftNameTextField = tk.Entry(liftFrame, width=8, textvariable=liftBtnNames[i])
        liftNameText.append(liftNameTextField)
        liftNameText[i].grid(row=i+4, column=2, sticky=tk.W)

        liftBtnTime = tk.StringVar()
        liftBtnTimes.append(liftBtnTime)
        liftPulseTimeTextField = tk.Entry(liftFrame, width=4, textvariable=liftBtnTimes[i])
        liftPulseTimeText.append(liftPulseTimeTextField)
        liftPulseTimeText[i].grid(row=i+4, column=3, sticky=tk.W)
# endregion

# region Sleep Timer
sleepLabel = tk.Label(frameRight, text="Will this room have a sleep timer?")
sleepLabel.grid(row=12, column=0, sticky=tk.E)
sleepVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=sleepVis, command=sleep_visible, value=True).grid(row=12, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=sleepVis, command=sleep_visible, value=False).grid(row=12, column=1)

sleepScenario = tk.Label(sleepFrame, text="Enter the sleep page scenario number:")
sleepScenario.grid(row=1, column=0, sticky=tk.E)
sleepScenarioNum = tk.StringVar()
sleepScenarioTextField = tk.Entry(sleepFrame, width=3, textvariable=sleepScenarioNum)
sleepScenarioTextField.grid(row=1, column=1, sticky=tk.W)

sleepButtonText = tk.Label(sleepFrame, text="Enter the label for the sleep button:")
sleepButtonText.grid(row=2, column=0, sticky=tk.E)
sleepButtonName = tk.StringVar()
sleepButtonTextField = tk.Entry(sleepFrame, width=8, textvariable=sleepButtonName)
sleepButtonTextField.grid(row=2, column=1, sticky=tk.W)

sleepTimerText = tk.Label(sleepFrame, text="Enter the label for each of the sleep buttons followed by the timer length in minutes:")
sleepTimerText.grid(row=4, column=0, sticky=tk.E)

sleepBtnNames = []
sleepNamesText = []

sleepTimes = []
sleepTimesText = []

for i in range(0, 4):
        sleepBtnName = tk.StringVar()
        sleepBtnNames.append(sleepBtnName)
        sleepButtonTextField = tk.Entry(sleepFrame, width=8, textvariable=sleepBtnNames[i])
        sleepNamesText.append(sleepButtonTextField)
        sleepNamesText[i].grid(row=i+4, column=1, sticky=tk.W)

        sleepTime = tk.StringVar()
        sleepTimes.append(sleepTime)
        sleepTimeTextField = tk.Entry(sleepFrame, width=3, textvariable=sleepTimes[i])
        sleepTimesText.append(sleepTimeTextField)
        sleepTimesText[i].grid(row=i+4, column=2, sticky=tk.W)
# endregion

# region Surround / Video Formats
surroundLabel = tk.Label(frameRight, text="Will this room have surround or video format selections?")
surroundLabel.grid(row=15, column=0, sticky=tk.E)
formatVis = tk.IntVar()
tk.Radiobutton(frameRight, text="Yes", variable=formatVis, command=surround_visible, value=True).grid(row=15, column=1, sticky=tk.W)
tk.Radiobutton(frameRight, text="No", variable=formatVis, command=surround_visible, value=False).grid(row=15, column=1)

surroundScenario = tk.Label(formatFrame, text="Enter the surround/format page scenario number:")
surroundScenario.grid(row=1, column=0, sticky=tk.E)
surroundScenarioNum = tk.StringVar()
surroundScenarioTextField = tk.Entry(formatFrame, width=3, textvariable=surroundScenarioNum)
surroundScenarioTextField.grid(row=1, column=1, sticky=tk.W)

surroundButtonText = tk.Label(formatFrame, text="Enter the label for the format button:")
surroundButtonText.grid(row=2, column=0, sticky=tk.E)
surroundButtonName = tk.StringVar()
surroundButtonTextField = tk.Entry(formatFrame, width=8, textvariable=surroundButtonName)
surroundButtonTextField.grid(row=2, column=1, sticky=tk.W)

surroundText = tk.Label(formatFrame, text="Enter the command number for each of the format buttons followed by their names:")
surroundText.grid(row=4, column=0, sticky=tk.E)

formatCmds = []
formatCmdsText = []

formatBtnNames = []
formatBtnNamesText = []

for i in range(0, 4):
        formatCmd = tk.StringVar()
        formatCmds.append(formatCmd)
        formatCmdsTextField = tk.Entry(formatFrame, width=2, textvariable=formatCmds[i])
        formatCmdsText.append(formatCmdsTextField)
        formatCmdsText[i].grid(row=i+4, column=1, sticky=tk.W)

        formatBtnName = tk.StringVar()
        formatBtnNames.append(formatBtnName)
        formatButtonTextField = tk.Entry(formatFrame, width=8, textvariable=formatBtnNames[i])
        formatBtnNamesText.append(formatButtonTextField)
        formatBtnNamesText[i].grid(row=i+4, column=2, sticky=tk.W)
# endregion

update = tk.Button(frameRight, text="update room", width=15, command=update_room).grid(row=30, column=0)
printBtns = tk.Button(frameRight, text="print buttons", width=15, command=print_button_list).grid(row=31, column=0)
printRooms = tk.Button(frameRight, text="print Rooms", width=15, command=print_room_list).grid(row=32, column=0)


root.mainloop()

# END
