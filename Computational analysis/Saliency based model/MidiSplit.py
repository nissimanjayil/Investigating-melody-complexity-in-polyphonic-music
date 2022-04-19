#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nissimol Aji
"""

import os
from mido import MidiFile,MidiTrack


'''

MidiSplit class, splits the midi files into individual midi file track
'''
class MidiSplit:
    
    def split_midi_tracks(midi_file,output_path):
        try:
            file=os.path.basename(midi_file)
            file_name = os.path.splitext(file)[0]
            mid = MidiFile(midi_file,clip=True)
            path = output_path + str(file_name)
            os.mkdir(path) 
            original_channel = MidiFile()
            original_channel.ticks_per_beat=mid.ticks_per_beat
        
            channel_present = False
            channel_absent =False
            count =0 
            for i,track in enumerate(mid.tracks): 
                
                if len(track.name) == 0:
                    track.name = "piano track "+str(count)
                    count = count+1
                    print('Track {}: {}'.format(i, track.name))
                    
                    

                instrument_channel = MidiFile() # getting the current track
                instrument_channel.ticks_per_beat = mid.ticks_per_beat
        
                for msg in track:
                    if msg.is_meta ==False:
                        try:
                            if msg.channel >=0:
                                channel_absent = False
                                channel_present = True
                                break
                            else:
                                channel_present = False
                        except:
                            channel_present=False
                    else:
                        channel_present =False
                if channel_present ==True:
                    instrument_channel.tracks.append(track)
                    original_channel.tracks.append(track)
        
                    instrument_channel.save(output_path+'/'+str(file_name) +'/'+str(track.name)+ '.mid')
            original_channel.save(output_path+'/'+str(file_name) +'/'+ str(file_name)+ '.mid')
        
            return path,mid     
        except:
            print("Mid file does not contains track names or the channels are not in chronological order")