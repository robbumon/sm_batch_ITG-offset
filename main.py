import os
import shutil
import fileinput
from pathlib import Path
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

                replaced_content = ''
                # read file
                smFile = open(smPath, 'r+', encoding='utf-8')
                for line in smFile:
                    newline = line.strip()

                    if '#TITLE:' in line:
                        smTitle = line[7:-2]
                    if '#OFFSET:' in line:
                        smOffset_old = round(float(line[8:-2]),3)
                        smOffset_new = round(smOffset_old + _offset,3)
                        newline = '#OFFSET:' + str(smOffset_new) + ';'

                    if '#SAMPLESTART:' in line:
                        smSamplestart_old = round(float(line[13:-2]),3)
                        smSamplestart_new = round(smSamplestart_old + _offset,3)
                        newline = '#SAMPLESTART:' + str(smSamplestart_new) + ';'

                    replaced_content = replaced_content + newline + '\n'

                output = StepFile(smPath, smTitle, smOffset_old, smOffset_new, smSamplestart_old, smSamplestart_new)
                StepFiles.append(output)

                smFile.close()

                # write content to file
                write_file = open(smPath, 'w')
                write_file.write(replaced_content)
                write_file.close()

                # loop through array and print stepfile objects
                for x in StepFiles:
                    printoutput = x.title + ' | ' + str(x.offset_old) + ' => ' + str(x.offset_new) + "\n"
                    printoutput = printoutput + str(x.sample_old) + ' => ' + str(x.sample_new)
                    print(printoutput)


# --- MAIN PROGRAM ---
packpath = get_folder_dialog()
backup_folder(packpath)
update_offset(packpath, input_offset)