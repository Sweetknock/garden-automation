#!/usr/bin/env python3
import os
import sys
from serial import Serial
from datetime import datetime
import pandas as pd

class UpdateDataFile:
    def update(self, ser):

        date_string, time_string =  self.get_datetime()
        filename = "{}_daily_data.csv".format(date_string) 

        #initialize dictionary
        #Put time and date in column data
        data_dict = {}
        data_dict["Time"] = time_string
        data_dict["Date"] = date_string

        #Also use date for file name
        #filename = "/var/www/html/garden-automation/{}_daily_data.csv".format(date_string) 
        if os.path.exists(filename):
            df = self.get_database(filename)
        else:
            df = pd.DataFrame()


        #Loop average# times and average at the end
        averages = 3
        for i in range(averages):
            #Initialize data variables and loop until filled
            humidity_data = []
            temperature_data = []
            while len(humidity_data)<(i+1) or len(temperature_data)<(i+1):
                line1 = ser.readline().decode('utf-8').rstrip()
                if line1 == '': line1 = ser.readline().decode('utf-8').rstrip()
                line2 = ser.readline().decode('utf-8').rstrip()

                if line1.startswith("Humidity(%),"):  
                    humidity_data.append(float(line1.replace("Humidity(%),", "")))
                    temperature_data.append(float(line2.replace("Temperature(F),", "")))
                elif line1.startswith("Temperature(F),"):
                    humidity_data.append(float(line2.replace("Humidity(%),", ""))) 
                    temperature_data.append(float(line1.replace("Temperature(F),", "")))
                else:
                    print("Data read error.")
                    continue

        data_dict["Humidity(%)"] = round(sum(humidity_data)/averages,1)
        data_dict["Temperature(F)"] = round(sum(temperature_data)/averages,1)
        df = pd.concat([df, pd.DataFrame(data_dict,index=[i])])

        df.to_csv(filename, index=False)
        return df
    
    def get_datetime(self):
        #Get current date and time
        now = datetime.now()
        time_string = now.strftime("%H%M")
        date_string = now.strftime("%Y_%m_%d")

        return date_string, time_string

    def get_database(self, filename):
        if os.path.exists(filename):
            os.system("sudo chown -R www-data /var/www/html/garden-automation && sudo chmod -R 774 /var/www/html/garden-automation && sudo chgrp -R www-data /var/www/html/garden-automation".format(filename,filename,filename))
            df = pd.read_csv(filename)
            return df

if __name__ == '__main__':
    if os.name == 'nt':
        ser = Serial('COM4', 9600, timeout=1)# For linux environment
    elif os.name == 'posix':
        ser = Serial('/dev/ttyACM0', 9600, timeout=1)# For linux environment
    else:
        print("System not supported.")
        sys.exit()
    ser.reset_input_buffer()

    df = UpdateDataFile().update(ser)


