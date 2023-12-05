from concurrent.futures import ThreadPoolExecutor
from abi_store import * 
import logging
from kwenta_tui_dashboard import web3, provider_rpc, account 
logging.basicConfig(level=logging.ERROR)
executor = ThreadPoolExecutor(max_workers=100)

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr

#Calculate Average True Range
def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()
    return atr

#calculate SuperTrend
def supertrend(df, period=18, atr_multiplier=2):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True
    for current in range(1, len(df.index)):
        previous = current - 1
        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]
            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
    return df 

#calculate Triple SuperTrend
def triplesupertrend(df, period1=16, period2 =17, period3 = 18, atr_multiplier1=1, atr_multiplier2=2, atr_multiplier3 = 3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr1'] = atr(df, period1)
    df['atr2'] = atr(df, period2)
    df['atr3'] = atr(df, period3)
    df['upperband1'] = hl2 + (atr_multiplier1 * df['atr1'])
    df['lowerband1'] = hl2 - (atr_multiplier1 * df['atr1'])
    df['in_uptrend1'] = True
    df['upperband2'] = hl2 + (atr_multiplier2 * df['atr2'])
    df['lowerband2'] = hl2 - (atr_multiplier2 * df['atr2'])
    df['in_uptrend2'] = True
    df['upperband3'] = hl2 + (atr_multiplier3 * df['atr3'])
    df['lowerband3'] = hl2 - (atr_multiplier3 * df['atr3'])
    df['in_uptrend3'] = True
    for current in range(1, len(df.index)):
        previous = current - 1
#trend1
        if df['close'][current] > df['upperband1'][previous]:
            df['in_uptrend1'][current] = True
        elif df['close'][current] < df['lowerband1'][previous]:
            df['in_uptrend1'][current] = False
        else:
            df['in_uptrend1'][current] = df['in_uptrend1'][previous]
            if df['in_uptrend1'][current] and df['lowerband1'][current] < df['lowerband1'][previous]:
                df['lowerband1'][current] = df['lowerband1'][previous]
            if not df['in_uptrend1'][current] and df['upperband1'][current] > df['upperband1'][previous]:
                df['upperband1'][current] = df['upperband1'][previous]
#trend2
        if df['close'][current] > df['upperband2'][previous]:
            df['in_uptrend2'][current] = True
        elif df['close'][current] < df['lowerband2'][previous]:
            df['in_uptrend2'][current] = False
        else:
            df['in_uptrend2'][current] = df['in_uptrend2'][previous]
            if df['in_uptrend2'][current] and df['lowerband2'][current] < df['lowerband2'][previous]:
                df['lowerband2'][current] = df['lowerband2'][previous]
            if not df['in_uptrend2'][current] and df['upperband2'][current] > df['upperband2'][previous]:
                df['upperband2'][current] = df['upperband2'][previous]
#Trend3 
        if df['close'][current] > df['upperband3'][previous]:
            df['in_uptrend3'][current] = True
        elif df['close'][current] < df['lowerband3'][previous]:
            df['in_uptrend3'][current] = False
        else:
            df['in_uptrend3'][current] = df['in_uptrend3'][previous]
            if df['in_uptrend3'][current] and df['lowerband3'][current] < df['lowerband3'][previous]:
                df['lowerband3'][current] = df['lowerband3'][previous]
            if not df['in_uptrend3'][current] and df['upperband3'][current] > df['upperband3'][previous]:
                df['upperband3'][current] = df['upperband3'][previous]
    return df 

#calculate Pivot Points
#will need at least 1 day's worth of closing pricing
def PivotPoint(high,low,close):
    Pivot = (high + low + close)/3
    R1 = 2*Pivot - low
    S1= 2*Pivot - high
    R2 = Pivot + (high - low)
    S2 = Pivot - (high - low)
    R3 = Pivot + 2*(high - low)
    S3 = Pivot - 2*(high - low)
    return Pivot,S3,S2,S1,R1,R2,R3

# Advanced Pivot grid. Not implemented, but available to use. 
def pivotGrid(last_second_price,df):
    last_row_index = len(df.index) - 1
    pivotmid = (df['Pivot'][last_row_index]+df['R1'][last_row_index])/2
    pivotlowmid = (df['Pivot'][last_row_index]+pivotmid)/2
    pivothighmid = (df['R1'][last_row_index]+pivotmid)/2
    if(last_second_price > df['Pivot'][last_row_index] and last_second_price < pivotlowmid):
        pivot_price = df["Pivot"][last_row_index]
    elif(last_second_price > pivotlowmid and last_second_price < pivotmid):
        pivot_price = pivotlowmid
    elif(last_second_price > pivotmid and last_second_price < pivothighmid):
        pivot_price = pivotmid
    elif(last_second_price > pivothighmid and last_second_price < df['R1'][last_row_index]):
        pivot_price = pivothighmid
    else:
        pivotmid = (df['R1'][last_row_index]+df['R2'][last_row_index])/2
        pivotlowmid = (df['R1'][last_row_index]+pivotmid)/2
        pivothighmid = (df['R2'][last_row_index]+pivotmid)/2
        if(last_second_price > df['R1'][last_row_index] and last_second_price < pivotlowmid):
                pivot_price = df["R1"][last_row_index]
        elif(last_second_price > pivotlowmid and last_second_price < pivotmid):
            pivot_price = pivotlowmid
        elif(last_second_price > pivotmid and last_second_price < pivothighmid):
            pivot_price = pivotmid
        elif(last_second_price > pivothighmid and last_second_price < df['R2'][last_row_index]):
            pivot_price = pivothighmid
        else:
            pivotmid = (df['R2'][last_row_index]+df['R3'][last_row_index])/2
            pivotlowmid = (df['R2'][last_row_index]+pivotmid)/2
            pivothighmid = (df['R3'][last_row_index]+pivotmid)/2
            if(last_second_price > df['R2'][last_row_index] and last_second_price < pivotlowmid):
                    pivot_price = df["R2"][last_row_index]
            elif(last_second_price > pivotlowmid and last_second_price < pivotmid):
                pivot_price = pivotlowmid
            elif(last_second_price > pivotmid and last_second_price < pivothighmid):
                pivot_price = pivotmid
            elif(last_second_price > pivothighmid and last_second_price < df['R3'][last_row_index]):
                pivot_price = pivothighmid
            elif(last_second_price > df['R3'][last_row_index]):
                pivot_price = df['R3'][last_row_index]
            else:
                pivotmid = (df['Pivot'][last_row_index]+df['S1'][last_row_index])/2
                pivotlowmid = (df['S1'][last_row_index]+pivotmid)/2
                pivothighmid = (df['Pivot'][last_row_index]+pivotmid)/2
                if(last_second_price < df['Pivot'][last_row_index] and  last_second_price > pivothighmid):
                    pivot_price = df["Pivot"][last_row_index]
                elif(last_second_price < pivothighmid and last_second_price > pivotmid):
                    pivot_price = pivothighmid
                elif(last_second_price < pivotmid and last_second_price > pivotlowmid):
                    pivot_price = pivotmid
                elif(last_second_price < pivotlowmid and last_second_price > df['S2'][last_row_index]):
                    pivot_price = pivotlowmid
                else:
                    pivotmid = (df['S1'][last_row_index]+df['S2'][last_row_index])/2
                    pivotlowmid = (df['S2'][last_row_index]+pivotmid)/2
                    pivothighmid = (df['S1'][last_row_index]+pivotmid)/2
                    if(last_second_price < df['S1'][last_row_index] and  last_second_price > pivothighmid):
                        pivot_price = df["S1"][last_row_index]
                    elif(last_second_price < pivothighmid and last_second_price > pivotmid):
                        pivot_price = pivothighmid
                    elif(last_second_price < pivotmid and last_second_price > pivotlowmid):
                        pivot_price = pivotmid
                    elif(last_second_price < pivotlowmid and last_second_price > df['S3'][last_row_index]):
                        pivot_price = pivotlowmid
                    else:
                        pivotmid = (df['S2'][last_row_index]+df['S3'][last_row_index])/2
                        pivotlowmid = (df['S3'][last_row_index]+pivotmid)/2
                        pivothighmid = (df['S2'][last_row_index]+pivotmid)/2
                        if(last_second_price < df['S2'][last_row_index] and  last_second_price > pivothighmid):
                            pivot_price = df["S2"][last_row_index]
                        elif(last_second_price < pivothighmid and last_second_price > pivotmid):
                            pivot_price = pivothighmid
                        elif(last_second_price < pivotmid and last_second_price > pivotlowmid):
                            pivot_price = pivotmid
                        elif(last_second_price < pivotlowmid and last_second_price > df['S3'][last_row_index]):
                            pivot_price = pivotlowmid
                        elif(last_second_price < df['S3'][last_row_index]):
                            pivot_price = df['S3'][last_row_index]
    return pivot_price

async def get_candle_data(token_symbol,time_back=10, period=900):
    global candles_df 
    #5min timeframe, 72 hours back
    candles_df = await account.queries.candles(token_symbol,time_back=time_back, period=period)
    candles_df['open'] = candles_df['open'].astype(float)
    candles_df['close'] = candles_df['close'].astype(float)
    candles_df['high'] = candles_df['high'].astype(float)
    candles_df['low'] = candles_df['low'].astype(float)
    return candles_df

async def run_strat(token_symbol):
    global strat_data
    # loop = asyncio.get_event_loop()
    # candles_task = loop.create_task(get_candle_data(token_symbol))
    # candles_df = await asyncio.gather(candles_task)
    candles_df = await get_candle_data(token_symbol)
    triple_trend_period1 = 19
    triple_trend_period2 = 20
    triple_trend_period3 = 22
    atr_multiplier1 =1.5
    atr_multiplier2 =2
    atr_multiplier3 =2.5
    try:
        strat_data = triplesupertrend(candles_df, period1=triple_trend_period1 ,period2=triple_trend_period2,period3=triple_trend_period3, atr_multiplier1=atr_multiplier1, atr_multiplier2=atr_multiplier2, atr_multiplier3 = atr_multiplier3)
    except Exception as e:
        print(e)
        print("Failed to calculate triplesupertrend.")
        return
    #calculate the last period Pivot Points -- Works Better if you calculate this with a day timeframe. (generate a second set of candles) 
    try:    
        strat_data['Pivot'],strat_data['S3'],strat_data['S2'],strat_data['S1'],strat_data['R1'],strat_data['R2'],strat_data['R3'] = PivotPoint(candles_df.tail(1)["high"],candles_df.tail(1)["low"],candles_df.tail(1)["close"])
    except Exception as e:
        print(e)
        print("Error Calculating Pivot Points, Wait for More Data to Populate...")
        return
    latest_candle = strat_data.to_dict("records")
    return latest_candle[-1]