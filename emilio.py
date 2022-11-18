
from machine import Pin, ADC, PWM
import usocket as socket
import socket
import network
from time import sleep_ms


pot = ADC(26)# the middle pin on the Potentiometer
pot2 = ADC(27)
pot3 = ADC(28)

def map(x, in_min, in_max, out_min, out_max):
    """ Maps two ranges together """
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)


    
    
    
    
    
    
    
    

ssid = 'Totalplay-F0A5'
password = 'F0A5B88CFzEXMQ39'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Conexion correcta')
print(station.ifconfig())



def pagina_web():
  html = """<!DOCTYPE HTML><html>
<head>
  <meta http-equiv=\"refresh\" content=\"30\">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 2.0rem; }
    p { font-size: 2.0rem; }
    .units { font-size: 1.2rem; }
    .bme-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>Iot Agriculture System</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="bme-labels">Humedad de la tierra:</span> 
    <span>"""+str(percentage)+"""</span>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="bme-labels">Nivel de lluvia:</span>
    <span>"""+str(percentage2)+"""</span>
  </p>
  <p>
    <i class="fas fa-tachometer-alt"></i>
    <span class="bme-labels">Nivel de luz:</span>
    <span>"""+str(percentage3)+"""</span>
  </p>
</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    pot_value = pot.read_u16()
    percentage = map(pot_value,288, 65535,0,100)
    pot_value2 = pot2.read_u16()
    percentage2 = map(pot_value2,288, 65535,0,100)
    pot_value3 = pot3.read_u16()
    percentage3 = map(pot_value3,288, 65535,0,100)
    
    print("Percentage:", percentage, "Raw, ", pot_value)
    print("Percentage2:", percentage2, "Raw, ", pot_value2)
    print("Percentage3:", percentage3, "Raw, ", pot_value3)
    sleep_ms(1000)
    conexion, direccion = s.accept()
    request = conexion.recv(1024)
    respuesta = pagina_web()
    conexion.send('HTTP/1.1 200 OK\n')
    conexion.send('Content-Type: text/html\n')
    conexion.send('Connection: close\n\n')
    conexion.sendall(respuesta)
    conexion.close()

