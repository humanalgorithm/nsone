#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

###########
# TWISTED #
###########

import nsone
from nsone import NSONE, Config

from twisted.internet import defer, reactor

config = Config()
config['transport'] = 'twisted'
config.createFromAPIKey('YmZB3gnt2MxolyCCKMOR')

nsone = nsone.NSONE(config=config)

@defer.inlineCallbacks
def getZone():
    # when twisted transport is in use, all of the NSONE methods return
    # Deferred. yield them to gather the results, or add callbacks/errbacks
    # to be run when results are available
    zone = yield nsone.loadZone('example3.test')
    defer.returnValue(zone)


def gotZone(result):
    print "result from got zone is ", result
    reactor.callFromThread(reactor.stop)

def handleError(failure):
    print(failure)
    reactor.callFromThread(reactor.stop)

zone = getZone()
zone.addCallback(gotZone)
zone.addErrback(handleError)

reactor.run()
