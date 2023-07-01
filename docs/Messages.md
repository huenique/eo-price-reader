# Messages

## WebSocket Client Messages (Send)

```json
{"action":"setContext","message":{"is_demo":1},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":1}

{"action":"multipleAction","message":{"actions":[{"action":"userGroup","ns":1,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"profile","ns":2,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"assets","message":{"mode":["vanilla"],"subscribeMode":["vanilla"]},"ns":3,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"getCurrency","ns":4,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"getCountries","ns":5,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"environment","ns":6,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"defaultSubscribeCandles","message":{"modes":["vanilla"],"timeframes":[0,5]},"ns":7,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"setTimeZone","message":{"timeZone":480},"ns":8,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"getCandlesTimeframes","ns":9,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"referralOfferInfo","ns":10,"token":"1a79a4d60de6718e8e5b326e338ae533"}]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":2}

{"action":"pong","message":{"data":"1688169369371"},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":3}

{"action":"multipleAction","message":{"actions":[{"action":"openOptions","ns":1,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"tradeHistory","message":{"index_from":0,"count":20,"is_demo":1},"ns":2,"token":"1a79a4d60de6718e8e5b326e338ae533"},{"action":"tradeHistory","message":{"index_from":0,"count":20,"is_demo":0},"ns":3,"token":"1a79a4d60de6718e8e5b326e338ae533"}]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":4}

{"action":"historySteps","token":"1a79a4d60de6718e8e5b326e338ae533","ns":5}

{"action":"expertUnsubscribe","token":"1a79a4d60de6718e8e5b326e338ae533","ns":6}

{"action":"registerNewDeviceToken","message":{"token":"exdJ08q9E2amowx2SrYcUd:APA91bHZOcoRT4nHvDn8lXRKYAwdJr7kXh249YGsmEU4vcp6xaIUNexCQNjwe7RgEICE_COmcpT2ZCGTgt7-7MVFId84IqI_EsPGlkVl7YCm3LnVkHM8_fIuCsfcpQb7zfG3xNEOvbtD","token_type":"web_fcm"},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":7}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688165120,1688170235]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":8}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169385,1688169390]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":9}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169415,1688169420]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":10}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169445,1688169450]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":11}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169475,1688169480]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":12}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169505,1688169510]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":13}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169535,1688169540]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":14}

{"action":"assetHistoryCandles","message":{"assetid":160,"periods":[[1688169565,1688169570]],"timeframes":[5]},"token":"1a79a4d60de6718e8e5b326e338ae533","ns":15}

{"action":"pong","message":{"data":"1688173908619"},"token":"459fea0be4c54eafe0297de5adea96cc","ns":1}
```

## WebSocket Server Messages (Receive)

### Candlestick Data

```json
{'action': 'candles', 'message': {'assetId': 160, 'candles': [{'tf': 0, 'tt': 1688179038.5, 't': 1688179038.5, 'v': [30468.708]}, {'tf': 5, 'tt': 1688179038.5, 't': 1688179035, 'v': [30468.757, 30468.757, 30468.619, 30468.708]}], 'expTimes': [[1688179020, 1688179050, [[30468.708, 76, 76, 1], [30468.0986, 77, 2, 2], [30469.3174, 6, 76, 3]]], [1688179050, 1688179080, [[30468.708, 76, 76, 1], [30468.0986, 76, 5, 2], [30469.3174, 6, 76, 3]]], [1688179080, 1688179110, [[30468.708, 76, 76, 1], [30468.0986, 76, 6, 2], [30469.3174, 6, 76, 3]]], [1688179110, 1688179140, [[30468.708, 76, 76, 1], [30468.0986, 76, 6, 2], [30469.3174, 8, 76, 3]]]]}}

{'action': 'candles', 'message': {'assetId': 160, 'candles': [{'tf': 0, 'tt': 1688179039, 't': 1688179039, 'v': [30468.705]}, {'tf': 5, 'tt': 1688179039, 't': 1688179035, 'v': [30468.757, 30468.757, 30468.619, 30468.705]}], 'expTimes': [[1688179020, 1688179050, [[30468.705, 76, 76, 1], [30468.0956, 77, 2, 2], [30469.3144, 6, 76, 3]]], [1688179050, 1688179080, [[30468.705, 76, 76, 1], [30468.0956, 76, 5, 2], [30469.3144, 6, 76, 3]]], [1688179080, 1688179110, [[30468.705, 76, 76, 1], [30468.0956, 76, 6, 2], [30469.3144, 6, 76, 3]]], [1688179110, 1688179140, [[30468.705, 76, 76, 1], [30468.0956, 76, 6, 2], [30469.3144, 8, 76, 3]]]]}}

{'action': 'candles', 'message': {'assetId': 160, 'candles': [{'tf': 0, 'tt': 1688179039.5, 't': 1688179039.5, 'v': [30468.707]}, {'tf': 5, 'tt': 1688179039.5, 't': 1688179035, 'v': [30468.757, 30468.757, 30468.619, 30468.707]}], 'expTimes': [[1688179020, 1688179050, [[30468.707, 76, 76, 1], [30468.0976, 77, 2, 2], [30469.3164, 6, 76, 3]]], [1688179050, 1688179080, [[30468.707, 76, 76, 1], [30468.0976, 76, 5, 2], [30469.3164, 6, 76, 3]]], [1688179080, 1688179110, [[30468.707, 76, 76, 1], [30468.0976, 76, 6, 2], [30469.3164, 6, 76, 3]]], [1688179110, 1688179140, [[30468.707, 76, 76, 1], [30468.0976, 76, 6, 2], [30469.3164, 8, 76, 3]]]]}}

{'action': 'candles', 'message': {'assetId': 160, 'candles': [{'tf': 0, 'tt': 1688179040, 't': 1688179040, 'v': [30468.709]}, {'tf': 5, 'tt': 1688179040, 't': 1688179040, 'v': [30468.709, 30468.709, 30468.709, 30468.709]}], 'expTimes': [[1688179020, 1688179050, [[30468.709, 76, 76, 1], [30468.0996, 77, 2, 2], [30469.3184, 6, 76, 3]]], [1688179050, 1688179080, [[30468.709, 76, 76, 1], [30468.0996, 76, 5, 2], [30469.3184, 6, 76, 3]]], [1688179080, 1688179110, [[30468.709, 76, 76, 1], [30468.0996, 76, 6, 2], [30469.3184, 6, 76, 3]]], [1688179110, 1688179140, [[30468.709, 76, 76, 1], [30468.0996, 76, 6, 2], [30469.3184, 8, 76, 3]]]]}}

{'action': 'candles', 'message': {'assetId': 160, 'candles': [{'tf': 0, 'tt': 1688179040.5, 't': 1688179040.5, 'v': [30468.708]}, {'tf': 5, 'tt': 1688179040.5, 't': 1688179040, 'v': [30468.709, 30468.709, 30468.708, 30468.708]}], 'expTimes': [[1688179020, 1688179050, [[30468.708, 76, 76, 1], [30468.0986, 77, 0, 2], [30469.3174, 6, 76, 3]]], [1688179050, 1688179080, [[30468.708, 76, 76, 1], [30468.0986, 76, 4, 2], [30469.3174, 6, 76, 3]]], [1688179080, 1688179110, [[30468.708, 76, 76, 1], [30468.0986, 76, 6, 2], [30469.3174, 6, 76, 3]]], [1688179110, 1688179140, [[30468.708, 76, 76, 1], [30468.0986, 76, 6, 2], [30469.3174, 6, 76, 3]]]]}}
```
