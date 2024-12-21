#include <HTTPClient.h>

#include <WiFi.h>

// WiFi credentials
const char* ssid = "";
const char* password = "";

// Server details
const char* serverDataUrl = "http://192.168.12.179:5000/api/esp_data";

// LDR pins
const int ldrPins[] = {4, 5, 6, 7};
const int numLDRs = sizeof(ldrPins) / sizeof(ldrPins[0]);

// Global variables to store sector and table IDs
String sectorID = "";
int tableID = -1;

void setup() {
  Serial.begin(115200);

  // Initialize LDR pins
  for (int i = 0; i < numLDRs; i++) {
    pinMode(ldrPins[i], INPUT);
  }

  // Connect to Wi-Fi
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");

  // Get initial data (sector and table IDs) from the server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverDataUrl);
    http.addHeader("Content-Type", "application/json");

    // Send MAC address to get the IDs
    String macAddress = WiFi.macAddress();
    String initialPayload = "{";
    initialPayload += "\"sectorID\":\"\",";
    initialPayload += "\"tableID\":\"\",";
    initialPayload += "\"MAC\":\"" + macAddress + "\",";
    initialPayload += "\"data\":\"\"";
    initialPayload += "}";

    int httpResponseCode = http.POST(initialPayload);
    if (httpResponseCode > 0) {
      String responseBody = http.getString();
      Serial.println("Initial server response: " + responseBody);

      // Parse the response to extract sector_id and table_id
      int sectorStart = responseBody.indexOf("\"sector_id\":") + 14;
      int sectorEnd = responseBody.indexOf("\"", sectorStart);
      if (sectorStart > 12 && sectorEnd > sectorStart) {
        sectorID = responseBody.substring(sectorStart, sectorEnd);
        Serial.println("Received sector ID: " + sectorID);
      } else {
        Serial.println("Failed to extract sector ID from response.");
      }

      int tableStart = responseBody.indexOf("\"table_id\":") + 11;
      int tableEnd = responseBody.indexOf(",", tableStart);
      if (tableStart > 10) {
        tableID = responseBody.substring(tableStart, tableEnd).toInt();
        Serial.println("Received table ID: " + String(tableID));
      } else {
        Serial.println("Failed to extract table ID from response.");
      }
    } else {
      Serial.println("Error getting initial IDs: " + String(http.errorToString(httpResponseCode).c_str()));
    }
    http.end();
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Count how many LDRs are dark
    int darkCount = 0;
    for (int i = 0; i < numLDRs; i++) {
      int value = digitalRead(ldrPins[i]);
      Serial.print("Sensor");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(value);
      if (value == 0) {
        darkCount++;
      }
    }

    // Prepare JSON payload
    String macAddress = WiFi.macAddress();
    String payload = "{";
    payload += "\"sectorID\":\"" + String(sectorID) + "\",";
    payload += "\"tableID\":" + ((tableID >= 0) ? String(tableID): "\"\"") + ",";
    payload += "\"MAC\":\"" + macAddress + "\",";
    payload += "\"data\":\"" + String(darkCount) + "\"";
    payload += "}";

    Serial.println("Sending data: " + payload);

    http.begin(serverDataUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.println("Response: " + String(httpResponseCode));
      Serial.println("Response body: " + http.getString());
    } else {
      Serial.println("Error sending data: " + String(http.errorToString(httpResponseCode).c_str()));
    }

    http.end();
  } else {
    Serial.println("Wi-Fi not connected");
  }

  delay(5000); // Wait 5 seconds before sending data again
}