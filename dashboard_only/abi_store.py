import json

# Contracts from https://github.com/Synthetixio/synthetix-docs/blob/master/content/addresses.md?ref=synthetix-blog#mainnet-optimism-l2
#SUSD contract 
susd_contract = {
    "susd_addr": '0x8c6f28f2f1a3c87f0f938b96d27520d9751ec8d9',
    "susd_abi": '[{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":false,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerNominated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract Proxyable","name":"newTarget","type":"address"}],"name":"TargetUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"constant":false,"inputs":[{"internalType":"bytes","name":"callData","type":"bytes"},{"internalType":"uint256","name":"numTopics","type":"uint256"},{"internalType":"bytes32","name":"topic1","type":"bytes32"},{"internalType":"bytes32","name":"topic2","type":"bytes32"},{"internalType":"bytes32","name":"topic3","type":"bytes32"},{"internalType":"bytes32","name":"topic4","type":"bytes32"}],"name":"_emit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"acceptOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"nominateNewOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"nominatedOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"contract Proxyable","name":"_target","type":"address"}],"name":"setTarget","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"target","outputs":[{"internalType":"contract Proxyable","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
}

#contract addresses
contracts = {
	"Exchanger": {
		1: '0xD64D83829D92B5bdA881f6f61A4e4E27Fc185387',
		5: '0x889d8a97f43809Ef3FBb002B4b7a6A65319B61eD',
		10: '0xC37c47C55d894443493c1e2E615f4F9f4b8fDEa4',
		420: '0x601A1Cf1a34d9cF0020dCCD361c155Fe54CE24fB',
	},
	"SystemStatus": {
		1: '0x696c905F8F8c006cA46e9808fE7e00049507798F',
		5: '0x31541f35F6Bd061f4A894fB7eEE565f81EE50df3',
		10: '0xE8c41bE1A167314ABAF2423b72Bf8da826943FFD',
		420: '0x9D89fF8C6f3CC22F4BbB859D0F85FB3a4e1FA916',
	},
	"ExchangeRates": {
		1: '0xb4dc5ced63C2918c89E491D19BF1C0e92845de7C',
		5: '0xea765947303051507033202CAB7D3f5d4961CF5d',
		10: '0x0cA3985f973f044978d2381AFEd9c4D85a762d11',
		420: '0x061B75475035c20ef2e35E1002Beb90C3c1f24cC',
	},
	"SynthUtil": {
		1: '0x81Aee4EA48f678E172640fB5813cf7A96AFaF6C3',
		5: '0x492395BA6866EF703DA49667fF92Cb8551e7a2D1',
		10: '0x87b1481c82913301Fc6c884Ac266a7c430F92cFA',
		420: '0xC647DecC9c4f9162dBF77E4367199F5ED0950355',
	},
	"SystemSettings": {
		1: '0x5ad055A1F8C936FB0deb7024f1539Bb3eAA8dc3E',
		5: '0xA1B0898C54124E06aEAa823dC46ad0C306Ca6CD5',
		10: '0x05E1b1Dff853B1D67828Aa5E8CB37cC25aA050eE',
		420: '0xD2cECA6DD62243aB2d342Eb04882c86a10b35274',
	},
	"SynthRedeemer": {
		1: '0xe533139Af961c9747356D947838c98451015e234',
		5: '0x32A0BAA5Acec418a85Fd032f0292893B8E4f743B',
		10: '0xA997BD647AEe62Ef03b41e6fBFAdaB43d8E57535',
		420: '0x2A8338199D802620B4516a557195a498595d7Eb6',
	},
	"FuturesMarketData": {
		10: '0xC51aeDBEC3aCD26650a7E85B6909E8AEc4d0F19e',
		420: '0x3FAe35Cfea950Fada314589213BABC54A084d5Bf',
	},
	"FuturesMarketSettings": {
		10: '0xaE55F163337A2A46733AA66dA9F35299f9A46e9e',
		420: '0x0dde87714C3bdACB93bB1d38605aFff209a85998',
	},
	"FuturesMarketManager": {
		10: '0xdb89f3fc45A707Dd49781495f77f8ae69bF5cA6e'
	},
	"PerpsV2MarketData": {
		10: '0xF7D3D05cCeEEcC9d77864Da3DdE67Ce9a0215A9D',
		420: '0x0D9eFa310a4771c444233B10bfB57e5b991ad529',
	},
	"PerpsV2MarketSettings": {
		10: '0xd442Dc2Ac1f3cA1C86C8329246e47Ca0C91D0471',
		420: '0x14fA3376E2ffa41708A0636009A35CAE8D8E2bc7',
	},
	"Pyth": {
		10: '0xff1a0f4744e8582DF1aE09D5611b887B6a12925C',
		420: '0xff1a0f4744e8582DF1aE09D5611b887B6a12925C',
	},
	"SUSD": {
		1: '0x57Ab1ec28D129707052df4dF418D58a2D46d5f51',
		10: '0x8c6f28f2F1A3C87F0f938b96d27520d9751ec8d9',
		420: '0xebaeaad9236615542844adc5c149f86c36ad1136',
	},
	"Synthetix": {
		1: '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
		5: '0x51f44ca59b867E005e48FA573Cb8df83FC7f7597',
		10: '0x8700dAec35aF8Ff88c16BdF0418774CB3D7599B4',
		420: '0x2E5ED97596a8368EB9E44B1f3F25B2E813845303',
	},
	"SynthSwap": {
		10: '0x6d6273f52b0C8eaB388141393c1e8cfDB3311De6',
	},
	"KwentaArrakisVault": {
		10: '0x56dEa47c40877c2aaC2a689aC56aa56cAE4938d2',
	},
	"StakingRewards": {
		10: '0x6077987e8e06c062094c33177Eb12c4A65f90B65',
	},
	"KwentaToken": {
		10: '0x920Cf626a271321C151D027030D5d08aF699456b',
		420: '0xDA0C33402Fc1e10d18c532F0Ed9c1A6c5C9e386C',
	},
	"KwentaStakingRewards": {
		10: '0x6e56A5D49F775BA08041e28030bc7826b13489e0',
		420: '0x1653a3a3c4ccee0538685f1600a30df5e3ee830a',
	},
	"RewardEscrow": {
		10: '0x1066A8eB3d90Af0Ad3F89839b974658577e75BE2',
		420: '0xaFD87d1a62260bD5714C55a1BB4057bDc8dFA413',
	},
	"vKwentaToken": {
		10: '0x6789D8a7a7871923Fc6430432A602879eCB6520a',
		420: '0xb897D76bC9F7efB66Fb94970371ef17998c296b6',
	},
	"veKwentaToken": {
		10: '0x678d8f4ba8dfe6bad51796351824dcceceaeff2b',
		420: '0x3e52b5f840eafd79394c6359e93bf3ffdae89ee4',
	},
	"vKwentaRedeemer": {
		10: '0x8132EE584bCD6f8Eb1bea141DB7a7AC1E72917b9',
		420: '0x03c3E61D624F279243e1c8b43eD0fCF6790D10E9',
	},
	"veKwentaRedeemer": {
		10: '0xc7088AC8F287539567e458C7D08C2a1470Fd25B7',
		420: '0x86ca3CEbEA60101292EEFCd5802fD6e55D647c87',
	},
	"TradingRewards": {
		10: '0xf486A72E8c8143ACd9F65A104A16990fDb38be14',
		420: '0x74c0A3bD10634759DC8B4CA7078C8Bf85bFE1271',
	},
	"TradingRewardsPerpsV2": {
		10: '0x2787CC20e5ECb4BF1bfB79eAE284201027683179',
	},
	"BatchClaimer": {
		10: '0x6Fd879830D9b1EE5d4f9ef12f8D5deE916bebD0b',
	},
}
