#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:13:50 2022

@author: nissimolaji
"""





import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats.stats import pearsonr
import os
import numpy
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from scipy.io import wavfile
from mido import MidiFile,MidiTrack
from predict_on_audio import DeepSalience

from Melodia import Melodia
from MidiSplit import MidiSplit
from WavSynth import WavSynth
import math
import pandas as pd
import mir_eval

'Main function'
def main():
     # Add path to the dataset
    Pipeline=EvalPipeline()
    dataset_path = '/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/dataset/j/'
    midi_output_path = '/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/output_midi/deepsalience/Jazz/'
    wav_output_path = '/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/output_wav/deepsalience/Jazz/'
    

    Pipeline.evaluation(dataset_path, midi_output_path, wav_output_path)


'Evaluation pipeline class'
    
class EvalPipeline:
    """
      Compute correlation function ,computes the correlation between the original melody piece and the individual tracks
      
      Parameters: 
      1) Melody data(audio_melody): arr[timestamps,melody,audio_name]
      2) Individual track melody data(the individual tracks that is passed through the melody extractor algorithm): arr with all the tracks arr[timestamps,melody,audio_name]
    """
    
    def compute_correlation(self,audio_melody_data,track_files_data,option):
        #   Gets the time stamps,melody and audio name from the arr audio_melody

        original_timestamps = audio_melody_data[0][0]
        
        original_melody = audio_melody_data[0][1]
        original_audio_name = audio_melody_data[0][3]
          #   Dictionary to store the data

        dictionary ={}
    
        # retrieve the melody greater than 0 and append it to the dictionary

        for t,m in zip(original_timestamps,original_melody):
            if m >0:           
                dictionary[t] = m
        # To store the correlations between the original melody and tracks

        tracks =[]
        correlations=[]
        # Iterate through each track in the audio file

        for track in track_files_data:
            track_dict ={}
            # get the timestamps and melody

            track_timestamps =track[0]
            track_melody = track[1]
            # Only retrieves the melody and timestamps that is greater than 0

            for t,m in zip(track_timestamps,track_melody):
                if m >0:           
                    track_dict[t] = m
            #   Get both the melody timestamps and track timestamps

            keys = list(dictionary.keys() & track_dict.keys())
            try:          
                                # computes the melody correlation on the same timestamps

                corr, _ = pearsonr([dictionary.get(x, 0) for x in keys],[track_dict.get(x, 0) for x in keys])
                corr_round = numpy.round(corr,3)
                # Appends the track name and the correlation between the original and track

                tracks.append(track[3])
                correlations.append(corr_round)
            except:
                pass
            
        
    #     plot_correlation(tracks,correlations,original_audio_name)
        tracks_to_remove=""
        if option=="max":            
            tracks_to_remove = self.max_correlated_track(tracks,correlations,original_audio_name)
        elif option =="least":
            tracks_to_remove = self.least_correlated_track(tracks,correlations,original_audio_name)

        return tracks,correlations,original_audio_name,tracks_to_remove
    
    
    
    
    """
      Removes the track

      Parameters: 
      1) Track name to remove, the original mid file, audio name,output path and the iteration number
     """
    
    def remove_track(self,remove_track,midi_file,audio_file_name,output_path,iteration):
        mid = midi_file
                # Creates a new folder to store the midi file with track removed

        path = output_path + str(audio_file_name)+'/'+'iteration'+str(iteration)
        os.mkdir(path) 
        
                # Creates a new midi file

        original_channel = MidiFile()
        original_channel.ticks_per_beat=mid.ticks_per_beat
    
        channel_present = False
        channel_absent =False
        
                # Iterate through the midi tracks

        for i,track in enumerate(mid.tracks): 
            instrument_channel = MidiFile() # getting the current track
            instrument_channel.ticks_per_beat = mid.ticks_per_beat
                        # gets the track name to remove

            track_to_remove =""
            for m in remove_track:
                                # Checks if the midi file have the track name

                if track.name == m:
                    track_to_remove = track.name
                    
                            #  iterate to append all the other tracks excluding the track to be removed

            if track.name != track_to_remove:
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
                            channel_present =False
                    else:
                        channel_present =False
                                # Track is found

                if channel_present ==True:
                    original_channel.tracks.append(track)
    #     print(iteration)
    #     for i, track in enumerate(original_channel.tracks):
    #         print('Track {}: {}'.format(i, track.name))
        
                
        original_channel.save(path+'/'+str(audio_file_name)+ '.mid')        
        return path   




    """
      Get the max_correlated_ track

      Parameters: 
      1) track name,correlations and audio file name
     """  
    def max_correlated_track(self,track_name,correlation,audio_file_name):
        # Dictionary to store the tracks and corr
        dictionary = {}
    
        for track,correlation in zip(track_name,correlation):
                        # For max track will always be greater than 0 ,so ignoring the negative values

            if correlation >0:
                dictionary[track] =correlation
        try:
                        # Delete the data for the original melody, since its comparing itself the corr will be 1.0

            del dictionary[audio_file_name]
        except:
            pass
        dictionary = dict((k, v) for k, v in dictionary.items() if v >= 0)
        
        is_empty = bool(dictionary)
        if is_empty == True:
                        # Gets the max track data

            max_track = max(dictionary, key=dictionary.get)
            max_corr = dictionary.get(max_track)
            
        #     print(max_track)
        #     print(max_corr)
            return str(max_track)
        
        
      
    """
      Get the least_correlated_track

      Parameters: 
      1) track name,correlations and audio file name
     """  
        
    def least_correlated_track(self,track_name,correlation,audio_file_name):
                # Dictionary to store the tracks and corr

        dictionary= {}
    
        for track,correlation in zip(track_name,correlation):
            print(track)
            dictionary[track] =correlation
        
        try:
            del dictionary[audio_file_name]
        except:
            pass

        
        is_empty = bool(dictionary)
        if is_empty == True:
            least_track_name = min(dictionary, key=dictionary.get)
            least_corr = dictionary.get(least_track_name)
          
            return str(least_track_name)   
     
        
    """
      Plots the correlation plot

      Parameters: 
      1) track name,correlations and audio file name and the tracks that removed
     """
            
    def plot_correlation(self,track_name,correlation,audio_file_name,tracks_removed):
        dictionary = {}
        deleted=False
       
        for track,correlation in zip(track_name,correlation):
            dictionary[track] =correlation
        
        
        positive_correlation = dict((k, v) for k, v in dictionary.items() if v >=0)
        

        is_empty=bool(dictionary)
        
    
      
        sorted_dict= dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

            
        for i in tracks_removed:               
            if i not in dictionary:
                dictionary[i]=0
                print(tracks_removed)
    
    
    
        tracks= list(dictionary.keys())
        corr = list(dictionary.values())
        
       
        
        fig = plt.figure(figsize = (10,5))
    
        ax = plt.subplot()            
    #create chart
        ax.bar(x=tracks, #x-coordinates of bars
                   height=corr, #height of bars
                   color ='seagreen',#error bar width
                   width = 0.5,align='center') #length of error bar caps
        
        
    
        ax.set_yticks([-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1])
        plt.axhline(0, color='dimgray')
        ax.tick_params(axis='both', which='major', labelsize=5)
        ax.set_xlabel('Isolated instrument tracks',fontsize=9)
        ax.set_ylabel("Correlation (r) ",fontsize=9)
        plt.show()
            
            
    """
      Synthesises melody output

     https://github.com/justinsalamon/melosynth
     """
      
            
    def melosynth_output(self,track_path,pop_genre_melody_path,file_name):
        output_file = pop_genre_melody_path +file_name+'.csv'
        wav_file = pop_genre_melody_path+file_name+'.wav'
        melodia = Melodia()

        return melodia.melodia_plugin_melosynth(track_path,output_file,wav_file)
    
    
    
    """
      Returns the time frequency representations of melody for both algorithms

     https://github.com/justinsalamon/melosynth
     """
    
    def melody_extraction_algorithms(self,algorithm_name,audio_file):
        if algorithm_name =='melodia':
            melodia=Melodia()
            timestamps,melody,audio_file=melodia.melodia_plugin(audio_file)
            return timestamps,melody,audio_file
      
        elif algorithm_name=='deepsalience':
            deepsalience=DeepSalience()
            audio_fpath = audio_file
            task = "melody2"
            save_dir = '/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/ismir2017-deepsalience-master/predict/outputs/melody2/'
            output_format="singlef0"
            
            times,freqs=deepsalience.get_parser(audio_fpath,task,save_dir)
            return times,freqs,audio_file

    
    def evaluation(self,genre_dataset_path,genre_midi_output_path,genre_wav_output_path):
        output_melody_file ='/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/melody_output/'

        
        
        correlations_output = []
        recall_output=[]
        for file in os.listdir(genre_dataset_path):
          
                original_melody_data=[]
        
                if not file.startswith('.'):
                    audio_file_name = os.path.splitext(file)[0]
                    audio_file_name_path = genre_dataset_path+file
                     # print("original")
                     # print(audio_file_name)
                    
        # Create directory to store each genre wav files
                    genre_wav_path = genre_wav_output_path + str(audio_file_name)+"/"
                    
                    genre_melody_path = output_melody_file+str(audio_file_name)+"/"
                    os.mkdir(genre_wav_path)       
                    #os.mkdir(genre_melody_path)
                    track_melody_data =[]
        
        
        # Split the track into individual tracks and combine 
                                
                    midi_files,file_in_midi = MidiSplit.split_midi_tracks(audio_file_name_path,genre_midi_output_path)
             
                    for m_file in os.listdir(midi_files):
                        midi_file_name = midi_files+'/'+m_file
                        track_file_name = os.path.splitext(m_file)[0]
        
                   
                        if str(m_file) == str(file):
                            original_wav = WavSynth.wav_synthesizer(midi_file_name,genre_wav_path)
                            
                             #timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", original_wav)
                            timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", original_wav)

                            original_melody_data.append([timestamps,melody,audio_file,track_file_name])
                            #self.melosynth_output(original_wav,pop_genre_melody_path,"initial_iteration")
                            
                            #self.melody_extraction_algorithms("deepsalience", original_wav)
                            
                            

                        else:
                            track_path=WavSynth.wav_synthesizer(midi_file_name,genre_wav_path)
                             #timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", track_path)
                            timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", track_path)


                            
                            
                            
        
                            track_melody_data.append([timestamps,melody,audio_file,track_file_name])
                        
                    tracks,correlations,original_audio_name,track_removed = self.compute_correlation(original_melody_data,track_melody_data,"least")
                    correlations_output.append([original_audio_name,"initial iteration",tracks,correlations,[track_removed]])
    
                     #self.plot_correlation(tracks,correlations,original_audio_name,[track_removed])
    
            
            
        #             Remove  track
                    iteration = 1
                    remove=[]
                    remove.append(track_removed)
        
                    while iteration <=3:
        
                        path_iteration = self.remove_track(remove,file_in_midi,audio_file_name,genre_midi_output_path,iteration)               
                        new_data=[]
                        track_data= track_melody_data
                        
                        for m in remove:
                            for i,track in enumerate(track_data):
                                track_file = track[3]
        
                                if m == track_file:
                                    track_data.pop(i)
                            
                           
                                
                        for i in os.listdir(path_iteration):
                            if not i.startswith('.'):
                                removed_mid_file_name = os.path.splitext(i)[0]
                                removed_file_path = path_iteration+'/'+i
                                removed_file_wav_path = genre_wav_output_path + str(audio_file_name)+"/"+'iteration'+str(iteration)+'/'
                                os.mkdir(removed_file_wav_path)       
                                
                                wav_file = WavSynth.wav_synthesizer(removed_file_path,removed_file_wav_path)
                         #timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", wav_file)
                        timestamps,melody,audio_file=self.melody_extraction_algorithms("melodia", wav_file)

                        #self.melosynth_output(wav_file,pop_genre_melody_path,"iteration"+str(iteration))
    
                        new_data.append([timestamps,melody,audio_file,removed_mid_file_name])
                        tracks,correlations,original_audio_name,track_to_remove  = self.compute_correlation(new_data,track_data,"max")
    
                        remove.append(track_to_remove)
                         # print(remove)
                         #self.plot_correlation(tracks,correlations,original_audio_name,remove)
                        correlations_output.append([original_audio_name,"iteration"+str(iteration),tracks,correlations,[track_to_remove]])
    
    
    
    
                        
    
    
                        
                    # Create directory to store each genre wav files               
                        
                        iteration = iteration +1
         
            
            
        df_corr = pd.DataFrame(correlations_output,columns = ['Audio file name','Iterations','Tracks','Correlations','Tracks removed'])    
        return df_corr.to_csv('/Users/nissimolaji/Desktop/5thyear/Dissertation/Evaluation/Evaluation_output/jazzDSCORRL302.csv')
        
    
            

    

    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()
