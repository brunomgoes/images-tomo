import copy
import glob
import os
import subprocess as sub
from functools import reduce
from math import *

import ipywidgets as widgets
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import plotly
import pydicom
from ipywidgets.widgets import *
from plotly.graph_objs import *


def rename_files(img_dir):
    paths_list = []
    patients = os.listdir(img_dir)

    for patient in patients:
        patient_path = os.path.join(img_dir, patient)
        screenings = os.listdir(patient_path)

        for screening in screenings:
            screening_path = os.path.join(patient_path, screening)
            exams = os.listdir(screening_path)

            for exam in exams:
                exam_path = os.path.join(screening_path, exam)
                img_path = os.path.join(exam_path, '*dcm')
                imgs = glob.glob(img_path)

                for img in imgs:
                    screening_num = screening[-5:]
                    img_name = patient + '-' + screening_num + '-' + exam.replace('.', '-') + '.dcm'
                    img_name = os.path.join(exam_path, img_name)
                    os.rename(img, img_name)
                    paths_list.append(img_name)
    
    return paths_list

def convert_dicom(img):
    img_2 = "E:\\medicalimages\\tomossintese-descompactada\\" + img[-42:]
    command = f"gdcmconv -w {img} {img_2}"
    print(f"> Convertendo  {img}...", end="")
    # command2=['gdcmconv', '-w',original_image_full_path,converted_image_full_path]
    try:
        # sub.run(command2,stdout=sub.PIPE)
        sub.run(command)
        print("SUCESSO")
    except Exception as e:
        print(f"Erro ao converter {img}")
        print(e)

    return img

def img_show(img):
    img = img.pixel_array

    fig, ax = plt.subplots()
    ims = []
    for i in img:
        im = ax.imshow(i, cmap='gray', vmin=0, vmax=4095, animated=True)
        ax.axis('off')
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=500)
    plt.show()

img_dir = 'E:\\medicalimages\\tomossintese'

paths_list = rename_files(img_dir)

for img_path in paths_list:
    img_path = convert_dicom(img_path)
    dicom_file = pydicom.dcmread(img_path)
    print(dicom_file['BitsAllocated'])
    print(dicom_file['NumberOfFrames'])
    print(dicom_file['ViewPosition'])

    img_show(dicom_file)

    print(img_path)
