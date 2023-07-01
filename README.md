# eo-price-reader

These messages are [WebSocket client messages](./docs/Messages.md#websocket-client-messages-send) sent to eo's server:

1. {"action":"setContext","message":{"is_demo":1},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":1}
   - This message sets the context for the client and indicates that the client is using the demo mode. The token "1a79a4d60de6718e8e5b326e338ae533" is used for authentication.

2. {"action":"multipleAction","message":{"actions":[...]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":2}
   - This message performs multiple actions on the server. The actions include:
     - "userGroup": Retrieves information about the user group.
     - "profile": Retrieves the user's profile information.
     - "assets": Retrieves information about available assets for trading.
     - "getCurrency": Retrieves information about currency.
     - "getCountries": Retrieves information about available countries.
     - "environment": Retrieves information about the trading environment.
     - "defaultSubscribeCandles": Subscribes to default candle data for specific modes and timeframes.
     - "setTimeZone": Sets the time zone for the client.
     - "getCandlesTimeframes": Retrieves information about available candle timeframes.
     - "referralOfferInfo": Retrieves information about referral offers.

3. {"action":"pong","message":{"data":"1688169369371"},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":3}
   - This message is a response from the server indicating a successful ping-pong connection. The "data" field contains a timestamp or identifier related to the ping request.

4. {"action":"multipleAction","message":{"actions":[...]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":4}
   - This message performs multiple actions on the server. The actions include:
     - "openOptions": Opens options for trading.
     - "tradeHistory": Retrieves trade history for both demo and non-demo accounts.

5. {"action":"historySteps","token":"1a79a4d60de6718e8e5b326e338ae533","ns":5}
   - This message requests historical steps or events related to the client's trading history.

6. {"action":"expertUnsubscribe","token":"1a79a4d60de6718e8e5b326e338ae533","ns":6}
   - This message unsubscribes the client from expert-related updates or notifications.

7. {"action":"registerNewDeviceToken","message":{"token":"exdJ08q9E2amowx2SrYcUd:APA91bHZOcoRT4nHvDn8lXRKYAwdJr7kXh249YGsmEU4vcp6xaIUNexCQNjwe7RgEICE_COmcpT2ZCGTgt7-7MVFId84IqI_EsPGlkVl7YCm3LnVkHM8_fIuCsfcpQb7zfG3xNEOvbtD","token_type":"web_fcm"},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":7}
   - This message registers a new device token for receiving push notifications. The "token" field contains the device token, and "token_type" specifies the type of token (in this case, "web_fcm" indicates Firebase Cloud Messaging for web).

8. (8-15) {"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[...]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":8-15}

    - These messages request the historical candle data for a specific asset and timeframe. Each message contains different time period information in the "periods" field and the desired timeframe in the "timeframes" field. The "assetid" field specifies the asset for which the historical candle data is requested.

---

The following messages are example responses from the server:

[Candlestick Data](./docs/Messages.md#candlestick-data)

```json
{"action":"candles","message":{"assetId":160,"candles":[{"tf":0,"tt":1688179038.5,"t":1688179038.5,"v":[30468.708]},{"tf":5,"tt":1688179038.5,"t":1688179035,"v":[30468.757,30468.757,30468.619,30468.708]}],"expTimes":[[1688179020,1688179050,[[30468.708,76,76,1],[30468.0986,77,2,2],[30469.3174,6,76,3]]],[1688179050,1688179080,[[30468.708,76,76,1],[30468.0986,76,5,2],[30469.3174,6,76,3]]],[1688179080,1688179110,[[30468.708,76,76,1],[30468.0986,76,6,2],[30469.3174,6,76,3]]],[1688179110,1688179140,[[30468.708,76,76,1],[30468.0986,76,6,2],[30469.3174,8,76,3]]]]}}
```
