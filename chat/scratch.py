import hashlib
import pdb
import datetime

FIRST_CUTOFF = 0
SECOND_CUTOFF = 487167212443634306067894944238761006551977514325L
THIRD_CUTOFF = 974334424887268612135789888477522013103955028650L


CUTOFF_TO_TEAM_MAP = {
    FIRST_CUTOFF : 'red',
    SECOND_CUTOFF : 'blue',
    THIRD_CUTOFF : 'green'
}


ip_list = [
"8.206.27.226",
"214.94.244.21",
"14.232.183.211",
"15.233.105.169",
"83.84.121.174",
"233.167.91.52",
"222.246.74.119",
"57.231.204.64",
"183.230.36.143",
"70.26.163.84",
"4.91.40.18",
"70.145.186.152",
"229.53.71.208",
"219.162.6.187",
"154.79.52.210",
"56.1.19.238",
"230.54.126.46",
"80.35.129.83",
"126.169.100.195",
"59.31.92.34",
"83.162.241.48",
"69.246.235.223",
"71.32.178.126",
"32.196.110.8",
"250.236.53.75",
"17.181.157.142",
"96.3.82.155",
"34.173.188.116",
"81.175.164.150",
"166.145.118.237",
"204.70.171.144",
"87.215.233.120",
"112.215.49.127",
"95.245.175.85",
"110.40.24.252",
"145.195.225.49",
"2.114.105.144",
"83.151.130.33",
"221.47.177.54",
"8.155.173.120",
"115.222.246.210",
"212.167.41.68",
"206.64.65.97",
"5.36.145.7",
"149.249.150.232",
"146.26.10.112",
"73.187.166.80",
"88.84.199.202",
"52.191.158.9",
"103.198.76.55",
"8.141.151.12",
"176.41.18.71",
"36.168.48.181",
"193.58.39.11",
"244.204.91.77",
"34.36.25.85",
"226.182.93.75",
"126.168.129.133",
"55.25.144.231",
"65.161.47.100",
"120.119.43.197",
"25.132.122.233",
"4.172.240.76",
"79.94.212.205",
"17.79.228.22",
"222.124.56.139",
"1.22.145.183",
"179.155.182.44",
"19.225.241.44",
"103.109.23.107",
"26.9.183.105",
"102.140.55.119",
"219.28.140.186",
"152.195.71.152",
"217.216.81.142",
"116.9.185.135",
"234.171.179.82",
"25.201.188.51",
"210.116.155.57",
"2.210.175.220",
"238.61.152.136",
"1.222.34.218",
"184.114.105.45",
"122.36.180.101",
"206.104.183.231",
"51.116.27.6",
"231.182.62.233",
"138.237.198.122",
"43.96.3.44",
"64.36.7.247",
"222.225.95.116",
"220.201.113.36",
"254.149.178.21",
"192.159.141.88",
"151.194.94.41",
"233.245.86.63",
"204.252.135.243",
"121.1.67.88",
"225.162.204.191",
"108.63.226.107",
"211.149.128.149",
"54.14.237.205",
"208.76.245.187",
"67.77.249.16",
"74.130.4.195",
"130.71.29.101",
"232.232.37.85",
"41.9.192.252",
"158.65.147.211",
"79.129.161.32",
"205.151.218.18",
"228.213.33.47",
"88.37.242.218",
"108.16.65.85",
"248.101.170.34",
"109.108.31.12",
"172.177.223.251",
"52.129.29.2",
"26.246.19.254",
"205.52.47.39",
"149.15.50.71",
"10.66.61.242",
"50.4.28.159",
"121.216.137.50",
"170.171.52.204",
"226.160.83.34",
"125.123.132.187",
"160.251.208.54",
"11.3.124.20",
"69.185.8.118",
"188.35.22.55",
"251.159.105.166",
"76.156.116.47",
"61.199.81.186",
"67.212.118.226",
"209.72.25.219",
"75.149.239.143",
"79.246.7.13",
"27.29.67.23",
"187.171.188.8",
"72.50.55.133",
"248.135.65.60",
"93.183.32.47",
"1.56.12.75",
"205.250.218.29",
"242.224.41.14",
"253.108.36.185",
"24.224.193.96",
"19.247.229.13",
"127.40.73.220",
]


#def test():
#    start_time = datetime.datetime.now()
#    for i in xrange(100000):
#    result_dict = {}
#    for ip in ip_list:
#        team = _get_team_from_ip(ip)
#        if team not in result_dict:
#            result_dict[team] = 0
#        result_dict[team] += 1
#    end_time = datetime.datetime.now()
#    duration_delta = end_time - start_time
#    duration_ms = (duration_delta.seconds * 1000) + (float(duration_delta.microseconds) / 1000)
#
#    return duration_ms


def _get_team_from_ip(ip="127.40.73.220", trials=10000):
    start_time = datetime.datetime.now()
    for i in xrange(trials):
        digest = hashlib.sha1(ip).hexdigest()
        digest_int = int(digest, 16)
        if FIRST_CUTOFF <= digest_int < SECOND_CUTOFF:
            team = CUTOFF_TO_TEAM_MAP[FIRST_CUTOFF]
        elif SECOND_CUTOFF <= digest_int < THIRD_CUTOFF:
            team = CUTOFF_TO_TEAM_MAP[SECOND_CUTOFF]
        elif THIRD_CUTOFF <= digest_int:
            team = CUTOFF_TO_TEAM_MAP[THIRD_CUTOFF]
        else:
            raise ValueError("Clusterfuck has ensued")
    end_time = datetime.datetime.now()
    duration_delta = end_time - start_time
    duration_ms = (duration_delta.seconds * 1000) + (float(duration_delta.microseconds) / 1000)
    return duration_ms


def test(trials):
    return _get_team_from_ip(trials=trials)