from channels import route
from apps.bids.consumer import ws_connect

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/ws/(?P<pk>\d+)/$"),
]