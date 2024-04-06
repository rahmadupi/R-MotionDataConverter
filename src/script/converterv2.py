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
loc_bucket_sep="../../data/"+servo_type+"/motion_bucket/"
loc_movie="../../data/"+servo_type+"/"
loc_movie_sep="../../data/"+servo_type+"/motion_movie/"
loc_unit="../../data/"+servo_type+"/motion_unit/"

def verify_path():
    if not os.path.exists(loc_bucket_sep):
        print("[-] Folder missing\n[+] Creating folder..." + loc_bucket_sep)
        os.makedirs(loc_bucket_sep)
    if not os.path.exists(loc_movie_sep):
        print("[-] Folder missing\n[+] Creating folder..."+ loc_movie_sep)
        os.makedirs(loc_movie_sep)
    if not os.path.exists(loc_unit):
        print("[-] Folder missing\n[+] Creating folder..."+ loc_unit)
        os.makedirs(loc_unit)
        

#convert_data_function
def update_variable(servo_type):
    #output
    global loc_bucket
    global loc_bucket_sep
    global loc_movie
    global loc_movie_sep
    global loc_unit
    
    loc_bucket="../../data/"+servo_type+"/"
    loc_bucket_sep="../../data/"+servo_type+"/motion_bucket/"
    loc_movie="../../data/"+servo_type+"/"
    loc_movie_sep="../../data/"+servo_type+"/motion_movie/"
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

def getbucket(path, movie_data, unit_data):
    tree = ET.parse(path)
    root = tree.getroot()

    motion_buckets = []
    motion_bucket_id = 0
    
    for bucket in root.findall('.//Bucket'):
        motion_bucket = {
            "id": motion_bucket_id,
            "name": bucket.get('name'),
            "total_movie": len(bucket.findall('.//callFlow')),
            "motion_movie": []
        }
        start_frame=0;
        for movie in bucket.findall('.//callFlow'):
            #getting frame duration
            end_frame=0;
            for unit in movie_data[motion_movie_name.index(movie.get('flow'))]["motion_unit"]:
                end_frame+=unit_data[unit["id"]]["time"][unit_data[unit["id"]]["total_frame"]-1]
            end_frame+=start_frame
            motion_movie = {
                "id": motion_movie_name.index(movie.get('flow')),#motion_movie_id,
                "name": movie.get('flow'),
                "start_frame": start_frame,
                "end_frame": end_frame
            }
            motion_bucket["motion_movie"].append(motion_movie)
            
            start_frame=end_frame+1

        motion_buckets.append(motion_bucket)
        motion_bucket_id += 1
    
    return motion_buckets

def getmovie(path):
    tree = ET.parse(path)
    root = tree.getroot()

    motion_movies = []
    motion_movie_id = 0

    for movie in root.findall('.//Flow'):
        #initialize name of unit
        motion_movie_name.append(movie.get('name'))
        
        motion_movie = {
            "id": motion_movie_id,
            "name": movie.get('name'),
            "total_unit": len(movie.findall('.//unit')),##
            "motion_unit": []
        }

        for unit in movie.findall('.//unit'):
            motion_unit = {
                "id": motion_unit_name.index(unit.get('main')),#motion_unit_id,
                # "name": unit.get('main'),
                "speed": float(unit.get('mainSpeed')),
                "loop": int(unit.get('loop'))
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
        to_json=json.dumps(data, separators=(',', ':'))
        output_file=open(loc_bucket+"MOTION_BUCKET.json",'w')
        output_file.write(to_json)
        output_file.close()
        
        iter=0
        for i in data:
            to_json=json.dumps(i, separators=(',', ':'))
            output_file=open(loc_bucket_sep+str(iter)+".json",'w')
            output_file.write(to_json)
            output_file.close()
            iter+=1
            
            
    elif(what==1): #motion_movie
        to_json=json.dumps(data, separators=(',', ':'))
        output_file=open(loc_movie+"MOTION_MOVIE.json",'w')
        output_file.write(to_json)
        output_file.close()
        
        iter=0
        for i in data:
            to_json=json.dumps(i, separators=(',', ':'))
            output_file=open(loc_movie_sep+str(iter)+".json",'w')
            output_file.write(to_json)
            output_file.close()
            iter+=1
            
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
    elif(re.search("XL", file_inp)!=None):
        servo_type="XL"
        update_variable(servo_type)
    
    #verify output path is exist
    verify_path()
    
    #scrap data from .mtnx
    unit_data=getunit(file_inp, servo_type)
    movie_data=getmovie(file_inp)
    bucket_data=getbucket(file_inp, movie_data, unit_data)
    
    #write data to json separately  
    generate_file(bucket_data, 0)
    generate_file(movie_data, 1)
    generate_file(unit_data, 2)

#main
files=[data_loc_mx, data_loc_xl]
for i in files:
    motion_unit_name=[]
    motion_movie_name=[]
    if re.search("MX", i)!=None or re.search("XL", i)!=None:
        start_get(i)
        print(f"[+] Convert Success")
        # try:
        #     start_get(i)
        #     print(f"[+] Convert Success")
        # except:
        #     print("[-] Convert Failed")
        #     print(f"Exception: {sys.exc_info()[0]}")
    else:
        print("[-] Missing Servo type XL or MX speceifier in file name")