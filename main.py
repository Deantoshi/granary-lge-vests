from web3 import Web3
from web3.middleware import geth_poa_middleware 
import pandas as pd
import time

# Replace with the actual Optimism RPC URL
rpc_url = 'https://mantle.drpc.org'
# # rpc_url = ''

# Create a Web3 instance to connect to the Optimism blockchain
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# LATEST_BLOCK = web3.eth.get_block_number()
LATEST_BLOCK = 951714 + 1
#Lending pool founding block
# FROM_BLOCK = 758632
FROM_BLOCK = 778064
# FROM_BLOCK = 0

# returns basic data about our reserves in a dataframe
def get_reserve_data():
    # a_token_list = ['0x245B368d5a969179Df711774e7BdC5eC670e92EF', '0x5C4866349ff0Bf1e7C4b7f6d8bB2dBcbe76f8895', '0xa0f8323A84AdC89346eD3F7c5dcddf799916b51E', '0xB36535765A7421B397Cfd9fEc03cF96aA99C8D08', '0xdc66aC2336742E387b766B4c264c993ee6a3EF28']
    # v_token_list = ['0xd4c3692B753302Ef0Ef1d50dd7928D60ef00B9ff', '0x157903B7c6D759c9D3c65A675a15aA0723eea95B', '0x393a64Fc561D6c8f5D8D8c427005cAB66DfeCA9D', '0xd8A40a27dD36565cC2B17C8B937eE50B69209E22', '0x9576c6FDd82474177781330Fc47C38D89936E7c8']

    reserve_address_list = ['0x245B368d5a969179Df711774e7BdC5eC670e92EF', '0x5C4866349ff0Bf1e7C4b7f6d8bB2dBcbe76f8895', '0xa0f8323A84AdC89346eD3F7c5dcddf799916b51E', '0xB36535765A7421B397Cfd9fEc03cF96aA99C8D08', '0xdc66aC2336742E387b766B4c264c993ee6a3EF28',
                '0xd4c3692B753302Ef0Ef1d50dd7928D60ef00B9ff', '0x157903B7c6D759c9D3c65A675a15aA0723eea95B', '0x393a64Fc561D6c8f5D8D8c427005cAB66DfeCA9D', '0xd8A40a27dD36565cC2B17C8B937eE50B69209E22', '0x9576c6FDd82474177781330Fc47C38D89936E7c8']

    reserve_decimal_list = [1e18, 1e6, 1e6, 1e18, 1e8, 1e18, 1e6, 1e6, 1e18, 1e8]

    reserve_name_list = ['a_dai', 'a_usdc', 'a_usdt', 'a_eth', 'a_wbtc', 'v_dai', 'v_usdc', 'v_usdt', 'v_eth', 'v_wbtc']

    df = pd.DataFrame()

    df['reserve_name'] = reserve_name_list
    df['reserve_address'] = reserve_address_list
    df['reserve_decimal'] = reserve_decimal_list

    return df

# gets the ABI for our redemption contract
def get_trove_manager_contract_abi ():
    contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_activePoolAddress","type":"address"}],"name":"ActivePoolAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_baseRate","type":"uint256"}],"name":"BaseRateUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_newBorrowerOperationsAddress","type":"address"}],"name":"BorrowerOperationsAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collSurplusPoolAddress","type":"address"}],"name":"CollSurplusPoolAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_newCollateralConfigAddress","type":"address"}],"name":"CollateralConfigAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_defaultPoolAddress","type":"address"}],"name":"DefaultPoolAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_gasPoolAddress","type":"address"}],"name":"GasPoolAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_lqtyStakingAddress","type":"address"}],"name":"LQTYStakingAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_lqtyTokenAddress","type":"address"}],"name":"LQTYTokenAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_L_Collateral","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_L_LUSDDebt","type":"uint256"}],"name":"LTermsUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_newLUSDTokenAddress","type":"address"}],"name":"LUSDTokenAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_lastFeeOpTime","type":"uint256"}],"name":"LastFeeOpTimeUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_liquidatedDebt","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_liquidatedColl","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_collGasCompensation","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_LUSDGasCompensation","type":"uint256"}],"name":"Liquidation","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_liquidationHelperAddress","type":"address"}],"name":"LiquidationHelperAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_newPriceFeedAddress","type":"address"}],"name":"PriceFeedAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_attemptedLUSDAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_actualLUSDAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_collSent","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_collFee","type":"uint256"}],"name":"Redemption","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_redemptionHelperAddress","type":"address"}],"name":"RedemptionHelperAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_sortedTrovesAddress","type":"address"}],"name":"SortedTrovesAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_stabilityPoolAddress","type":"address"}],"name":"StabilityPoolAddressChanged","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_totalStakesSnapshot","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_totalCollateralSnapshot","type":"uint256"}],"name":"SystemSnapshotsUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_newTotalStakes","type":"uint256"}],"name":"TotalStakesUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_borrower","type":"address"},{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_newIndex","type":"uint256"}],"name":"TroveIndexUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_borrower","type":"address"},{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_debt","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_coll","type":"uint256"},{"indexed":False,"internalType":"enum TroveManager.TroveManagerOperation","name":"_operation","type":"uint8"}],"name":"TroveLiquidated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_L_Collateral","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_L_LUSDDebt","type":"uint256"}],"name":"TroveSnapshotsUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"_borrower","type":"address"},{"indexed":False,"internalType":"address","name":"_collateral","type":"address"},{"indexed":False,"internalType":"uint256","name":"_debt","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_coll","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"_stake","type":"uint256"},{"indexed":False,"internalType":"enum TroveManager.TroveManagerOperation","name":"_operation","type":"uint8"}],"name":"TroveUpdated","type":"event"},{"inputs":[],"name":"BETA","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BORROWING_FEE_FLOOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DECIMAL_PRECISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LUSD_GAS_COMPENSATION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"L_Collateral","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"L_LUSDDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_BORROWING_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINUTE_DECAY_FACTOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_NET_DEBT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERCENT_DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REDEMPTION_FEE_FLOOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SECONDS_IN_ONE_MINUTE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"TroveOwners","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"Troves","outputs":[{"internalType":"uint256","name":"debt","type":"uint256"},{"internalType":"uint256","name":"coll","type":"uint256"},{"internalType":"uint256","name":"stake","type":"uint256"},{"internalType":"enum TroveStatus","name":"status","type":"uint8"},{"internalType":"uint128","name":"arrayIndex","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_100pct","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activePool","outputs":[{"internalType":"contract IActivePool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"addTroveOwnerToArray","outputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"applyPendingRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"baseRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"address[]","name":"_troveArray","type":"address[]"}],"name":"batchLiquidateTroves","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"borrowerOperationsAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_redeemer","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_attemptedLUSDAmount","type":"uint256"},{"internalType":"uint256","name":"_actualLUSDAmount","type":"uint256"},{"internalType":"uint256","name":"_collSent","type":"uint256"},{"internalType":"uint256","name":"_collFee","type":"uint256"}],"name":"burnLUSDAndEmitRedemptionEvent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"checkRecoveryMode","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_closedStatusNum","type":"uint256"}],"name":"closeTrove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"collateralConfig","outputs":[{"internalType":"contract ICollateralConfig","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decayBaseRateFromBorrowing","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_collDecrease","type":"uint256"}],"name":"decreaseTroveColl","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_debtDecrease","type":"uint256"}],"name":"decreaseTroveDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"defaultPool","outputs":[{"internalType":"contract IDefaultPool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_liquidatedDebt","type":"uint256"},{"internalType":"uint256","name":"_liquidatedColl","type":"uint256"},{"internalType":"uint256","name":"_collGasCompensation","type":"uint256"},{"internalType":"uint256","name":"_LUSDGasCompensation","type":"uint256"}],"name":"emitLiquidationEvent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_debt","type":"uint256"},{"internalType":"uint256","name":"_coll","type":"uint256"},{"internalType":"bool","name":"_isRecoveryMode","type":"bool"}],"name":"emitTroveLiquidatedAndTroveUpdated","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_LUSDDebt","type":"uint256"}],"name":"getBorrowingFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_LUSDDebt","type":"uint256"}],"name":"getBorrowingFeeWithDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBorrowingRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBorrowingRateWithDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"getCurrentICR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getEntireDebtAndColl","outputs":[{"internalType":"uint256","name":"debt","type":"uint256"},{"internalType":"uint256","name":"coll","type":"uint256"},{"internalType":"uint256","name":"pendingLUSDDebtReward","type":"uint256"},{"internalType":"uint256","name":"pendingCollateralReward","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"}],"name":"getEntireSystemColl","outputs":[{"internalType":"uint256","name":"entireSystemColl","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"}],"name":"getEntireSystemDebt","outputs":[{"internalType":"uint256","name":"entireSystemDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getNominalICR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getPendingCollateralReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getPendingLUSDDebtReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_collateralDrawn","type":"uint256"}],"name":"getRedemptionFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_collateralDrawn","type":"uint256"}],"name":"getRedemptionFeeWithDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRedemptionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRedemptionRateWithDecay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"getTCR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getTroveColl","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getTroveDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"getTroveFromTroveOwnersArray","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"}],"name":"getTroveOwnersCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getTroveStake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"getTroveStatus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"hasPendingRewards","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_collIncrease","type":"uint256"}],"name":"increaseTroveColl","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_debtIncrease","type":"uint256"}],"name":"increaseTroveDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"lastCollateralError_Redistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastFeeOperationTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"lastLUSDDebtError_Redistribution","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"liquidate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_n","type":"uint256"}],"name":"liquidateTroves","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"liquidationHelper","outputs":[{"internalType":"contract ILiquidationHelper","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lqtyStaking","outputs":[{"internalType":"contract ILQTYStaking","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lqtyToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lusdToken","outputs":[{"internalType":"contract ILUSDToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IActivePool","name":"_activePool","type":"address"},{"internalType":"contract IDefaultPool","name":"_defaultPool","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_LUSD","type":"uint256"},{"internalType":"uint256","name":"_collAmount","type":"uint256"}],"name":"movePendingTroveRewardsToActivePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceFeed","outputs":[{"internalType":"contract IPriceFeed","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_id","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_newNICR","type":"uint256"},{"internalType":"address","name":"_prevId","type":"address"},{"internalType":"address","name":"_nextId","type":"address"}],"name":"reInsert","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_LUSD","type":"uint256"},{"internalType":"uint256","name":"_collAmount","type":"uint256"}],"name":"redeemCloseTrove","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_LUSDamount","type":"uint256"},{"internalType":"address","name":"_firstRedemptionHint","type":"address"},{"internalType":"address","name":"_upperPartialRedemptionHint","type":"address"},{"internalType":"address","name":"_lowerPartialRedemptionHint","type":"address"},{"internalType":"uint256","name":"_partialRedemptionHintNICR","type":"uint256"},{"internalType":"uint256","name":"_maxIterations","type":"uint256"},{"internalType":"uint256","name":"_maxFeePercentage","type":"uint256"}],"name":"redeemCollateral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"redemptionHelper","outputs":[{"internalType":"contract IRedemptionHelper","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IActivePool","name":"_activePool","type":"address"},{"internalType":"contract IDefaultPool","name":"_defaultPool","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_debt","type":"uint256"},{"internalType":"uint256","name":"_coll","type":"uint256"},{"internalType":"uint256","name":"_collDecimals","type":"uint256"}],"name":"redistributeDebtAndColl","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"removeStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"rewardSnapshots","outputs":[{"internalType":"uint256","name":"collAmount","type":"uint256"},{"internalType":"uint256","name":"LUSDDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IActivePool","name":"_activePool","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"address","name":"_liquidator","type":"address"},{"internalType":"uint256","name":"_LUSD","type":"uint256"},{"internalType":"uint256","name":"_collAmount","type":"uint256"}],"name":"sendGasCompensation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrowerOperationsAddress","type":"address"},{"internalType":"address","name":"_collateralConfigAddress","type":"address"},{"internalType":"address","name":"_activePoolAddress","type":"address"},{"internalType":"address","name":"_defaultPoolAddress","type":"address"},{"internalType":"address","name":"_gasPoolAddress","type":"address"},{"internalType":"address","name":"_collSurplusPoolAddress","type":"address"},{"internalType":"address","name":"_priceFeedAddress","type":"address"},{"internalType":"address","name":"_lusdTokenAddress","type":"address"},{"internalType":"address","name":"_sortedTrovesAddress","type":"address"},{"internalType":"address","name":"_lqtyTokenAddress","type":"address"},{"internalType":"address","name":"_lqtyStakingAddress","type":"address"},{"internalType":"address","name":"_redemptionHelperAddress","type":"address"},{"internalType":"address","name":"_liquidationHelperAddress","type":"address"}],"name":"setAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_num","type":"uint256"}],"name":"setTroveStatus","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sortedTroves","outputs":[{"internalType":"contract ISortedTroves","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalCollateralSnapshot","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalStakes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalStakesSnapshot","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_collateralDrawn","type":"uint256"},{"internalType":"uint256","name":"_price","type":"uint256"},{"internalType":"uint256","name":"_collDecimals","type":"uint256"},{"internalType":"uint256","name":"_collDebt","type":"uint256"}],"name":"updateBaseRateFromRedemption","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_newDebt","type":"uint256"},{"internalType":"uint256","name":"_newColl","type":"uint256"}],"name":"updateDebtAndCollAndStakesPostRedemption","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"updateStakeAndTotalStakes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IActivePool","name":"_activePool","type":"address"},{"internalType":"address","name":"_collateral","type":"address"},{"internalType":"uint256","name":"_collRemainder","type":"uint256"}],"name":"updateSystemSnapshots_excludeCollRemainder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_borrower","type":"address"},{"internalType":"address","name":"_collateral","type":"address"}],"name":"updateTroveRewardSnapshots","outputs":[],"stateMutability":"nonpayable","type":"function"}]
    return contract_abi

print(get_trove_manager_contract_abi())

#gets our web3 contract object
# @cache
def get_contract():
    contract_address = "0x871AfF0013bE6218B61b28b274a6F53DB131795F"
    contract_abi = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"onBehalfOf","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"borrowRateMode","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"borrowRate","type":"uint256"},{"indexed":True,"internalType":"uint16","name":"referral","type":"uint16"}],"name":"Borrow","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"onBehalfOf","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":True,"internalType":"uint16","name":"referral","type":"uint16"}],"name":"Deposit","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"target","type":"address"},{"indexed":True,"internalType":"address","name":"initiator","type":"address"},{"indexed":True,"internalType":"address","name":"asset","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"premium","type":"uint256"},{"indexed":False,"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"FlashLoan","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"collateralAsset","type":"address"},{"indexed":True,"internalType":"address","name":"debtAsset","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"debtToCover","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"liquidatedCollateralAmount","type":"uint256"},{"indexed":False,"internalType":"address","name":"liquidator","type":"address"},{"indexed":False,"internalType":"bool","name":"receiveAToken","type":"bool"}],"name":"LiquidationCall","type":"event"},{"anonymous":False,"inputs":[],"name":"Paused","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"RebalanceStableBorrowRate","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"repayer","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Repay","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":False,"internalType":"uint256","name":"liquidityRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"stableBorrowRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"variableBorrowRate","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"liquidityIndex","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"variableBorrowIndex","type":"uint256"}],"name":"ReserveDataUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"ReserveUsedAsCollateralDisabled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"}],"name":"ReserveUsedAsCollateralEnabled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":False,"internalType":"uint256","name":"rateMode","type":"uint256"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[],"name":"Unpaused","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"reserve","type":"address"},{"indexed":True,"internalType":"address","name":"user","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"FLASHLOAN_PREMIUM_TOTAL","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"LENDINGPOOL_REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_NUMBER_RESERVES","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_STABLE_RATE_BORROW_SIZE_PERCENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"interestRateMode","type":"uint256"},{"internalType":"uint16","name":"referralCode","type":"uint16"},{"internalType":"address","name":"onBehalfOf","type":"address"}],"name":"borrow","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"onBehalfOf","type":"address"},{"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"balanceFromBefore","type":"uint256"},{"internalType":"uint256","name":"balanceToBefore","type":"uint256"}],"name":"finalizeTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"receiverAddress","type":"address"},{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"uint256[]","name":"modes","type":"uint256[]"},{"internalType":"address","name":"onBehalfOf","type":"address"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint16","name":"referralCode","type":"uint16"}],"name":"flashLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getAddressesProvider","outputs":[{"internalType":"contract ILendingPoolAddressesProvider","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getConfiguration","outputs":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveData","outputs":[{"components":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"configuration","type":"tuple"},{"internalType":"uint128","name":"liquidityIndex","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"currentLiquidityRate","type":"uint128"},{"internalType":"uint128","name":"currentVariableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"currentStableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint8","name":"id","type":"uint8"}],"internalType":"struct DataTypes.ReserveData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveNormalizedIncome","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveNormalizedVariableDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReservesList","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralETH","type":"uint256"},{"internalType":"uint256","name":"totalDebtETH","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsETH","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserConfiguration","outputs":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.UserConfigurationMap","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtAddress","type":"address"},{"internalType":"address","name":"variableDebtAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"}],"name":"initReserve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILendingPoolAddressesProvider","name":"provider","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"collateralAsset","type":"address"},{"internalType":"address","name":"debtAsset","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"debtToCover","type":"uint256"},{"internalType":"bool","name":"receiveAToken","type":"bool"}],"name":"liquidationCall","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"rebalanceStableBorrowRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rateMode","type":"uint256"},{"internalType":"address","name":"onBehalfOf","type":"address"}],"name":"repay","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"configuration","type":"uint256"}],"name":"setConfiguration","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"val","type":"bool"}],"name":"setPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"rateStrategyAddress","type":"address"}],"name":"setReserveInterestRateStrategyAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"bool","name":"useAsCollateral","type":"bool"}],"name":"setUserUseReserveAsCollateral","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"rateMode","type":"uint256"}],"name":"swapBorrowRateMode","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"withdraw","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]
    
    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# gets the last block number we have gotten data from and returns this block number
def get_last_block_tracked():
    df = pd.read_csv('all_users.csv')
    
    last_block_monitored = df['last_block_number'].max()

    last_block_monitored = int(last_block_monitored)

    return last_block_monitored

# print(get_last_block_tracked())

def make_checksum_values(df):

    lowered_tokenAddress_list = df['tokenAddress'].to_list()
    lowered_wallet_address_list = df['wallet_address'].to_list()

    # check_sum_tx_hash_list = [Web3.to_checksum_address(x) for x in lowered_tx_hash_list]

    check_sum_wallet_address_list = [Web3.to_checksum_address(x) for x in lowered_wallet_address_list]
    # print(check_sum_wallet_address_list)

    check_sum_tokenAddress_list = [Web3.to_checksum_address(x) for x in lowered_tokenAddress_list]
    # print(check_sum_tokenAddress_list)

    df['wallet_address'] = check_sum_wallet_address_list
    df['tokenAddress'] = check_sum_tokenAddress_list

    return df

#makes a dataframe and stores it in a csv file
def make_user_data_csv(df):
    old_df = pd.read_csv('all_events.csv')
    old_df = old_df.drop_duplicates(subset=['wallet_address', 'txHash', 'lendBorrowType'], keep='last')

    combined_df_list = [df, old_df]
    combined_df = pd.concat(combined_df_list)
    combined_df = combined_df.drop_duplicates(subset=['wallet_address', 'txHash', 'lendBorrowType'], keep='last')

    combined_df['txHash'] = combined_df['txHash'].str.lower()
    combined_df['tokenAddress'] = combined_df['tokenAddress'].str.lower()

    # combined_df['txHash'] = Web3.to_checksum_address(combined_df['txHash'])
    # combined_df['tokenAddress'] = Web3.to_checksum_address(combined_df['tokenAddress'])
    # combined_df['wallet_address'] = Web3.to_checksum_address(combined_df['wallet_address'])

    combined_df = make_checksum_values(combined_df)
    # print(df)
    # print(len(old_df), len(df), len(combined_df))
    if len(combined_df) >= len(old_df):
        combined_df.to_csv('all_events.csv', index=False)
        print('Event CSV Updated')
    return

# # takes in an a_token address and returns it's contract object
def get_a_token_contract(contract_address):
    # contract_address = "0xEB329420Fae03176EC5877c34E2c38580D85E069"
    contract_abi = [{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"BalanceTransfer","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"target","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"underlyingAsset","type":"address"},{"indexed":True,"internalType":"address","name":"pool","type":"address"},{"indexed":False,"internalType":"address","name":"treasury","type":"address"},{"indexed":False,"internalType":"address","name":"incentivesController","type":"address"},{"indexed":False,"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"indexed":False,"internalType":"string","name":"aTokenName","type":"string"},{"indexed":False,"internalType":"string","name":"aTokenSymbol","type":"string"},{"indexed":False,"internalType":"bytes","name":"params","type":"bytes"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"index","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"ATOKEN_REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EIP712_REVISION","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"POOL","outputs":[{"internalType":"contract ILendingPool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RESERVE_TREASURY_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"receiverOfUnderlying","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getIncentivesController","outputs":[{"internalType":"contract IAaveIncentivesController","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getScaledUserBalanceAndSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"handleRepayment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract ILendingPool","name":"pool","type":"address"},{"internalType":"address","name":"treasury","type":"address"},{"internalType":"address","name":"underlyingAsset","type":"address"},{"internalType":"contract IAaveIncentivesController","name":"incentivesController","type":"address"},{"internalType":"uint8","name":"aTokenDecimals","type":"uint8"},{"internalType":"string","name":"aTokenName","type":"string"},{"internalType":"string","name":"aTokenSymbol","type":"string"},{"internalType":"bytes","name":"params","type":"bytes"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"mintToTreasury","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"scaledBalanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"scaledTotalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferOnLiquidation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferUnderlyingTo","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # takes in an v_token address and returns it's contract object
def get_v_token_contract(contract_address):
    # contract_address = "0xBE8afE7E442fFfFE576B979D490c5ADb7823C3c6"
    contract_abi = [{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":True},{"type":"address","name":"spender","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"BorrowAllowanceDelegated","inputs":[{"type":"address","name":"fromUser","internalType":"address","indexed":True},{"type":"address","name":"toUser","internalType":"address","indexed":True},{"type":"address","name":"asset","internalType":"address","indexed":False},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Burn","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False},{"type":"uint256","name":"currentBalance","internalType":"uint256","indexed":False},{"type":"uint256","name":"balanceIncrease","internalType":"uint256","indexed":False},{"type":"uint256","name":"avgStableRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"newTotalSupply","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Initialized","inputs":[{"type":"address","name":"underlyingAsset","internalType":"address","indexed":True},{"type":"address","name":"pool","internalType":"address","indexed":True},{"type":"address","name":"incentivesController","internalType":"address","indexed":False},{"type":"uint8","name":"debtTokenDecimals","internalType":"uint8","indexed":False},{"type":"string","name":"debtTokenName","internalType":"string","indexed":False},{"type":"string","name":"debtTokenSymbol","internalType":"string","indexed":False},{"type":"bytes","name":"params","internalType":"bytes","indexed":False}],"anonymous":False},{"type":"event","name":"Mint","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"address","name":"onBehalfOf","internalType":"address","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False},{"type":"uint256","name":"currentBalance","internalType":"uint256","indexed":False},{"type":"uint256","name":"balanceIncrease","internalType":"uint256","indexed":False},{"type":"uint256","name":"newRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"avgStableRate","internalType":"uint256","indexed":False},{"type":"uint256","name":"newTotalSupply","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":True},{"type":"address","name":"to","internalType":"address","indexed":True},{"type":"uint256","name":"value","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"DEBT_TOKEN_REVISION","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract ILendingPool"}],"name":"POOL","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"UNDERLYING_ASSET_ADDRESS","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"approveDelegation","inputs":[{"type":"address","name":"delegatee","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"borrowAllowance","inputs":[{"type":"address","name":"fromUser","internalType":"address"},{"type":"address","name":"toUser","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"burn","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getAverageStableRate","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IRewarder"}],"name":"getIncentivesController","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint40","name":"","internalType":"uint40"}],"name":"getSupplyData","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"}],"name":"getTotalSupplyAndAvgRate","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint40","name":"","internalType":"uint40"}],"name":"getTotalSupplyLastUpdated","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint40","name":"","internalType":"uint40"}],"name":"getUserLastUpdated","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getUserStableRate","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"initialize","inputs":[{"type":"address","name":"pool","internalType":"contract ILendingPool"},{"type":"address","name":"underlyingAsset","internalType":"address"},{"type":"address","name":"incentivesController","internalType":"contract IRewarder"},{"type":"uint8","name":"debtTokenDecimals","internalType":"uint8"},{"type":"string","name":"debtTokenName","internalType":"string"},{"type":"string","name":"debtTokenSymbol","internalType":"string"},{"type":"bytes","name":"params","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"mint","inputs":[{"type":"address","name":"user","internalType":"address"},{"type":"address","name":"onBehalfOf","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"rate","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"principalBalanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]}]    
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    return contract

# # takes in a contract object and returns all associated deposit events
def get_deposit_events(contract, from_block, to_block):

    # events = contract.events.Transfer.get_logs(fromBlock=from_block, toBlock=latest_block)
    events = contract.events.Deposit.get_logs(fromBlock=from_block, toBlock=to_block)

    return events

# # takes in a contract object and returns all associated withdrawal events
def get_withdraw_events(contract, from_block, to_block):

    # events = contract.events.Transfer.get_logs(fromBlock=from_block, toBlock=latest_block)
    events = contract.events.Withdraw.get_logs(fromBlock=from_block, toBlock=to_block)

    return events

# # takes in a contract object and returns all associated borrow events
def get_borrow_events(contract, from_block, to_block):

    # events = contract.events.Transfer.get_logs(fromBlock=from_block, toBlock=latest_block)
    events = contract.events.Borrow.get_logs(fromBlock=from_block, toBlock=to_block)

    return events

# # takes in a contract object and returns all associated repay events
def get_repay_events(contract, from_block, to_block):
    events = contract.events.Repay.get_logs(fromBlock=from_block, toBlock=to_block)

    return events

#handles our weth_gateway events and returns the accurate user_address
def handle_weth_gateway(event, enum_name):

    payload_address = event['args']['user'].lower()

    if payload_address.lower() == '0x9546f673ef71ff666ae66d01fd6e7c6dae5a9995'.lower():
        if enum_name == 'LEND' or enum_name == 'BORROW':
            user = 'onBehalfOf'
            payload_address = event['args'][user].lower()
    
    return payload_address

#returns a df if a tx_hash exists
def tx_hash_exists(df, tx_hash):

    new_df = pd.DataFrame()

    if ((df['txHash'] == tx_hash)).any():
        new_df = df.loc[df['txHash'] == tx_hash]
    
    return new_df

#returns whether a enum_name exists, and returns blank df if not
def lend_borrow_type_exists(df, lend_borrow_type):

    if ((df['lendBorrowType'] == lend_borrow_type)).any():
        df = df.loc[df['lendBorrowType'] == lend_borrow_type]

    else:
        df = pd.DataFrame()

    return df

#returns df if wallet_address exists
def wallet_address_exists(df, wallet_address):

    if ((df['wallet_address'] == wallet_address)).any():
        df = df.loc[df['wallet_address'] == wallet_address]

    else:
        df = pd.DataFrame()

    return df

# will tell us whether we need to find new data
# returns a list of [tx_hash, wallet_address]
def already_part_of_df(event, enum):

    all_exist = False
    tx_hash = ''
    wallet_address = ''

    df = pd.read_csv('all_events.csv')

    tx_hash = event['transactionHash'].hex()
    tx_hash = tx_hash.lower()

    new_df = tx_hash_exists(df, tx_hash)

    if len(new_df) > 0:
        new_df = lend_borrow_type_exists(new_df, enum)

        if len(new_df) > 0:
            wallet_address = handle_weth_gateway(event, enum).lower()
            new_df = wallet_address_exists(df, wallet_address)

            if len(new_df) > 0:
                all_exist = True

    response_list = [tx_hash, wallet_address, all_exist]

    return response_list

#gets how many decimals our reserve is
def get_reserve_decimals(reserve_address):
    decimals = 0
    if reserve_address == '0x4AF15ec2A0BD43Db75dd04E62FAA3B8EF36b00d5': # dai
        decimals = 1e18
    elif reserve_address == '0x176211869cA2b568f2A7D4EE941E073a821EE1ff': # usdc
        decimals = 1e6
    elif reserve_address == '0xA219439258ca9da29E9Cc4cE5596924745e12B93': # usdt
        decimals = 1e6
    elif reserve_address == '0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f': # weth
        decimals = 1e18
    elif reserve_address == '0x3aAB2285ddcDdaD8edf438C1bAB47e1a9D05a9b4': # wbtc
        decimals = 1e8
    
    return decimals

#gets our reserve price
#@cache
def get_tx_usd_amount(reserve_address, token_amount):
    contract_address = '0x8429d0AFade80498EAdb9919E41437A14d45A00B'
    contract_abi = [{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address[]","name":"sources","type":"address[]"},{"internalType":"address","name":"fallbackOracle","type":"address"},{"internalType":"address","name":"baseCurrency","type":"address"},{"internalType":"uint256","name":"baseCurrencyUnit","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"asset","type":"address"},{"indexed":True,"internalType":"address","name":"source","type":"address"}],"name":"AssetSourceUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"baseCurrency","type":"address"},{"indexed":False,"internalType":"uint256","name":"baseCurrencyUnit","type":"uint256"}],"name":"BaseCurrencySet","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"fallbackOracle","type":"address"}],"name":"FallbackOracleUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"BASE_CURRENCY","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BASE_CURRENCY_UNIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"}],"name":"getAssetsPrices","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getFallbackOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getSourceOfAsset","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address[]","name":"sources","type":"address[]"}],"name":"setAssetSources","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"fallbackOracle","type":"address"}],"name":"setFallbackOracle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    value_usd = contract.functions.getAssetPrice(reserve_address).call()
    decimals = get_reserve_decimals(reserve_address)
    usd_amount = (value_usd/1e18)*(token_amount/decimals)
    # print(usd_amount)
    return usd_amount

#makes our dataframe
def user_data(events, enum_name):
    
    df = pd.DataFrame()

    user_address_list = []
    tx_hash_list = []
    timestamp_list = []
    token_address_list = []
    token_volume_list = []
    token_usd_amount_list = []
    lend_borrow_type_list = []
    block_list = []

    user = ''

    start_time = time.time()
    i = 1
    for event in events:
        time.sleep(0.25)
        print('Batch of Events Processed: ', i, '/', len(events))
        i+=1
        # if enum_name == 'REPAY':
        #     user = 'user'
        # elif enum_name == 'COLLATERALISE':
        #     user = 'user'
        # else:
        #     user = 'user'

        # block = web3.eth.get_block(event['blockNumber'])
        # if block['timestamp'] >= 1701086400:
        if enum_name != 'COLLATERALISE':
            
            exists_list = already_part_of_df(event, enum_name)

            tx_hash = exists_list[0]
            wallet_address = exists_list[1]
            exists = exists_list[2]

            if exists == False and len(wallet_address) < 2:
                
                #adds wallet_address if it doesn't exist
                if len(wallet_address) < 2:
                    wallet_address = handle_weth_gateway(event, enum_name)
                

                block = web3.eth.get_block(event['blockNumber'])
                block_number = int(block['number'])
                block_list.append(block_number)

                user_address_list.append(wallet_address)
                tx_hash_list.append(tx_hash)
                timestamp_list.append(block['timestamp'])
                token_address = event['args']['reserve']
                token_address_list.append(token_address)
                token_volume = event['args']['amount']
                token_volume_list.append(token_volume)
                token_usd_amount_list.append(get_tx_usd_amount(token_address, token_volume))
                lend_borrow_type_list.append(enum_name)
            
            else:
                pass

        else:
            exists_list = already_part_of_df(event, enum_name)

            tx_hash = exists_list[0]
            wallet_address = exists_list[1]
            exists = exists_list[2]
            
            if exists == False and len(wallet_address) < 2:
                
                wallet_address = handle_weth_gateway(event, enum_name)

                block = web3.eth.get_block(event['blockNumber'])
                block_list.append(block)

                user_address_list.append(wallet_address)
                tx_hash_list.append(tx_hash)
                timestamp_list.append(block['timestamp'])
                token_address_list.append(event['args']['reserve'])
                token_volume_list.append(0)
                token_usd_amount_list.append(0)
                lend_borrow_type_list.append(enum_name)
            
            else:
                pass

    df['wallet_address'] = user_address_list
    df['txHash'] = tx_hash_list
    df['timestamp'] = timestamp_list
    df['tokenAddress'] = token_address_list
    df['tokenVolume'] = token_volume_list
    df['tokenUSDAmount'] = token_usd_amount_list
    df['blockNumber'] = block_list
    df['lendBorrowType'] = lend_borrow_type_list

    # print('User Data Event Looping done in: ', time.time() - start_time)
    return df

# # runs all our looks
# # updates our csv
def find_all_transactions():
    # # aZen
    # contract_address = '0xEB329420Fae03176EC5877c34E2c38580D85E069' 
    # # # vZen
    # # contract_address = '0xBE8afE7E442fFfFE576B979D490c5ADb7823C3c6'
    reserve_df = get_reserve_data()

    # reserve_address_list = reserve_df['reserve_address'].tolist()

    a_token_list = ['0x245B368d5a969179Df711774e7BdC5eC670e92EF', '0x5C4866349ff0Bf1e7C4b7f6d8bB2dBcbe76f8895', '0xa0f8323A84AdC89346eD3F7c5dcddf799916b51E', '0xB36535765A7421B397Cfd9fEc03cF96aA99C8D08', '0xdc66aC2336742E387b766B4c264c993ee6a3EF28']
    v_token_list = ['0xd4c3692B753302Ef0Ef1d50dd7928D60ef00B9ff', '0x157903B7c6D759c9D3c65A675a15aA0723eea95B', '0x393a64Fc561D6c8f5D8D8c427005cAB66DfeCA9D', '0xd8A40a27dD36565cC2B17C8B937eE50B69209E22', '0x9576c6FDd82474177781330Fc47C38D89936E7c8']

    reserve_address_list = ['0x245B368d5a969179Df711774e7BdC5eC670e92EF', '0x5C4866349ff0Bf1e7C4b7f6d8bB2dBcbe76f8895', '0xa0f8323A84AdC89346eD3F7c5dcddf799916b51E', '0xB36535765A7421B397Cfd9fEc03cF96aA99C8D08', '0xdc66aC2336742E387b766B4c264c993ee6a3EF28',
                    '0xd4c3692B753302Ef0Ef1d50dd7928D60ef00B9ff', '0x157903B7c6D759c9D3c65A675a15aA0723eea95B', '0x393a64Fc561D6c8f5D8D8c427005cAB66DfeCA9D', '0xd8A40a27dD36565cC2B17C8B937eE50B69209E22', '0x9576c6FDd82474177781330Fc47C38D89936E7c8']

    contract = get_contract()

    latest_block = web3.eth.get_block('latest')
    latest_block = int(latest_block['number'])

    event_df = pd.read_csv('all_events.csv')
    
    try:
        from_block = int(max(event_df['blockNumber']))
    except:
        from_block = FROM_BLOCK

    # from_block = FROM_BLOCK
    
    # from_block = 2869000

    # to_block = from_block + 955
    to_block = from_block + 955

    while to_block < latest_block:

        print('Current Event Block vs Latest Event Block to Check: ', from_block, '/', latest_block)

        deposit_events = get_deposit_events(contract, from_block, to_block)
        withdraw_events = get_withdraw_events(contract, from_block, to_block)
        borrow_events = get_borrow_events(contract, from_block, to_block)
        repay_events = get_repay_events(contract, from_block, to_block)

        if len(deposit_events) > 0:
            deposit_df = user_data(deposit_events, 'DEPOSIT')
            make_user_data_csv(deposit_df)

        if len(withdraw_events) > 0:
            withdraw_df = user_data(withdraw_events, 'WITHDRAW')
            make_user_data_csv(withdraw_df)

        if len(borrow_events) > 0:
            borrow_df = user_data(borrow_events, 'BORROW')
            make_user_data_csv(borrow_df)
            
        if len(repay_events) > 0:
            repay_df = user_data(repay_events, 'REPAY')
            make_user_data_csv(repay_df)

        from_block += 955
        to_block += 955

        # print(deposit_events)

        time.sleep(2.5)

        if from_block >= latest_block:
            from_block = latest_block - 1
        
        if to_block >= latest_block:
            to_block = latest_block
    
    return deposit_df

# Gets transactions of all blocks within a specified range and returns a df with info from blocks that include our contract
def get_all_gateway_transactions():

    weth_gateway_address = "0x0fdbD7BAB654B5444c96FCc4956B8DF9CcC508bE"

    # from_block = get_last_block_tracked()

    from_block = 946990

    print('Last Block Number: ', from_block)
    # from_block = 940460

    tx_hash_list = []
    value_list = []
    user_address_list = []
    block_number_list = []

    i = 0
    blocks_to_cover = LATEST_BLOCK - from_block
    
    last_block_number = 0
    # adds our values to our above lists
    for block_number in range(from_block, LATEST_BLOCK + 1):
        block = web3.eth.get_block(block_number)
        tx_hashes = block.transactions

        print(i, '/', blocks_to_cover)
        i += 1

        for tx_hash in tx_hashes:
            transaction = web3.eth.get_transaction(tx_hash)
            # print(transaction)
            # print('')
            if transaction['to'] == weth_gateway_address:
               # print(transaction)
                user_address_list.append(transaction['from'])
                tx_hash_list.append(transaction['hash'].hex())
                value_list.append(transaction['value'])
                block_number_list.append(transaction['blockNumber'])
        
        last_block_number = int(block_number)
                # print('found')

    print('Last Block Number: ', last_block_number)


    # handles blank dataframes
    if len(user_address_list) < 1:
        df = pd.read_csv('all_users.csv')
        df['last_block_number'] = last_block_number

    else:
        df = pd.DataFrame()
        df['wallet_address'] = user_address_list
        df['tx_hash'] = tx_hash_list
        df['number_of_tokens'] = value_list
        df['block_number'] = block_number_list
        df['last_block_number'] = last_block_number

    make_user_data_csv(df)

# # makes deposits and borrows positive numbers
# # makes withdrawals and repays as negative numbers
def prep_balance_df():

    df_list = []

    df = pd.read_csv('all_events.csv')

    deposit_df = df.loc[df['lendBorrowType'] == 'DEPOSIT']

    withdraw_df = df.loc[df['lendBorrowType'] == 'WITHDRAW']
    withdraw_df['tokenUSDAmount'] *= -1

    borrow_df = df.loc[df['lendBorrowType'] == 'BORROW']

    repay_df = df.loc[df['lendBorrowType'] == 'REPAY']
    repay_df['tokenUSDAmount'] *= -1

    df_list = [deposit_df, withdraw_df, borrow_df, repay_df]

    df = pd.concat(df_list)

    df['blockNumber'] = df['blockNumber'].astype(int)

    # df['user'] = df['wallet_address']
    # df['pool'] = '0x6997BA833148cA964ab51E4dF889b4b2a4Fc0B0d'
    # df['position'] = 0
    # df['lpvalue'] = 0

    # print(df)
    return df

# calculates the rolling balances of lps
def find_rolling_lp_balance(df):

    df['user'] = df['wallet_address']
    df['pool'] = '0x6997BA833148cA964ab51E4dF889b4b2a4Fc0B0d'
    df['position'] = 0
    df['lpvalue'] = 0
    df['block'] = df['blockNumber']

    df = df.sort_values(by=['blockNumber'])

    calculated_df = df[['user', 'pool', 'block', 'position', 'lpvalue']]

    calculated_df['lpvalue'] = df.groupby('user')['tokenUSDAmount'].transform(pd.Series.cumsum)

    calculated_df = calculated_df.sort_values(by=['block'], ascending=False)
    calculated_df = calculated_df.reset_index(drop=True)

    print(calculated_df)

    calculated_df.to_csv('outputData.csv', index=False)

    calculated_df.to_json('outputData.json', orient='records')
    return df

find_all_transactions()

df = prep_balance_df()
find_rolling_lp_balance(df)