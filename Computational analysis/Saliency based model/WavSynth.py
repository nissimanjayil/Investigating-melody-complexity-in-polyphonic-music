#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:20:03 2022

@author: nissimolaji
"""

'''
WavSynth class converts the midi files into a wav format
'''

from midi2audio import FluidSynth
import os

class WavSynth:
    def wav_synthesizer(midi_files,output_path): 
        file=os.path.basename(midi_files)
        fs = FluidSynth('/Library/Audio/Sounds/Banks/FluidR3Mono_GM.sf3')
        file_name = os.path.splitext(file)[0]
        path = output_path+str(file_name)+'.wav'
        fs.midi_to_audio(midi_files,output_path+str(file_name)+'.wav')
        return path
