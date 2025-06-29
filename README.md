## Introduction
This is a small project of integrating a light detection sensor to a microcontroller (ESP32), and display the real-time light data on web applications(Flask application and Grafana dashboard).<br><br>
<b>How it works:</b>
ESP32 --- light data ---> Web server ---> Stores light data in InfluxDB ---> Flask web application and Grafana reads data from database. 

## Preview

### Webpage
![image](https://github.com/user-attachments/assets/ff54c8dc-049b-43a5-971d-20f44a099f16)

### Grafana
![image](https://github.com/user-attachments/assets/afd8ff97-20ef-45a6-a68b-d0378fa75d5a)
