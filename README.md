# Rfid_Attendence_System
RFID Crad baseed attendnce system using esp8266 module and using python server.

### Working of RFID Attendance System.

First to capture the card id , RFID card must be brought within the range of 5cm of RFID module. After capturing the card ID RFID module send it with their device ID to nodemcu.

Then nodemcu which is connected to our local router(like Wi-Fi), takes the card and device ID and send request to add attendance, with our data to our python server.

Then python server get a request to add attendance and it process the data and send it to MongoDB cloud to save it.

This data can be visualized on our web application. We can also add remove & edit users and devices through our web application.

Only the admin user will be able to get access to our admin dashboard.
