import csv
import os
from dns_processing.zone_processing import ZoneProcessing
from dns_processing.record_processing import RecordProcessing
from shared import zone_store

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")
file = os.path.join(FILE_DIRECTORY, "ZoneData3.csv")


class NSONECsvReader():
    def __init__(self):
        self._batch_size = 4
    def import_zones(self):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row_data in reader:
                zone_name = row_data['Zone']
                if not zone_store.zone_records.get(zone_name, None):
                    zone = ZoneProcessing().get_or_create_zone(zone_name)
                    zone.addCallback(ZoneProcessing().gotZone)
                    zone.addErrback(ZoneProcessing().handleError)
                else:
                    if len(zone_store.zone_record_queues.get(zone_name, [])) >= self._batch_size:
                        QueueProcessing().process_row_data_in_zone_queue(zone_name)

                QueueProcessing().add_row_data_to_zone_record_queues(zone_name, row_data)
        zone_store.all_rows_processed = True
        QueueProcessing().process_remaining_queue_records()

class QueueProcessing():
    def process_remaining_queue_records(self):
        for zone_name in zone_store.zone_record_queues:
            self.process_row_data_in_zone_queue(zone_name)

    def add_row_data_to_zone_record_queues(self, zone_name, row_data):
        if not zone_store.zone_record_queues.get(zone_name):
            zone_store.zone_record_queues[zone_name] = [row_data]
        else:
            zone_store.zone_record_queues[zone_name].append(row_data)

    def process_row_data_in_zone_queue(self, zone_name):
        zone = zone_store.zone_records.get(zone_name)
        if not zone:
            return
        for row_data in zone_store.zone_record_queues[zone_name]:
            record = RecordProcessing().process_record(row_data, zone)
            record.addCallback(RecordProcessing().gotRecord, row_data=row_data)
            record.addErrback(ZoneProcessing().handleError)