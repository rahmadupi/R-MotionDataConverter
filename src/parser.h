#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>
#include <SPIFFS.h>

#include <vector>

#define BUCKET_MOVIE_DATASIZE 150
#define MOVIE_UNIT_DATASIZE 200
#define UNIT_VALUE_DATASIZE 100

#define BUCKET_SIZE 50
#define MOVIE_SIZE 150
#define UNIT_SIZE 200

#define MAX 50

typedef struct MotionUnit {
    int id = 0;
    char name[MAX] = "";
    int time[UNIT_VALUE_DATASIZE];
    int data[UNIT_VALUE_DATASIZE][15];
} MotionUnit;

typedef struct MotionMovie {
    int id = 0;
    char name[MAX] = " ";
    int motion_unit_id[MOVIE_UNIT_DATASIZE];
    float motion_unit_speed[MOVIE_UNIT_DATASIZE];
    int motion_unit_loop[MOVIE_UNIT_DATASIZE];
} MotionMovie;

typedef struct MotionBucket {
    int id = 0;
    char name[MAX] = "";
    int motion_movie_id[BUCKET_MOVIE_DATASIZE];
} MotionBucket;

extern const String motion_bucket_filename;
extern const String motion_movie_filename;
extern const String motion_unit_foldername;

extern MotionBucket *motion_bucket_mx;
extern MotionMovie *motion_movie_mx;
extern MotionUnit *motion_unit_mx;

extern MotionBucket *motion_bucket_xl;
extern MotionMovie *motion_movie_xl;
extern MotionUnit *motion_unit_xl;