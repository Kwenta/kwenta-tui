import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import concurrent.futures
import json
from abi_store import * 
import kwenta_strats as strats
import aiohttp
import asyncio
import logging
logging.basicConfig(level=logging.ERROR)
from kwenta_tui_dashboard import web3, provider_rpc, account, enable_strats

strat_filtered_keys = ['in_uptrend1', 'in_uptrend2', 'in_uptrend3', 'Pivot', 'S3', 'S2', 'S1', 'R1', 'R2', 'R3']
executor = ThreadPoolExecutor(max_workers=100)

def load_json(file):
    with open(file) as json_file:
        return json.load(json_file)

def process_market_inits(market, PerpsV2Proxy_abi, PerpsV2MarketViews_abi, PerpsV2ExchangeRates_abi,pyth_price_abi):
    proxy_contract = web3.eth.contract(web3.to_checksum_address(market[0]), abi=PerpsV2Proxy_abi)
    marketViews_addr = (proxy_contract.functions.getAllTargets().call())[4]
    marketViews_contract = web3.eth.contract(web3.to_checksum_address(marketViews_addr), abi=PerpsV2MarketViews_abi)
    marketState_addr = (marketViews_contract.functions.marketState().call())
    exchangeRates_addr = '0x2C15259D4886e2C0946f9aB7a5E389c86b3c3b04'
    exchangeRates_contract =  web3.eth.contract(web3.to_checksum_address(exchangeRates_addr), abi=PerpsV2ExchangeRates_abi)
    pyth_feed_id = exchangeRates_contract.functions.offchainPriceFeedId(market[1]).call()
    pyth_bytes32 = '0x'+(pyth_feed_id.hex().rstrip("0"))
    try:
        pyth_pricing = asyncio.run(get_pyth_price_single(pyth_bytes32))
        pyth_price = pyth_pricing['price']
        if pyth_price['price'] != 0:
            pyth_price = int(pyth_price['price']) * 10**(pyth_price['expo'])
        else:
            pyth_price = 0
    except:
        pyth_price = 0
    normalized_market = {
            "market_address": market[0],
            "asset": market[1].decode('utf-8').strip("\x00"),
            "asset_key":market[1],
            "key": market[2],
            "market_key_hex":'0x'+(market[2].hex()),
            "maxLeverage": market[3],
            "price": market[4],
            "marketSize": market[5],
            "marketSkew": market[6],
            "marketDebt": market[7],
            "currentFundingRate": market[8],
            "currentFundingVelocity": market[9],
            "takerFee": market[10][0],
            "makerFee": market[10][1],
            "takerFeeDelayedOrder": market[10][2],
            "makerFeeDelayedOrder": market[10][3],
            "takerFeeOffchainDelayedOrder": market[10][4],
            "makerFeeOffchainDelayedOrder": market[10][5],
            "overrideCommitFee": market[10][6],
            "marketState_addr":marketState_addr,
            "pyth_feed_id":pyth_bytes32,
            "pyth_price":pyth_price
    }
    if normalized_market['asset'] == "sETH":
        normalized_market['asset'] = "ETH"
    elif normalized_market['asset'] == "sBTC":
        normalized_market['asset'] = "BTC"
    return normalized_market['asset'], normalized_market

def init_markets():
    global allmarket_listings, PerpsV2MarketData_abi, PerpsV2Market_abi, PerpsV2MarketViews_abi, PerpsV2Proxy_abi, PerpsV2MarketState_abi, PerpsV2ExchangeRates_abi, pyth_price_abi
    with concurrent.futures.ThreadPoolExecutor() as executor:
        files = ['PerpsV2MarketData.json', 'PerpsV2Market.json', 'PerpsV2MarketViews.json', 'PerpsV2Proxy.json', 'PerpsV2MarketState.json', 'PerpsV2ExchangeRate.json','Pyth_Proxabi.json']
        PerpsV2MarketData_abi, PerpsV2Market_abi, PerpsV2MarketViews_abi, PerpsV2Proxy_abi, PerpsV2MarketState_abi, PerpsV2ExchangeRates_abi, pyth_price_abi = executor.map(load_json, files)
    marketdata_contract = web3.eth.contract(web3.to_checksum_address(contracts['PerpsV2MarketData'][10]), abi=PerpsV2MarketData_abi)
    allmarketsdata = (marketdata_contract.functions.allProxiedMarketSummaries().call())
    allmarket_listings = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_market = {executor.submit(process_market_inits, market, PerpsV2Proxy_abi, PerpsV2MarketViews_abi, PerpsV2ExchangeRates_abi,pyth_price_abi): market for market in allmarketsdata}
        for future in concurrent.futures.as_completed(future_to_market):
            market_key, market_value = future.result()
            allmarket_listings[market_key] = market_value
    return allmarket_listings

async def get_pyth_price_single(asset_id: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://xc-mainnet.pyth.network/api/latest_price_feeds"
        params = {'ids[]': asset_id}
        try:
            async with session.get(url, params=params) as response:
                price_data = await response.json()
                return price_data[0]
        except Exception:
            return 0

async def get_pyth_price(pyth_feed_list):
    async with aiohttp.ClientSession() as session:
        url = f"https://xc-mainnet.pyth.network/api/latest_price_feeds"
        params = {'ids[]': pyth_feed_list}
        try:
            async with session.get(url, params=params) as response:
                price_data = await response.json()
                return price_data
        except Exception as e:
            logging.info(e)
            return 0


def get_pyth_price(pyth_feed_list):
    url = "https://xc-mainnet.pyth.network/api/latest_price_feeds"
    params = {'ids[]': pyth_feed_list}
    try:
        response = requests.get(url, params=params)
        price_data = response.json()
        return price_data
    except Exception as e:
        logging.info(e)
        return 0

def get_chainlink_price():
    marketdata_contract = web3.eth.contract(web3.to_checksum_address(contracts['PerpsV2MarketData'][10]), abi=PerpsV2MarketData_abi)
    chainlink_data = (marketdata_contract.functions.allProxiedMarketSummaries().call())
    chainlink_markets = []
    for market in chainlink_data:
        normalized_market = {
                    "market_address": market[0],
                    "asset": market[1].decode('utf-8').strip("\x00"),
                    "maxLeverage": market[3],
                    "wei_price": market[4],
                    "usd_price":  market[4]/(10**18),
                    "marketSize": market[5],
                    
            }
        if normalized_market['asset'] == "sETH":
            normalized_market['asset'] = "ETH"
        elif normalized_market['asset'] == "sBTC":
            normalized_market['asset'] = "BTC"
        chainlink_markets.append(normalized_market)
    return pd.DataFrame(chainlink_markets)

async def pyth_process_pricing_market(market,pyth_data,chainlink_data):
    try:
        if 'id' not in pyth_data.columns:
            raise ValueError(f"Column 'id' not found in pyth_data | {market['asset']}")
        market_lookup = pyth_data[pyth_data['id'].str.contains(market['pyth_feed_id'][2:])]
        if not market_lookup.empty:
            market_pyth_price = (pyth_data[pyth_data['id'].str.contains(market['pyth_feed_id'][2:])]['price'].reset_index(drop=True).iloc[0])
            market_pyth_ema = (pyth_data[pyth_data['id'].str.contains(market['pyth_feed_id'][2:])]['ema_price'].reset_index(drop=True).iloc[0])
            pyth_price = int(market_pyth_price['price']) * 10**(market_pyth_price['expo'])
            pyth_ema = float(market_pyth_ema['price']) * 10**(market_pyth_ema['expo'])
            pyth_ema_trend = ((pyth_price / pyth_ema)-1) * 100
            pyth_oracle = True
            chainlink_price = (chainlink_data[chainlink_data['asset'].str.contains(market['asset'])]['usd_price'].reset_index(drop=True).iloc[0])
            # print(f"Market:{market['asset']} | Chainlink Price: {chainlink_price} | Pyth Price: {pyth_price}")
            price_drift_percent = ((float(pyth_price) / float(chainlink_price)) - 1) * 100
            if price_drift_percent > 0.60:
                big_drift = True
            else:
                big_drift = False
            if abs(pyth_ema_trend) > 1:
                big_ema_drift = True
                if pyth_ema_trend > 0:
                    ema_drift_direction = "Long"
                else:
                    ema_drift_direction = "Short"
            else:
                big_ema_drift = False
                ema_drift_direction = "N/A"
        else:
            chainlink_price = (chainlink_data[chainlink_data['asset'].str.contains(market['asset'])]['usd_price'].reset_index(drop=True).iloc[0])
            pyth_price = chainlink_price
            pyth_oracle = False
            pyth_ema_trend = 0
            big_ema_drift = False
            ema_drift_direction = "N/A"
            big_drift = False
            price_drift_percent = 0
    except Exception as e:
        print(e)
        chainlink_price = (chainlink_data[chainlink_data['asset'].str.contains(market['asset'])]['usd_price'].reset_index(drop=True).iloc[0])
        pyth_price = chainlink_price
        pyth_oracle = False
        pyth_ema_trend = 0
        big_ema_drift = False
        ema_drift_direction = "N/A"
        big_drift = False
        price_drift_percent = 0
    market_data = {
            "asset": market['asset'],
            "chainlink_price": chainlink_price,
            "pyth_price": pyth_price,
            "price_drift_percent": price_drift_percent,
            "big_drift": big_drift,
            "pyth_oracle": pyth_oracle,
            "pyth_ema_trend": pyth_ema_trend,
            "big_ema_drift": big_ema_drift,
            "ema_drift_direction": ema_drift_direction,
        }
    #Enable Strategies to be added to table. THIS WILL SLOW DOWN PRICE PULLS.
    if enable_strats:
        try:
            strat_output = await(strats.run_strat(market['asset']))
            strat_output_filtered = {k: strat_output[k] for k in strat_filtered_keys if k in strat_output}
            if strat_output_filtered:
                market_data = {**market_data, **strat_output_filtered}
                return market_data
            else:
                return market_data
        except Exception as e:
            logging.info(f'Error occurred: {e}')
    
    return market_data

async def pyth_process_market_pricing():
    try:
        pyth_feed_list = []
        for market in allmarket_listings:
            if allmarket_listings[market]['pyth_price'] != 0:
                pyth_feed_list.append(allmarket_listings[market]['pyth_feed_id'])
        chainlink_price_data = get_chainlink_price()
        pyth_pricing = get_pyth_price(pyth_feed_list)
        pyth_price_data = pd.DataFrame(pyth_pricing)
        market_data = await asyncio.gather(
            *(pyth_process_pricing_market(market,pyth_price_data,chainlink_price_data) for market in allmarket_listings.values())
        )
        return market_data
    except Exception as e:
        logging.info(f'Error occurred: {e}')
        
        