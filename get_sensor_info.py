from os import path, system
from serial import Serial
from datetime import datetime
import pandas as pd

class UpdateDataFile:
    def update(ser):
        
        #Get current date and time
        now = datetime.now()
        time_string = now.strftime("%H%M")
        date_string = now.strftime("%Y_%m_%d")

        #Put time and date in column data
        data_dict = {}
        data_dict["Time"] = time_string
        data_dict["Date"] = date_string
        
        #Also use date for file name
        filename = "/var/www/html/garden-automation/{}_daily_data.csv".format(date_string) 
        if path.exists(filename):
            df = pd.read_csv(filename)
            system("sudo chown -R www-data /var/www/html/garden-automation && sudo chmod -R 774 /var/www/html/garden-automation && sudo chgrp -R www-data /var/www/html/garden-automation".format(filename,filename,filename))
        else:
            df = pd.DataFrame()


        #Loop average# times and average at the end
        averages = 3
        for i in range(averages):
            #Initialize data variables and loop until filled
            humidity_data = []
            temperature_data = []
            while len(humidity_data)<(i+1) or len(temperature_data)<(i+1):
                line = ser.readline().decode('utf-8').rstrip()
                if line.startswith("Humidity (%): "):  humidity_data.append(float(line.replace("Humidity (%): ", "")))
                elif line.startswith("Temperature  (F): "): temperature_data.append(float(line.replace("Temperature  (F): ", "")))

        data_dict["Humidity(%)"] = round(sum(humidity_data)/averages,1)
        data_dict["Temperature(F)"] = round(sum(temperature_data)/averages,1)
        df = pd.concat([df, pd.DataFrame(data_dict,index=[i])])

        df.to_csv(filename, index=False)
        return df

if __name__ == '__main__':
    #ser = Serial('COM4', 9600, timeout=1) # For Windows Environment
    ser = Serial('/dev/ttyACM0', 9600, timeout=1)# For linux environment
    ser.reset_input_buffer()

    df = UpdateDataFile.update(ser)


