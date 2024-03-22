#include "parser.h"

using namespace std;

JsonDocument doc;

JsonObject parse_json(File file) {
    DeserializationError error = deserializeJson(doc, file);
    if (error) {
        Serial.print(F("[-] deserializeJson() failed: "));
        Serial.println(error.f_str());
    }
    JsonObject root = doc.as<JsonObject>();
    return root;
}

void get_motion_bucket(String servo_type) {
    File file = SPIFFS.open("/" + servo_type + motion_bucket_filename, "r");
    if (!file) {
        Serial.println("[-] Failed to open file for reading");
        return;
    } else {
        Serial.println("[+] File opened: " + String(file.name()));
    }

    // parse json file
    JsonObject root = parse_json(file);
    // JsonDocument doc;

    JsonArray motionBucketArray = root["BUCKET"].as<JsonArray>();

    // testonly
    int bucket_size = motionBucketArray.size();
    // testonly
    int movie_size[100];

    for (JsonVariant motionBucket : motionBucketArray) {
        if (servo_type == "MX") {
            int id = motionBucket["id"].as<int>();
            String name = motionBucket["name"].as<String>();
            motion_bucket_mx[id].id = id;
            strcpy(motion_bucket_mx[id].name, name.c_str());
            JsonArray motion_movie = motionBucket["motion_movie"].as<JsonArray>();

            // testonly
            movie_size[id] = motion_movie.size();

            Serial.print("[+] Load Bucket: " + name + " " + servo_type);

            int iter = 1;
            for (JsonVariant motion_movie_id : motion_movie) {
                motion_bucket_mx[id].motion_movie_id[iter++] = motion_movie_id["id"].as<int>();
            }
        } else if (servo_type == "XL") {
            int id = motionBucket["id"].as<int>();
            String name = motionBucket["name"].as<String>();
            motion_bucket_xl[id].id = id;
            strcpy(motion_bucket_xl[id].name, name.c_str());
            JsonArray motion_movie = motionBucket["motion_movie"].as<JsonArray>();

            // testonly
            movie_size[id] = motion_movie.size();

            Serial.print("[+] Load Bucket: " + name + " " + servo_type);

            int iter = 1;
            for (JsonVariant motion_movie_id : motion_movie) {
                motion_bucket_xl[id].motion_movie_id[iter++] = motion_movie_id["id"].as<int>();
            }
        }
        Serial.println(" [+] Done");
        if (file) {
            file.close();
            Serial.println("[+] File closed");
        }
    }
    // for (int i = 1; i <= bucket_size; i++) {
    //     Serial.println("id: " + String(motion_bucket_mx[i].id));
    //     // Serial.println("nama: " + String(motion_bucket_xl[i].name));
    //     for (int j = 1; j <= movie_size[i]; j++) {
    //         String a = " " + String(motion_bucket_mx[i].motion_movie_id[j]);
    //         Serial.print(a);
    //     }
    //     Serial.println();
    //     delay(2000);
    // }
}

void get_motion_movie(String servo_type) {
    File file = SPIFFS.open("/" + servo_type + motion_movie_filename, "r");
    if (!file) {
        Serial.println("[-] Failed to open file for reading");
        return;
    }
    // main
    JsonObject root = parse_json(file);

    if (file) {
        file.close();
        Serial.println("[+] File closed");
    }
}
void get_motion_unit(String servo_type) {
    File dir = SPIFFS.open("/" + servo_type + motion_unit_foldername);

    int count = 0;
    while (dir.openNextFile()) {
        // main
        count++;
    }
    dir.close();
}
void get_data_from_json() {
    for (int i = 0; i < 2; i++) {
        String servo_type = i == 0 ? "MX" : "XL";
        get_motion_bucket(servo_type);
        // get_motion_movie(servo_type);
        // get_motion_unit(servo_type);
    }
}

void setup() {
    // Initialize Serial port
    Serial.begin(115200);
    if (!SPIFFS.begin(true)) {
        Serial.println("[-] An Error has occurred while mounting SPIFFS");
        return;
    }

    get_data_from_json();

    free(motion_bucket_mx);
    // free(motion_movie_mx);
    // free(motion_unit_mx);

    free(motion_bucket_xl);
    // free(motion_movie_xl);
    // free(motion_unit_xl);

    //  File file = SPIFFS.open("/test.json", "r");
    //  if (!file) {
    //      Serial.println("Failed to open file for reading");
    //      return;
    //  }

    // // printf("File opened: %s\n", file.name());

    // size_t size = file.size();
    // printf("File size: %d\n", size);

    // JsonDocument doc;

    // DeserializationError error = deserializeJson(doc, file);
    // if (error) {
    //     Serial.print(F("[-] deseri=alizeJson() failed: "));
    //     Serial.println(error.f_str());
    //     return;
    // }

    // JsonObject root = doc.as<JsonObject>();

    // JsonArray array = doc["data"].as<JsonArray>();
    // for (JsonVariant v : array) {
    //     Serial.println(v.as<int>());
    // }
    // String nama = doc["name"];
    // // for (int i = 0; i < doc["data"].size(); i++) {
    // //     Serial.println(doc["data"][i].asInt());
    // // }
    // Serial.println(nasma);

    // if (root.containsKey("XL_MOTION_BUCKET") && root["XL_MOTION_BUCKET"].is<JsonArray>()) {
    //     JsonArray motionBucketArray = root["XL_MOTION_BUCKET"].as<JsonArray>();
    //     for (JsonVariant motionBucket : motionBucketArray) {
    //         if (motionBucket["id"] == 1) {
    //             const char* name = motionBucket["name"];
    //             Serial.print("Motion Bucket Name: ");
    //             Serial.println(name);
    //             break;
    //         }
    //     }
    // } else {
    //     Serial.println("XL_MOTION_BUCKET not found or not an array");
    // }
}

void loop() {
    // put your main code here, to run repeatedly:
    // print heap
    // Serial.println(ESP.getFreeHeap());
    // print stack
    // Serial.println(ESP.getFreeSketchSpace());
}