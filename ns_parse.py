import csv
import argparse
import os
import sys
import nsone
from nsone.zones import Zone
import getopt
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
file = os.path.join(FILE_DIRECTORY, "ZoneData3.csv")

nx_ttl_default = 3600

class NSONECsvReader(object):
    def __init__(self, *args, **kwargs):
        self.processed_zones = set()
        self._nsone = nsone.NSONE(apiKey='YmZB3gnt2MxolyCCKMOR')

    def import_zones(self):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                zone_name = row['Zone']
                ns_zone = self._process_zone(zone_name)

    def _process_zone(self, zone_name):
        zone_name_processed_from_file = zone_name in self.processed_zones
        ns_zone = self._nsone.loadZone(zone_name)
        if zone_name_processed_from_file:
            return ns_zone
        else:
            if not ns_zone:
                ns_zone = self._nsone.create_zone(zone_name, nx_ttl=nx_ttl_default)
            else:
                print "ns zone is ", ns_zone
                ns_zone = ns_zone.update(nx_ttl=nx_ttl_default)
            self.processed_zones.add(zone_name)
            return ns_zone

if __name__ == "__main__":

    #parser = argparse.ArgumentParser(description='Adds zone records to nsone')
    #parser.add_argument('--overwrite-zone', action="store_true", help='Use this if you would like to overwrite existing zone records')
    #parser.add_argument('--overwrite-records', action="store_true", help='Use this if you would like to overwrite existing zone records')
    #args = parser.parse_args()
    NSONECsvReader().import_zones()