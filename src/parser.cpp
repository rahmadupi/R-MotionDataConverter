#include "parser.h"

const String motion_bucket_filename = "/motion_bucket.json";
const String motion_movie_filename = "/motion_movie.json";
const String motion_unit_foldername = "/motion_unit";

MotionBucket *motion_bucket_mx = (MotionBucket *)malloc(sizeof(MotionBucket) * BUCKET_SIZE);
// MotionMovie *motion_movie_mx = (MotionMovie *)malloc(sizeof(MotionMovie) * MOVIE_SIZE);
// MotionUnit *motion_unit_mx = (MotionUnit *)malloc(sizeof(MotionUnit) * UNIT_SIZE);
MotionBucket *motion_bucket_xl = (MotionBucket *)malloc(sizeof(MotionBucket) * BUCKET_SIZE);
// MotionMovie *motion_movie_xl = (MotionMovie *)malloc(sizeof(MotionMovie) * MOVIE_SIZE);
// MotionUnit *motion_unit_xl = (MotionUnit *)malloc(sizeof(MotionUnit) * UNIT_SIZE);
