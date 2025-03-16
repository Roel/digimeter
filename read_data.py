import datetime
import os

from lib import p1

from influxdb import InfluxDBClient


def read_secret(variable_name):
    if f'{variable_name}_FILE' in os.environ:
        with open(os.environ.get(f'{variable_name}_FILE'), 'r') as secret_file:
            secret = secret_file.read()
    else:
        secret = os.environ.get(variable_name, None)
    return secret


INFLUX_HOST = os.environ['INFLUX_HOST']
INFLUX_DB = os.environ['INFLUX_DB']
INFLUX_USER = os.environ['INFLUX_USER']
INFLUX_PASSWORD = read_secret('INFLUX_PASSWORD')
READ_INTERVAL = int(os.environ.get('READ_INTERVAL', 30))

dbclient = InfluxDBClient(INFLUX_HOST, database=INFLUX_DB,
                          username=INFLUX_USER, password=INFLUX_PASSWORD)

registers = {
    'Rate 1 (day) - total consumption': 'p1_elec_rate1_fromgrid',
    'Rate 2 (night) - total consumption': 'p1_elec_rate2_fromgrid',
    'Rate 1 (day) - total production': 'p1_elec_rate1_togrid',
    'Rate 2 (night) - total production': 'p1_elec_rate2_togrid',
    'All phases consumption': 'p1_elec_power_fromgrid',
    'All phases production': 'p1_elec_power_togrid',
    'Water consumption': 'p1_water_consumption'
}


def upload_digimeter_data(data):
    now = datetime.datetime.now()
    timestamp = int(now.strftime('%s'))

    if (timestamp+1) % READ_INTERVAL != 0:
        return

    influxdata = []
    # influxdata_24h = []

    for result in data:
        register = result[0]
        value = result[1]
        unit = result[2]

        if register in registers:
            if registers[register] == 'p1_elec_rate1_fromgrid':
                ms = {}
                ms["time"] = timestamp * 10**9

                ms["measurement"] = 'p1_elec_total_fromgrid'
                ms["fields"] = {"value": value}
                ms['tags'] = {"unit": unit, "rate": 'rate1',
                              "month": now.month, "year": now.year}
                if value > 0:
                    influxdata.append(ms)
            elif registers[register] == 'p1_elec_rate2_fromgrid':
                ms = {}
                ms["time"] = timestamp * 10**9

                ms["measurement"] = 'p1_elec_total_fromgrid'
                ms["fields"] = {"value": value}
                ms['tags'] = {"unit": unit, "rate": 'rate2',
                              "month": now.month, "year": now.year}
                if value > 0:
                    influxdata.append(ms)
            elif registers[register] == 'p1_elec_rate1_togrid':
                ms = {}
                ms["time"] = timestamp * 10**9

                ms["measurement"] = 'p1_elec_total_togrid'
                ms["fields"] = {"value": value}
                ms['tags'] = {"unit": unit, "rate": 'rate1',
                              "month": now.month, "year": now.year}
                if value > 0:
                    influxdata.append(ms)
            elif registers[register] == 'p1_elec_rate2_togrid':
                ms = {}
                ms["time"] = timestamp * 10**9

                ms["measurement"] = 'p1_elec_total_togrid'
                ms["fields"] = {"value": value}
                ms['tags'] = {"unit": unit, "rate": 'rate2',
                              "month": now.month, "year": now.year}
                if value > 0:
                    influxdata.append(ms)
            else:
                ms = {}
                ms["time"] = timestamp * 10**9

                ms["measurement"] = registers[register]
                ms["fields"] = {"value": value}
                ms['tags'] = {"unit": unit}
                if value > 0:
                    influxdata.append(ms)

    if len(influxdata) > 0:
        dbclient.write_points(influxdata)


def get_digimeter_data():
    p1.main(upload_digimeter_data)


get_digimeter_data()
