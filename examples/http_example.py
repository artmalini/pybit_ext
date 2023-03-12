"""
To see which endpoints are available, you can read the API docs at
https://bybit-exchange.github.io/docs/inverse/#t-introduction

Some methods will have required parameters, while others may be optional.
The arguments in pybit methods match those provided in the Bybit API
documentation.

The following functions are available:

Public Methods: 
------------------------

API Data endpoints:

get_server_time()

Market Data Endpoints:

get_instruments()
get_order_book()
get_merged_order_book()
get_public_trading_history()
get_klines()
get_tickers()
get_last_traded_price()
get_best_bid_ask_price()

Leveraged Token Endpoints:

get_leveraged_token_asset_info()

Institutional Loan Endpoints:

get_institutional_loan_products()
get_institutional_loan_margin_coins()


Account Asset:
(requires authentication)
------------------------

Transfer Data Endpoints: 

create_internal_transfer()
create_subaccount_transfer()
get_internal_transfer_list()
get_subaccount_transfer_list()
get_subaccount_list()
enable_universal_transfer()
create_universal_transfer()
get_universal_transfer_list()
get_transferable_coin_list()
get_account_coin_balance()
get_asset_info()

Withdraw and Deposit Endpoints:

get_supported_deposit_list()
get_deposit_records()
get_sub_deposit_records_by_master_key()
get_withdraw_records()
get_coin_info()
withdraw()
cancel_withdrawal()
get_master_deposit_addresses()
get_sub_deposit_addresses()

Master-Sub User Endpoints:

create_sub_uid()
create_sub_uid_api_key()
get_sub_uid_list()
freeze_sub_uid()
get_api_key_info()
modify_master_api_key()
modify_sub_api_key()
delete_master_api_key()
delete_sub_api_key()


Spot:
(requires authentication)
------------------------

Wallet Data Endpoints:

get_wallet_balance()


Leveraged Token Endpoints:

get_leveraged_token_market_info()
purchase_leveraged_token()
redeem_leveraged_token()
get_leveraged_token_purchase_redemption_history()


Cross Margin Trading Endpoints:

borrow_cross_margin_loan()
repay_cross_margin_loan()
get_cross_margin_borrowing_info()
get_cross_margin_account_info()
get_cross_margin_interest_quota()
get_cross_margin_repayment_history()


Institutional Loan Endpoints:

get_institutional_loans()
get_institutional_loan_repayment_history()
get_institutional_loan_ltv()


Unified Margin Account: 
(requires authentication)
------------------------

Order actions:

place_order()
replace_order()
cancel_order()
get_open_orders()
get_orders()
batch_place_order()
batch_replace_order()
batch_cancel_order()
cancel_all_orders()

Position actions:

get_position()
set_leverage()
switch_tp_sl_mode()
set_risk_limit()
set_trading_stop()
get_trade_history()
get_usdc_options_settlement_history()
get_usdc_perpetuals_settlement_history()


Account actions: 

get_wallet_balance()
upgrade_to_unified_margin_account()
get_transaction_log()
get_exchange_coins_history()
get_borrowing_history()
get_borrowing_rate()
set_margin_mode()
get_account_info()
"""


# Import pybit and define the HTTP object, alias them with specifc usage
from pybit.spot import HTTP as spot_session
from pybit.unified_margin import HTTP as unified_margin_session
from pybit.account_asset import HTTP as account_asset


# For ease of use, create abstraction layer to use `auth_required` functions. 
# To use actual API, use `is_testnet` = False
class SpotManager:
    def __init__(self, api_key: str, api_secret: str, is_testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        if is_testnet:
            self.endpoint = 'https://api-testnet.bybit.com'
        self.session = spot_session(
            endpoint=self.endpoint,
            api_key=api_key,
            api_secret=api_secret
        )

spot_manager = SpotManager(api_key='...', api_secret='...', is_testnet=False)
spot_manager.session.get_wallet_balance()

# To access public endpoints
# If endpoint parameter is not specified, by default it uses "https://api.bybit.com"
session_unauth = spot_session()

# Let's get last traded price for BTC, note symbol "BTCUSDT"
session_unauth.get_last_traded_price(symbol="BTCUSDT")


# Similar like we created SpotManager, we can create UnifiedMargin object with correct seesion 
class UnifiedMarginManager:
    def __init__(self, api_key: str, api_secret: str, is_testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        if is_testnet:
            self.endpoint = 'https://api-testnet.bybit.com'
        self.session = unified_margin_session(
            endpoint=self.endpoint,
            api_key=api_key,
            api_secret=api_secret
        )


unified_manager = UnifiedMarginManager(api_key='...', api_secret='...', is_testnet=False)
unified_manager.session.get_account_info()

# In case you receive error displayed below, account upgrade needs to be made: https://www.bybit.com/en-US/promo/events/unified-trading-account/
# pybit.exceptions.InvalidRequestError: The API can only be accessed by unified account users. (ErrCode: 10020) (ErrTime: 18:10:53).
# Otherwise response should be successfull

# To get balace (within unified margin) for specific coin. Note coin and coin name - "USDT"
unified_manager.session.get_wallet_balance(coin="USDT")


# To use API directly without extra class follow example below:

account_asset(
    api_key='...',
    api_secret='...',
    endpoint='mainnte or testnet endpoint'
).create_internal_transfer(
    transferId="UUID",
    coin="COIN",
    amount="10.0",
    fromAccountType="AccountTypeFrom",
    toAccountType="AccountTypeTo"
)
