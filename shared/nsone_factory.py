from nsone import NSONE, Config

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

nsone_async = NSONEFactory().get_nsone()
