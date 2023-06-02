from flask import Flask, render_template
from get_sensor_info import UpdateDataFile, Serial, name, sys

app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    if name == 'nt':
        ser = Serial('COM4', 9600, timeout=1)# For linux environment
    elif name == 'posix':
        ser = Serial('/dev/ttyACM0', 9600, timeout=1)# For linux environment
    else:
        print("System not supported.")
        sys.exit()
        
    ser.reset_input_buffer()
    df = UpdateDataFile.update(ser)
    return render_template('index.html', tables=[df.to_html(classes='table-bordered', index=False)], titles=["Bed Data"])

if __name__ == "__main__":
    app.run()
