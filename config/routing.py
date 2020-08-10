from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from tutor.consumers import NoseyConsumer
from django.urls import path

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter([
        path("notifications/", NoseyConsumer),
    ]))
    )
})
