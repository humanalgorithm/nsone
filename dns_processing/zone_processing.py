from twisted.internet import defer
from nsone.rest.errors import ResourceException
from shared.logger import log
from shared.nsone_factory import nsone_async
from shared import zone_store

class ZoneProcessing(object):
    @defer.inlineCallbacks
    def get_or_create_zone(self, zone_name):
        try:
            log("zone_request_load", zone_name)
            zone, source = yield nsone_async.loadZone(zone_name), "LOAD"
        except ResourceException as e:
            if e.message == "server error: zone not found":
                log("zone_request_create", zone_name)
                zone, source = yield nsone_async.createZone(zone_name), "CREATE"
            else: raise e
        defer.returnValue({"zone": zone, "source": source})

    def gotZone(self, zone_result):
        zone_record = zone_result['zone']
        zone_name = zone_record.zone
        zone_store.zone_records[zone_name] = zone_record
        log("zone_{}".format(zone_result['source']), zone_record)

    def handleError(self, failure):
        print failure
