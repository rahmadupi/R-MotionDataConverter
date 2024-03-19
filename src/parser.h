#pragma once

#define BUCKET_MOVIE_DATASIZE 250
#define MOVIE_UNIT_DATASIZE 500
#define UNIT_VALUE_DATASIZE 1000

typedef struct {
    int id;
    char name[100];
    int data[UNIT_VALUE_DATASIZE][16];
} MotionUnit;

typedef struct {
    int id;
    char name[100];
    int motion_unit_id[MOVIE_UNIT_DATASIZE];
} MotionMovie;

typedef struct {
    int id;
    char name[100];
    int motion_movie_id[BUCKET_MOVIE_DATASIZE];
} MotionBucket;

extern const String motion_bucket_filename;
extern const String motion_movie_filename;
extern const String motion_unit_foldername;

extern MotionBucket motion_bucket[BUCKET_SIZE];
extern MotionMovie motion_movie[MOVIE_SIZE];
extern MotionUnit motion_unit[UNIT_SIZE];

extern MotionBucket motion_bucket_xl[BUCKET_SIZE];
extern MotionMovie motion_movie_xl[MOVIE_SIZE];
extern MotionUnit motion_unit_xl[UNIT_SIZE];