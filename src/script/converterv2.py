import re
import json
import xml.etree.ElementTree as ET
import sys
import os

motion_unit_name=[]
motion_movie_name=[]

servo_type="None"
#konstanta string lokasi file
default_loc="../../data/"
# input
filenameMX="Motion MX Nina (M) NC.mtnx" #to be changed #specify file location and filename
filenameXL="Motion XL Nina NC.mtnx" #to be changed #specify file location and filename
data_loc_mx=filenameMX
data_loc_xl=filenameXL
#output
loc_bucket="../../data/"+servo_type+"/"
loc_movie="../../data/"+servo_type+"/"
loc_unit="../../data/"+servo_type+"/motion_unit/"

#gak kanggo tulis info motion
def write_info_unit(data):
    loc=default_loc+servo_type
    info={"count":len(data)-1}
    to_json=json.dumps(info, indent=4)
    output=open(loc+"/motion_unit_info.json",'w')
    output.write(to_json)
    output.close()

#convert_data_function
def update_variable(servo_type):
    #output
    global loc_bucket
    global loc_movie
    global loc_unit
    
    loc_bucket="../../data/"+servo_type+"/"
    loc_movie="../../data/"+servo_type+"/"
    loc_unit="../../data/"+servo_type+"/motion_unit/"
    
def convert_motion(data, type):
    angelMX = 180
    angelXL = 150
    precisionMX = 0.087890625
    precisionXL = 0.2929687
    converted_data=0
    if(type=="MX"):
        converted_data=(round((data+angelMX)/precisionMX))
    else:
        converted_data=(round((data+angelXL)/precisionXL))
        
    return converted_data

def getbucket(path):
    tree = ET.parse(path)
    root = tree.getroot()

    motion_buckets = []
    motion_bucket_id = 1

    for bucket in root.findall('.//Bucket'):
        motion_bucket = {
            "id": motion_bucket_id,
            "name": bucket.get('name'),
            "motion_movie": []
        }
        
        for movie in bucket.findall('.//callFlow'):
            motion_movie = {
                "id": motion_movie_name.index(movie.get('flow'))+1,#motion_movie_id,
                "name": movie.get('flow')
            }
            motion_bucket["motion_movie"].append(motion_movie)

        motion_buckets.append(motion_bucket)
        motion_bucket_id += 1
    
    return motion_buckets

def getmovie(path):
    tree = ET.parse(path)
    root = tree.getroot()

    motion_movies = []
    motion_movie_id = 1

    for movie in root.findall('.//Flow'):
        #initialize name of unit
        motion_movie_name.append(movie.get('name'))
        
        motion_movie = {
            "id": motion_movie_id,
            "name": movie.get('name'),
            "motion_unit": []
        }

        for unit in movie.findall('.//unit'):
            motion_unit = {
                "id": motion_unit_name.index(unit.get('main')),#motion_unit_id,
                "name": unit.get('main'),
                "speed": unit.get('mainSpeed'),
                "loop": unit.get('loop')
            }
            motion_movie["motion_unit"].append(motion_unit)

        motion_movies.append(motion_movie)
        motion_movie_id += 1
        
    return motion_movies

def getunit(path, servo):
    tree = ET.parse(path)
    root = tree.getroot()

    motion_units = []
    motion_unit_id = 1

    for unit in root.findall('.//Page'):
        #initialize name of unit
        motion_unit_name.append(unit.get('name'))
        
        #ignore motion progrees
        if unit.get('name') == "=== MOTION PROGRES ===":
            motion_unit = {
            "id": 0,
            "name": unit.get('name')
            }
            motion_units.append(motion_unit)
            continue
        
        #get time for each frame
        frames=[]
        for frame in unit.findall('.//step'):
            frames.append(int(frame.get('frame')))
            
        motion_unit = {
            "id": motion_unit_id,
            "name": unit.get('name'),
            "total_frame": len(frames), #len(unit.findall('step')),
            "time": frames, #str(frames),
            "motion_frame": []
        }
        
        for frame in unit.findall('.//step'):
            frame_pose=list(convert_motion(float(i), servo) for i in frame.get('pose').split(" "))
            motion_unit["motion_frame"].append(frame_pose)

        motion_units.append(motion_unit)
        motion_unit_id += 1

    return motion_units

#process_function
def generate_file(data, what):
    if(what==0): #motion_bucket
        to_json=json.dumps({"BUCKET":data}, separators=(',', ':'))
        output_file=open(loc_bucket+"MOTION_BUCKET.json",'w')
        output_file.write(to_json)
        output_file.close()
    elif(what==1): #motion_movie
        to_json=json.dumps({"MOVIE":data}, separators=(',', ':'))
        output_file=open(loc_movie+"MOTION_MOVIE.json",'w')
        output_file.write(to_json)
        output_file.close()
    else: #motion_unit
        iter=0
        for i in data:
            to_json=json.dumps(i, separators=(',', ':'))
            output_file=open(loc_unit+str(iter)+".json",'w')
            output_file.write(to_json)
            output_file.close()
            iter+=1

def start_get(path):
    #filename
    file_inp=path
    global servo_type
    if(re.search("MX", file_inp)!=None):
        servo_type="MX"
        update_variable(servo_type)
        # if not os.path.exists(default_loc+servo_type):
        #     print("[-] Folder missing\n[+] Creating folder...")
        #     os.makedirs(default_loc+servo_type)
    elif(re.search("XL", file_inp)!=None):
        servo_type="XL"
        update_variable(servo_type)
        # if not os.path.exists(default_loc+servo_type):
        #    print("[-] Folder missing\n[+] Creating folder...")
        #    os.makedirs(default_loc+servo_type)
    
    #scrap data from .mtnx
    unit=getunit(file_inp, servo_type)
    movie=getmovie(file_inp)
    bucket=getbucket(file_inp)
    #write_info_unit(unit) #cuma memberitahu berapa banyak motion unit #tidak digunakan
    
    #write data to json separately  
    generate_file(bucket, 0)
    generate_file(movie, 1)
    generate_file(unit, 2)

#main
files=[data_loc_mx, data_loc_xl]
for i in files:
    motion_unit_name=[]
    motion_movie_name=[]
    if re.search("MX", i)!=None or re.search("XL", i)!=None:
        try:
            start_get(i)
            print(f"[+] Convert Success")
        except:
            print("[-] Convert Failed")
            print(f"Exception: {sys.exc_info()[0]}")
    else:
        print("[-] Missing Servo type XL or MX speceifier in file name")