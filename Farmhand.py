import time, json, os, time, telegram, asyncio, traceback
import matplotlib.pyplot as plt
from datetime import datetime
from web3 import Web3
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import ConversationHandler, Filters, CommandHandler, CallbackContext, MessageHandler, Dispatcher, Updater

configFile = open("settings.json","r")
config = json.load(configFile)
configFile.close()
telegram_user = config['telegram_user']
walletAddress = config['wallet']
telegramBot = Bot(config['telegram_token'])
enabled = False
stakingABI = '[{"inputs":[{"internalType":"contract CakeToken","name":"_cake","type":"address"},{"internalType":"contract SyrupBar","name":"_syrup","type":"address"},{"internalType":"address","name":"_devaddr","type":"address"},{"internalType":"uint256","name":"_cakePerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"BONUS_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IBEP20","name":"_lpToken","type":"address"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cake","outputs":[{"internalType":"contract CakeToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cakePerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_devaddr","type":"address"}],"name":"dev","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"devaddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"enterStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"leaveStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"migrate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"migrator","outputs":[{"internalType":"contract IMigratorChef","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingCake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IMigratorChef","name":"_migrator","type":"address"}],"name":"setMigrator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract SyrupBar","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"multiplierNumber","type":"uint256"}],"name":"updateMultiplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
pancakeABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
bareABI = '[{"inputs":[{"internalType":"uint256","name":"initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'
poolABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenRecovered","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"AdminTokenRecovery","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"poolLimitPerUser","type":"uint256"}],"name":"NewPoolLimit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"rewardPerBlock","type":"uint256"}],"name":"NewRewardPerBlock","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"startBlock","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"endBlock","type":"uint256"}],"name":"NewStartAndEndBlocks","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"RewardsStop","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"PRECISION_FACTOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SMART_CHEF_FACTORY","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"accTokenPerShare","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"hasUserLimit","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IBEP20","name":"_stakedToken","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"},{"internalType":"uint256","name":"_poolLimitPerUser","type":"uint256"},{"internalType":"address","name":"_admin","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isInitialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastRewardBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLimitPerUser","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenAddress","type":"address"},{"internalType":"uint256","name":"_tokenAmount","type":"uint256"}],"name":"recoverWrongTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stakedToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_hasUserLimit","type":"bool"},{"internalType":"uint256","name":"_poolLimitPerUser","type":"uint256"}],"name":"updatePoolLimitPerUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"}],"name":"updateRewardPerBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"name":"updateStartAndEndBlocks","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
lpABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
question = False
valuation = {1: 0,2: 0,3: 0,"updated": False}
lastProcessed = False
farmName = "<i>To be confirmed</i>"
poolName = "<i>To be confirmed</i>"
marketData = False

def handle_command(update,context):
    global enabled, question, valuation, lastProcessed, farmName, poolName, marketData
    if str(update.message.chat_id) == telegram_user:
        if update.message.text == "/start" or update.message.text == "🔙 Main Menu":
            keyboard = [["👨‍🌾 Farm status"],["✅ Start farm","❌ Stop farm"],["📈 Farm history","💵 Market prices"],["⚙️ Configure farm"]]
            context.bot.send_message(telegram_user,text="You are now on the Farmhand main menu.",reply_markup=ReplyKeyboardMarkup(keyboard,resize_keyboard=True))
            if question is not False:
                question = False
        elif update.message.text == "⚙️ Configure farm":
            keyboard = [["🔙 Main Menu"],["➕ Add L3 Pair","➖ Remove L3 Pair"],["🍰 L2 threshold","🌱 L3 threshold"]]
            context.bot.send_message(telegram_user,text="Please select a configuration option.",reply_markup=ReplyKeyboardMarkup(keyboard,resize_keyboard=True))
            if question is not False:
                question = False
        elif update.message.text == "✅ Start farm":
            if enabled == False:
                enabled = True
                context.bot.send_message(telegram_user,text="✅ Farming will now start.")
            elif enabled == True:
                context.bot.send_message(telegram_user,text="✅ Farming has already started.")
            if question is not False:
                question = False
        elif update.message.text == "❌ Stop farm":
            if enabled == True:
                enabled = False
                context.bot.send_message(telegram_user,text="❌ Farming will now stop.")
            elif enabled == False:
                context.bot.send_message(telegram_user,text="❌ Farming has already stopped.")
            if question is not False:
                question = False
        elif update.message.text == "👨‍🌾 Farm status":
            status = "🚜 <b>STATUS</b>\n<b>Farming:</b> "
            if enabled == True:
                status = status + "Started"
            else:
                status = status + " Stopped"
            
            lastStr = "Never"
            if lastProcessed is not False:
                lastMins = int((datetime.now() - lastProcessed).seconds / 60)
                if lastMins == 0:
                    lastStr = "Just now"
                elif lastMins == 1:
                    lastStr = str(lastMins) + " min ago"
                elif lastMins > 2:
                    lastStr = str(lastMins) + " mins ago (stale!)"
                else:
                    lastStr = str(lastMins) + " mins ago"

            valuationStr = "Never"
            if valuation["updated"] is not False:
                lastValuation = int((datetime.now() - valuation["updated"]).seconds / 60)
                if lastValuation == 0:
                    valuationStr = "Just now"
                elif lastValuation == 1:
                    valuationStr = str(lastValuation) + " min ago"
                elif lastValuation > 6:
                    valuationStr = str(lastValuation) + " mins ago (stale!)"
                else:
                    valuationStr = str(lastValuation) + " mins ago"

            status = status + "\n<b>Last Check:</b> " + str(lastStr) + "\n<b>Last Valuation</b>: " + str(valuationStr) + "\n\n💵 <b>VALUATION</b>\n"
            
            if valuationStr != "Never" and "stale!" not in valuationStr:
                status = status + "<b>Layer 1:</b> $" + "{:,}".format(valuation[1]) + "\n<b>Layer 2:</b> $" + "{:,}".format(valuation[2]) + "\n<b>Layer 3:</b> $" + "{:,}".format(valuation[3]) + "\n<b>Total:</b> $" + "{:,}".format(valuation[1] + valuation[2] + valuation[3])
            elif enabled == True:
                status = status + "<i>Check in a few minutes.</i>"
            else:
                status = status + "<i>Farming must be started.</i>"
            status = status + "\n\n⚙️ <b>CONFIG</b>\n<b>Farm:</b> " + farmName + "\n<b>Pool:</b> " + poolName + "\n<b>Layer 2 Threshold:</b> $" + str(config["l2_threshold"]) + "\n<b>Layer 3 Threshold:</b> $" + str(config["l3_threshold"])
            context.bot.send_message(telegram_user,text=status,parse_mode="html")
            if question is not False:
                question = False
        elif update.message.text == "💵 Market prices":
            if marketData is not False and marketData != "":
                context.bot.send_message(telegram_user,text=marketData,parse_mode="html")
            elif enabled == True:
                context.bot.send_message(telegram_user,text="<i>Check in a few minutes.</i>",parse_mode="html")
            else:
                context.bot.send_message(telegram_user,text="<i>Farming must be started.</i>",parse_mode="html")
            if question is not False:
                question = False
        elif update.message.text == "📈 Farm history":
            # Load the data from the file
            valuationsFile = open("valuations.json","r")
            valuations = json.load(valuationsFile)
            valuationsFile.close()

            # Populate data into arrays
            dates = []
            l1 = []
            l2 = []
            l3 = []
            for key,val in valuations.items():
                dates.append(key)
                l1.append(val["Layer 1"])
                l2.append(val["Layer 2"])
                l3.append(val["Layer 3"])

            # Render the graph
            fig, ax = plt.subplots()
            ax.bar(dates,l1,0.8,label='Layer 1')
            ax.bar(dates,l2,0.8,label='Layer 2')
            ax.bar(dates,l3,0.8,label='Layer 3')
            ax.set_ylabel("U.S. Dollars")
            ax.set_title("Daily farm valuations")
            ax.legend()
            fig.autofmt_xdate()
            plt.savefig(str(telegram_user) + ".png")
            context.bot.send_photo(telegram_user,photo=open(str(telegram_user) + ".png","rb"))
            os.remove(str(telegram_user) + ".png")
            if question is not False:
                question = False
        elif update.message.text == "➕ Add L3 Pair":
            context.bot.send_message(telegram_user,text="➕ Please provide the Farm PID for the pair. Use <b><a href='https://github.com/pancakeswap/pancake-frontend/blob/master/src/config/constants/farms.ts'>this page</a></b> for reference.",parse_mode="html",disable_web_page_preview=True)
            question = "AddL3"
        elif update.message.text == "🍰 L2 threshold":
            context.bot.send_message(telegram_user,text="🍰 Please specify a threshold in U.S. Dollars. Once this amount is reached, Cake will automatically be harvested from Layer 1.",parse_mode="html")
            question = "L2Threshold"
        elif question == "AddL3":
            pid = update.message.text
        elif question == "L2Threshold":
            try:
                usd = int(update.message.text)
                if usd >= 5:
                    config["l2_threshold"] = usd
                    configFile = open("settings.json","w")
                    json.dump(config,configFile,indent=4)
                    configFile.close()
                    context.bot.send_message(telegram_user,text="🍰 The L2 threshold has been updated.",parse_mode="html")
                else:
                    context.bot.send_message(telegram_user,text="📛 The L2 threshold cannot be less than five dollars.",parse_mode="html")
            except:
                context.bot.send_message(telegram_user,text="📛 The specified L2 threshold could not be interpreted as a number.",parse_mode="html")
            question = False


async def telegram():
    updater = Updater(config['telegram_token'])
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(".*"),handle_command))
    updater.start_polling()
    telegramBot.send_message(telegram_user,text="📣 Farmhand has been updated and/or restarted. Please use the 'Start farm' button to ensure your farm is running.")

def calculateLiquidityUSD(web3,pancakeContract,stakingContract,bnb,wallet,farmPID):
    lpToken = stakingContract.functions.poolInfo(farmPID).call()[0]
    lpContract = web3.eth.contract(address=lpToken,abi=lpABI)
    reserves = lpContract.functions.getReserves().call()
    usdValue = 0
    token0 = lpContract.functions.token0().call()
    token1 = lpContract.functions.token1().call()

    if token0 == bnb:
        usdValue += pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[1] * web3.fromWei(reserves[0],"ether") * 2
    elif token1 == bnb:
        usdValue += pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[1] * web3.fromWei(reserves[1],"ether") * 2

    poolShare = web3.fromWei(stakingContract.functions.userInfo(farmPID,wallet).call()[0],"ether") / web3.fromWei(lpContract.functions.totalSupply().call(),"ether")
    return web3.fromWei(usdValue,"ether") * poolShare

async def farming():
    global enabled, lastProcessed, farmName, poolName, marketData, walletAddress
    while True:
        if enabled == True:
            try:
                web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
                if web3.isConnected():
                    wallet = web3.toChecksumAddress(walletAddress)
                    bnb = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")
                    cake = web3.toChecksumAddress("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82")
                    cakeContract = web3.eth.contract(address=cake,abi=bareABI)
                    stakingContract = web3.eth.contract(address=web3.toChecksumAddress("0x73feaa1ee314f8c655e354234017be2193c9e24e"),abi=stakingABI)
                    pancakeContract = web3.eth.contract(address=web3.toChecksumAddress("0x10ED43C718714eb63d5aA57B78B54704E256024E"),abi=pancakeABI)

                    # Update info every 5th minute
                    if int(time.strftime("%M")) % 5 == 0:
                        # Valuation
                        valuation[1] = 0
                        valuation[2] = 0
                        valuation[3] = 0

                        cakeWalletBalance = cakeContract.functions.balanceOf(wallet).call()
                        if cakeWalletBalance > 0:
                            valuation[2] += web3.fromWei(pancakeContract.functions.getAmountsOut(cakeWalletBalance,[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")

                        if "farm_pid" in config:
                            valuation[1] += int(calculateLiquidityUSD(web3,pancakeContract,stakingContract,bnb,wallet,config["farm_pid"]))
                            cakeBalance = stakingContract.functions.pendingCake(config["farm_pid"],wallet).call()
                            if cakeBalance > 0:
                                valuation[2] += web3.fromWei(pancakeContract.functions.getAmountsOut(cakeBalance,[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")
                        if "pool" in config:
                            poolContract = web3.eth.contract(address=web3.toChecksumAddress(config["pool"]),abi=poolABI)
                            staked = poolContract.functions.userInfo(wallet).call()[0]
                            if staked > 0:
                                valuation[2] += web3.fromWei(pancakeContract.functions.getAmountsOut(staked,[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")

                            pending = poolContract.functions.pendingReward(wallet).call()
                            if pending > 0:
                                poolToken = poolContract.functions.rewardToken().call()
                                valuation[3] += web3.fromWei(pancakeContract.functions.getAmountsOut(pending,[poolToken,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")

                            tokenWalletBalance = web3.eth.contract(address=poolToken,abi=bareABI).functions.balanceOf(wallet).call()
                            if tokenWalletBalance > 0:
                                valuation[3] += web3.fromWei(pancakeContract.functions.getAmountsOut(tokenWalletBalance,[poolToken,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")
                        
                        valuation[1] = int(valuation[1])
                        valuation[2] = int(valuation[2])
                        valuation[3] = int(valuation[3])
                        valuation["updated"] = datetime.now()

                        # Generate graphing for valuation history
                        valuationsFile = open("valuations.json","r")
                        valuations = json.load(valuationsFile)
                        valuationsFile.close()
                        today = datetime.today().strftime("%Y-%m-%d")
                        valuations[today] = {"Layer 1": valuation[1],"Layer 2": valuation[2],"Layer 3": valuation[3]}
                        valuationsFile = open("valuations.json","w")
                        json.dump(valuations,valuationsFile,indent=4)
                        valuationsFile.close()

                        # Market prices
                        marketDataStr = ""
                        if "farm_pid" in config:
                            lpToken = stakingContract.functions.poolInfo(config["farm_pid"]).call()[0]
                            lpContract = web3.eth.contract(address=lpToken,abi=lpABI)
                            token0 = lpContract.functions.token0().call()
                            token1 = lpContract.functions.token1().call()
                            marketDataStr += "\n\n<b>LAYER 1</b>\n"
                            
                            if token0 == bnb:
                                marketDataStr += "<b>" + web3.eth.contract(address=token0,abi=bareABI).functions.symbol().call() + ":</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[token0,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[1],"ether")) + "\n"
                            else:
                                marketDataStr += "<b>" + web3.eth.contract(address=token0,abi=bareABI).functions.symbol().call() + ":</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[token0,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")) + "\n"
                            
                            if token1 == bnb:
                                marketDataStr += "<b>" + web3.eth.contract(address=token1,abi=bareABI).functions.symbol().call() + ":</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[token1,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[1],"ether"))
                            else:
                                marketDataStr += "<b>" + web3.eth.contract(address=token1,abi=bareABI).functions.symbol().call() + ":</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[token1,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether"))
                        
                        marketDataStr += "\n\n<b>LAYER 2</b>\n<b>Cake:</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether"))

                        if "pool" in config:
                            poolContract = web3.eth.contract(address=web3.toChecksumAddress(config["pool"]),abi=poolABI)
                            poolToken = poolContract.functions.rewardToken().call()
                            marketDataStr += "\n\n<b>LAYER 3</b>\n"
                            marketDataStr += "<b>" + web3.eth.contract(address=poolToken,abi=bareABI).functions.symbol().call() + ":</b> " + "${:0,.2f}".format(web3.fromWei(pancakeContract.functions.getAmountsOut(web3.toWei(1,"ether"),[poolToken,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether"))
                        
                        if marketDataStr != "":
                            marketData = marketDataStr[2:]
                        else:
                            marketData = ""
                    
                    if "farm_pid" in config:
                        if farmName == "<i>To be confirmed</i>":
                            lpToken = stakingContract.functions.poolInfo(config["farm_pid"]).call()[0]
                            lpContract = web3.eth.contract(address=lpToken,abi=lpABI)
                            token0 = lpContract.functions.token0().call()
                            token1 = lpContract.functions.token1().call()
                            farmName = web3.eth.contract(address=token0,abi=bareABI).functions.symbol().call() + " - " + web3.eth.contract(address=token1,abi=bareABI).functions.symbol().call() + " (PID: " + str(config["farm_pid"]) + ")"

                        # Harvest CAKE from Farm
                        balance = stakingContract.functions.pendingCake(config["farm_pid"],wallet).call()
                        if balance >= 0.1:
                            usdBalance = web3.fromWei(pancakeContract.functions.getAmountsOut(balance,[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")
                            if usdBalance >= config["l2_threshold"]:
                                txn = stakingContract.functions.withdraw(config["farm_pid"],0).buildTransaction({"from": wallet,"nonce": web3.eth.get_transaction_count(wallet)})
                                signed_txn = web3.eth.account.sign_transaction(txn,private_key=config['key'])
                                web3.eth.waitForTransactionReceipt(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
                                cakeBalance = cakeContract.functions.balanceOf(wallet).call()
                                telegramBot.send_message(telegram_user,text="🍰 Harvested CAKE from Layer 1 (Wallet Balance: " + str(round(web3.fromWei(cakeBalance,"ether"),3)) + ")")
                            
                            cakeBalance = cakeContract.functions.balanceOf(wallet).call()
                            if cakeBalance >= 0.1:
                                usdBalance = web3.fromWei(pancakeContract.functions.getAmountsOut(cakeBalance,[cake,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")
                                if usdBalance > config["l2_threshold"]:
                                    # Top up BNB if necessary
                                    # bnbBalance = web3.fromWei(web3.eth.getBalance(wallet),"ether")
                                    # if bnbBalance < 0.1:
                                        # txn = pancakeContract.functions.swapExactTokensForETH(0,0,[cake,bnb],wallet,(int(time.time()) + 10000)).buildTransaction({"from": wallet,"value": web3.toWei(web3.fromWei(cakeBalance,"ether") / 4,"ether"),"nonce": web3.eth.get_transaction_count(wallet)})
                                        # signed_txn = web3.eth.account.sign_transaction(txn,private_key=config['key'])
                                        # web3.eth.waitForTransactionReceipt(web3.eth.send_raw_transaction(signed_txn.rawTransaction))

                                        # bnbBalance = web3.fromWei(web3.eth.getBalance(wallet),"ether")
                                        # cakeBalance = cakeContract.functions.balanceOf(wallet).call()
                                        # telegramBot.send_message(telegram_user,text="🔔 BNB balance was low; 25%% of harvest was used to top-up:\n\nBNB: " + str(round(bnbBalance,3)) + "\nCAKE: " + str(round(web3.fromWei(cakeBalance,"ether"),3)))
                                    
                                    # Stake CAKE into pool
                                    if "pool" in config:
                                        poolContract = web3.eth.contract(address=web3.toChecksumAddress(config["pool"]),abi=poolABI)
                                        txn = poolContract.functions.deposit(cakeBalance).buildTransaction({"from": wallet,"nonce": web3.eth.get_transaction_count(wallet)})
                                        signed_txn = web3.eth.account.sign_transaction(txn,private_key=config['key'])
                                        web3.eth.waitForTransactionReceipt(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
                                        telegramBot.send_message(telegram_user,text="🌱 Staked " + str(round(web3.fromWei(cakeBalance,"ether"),3)) + " CAKE into the chosen Layer 2 pool.")
                                    else:
                                        telegramBot.send_message(telegram_user,text="📛 CAKE was not staked anywhere as no pool has been set. Use the 'Configuration' section to set the pool.")
                    else:
                        telegramBot.send_message(telegram_user,text="📛 Farm PID not set. Either stop the farm or set the PID under the 'Configuration' section.")
                    
                    # Check if we can harvest the Pool
                    if "pool" in config:
                        poolContract = web3.eth.contract(address=web3.toChecksumAddress(config["pool"]),abi=poolABI)
                        poolToken = poolContract.functions.rewardToken().call()

                        if poolName == "<i>To be confirmed</i>":
                            poolName = web3.eth.contract(address=poolToken,abi=bareABI).functions.symbol().call()
                        # pending = poolContract.functions.pendingReward(wallet).call()

                        # tokenContract = web3.eth.contract(address=poolToken,abi=bareABI)
                        # tokenBalance = web3.fromWei(tokenContract.functions.balanceOf(wallet).call(),"ether")

                        # pendingUSD = web3.fromWei(pancakeContract.functions.getAmountsOut(pending,[poolToken,bnb,web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")]).call()[2],"ether")
                        # if pendingUSD > 0.6 and tokenBalance+pendingUSD > 20:
                            # txn = poolContract.functions.withdraw(0).buildTransaction({"from": wallet,"nonce": web3.eth.get_transaction_count(wallet)})
                            # signed_txn = web3.eth.account.sign_transaction(txn,private_key=config['key'])
                            # web3.eth.waitForTransactionReceipt(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
                            # telegramBot.send_message(telegram_user,text="🚜 Harvested $" + str(round(pendingUSD,3)) + " of " + tokenContract.functions.name().call() + " from the pool.")
                        
                        # tokenBalance = web3.fromWei(tokenContract.functions.balanceOf(wallet).call(),"ether")
                        # if tokenBalance > 20:
                        # TODO: Put harvest into L3 liquidity farm
            except Exception as e:
                error = traceback.format_exc()
                print(error)
                if len(error) > 3000:
                    error = error[0:3000]
                telegramBot.send_message(telegram_user,text="📛 ERROR:\n\n" + error)
        
        lastProcessed = datetime.now()
        await asyncio.sleep(60)

async def main():
    await telegram()
    await farming()

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
