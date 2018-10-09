#!/usr/bin/python
from datetime import datetime
import urllib, json
import urllib2
import ssl
import time
import sys
import os.path


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

powerwallip=str(sys.argv[1])

def getcharge():
 charge = urllib2.urlopen("https://" + powerwallip + "/api/system_status/soe", context=ctx)
 return charge

def getaggregates():
 aggregates = urllib2.urlopen("https://" + powerwallip + "/api/meters/aggregates", context=ctx)
 return aggregates

def rounding(x, base=1):
 return int(base * round(float(x)/base))

def rounding1(x, base=1):
 return int(base * round(float(x)/base))

def rounding50(x, base=50):
 return int(base * round(float(x)/base))

def rounding1(x, base=1):
 return int(base * round(float(x)/base))

def writefile(filename,value):
    tempfile="/var/tmp/powerwall/" + str(filename)
    #print ("write " + tempfile)
    f = open(tempfile, 'wb')
    try:
        f.write(str(value) + "\n")
    finally:
        f.close()
#    print (filename + "    " + str(value))
    return()

def readfile(variable):
    filename="/var/tmp/powerwall/" + str(variable)
    #print ("filename is " + filename)
    file = open(filename, 'r')
    value = file.read().replace('\n','')
#    print (variable + value)
    return (value)

aggregates = getaggregates()
data = json.loads(aggregates.read())
datasolar = data["solar"]
dataload = data["load"]
databattery = data["battery"]
datasite = data["site"]



currentday=datetime.now().strftime('%d')


workingdir = r'/var/tmp/powerwall'
if not os.path.exists(workingdir):
 os.makedirs(workingdir)

# Check for new day

if os.path.isfile("/var/tmp/powerwall/powerwall_day"):
 d = open('/var/tmp/powerwall/powerwall_day', 'r')
 fileday = d.read().replace('\n','')

 if fileday==currentday:     # If it's the same day, read initial values from file
  if os.path.isfile("/var/tmp/powerwall/powerwall_solar_exported_newday"):
    solar_exported_newday = readfile("powerwall_solar_exported_newday")
    solar_imported_newday = readfile("powerwall_solar_imported_newday")
    load_exported_newday = readfile("powerwall_load_exported_newday")
    load_imported_newday = readfile("powerwall_load_imported_newday")
    battery_exported_newday = readfile("powerwall_battery_exported_newday")
    battery_imported_newday = readfile("powerwall_battery_imported_newday")
    site_exported_newday = readfile("powerwall_grid_exported_newday")
    site_imported_newday = readfile("powerwall_grid_imported_newday")

    #print ("same day")
#    print (solar_exported_newday)

 else:                       # If it's a new day, start counting from now
    solar_exported_newday = rounding1(datasolar["energy_exported"])
    writefile("powerwall_solar_exported_newday",solar_exported_newday)
    solar_imported_newday = rounding1(datasolar["energy_imported"])
    writefile("powerwall_solar_imported_newday",solar_imported_newday)
    load_exported_newday = rounding1(dataload["energy_exported"])
    writefile("powerwall_load_exported_newday",load_exported_newday)
    load_imported_newday = rounding1(dataload["energy_imported"])
    writefile("powerwall_load_imported_newday",load_imported_newday)
    battery_exported_newday = rounding1(databattery["energy_exported"])
    writefile("powerwall_battery_exported_newday",battery_exported_newday)
    battery_imported_newday = rounding1(databattery["energy_imported"])
    writefile("powerwall_battery_imported_newday",battery_imported_newday)
    site_exported_newday = rounding1(datasite["energy_exported"])
    writefile("powerwall_grid_exported_newday",site_exported_newday)
    site_imported_newday = rounding1(datasite["energy_imported"])
    writefile("powerwall_grid_imported_newday",site_imported_newday)

    writefile("powerwall_day",currentday)
else:
 writefile("powerwall_day",currentday)

 solar_exported_newday = rounding1(datasolar["energy_exported"])
 writefile("powerwall_solar_exported_newday",solar_exported_newday)
 solar_imported_newday = rounding1(datasolar["energy_imported"])
 writefile("powerwall_solar_imported_newday",solar_imported_newday)
 load_exported_newday = rounding1(dataload["energy_exported"])
 writefile("powerwall_load_exported_newday",load_exported_newday)
 load_imported_newday = rounding1(dataload["energy_imported"])
 writefile("powerwall_load_imported_newday",load_imported_newday)
 battery_exported_newday = rounding1(databattery["energy_exported"])
 writefile("powerwall_battery_exported_newday",battery_exported_newday)
 battery_imported_newday = rounding1(databattery["energy_imported"])
 writefile("powerwall_battery_imported_newday",battery_imported_newday)
 site_exported_newday = rounding1(datasite["energy_exported"])
 writefile("powerwall_grid_exported_newday",site_exported_newday)
 site_imported_newday = rounding1(datasite["energy_imported"])
 writefile("powerwall_grid_imported_newday",site_imported_newday)



    #print ("new day")

while True:

 charge = getcharge()
 chargedata = json.loads(charge.read())
 chargepercentage = round(chargedata["percentage"], 2)
 writefile("powerwall_battery_charge",chargepercentage)

 aggregates = getaggregates()
 data = json.loads(aggregates.read())
 datasolar = data["solar"]
 dataload = data["load"]
 databattery = data["battery"]
 datasite = data["site"]
 #print
 solar_last_communication_time = datasolar["last_communication_time"]
 solar_instant_power = rounding1(datasolar["instant_power"])
 writefile("powerwall_solar_power",solar_instant_power)
 solar_instant_reactive_power = rounding1(datasolar["instant_reactive_power"])
 writefile("powerwall_solar_reactive_power",solar_instant_reactive_power)
 solar_instant_apparent_power = rounding1(datasolar["instant_apparent_power"])
 writefile("powerwall_solar_apparent_power",solar_instant_apparent_power)
 solar_frequency = datasolar["frequency"]
 writefile("powerwall_solar_frequency",solar_frequency)

 solar_energy_exported = rounding1(datasolar["energy_exported"])
 writefile("powerwall_solar_exported",solar_energy_exported)
 solar_exported_today = int(solar_energy_exported) - int(solar_exported_newday)
 writefile("powerwall_solar_exported_today",solar_exported_today)

 solar_energy_imported = datasolar["energy_imported"]
 writefile("powerwall_solar_imported",solar_energy_imported)
 solar_imported_today = int(solar_energy_imported) - int(solar_imported_newday)
 writefile("powerwall_solar_imported_today",solar_imported_today)

 solar_instant_average_voltage = round(datasolar["instant_average_voltage"],2)
 writefile("powerwall_solar_voltage",solar_instant_average_voltage)
 solar_instant_total_current = round(datasolar["instant_total_current"],2)
 writefile("powerwall_solar_current",solar_instant_total_current)
 solar_i_a_current = datasolar["i_a_current"]
 solar_i_b_current = datasolar["i_b_current"]
 solar_i_c_current = datasolar["i_c_current"]


 #print
 load_last_communication_time = dataload["last_communication_time"]
 load_instant_power = rounding1(dataload["instant_power"])
 writefile("powerwall_load_power",load_instant_power)
 load_instant_reactive_power = rounding1(dataload["instant_reactive_power"])
 writefile("powerwall_load_reactive_power",load_instant_reactive_power)
 load_instant_apparent_power = rounding1(dataload["instant_apparent_power"])
 writefile("powerwall_load_apparent_power",load_instant_apparent_power)
 load_frequency = dataload["frequency"]
 writefile("powerwall_load_frequency",load_frequency)

 load_energy_exported = dataload["energy_exported"]
 writefile("powerwall_load_exported",load_energy_exported)
 load_exported_today = int(load_energy_exported) - int(load_exported_newday)
 writefile("powerwall_load_exported_today",load_exported_today)

 load_energy_imported = rounding1(dataload["energy_imported"])
 writefile("powerwall_load_imported",load_energy_imported)
 load_imported_today = int(load_energy_imported) - int(load_imported_newday)
 writefile("powerwall_load_imported_today",load_imported_today)



 load_instant_average_voltage = round(dataload["instant_average_voltage"],2)
 writefile("powerwall_load_voltage",load_instant_average_voltage)
 load_instant_total_current = round(dataload["instant_total_current"],2)
 writefile("powerwall_load_current",load_instant_total_current)
 load_i_a_current = dataload["i_a_current"]
 load_i_b_current = dataload["i_b_current"]
 load_i_c_current = dataload["i_c_current"]

 #print
 battery_last_communication_time = databattery["last_communication_time"]
 battery_instant_power = rounding1(databattery["instant_power"])
 writefile("powerwall_battery_power",battery_instant_power)
 battery_instant_reactive_power = rounding1(databattery["instant_reactive_power"])
 writefile("powerwall_battery_reactive_power",battery_instant_reactive_power)
 battery_instant_apparent_power = rounding1(databattery["instant_apparent_power"])
 writefile("powerwall_battery_apparent_power",battery_instant_apparent_power)
 battery_frequency = databattery["frequency"]
 writefile("powerwall_battery_frequency",battery_frequency)
 battery_energy_exported = rounding1(databattery["energy_exported"])
 writefile("powerwall_battery_exported",battery_energy_exported)
 battery_exported_today = int(battery_energy_exported) - int(battery_exported_newday)
 writefile("powerwall_battery_exported_today",battery_exported_today)
 battery_energy_imported = rounding1(databattery["energy_imported"])
 writefile("powerwall_battery_imported",battery_energy_imported)
 battery_imported_today = int(battery_energy_imported) - int(battery_imported_newday)
 writefile("powerwall_battery_imported_today",battery_imported_today)
 battery_instant_average_voltage = round(databattery["instant_average_voltage"],2)
 writefile("powerwall_battery_voltage",battery_instant_average_voltage)
 battery_instant_total_current = round(databattery["instant_total_current"],2)
 writefile("powerwall_battery_current",battery_instant_total_current)
 battery_i_a_current = databattery["i_a_current"]
 battery_i_b_current = databattery["i_b_current"]
 battery_i_c_current = databattery["i_c_current"]


 #print
 site_last_communication_time = datasite["last_communication_time"]
 site_instant_power = rounding1(datasite["instant_power"])
 writefile("powerwall_grid_power",site_instant_power)
 site_instant_reactive_power = rounding1(datasite["instant_reactive_power"])
 writefile("powerwall_grid_reactive_power",site_instant_reactive_power)
 site_instant_apparent_power = rounding1(datasite["instant_apparent_power"])
 writefile("powerwall_grid_apparent_power",site_instant_apparent_power)
 site_frequency = datasite["frequency"]
 writefile("powerwall_grid_frequency",site_frequency)
 site_energy_exported = rounding1(datasite["energy_exported"])
 writefile("powerwall_grid_exported",site_energy_exported)
 site_exported_today = int(site_energy_exported) - int(site_exported_newday)
 writefile("powerwall_grid_exported_today",site_exported_today)
 site_energy_imported = rounding1(datasite["energy_imported"])
 writefile("powerwall_grid_imported",site_energy_imported)
 site_imported_today = int(site_energy_imported) - int(site_imported_newday)
 writefile("powerwall_grid_imported_today",site_imported_today)
 site_instant_average_voltage = round(datasite["instant_average_voltage"],2)
 writefile("powerwall_grid_voltage",site_instant_average_voltage)
 site_instant_total_current = round(datasite["instant_total_current"],2)
 writefile("powerwall_grid_current",site_instant_total_current)
 site_i_a_current = datasite["i_a_current"]
 site_i_b_current = datasite["i_b_current"]
 site_i_c_current = datasite["i_c_current"]




 daydate=datetime.now().strftime('%d')
 if currentday!=daydate:
  currentday=datetime.now().strftime('%d')
  #print "Just changed day"


  solar_exported_newday = rounding1(datasolar["energy_exported"])
  writefile("powerwall_solar_exported_newday",solar_exported_newday)
  load_imported_newday = rounding1(dataload["energy_imported"])
  writefile("powerwall_load_imported_newday",load_imported_newday)
  battery_exported_newday = rounding1(databattery["energy_exported"])
  writefile("powerwall_battery_exported_newday",battery_exported_newday)
  battery_imported_newday = rounding1(databattery["energy_imported"])
  writefile("powerwall_battery_imported_newday",battery_imported_newday)
  site_exported_newday = rounding1(datasite["energy_exported"])
  writefile("powerwall_grid_exported_newday",site_exported_newday)
  site_imported_newday = rounding1(datasite["energy_imported"])
  writefile("powerwall_grid_imported_newday",site_imported_newday)

  writefile("powerwall_day",currentday)



# print
 time.sleep(5)




