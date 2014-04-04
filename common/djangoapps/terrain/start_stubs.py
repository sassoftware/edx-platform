"""
Initialize and teardown fake HTTP services for use in acceptance tests.
"""
import requests
from lettuce import before, after, world
from django.conf import settings
from terrain.stubs.youtube import StubYouTubeService
from terrain.stubs.xqueue import StubXQueueService
from terrain.stubs.lti import StubLtiService

SERVICES = {
    "youtube": {"port": settings.YOUTUBE_PORT, "class": StubYouTubeService},
    "xqueue": {"port": settings.XQUEUE_PORT, "class": StubXQueueService},
    "lti": {"port": settings.LTI_PORT, "class": StubLtiService},
}

YOUTUBE_API_RESPONSE = requests.get('http://www.youtube.com/iframe_api')


@before.each_scenario
def start_stubs(_):
    """
    Start each stub service running on a local port.
    """
    for name, service in SERVICES.iteritems():
        fake_server = service['class'](port_num=service['port'])
        if name == 'youtube':
            fake_server.config['youtube_api_response'] = YOUTUBE_API_RESPONSE
        setattr(world, name, fake_server)


@after.each_scenario
def stop_stubs(_):
    """
    Shut down each stub service.
    """
    for name in SERVICES.keys():
        stub_server = getattr(world, name, None)
        if stub_server is not None:
            stub_server.shutdown()
