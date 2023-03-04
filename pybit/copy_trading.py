from ._http_manager import _V3HTTPManager
from ._websocket_stream import _FuturesWebSocketManager
from ._websocket_stream import COPY_TRADING
from . import _helpers


ws_name = COPY_TRADING
PRIVATE_WSS = "wss://{SUBDOMAIN}.{DOMAIN}.com/realtime_private"


class HTTP(_V3HTTPManager):
    def get_instruments(self):
        """
        Get symbol info.

        :returns: Request results as dictionary.
        """

        suffix = "/contract/v3/public/copytrading/symbol/list"
        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix
        )

    def place_order(self, **kwargs):
        """
        https://bybit-exchange.github.io/docs/copy_trading/#t-ct_order
        """
        suffix = "/contract/v3/private/copytrading/order/create"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def get_orders(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/order/list"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def cancel_order(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/order/cancel"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def close_order(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/order/close"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def get_position(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/position/list"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def close_position(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/position/close"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def set_leverage(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/position/set-leverage"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def     get_wallet_balance(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/wallet/balance"

        return self._submit_request(
            method="GET",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )

    def transfer(self, **kwargs):
        suffix = "/contract/v3/private/copytrading/wallet/transfer"

        return self._submit_request(
            method="POST",
            path=self.endpoint + suffix,
            query=kwargs,
            auth=True
        )


class WebSocket:
    def __init__(
            self,
            testnet,
            domain="",
            api_key=None,
            api_secret=None,
            ping_interval=20,
            ping_timeout=10,
            retries=10,
            restart_on_error=True,
            trace_logging=False
    ):
        self.ws_public = None
        self.ws_private = None
        self.active_connections = []
        self.args = _helpers.make_private_args(locals())

    def _ws_private_subscribe(self, topic, callback):
        if not self.ws_private:
            self.ws_private = _FuturesWebSocketManager(
                ws_name, **self.args)
            self.ws_private._connect(PRIVATE_WSS)
            self.active_connections.append(self.ws_private)
        self.ws_private.subscribe(topic, callback)

    # Private topics
    def position_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/copy_trading/#t-websocketposition
        """
        topic = "copyTradePosition"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def execution_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/copy_trading/#t-websocketexecution
        """
        topic = "copyTradeExecution"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def order_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/copy_trading/#t-websocketorder
        """
        topic = "copyTradeOrder"
        self._ws_private_subscribe(topic=topic, callback=callback)

    def wallet_stream(self, callback):
        """
        https://bybit-exchange.github.io/docs/copy_trading/#t-websocketwallet
        """
        topic = "copyTradeWallet"
        self._ws_private_subscribe(topic=topic, callback=callback)
