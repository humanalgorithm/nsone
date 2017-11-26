import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from twisted.internet import reactor
from parsing.csv_reader import NSONECsvReader

file_name = "ZoneData3.csv"
ns_csv_reader = NSONECsvReader(file_name=file_name)
ns_csv_reader.import_zones()
reactor.run()