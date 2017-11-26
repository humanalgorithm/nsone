from twisted.internet import defer, reactor
from nsone.rest.errors import ResourceException
from shared.logger import log
from shared import zone_store


class RecordProcessing():
    @defer.inlineCallbacks
    def process_record(self, row_data, zone):
        try:
            record, source = yield zone.loadRecord(**ArgsBuilder().build_args("load", row_data)), "LOAD"
            record, source = yield record.update(
                **ArgsBuilder().build_args("update", row_data, record.answers)), "UPDATE"
        except ResourceException as e:
            if e.message == "server error: record not found":
                func_name = "add_{}".format(row_data['Type'])
                func = getattr(zone, func_name)
                record, source = yield func(**ArgsBuilder().build_args("create", row_data)), "CREATE"
        defer.returnValue({"record": record, "source": source})

    def gotRecord(self, record_result, row_data):
        log("record_{}".format(record_result['source']), record_result['record'])
        self.remove_record_from_zone_record_queue(row_data)
        self.terminate_reactor_if_done()

    def terminate_reactor_if_done(self):
        if zone_store.all_rows_processed:
            terminate = True
            for key in zone_store.zone_record_queues:
                if len(zone_store.zone_record_queues[key]) > 0:
                    terminate = False
                    break
            if terminate:
                reactor.callFromThread(reactor.stop)

    def remove_record_from_zone_record_queue(self, row_data):
        zone_name = row_data['Zone']
        zone_store.zone_record_queues[zone_name] = filter(lambda x: x != row_data,
                                                          zone_store.zone_record_queues[zone_name])


class ArgsBuilder():
    def build_args(self, key, row_data, existing_answers=[]):
        if existing_answers:
            log("existing_answers", existing_answers)
        data = {
            "load": {
                "domain": row_data['Zone'],
                "rtype": row_data['Type']
            },
            "update": {
                "rtype": row_data['Type'],
                "data": row_data['Data'],
                "ttl": row_data['TTL'],
                "answers": []
            },
            "create": {
                "domain": row_data['Zone'],
                "answers": row_data['Data'],
                "ttl": row_data['TTL'],
                "name": row_data['Name']
            }
        }
        return self._add_answers_to_args(data, key, existing_answers, row_data)

    def _add_answers_to_args(self, data, key, existing_answers, row_data):
        args = data[key]
        updated_answers = self._build_answers(existing_answers, key, row_data)
        if updated_answers:
            args['answers'] = updated_answers
        log("record_request_{}".format(key), args)
        return args

    def _build_answers(self, answers, key, row_data):
        def get_mx_answer():
            answers_update = []
            for answer in answers:
                answers_update.append(answer['answer'])

            new_answer = [int(row_data['Data'].split(" ")[0]), row_data['Data'].split(" ")[1]]
            if new_answer not in answers_update:
                answers_update.append(new_answer)
            return answers_update

        def get_non_mx_answer():
            answers_update = []
            for answer in answers:
                answers_update.append(answer['answer'][0])

            if row_data['Data'] not in answers_update:
                answers_update.append(row_data['Data'])
            return answers_update

        if key != "load":
            if row_data['Type'] == "MX":
                return get_mx_answer()
            else:
                return get_non_mx_answer()
