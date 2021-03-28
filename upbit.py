from websocket import WebSocketApp
import json, ssl, asyncio
from datetime import datetime
from model import add_data, fit, forecast

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
  msg = json.loads(message.decode('utf-8'))
  KRW_RATE = 1129
  price = msg["trade_price"] / KRW_RATE
  ts = datetime.fromtimestamp(int(msg["trade_timestamp"]) / 1000)
  
  add_data({
    "ts": ts,
    "price": price,
    "index": int(msg["trade_timestamp"])
  })
  fit()
  forecast_price = forecast()
  
  print('[%s] 실제가격: %10.2f, 예측가격: %10.2f, 예측가격 대비 실제가격: %10.2f'%(ts, price, forecast_price, (forecast_price-price) * KRW_RATE))
 

def on_error(ws, error):
  print(error)

def on_close(ws):
  print("close")

def on_open(ws):
  def run(*args):
    # https://docs.upbit.com/docs/upbit-quotation-websocket 문서참고
    # ticker:  현재가, trade: 채결내역, orderbook: 호가
    originData = [
        { "ticket": "UNIQUE_TICKET" },
        # { "type": "orderbook", "codes": ["KRW-MTL"], "isOnlyRealtime": True }, 
        { "type": "ticker", "codes": ["KRW-BTC"] }, 
        # { "type": "trade", "codes": ["KRW-MTL"] }
    ]

    ws.send(json.dumps(originData))

  thread.start_new_thread(run, ())


if __name__ == "__main__":
    fit()

    ws = WebSocketApp(
      "wss://api.upbit.com/websocket/v1",
      on_message = on_message,
      on_error = on_error,
      on_close = on_close,
    )
    
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})