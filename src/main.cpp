#include <Arduino.h>
#include <ArduinoJson.h>
#include <SPIFFS.h>

#include "parser.h"

// todo: move const of json file name to another folder

void get_motion_bucket(String servo_type) {
    File file = SPIFFS.open("/" + servo_type + motion_bucket_filename, "r");
    if (!file) {
        Serial.println("[-] Failed to open file for reading");
        return;
    }

    // main

    if (file) {
        file.close();
        Serial.println("[+] File closed");
    }
}

void get_motion_movie(String servo_type) {
    File file = SPIFFS.open("/" + servo_type + motion_movie_filename, "r");
    if (!file) {
        Serial.println("[-] Failed to open file for reading");
        return;
    }
    // main

    if (file) {
        file.close();
        Serial.println("[+] File closed");
    }
}
void get_motion_unit(String servo_type) {
    dir_t dir = SPIFFS.openDir("/" + servo_type + motion_unit_foldername);
    if (!file) {
        Serial.println("[-] Failed to open file for reading");
        return;
    }
    int count = 0;
    while (dir.openNextFile()) {
        // main
        count++;
    }
    dir.close();
}
void get_data_from_json() {
}

void setup() {
    // Initialize Serial port
    Serial.begin(115200);
    if (!SPIFFS.begin(true)) {
        Serial.println("[-] An Error has occurred while mounting SPIFFS");
        return;
    }

    File file = SPIFFS.open("/test.json", "r");
    if (!file) {
        Serial.println("Failed to open file for reading");
        return;
    }

    // printf("File opened: %s\n", file.name());

    size_t size = file.size();
    printf("File size: %d\n", size);

    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, file);
    if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
    }

    JsonObject root = doc.as<JsonObject>();

    JsonArray array = doc["data"].as<JsonArray>();
    for (JsonVariant v : array) {
        Serial.println(v.as<int>());
    }
    String nama = doc["name"];
    // for (int i = 0; i < doc["data"].size(); i++) {
    //     Serial.println(doc["data"][i].asInt());
    // }
    Serial.println(nama);

    if (root.containsKey("XL_MOTION_BUCKET") && root["XL_MOTION_BUCKET"].is<JsonArray>()) {
        JsonArray motionBucketArray = root["XL_MOTION_BUCKET"].as<JsonArray>();
        for (JsonVariant motionBucket : motionBucketArray) {
            if (motionBucket["id"] == 1) {
                const char* name = motionBucket["name"];
                Serial.print("Motion Bucket Name: ");
                Serial.println(name);
                break;
            }
        }
    } else {
        Serial.println("XL_MOTION_BUCKET not found or not an array");
    }
}

void loop() {
    // put your main code here, to run repeatedly:
}