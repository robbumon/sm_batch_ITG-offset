import os
import shutil
import simfile
import tkinter as tk
from tkinter import filedialog

# --- OFFSET FOR FILES ---
input_offset = 0.009


class StepFile:
    def __init__(self, path, title, offset_old, offset_new, sample_old, sample_new):
        self.path = path
        self.title = title
        self.offset_old = offset_old
        self.offset_new = offset_new
        self.sample_old = sample_old
        self.sample_new = sample_new


StepFiles = []


def get_folder_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    return file_path


def backup_folder(_path):
    dest =os.path.dirname(_path)
    dir = os.path.basename(_path)
    dest = dest + '/' + dir + '_NULL'
    dest = shutil.copytree(_path, dest)
    print('copied folder')


def update_offset(_path, _offset):
    for (dirpath, dirnames, filenames) in os.walk(_path):

        # check files
        for f in filenames:
            smPath = os.path.join(dirpath, f)
            FileExtension = os.path.splitext(smPath)[1]
            if FileExtension == '.sm':
                print(smPath)
                sim = simfile.open(smPath)
                print(sim.offset)
                oldoffset = float(sim.offset)
                oldsample = float(sim.samplestart)
                sim.offset = str(oldoffset + input_offset)
                sim.samplestart = str(oldsample + input_offset)
                with open(smPath, 'w', encoding='utf-8') as outfile:
                    sim.serialize(outfile)


# --- MAIN PROGRAM ---
packpath = get_folder_dialog()
backup_folder(packpath)
update_offset(packpath, input_offset)