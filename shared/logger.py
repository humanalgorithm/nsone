class Logger(object):
    def log(self, key, data):
        key = key.lower()
        log_config = {
            "record_update":  True,
            "record_create":  True,
            "record_load": True,
            "zone_update": True,
            "zone_create":  True,
            "zone_load": True,
            "record_request_create": True,
            "record_request_update": True,
            "record_request_load": True,
            "zone_request_load": True,
            "zone_request_create": True,
            "existing_answers": True
        }
        log_func = getattr(self, key)
        func_enabled = log_config[key]
        if func_enabled:
            log_func(data)

    def record_update(self, data):
        print "Existing record was updated: ", data

    def record_create(self, data):
        print "New record was created: ", data

    def record_load(self, data):
        print "Existing record was loaded:  ", data

    def zone_update(self, data):
        print "Existing zone was updated: ", data

    def zone_create(self, data):
        print "New zone was created: ", data

    def zone_load(self, data):
        print "Existing zone was loaded: ", data

    def record_request_create(self, data):
        print "Making CREATE record request with data: ", data

    def record_request_load(self, data):
        print "Making LOAD record request with data: ", data

    def record_request_update(self, data):
        print "Making UPDATE record request with data: ", data

    def zone_request_create(self, data):
        print "Making CREATE zone request with data: ", data

    def zone_request_load(self, data):
        print "Making LOAD zone request with data: ", data

    def existing_answers(self, data):
        print "Existing answers for record is: ", data

log = Logger().log

