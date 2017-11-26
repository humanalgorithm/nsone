import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from twisted.internet import reactor
from parsing.csv_reader import NSONECsvReader

ns_csv_reader = NSONECsvReader()
ns_csv_reader.import_zones()
reactor.run()