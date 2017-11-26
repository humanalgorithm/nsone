from nsone import NSONE, Config
from twisted.internet import defer, reactor
import csv
import os
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
file = os.path.join(FILE_DIRECTORY, "ZoneData3.csv")
from nsone.rest.errors import ResourceException

class NSONEFactory():
    def __init__(self):
        self._api_key = "YmZB3gnt2MxolyCCKMOR"
        self._transport = "twisted"
        self._transport_key = "transport"
        self._nsone = None

    def _build_nsone(self):
        config = Config()
        config[self._transport_key] = self._transport
        config.createFromAPIKey(self._api_key)
        self._nsone = NSONE(config=config)
        return self._nsone

    def get_nsone(self):
        if self._nsone:
            return self._nsone
        else:
            return self._build_nsone()


class NSONECsvReader(object):
    def __init__(self):
        self.zone_objects = {}
        self.zone_record_process_queues = {}
        self._nsone = NSONEFactory().get_nsone()
        self._batch_size = 3

    def import_zones(self):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row_data in reader:
                zone_name = row_data['Zone']
                if not self.zone_objects.get(zone_name, None):
                    zone = self.get_or_create_zone(zone_name)
                    zone.addCallback(self.gotZone)
                    zone.addErrback(self.handleError)
                else:
                    if len(self.zone_record_process_queues.get(zone_name, [])) >= self._batch_size:
                        self.process_records_in_queue(zone_name)

                self.add_record_to_process(zone_name, row_data)
        self.process_remaining_queue_records()

    def process_remaining_queue_records(self):
        for zone_name in self.zone_record_process_queues:
            self.process_records_in_queue(zone_name)

    def process_records_in_queue(self, zone_name):
        zone = self.zone_objects.get(zone_name)
        if not zone:
            return
        for row_data in self.zone_record_process_queues[zone_name]:
            record = self.process_record(row_data, zone)
            record.addCallback(self.gotRecord)
            record.addErrback(self.handleError)
        self.zone_record_process_queues[zone_name] = []

    @defer.inlineCallbacks
    def process_record(self, row_data, zone):

        def build_args(key):
            data = {
                "load": {
                    "domain": row_data['Zone'],
                    "rtype": row_data['Type']
                },
                "update": {
                    "rtype": row_data['Type'],
                    "data": row_data['Data'],
                    "ttl": row_data['TTL']
                },
                "create": {
                    "domain": row_data['Zone'],
                    "answers": row_data['Data'],
                    "ttl": row_data['TTL'],
                    "name": row_data['Name']
                }
            }
            args = data[key]
            if row_data['Type'] == "MX" and (key == "update" or key == "create"):
                args['answers'] = [[int(row_data['Data'].split(" ")[0]), row_data['Data'].split(" ")[1]]]
            print "args is ", args
            return args

        try:
            record = yield zone.loadRecord(**build_args("load"))
            record = yield record.update(**build_args("update"))
            print "updated record ", record
        except ResourceException as e:
            if e.message == "server error: record not found":

                func_name = "add_{}".format(row_data['Type'])
                func = getattr(zone, func_name)
                record = yield func(**build_args("create"))
                print "created record ", record
        defer.returnValue(record)

    def gotRecord(self, record_result):
        print record_result

    def add_record_to_process(self, zone_name, record_data):
        if not self.zone_record_process_queues.get(zone_name):
            self.zone_record_process_queues[zone_name] = [record_data]
        else:
            self.zone_record_process_queues[zone_name].append(record_data)

    @defer.inlineCallbacks
    def get_or_create_zone(self, zone_name):
        try:
            zone = yield self._nsone.loadZone(zone_name)
            print "loaded zone ", zone
        except ResourceException as e:
            if e.message == "server error: zone not found":
                zone = yield self._nsone.createZone(zone_name)
                print "created zone ", zone
            else: raise e
        defer.returnValue(zone)

    def gotZone(self, zone_result):
        zone_name = zone_result.zone
        self.zone_objects[zone_name] = zone_result

    def handleError(self, failure):
        print failure

ns_csv_reader = NSONECsvReader()
ns_csv_reader.import_zones()
reactor.run()