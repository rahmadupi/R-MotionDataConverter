#include "parser.h"
#define BUCKET_SIZE 50
#define MOVIE_SIZE 250
#define UNIT_SIZE 500

const String motion_bucket_filename = "/motion_bucket.json";
const String motion_movie_filename = "/motion_movie.json";
const String motion_unit_foldername = "/motion_unit";

MotionBucket motion_bucket_mx[BUCKET_SIZE];
MotionMovie motion_movie_mx[MOVIE_SIZE];
MotionUnit motion_unit_mx[UNIT_SIZE];

MotionBucket motion_bucket_xl[BUCKET_SIZE];
MotionMovie motion_movie_xl[MOVIE_SIZE];
MotionUnit motion_unit_xl[UNIT_SIZE];
