:
  # Core dimensions for the  matrix
     
       "ORIGINAL TRADE (OG)  signal_types": 
	   
			POINT IN TIME OR ECONOMIC EVENT OR VOLITILITY EVENT
			
                "ECO_HIGH": { "High impact economic events", 
				
                "ECO_MED": { "Medium impact economic events", 
				
                "ANTICIPATION_1HR": {: "Pre-event positioning trades_1HOURS BEFORE ECONOMIC Event", 
                
				"ANTICIPATION_4HR": {"Pre-event positioning trades_4HOURS BEFORE ECONOMIC Event"
				
				"ANTICIPATION_8HR": { "Pre-event positioning trades_8HOURS BEFORE ECONOMIC Event"
				
				"ANTICIPATION_12HR": { "Pre-event positioning trades_12HOURS BEFORE ECONOMIC Event", 
				
				"EQUITY_OPEN_ASIA": { "Equity market open In Asia "
				
				"EQUITY_OPEN_EUROPE": {"Equity market open in Europe "
				
				"EQUITY_OPEN_USA": { "Equity market open in the USA "
				
				
				
			Price Derived	
				
				"ALL Indicators":( Pure technical analysis signal derived from price"
				
	All indicators is just a placeholder for the actual indicator name that the user has yet to the side on 			
		 
		 
		 
          PROXIMITY TO PAST AND FUTURE VOLITILITY EVENT WITHIN A 24 HOUR WINDOW
            
			"PROXIMITY TO FUTURE VOLITILITY EVENT": { How many minutes Until the next  High volatility event FOR The currency associated with the economic Within a 24 hour window. Based on that calculation what bucket does it fall in :
			- **Immediate **:(0-5 minutes)
			- **SHORT**:(5-60 minutes)
			- **MEDIUM**:(61-240 minutes)
			- **LONG**:(241-480 minutes)
			- **EXTENDED**:(481-720 minutes)
			- **TOMMOROW**:(721-1440 minutes)
			- **NONE**
			
			"PROXIMITY TO PAST VOLITILITY EVENT": {How many minutes have elapsed since the last High volatility event FOR The currency associated with the economic Within a 24 hour window 
			
			- **Immediate **:(0-5 minutes)
			- **SHORT**:(5-60 minutes)
			- **MEDIUM**:(61-240 minutes)
			- **LONG**:(241-480 minutes)
			- **EXTENDED**:(481-720 minutes)
			- **YESTERDAY**:(721-1440 minutes)
			- **NONE**
			
			
			
	the combination For signals created by volatility events is based on the type of volatility event And what category it falls into for PAST and future high volatility events 		
			
	the combination For signals created by price derived indicators  is based on the indicator And what category it falls into for PAST and future high volatility events  		
	These are the combinations only for the original or first trade in a possible trade chain re entry trades have different combinations 
	
*******End of original trade combination variables *******	
	 

	There's a maximum of TWO  reentry Signals  for every original signal. The combination for reentry trades consist of the type of original trade :
	
ECO_HIGH
ECO_MED
ANTICIPATION_1HR
ANTICIPATION_4HR
ANTICIPATION_8HR
ANTICIPATION_12HR
EQUITY_OPEN_ASIA
EQUITY_OPEN_EUROPE
EQUITY_OPEN_USA
ALL Indicators
	
	What bucket the original trade falls into is a combination variable for reentry trades. For a reentry trade to occur an original trade must have closed the result of that closed original trade determines what bucket it falls in :
	
	Every trade gets classified into one of six buckets based on where it closed:

1. **BUCKET 1**: Hit stop loss (maximum loss)
2. **BUCKET 2**: Partial loss (lost money but not the maximum)
3. **BUCKET 3**: Breakeven (no profit, no loss)
4. **BUCKET 4**: Partial profit (made money but didn't hit target)
5. **BUCKET 5**: Hit take profit target (perfect execution)
6. **BUCKET 6**: Exceeded target (made more than expected)
			
The time elapsed from Trade open the trade close is a combination variable for re-entry trades 

### Time Categories (How Long It Lasted)
- **FLASH**: (0-5 minutes)
- **QUICK**: (6-15 minutes) 
- **MEDIUM**: (16-45 minutes)
- **LONG**: (46-90 minutes)
- **Extended **: (>90 minutes)




			
			
			The relative proximity to past and future volatility events is a combination variable for reentry trades :
			
			PROXIMITY TO PAST AND FUTURE VOLITILITY EVENT WITHIN A 24 HOUR WINDOW
            
			"PROXIMITY TO FUTURE VOLITILITY EVENT": { How many minutes Until the next  High volatility event FOR The currency associated with the economic Within a 24 hour window. Based on that calculation what bucket does it fall in :
			
			- **Immediate **:(0-5 minutes)
			- **SHORT**:(5-60 minutes)
			- **LONG**:(241-480 minutes)
			- **EXTENDED**:(481-720 minutes)
			- **TOMMOROW**:(721-1440 minutes)
			- **NONE**
			
			"PROXIMITY TO PAST VOLITILITY EVENT": {How many minutes have elapsed since the last High volatility event FOR The currency associated with the economic Within a 24 hour window 
			
			- **Immediate **:(0-5 minutes)
			- **SHORT**:(5-60 minutes)
			- **LONG**:(241-480 minutes)
			- **EXTENDED**:(481-720 minutes)
			- **YESTERDAY**:(721-1440 minutes)
			- **NONE**
			
			
	Regardless of original or re-entry or I  price Derived  or volatility event Signal,  a future high volatility event that falls within the Immediate  range Automatically Creates a no trade situation 		
			
	*******End of Reentry   trade combination variables *******		
			
	There is no Three-Tier Personality System Trade parameters for re-entry trades are Are based on the reentry combination variables and the And the parameter set that is called on by the unique combination of reentry variables  
	
	
	
	
	
	I think these parameters are more global or The same for all trades and not trade execution parameters that are specific to an individual parameter set and trade  

global_risk_percent - Base percentage of account risked per trade (0.1% to 3.5%)
risk_adjustment_multiplier - Multiplier to adjust risk up/down from global setting (0.1 to 1.17)
max_risk_cap_percent - Hard limit at 3.5% (system enforced, non-configurable
max_positions_total - Maximum open positions across all pairs
max_positions_per_pair - Maximum positions per currency pair
daily_loss_limit - Maximum daily loss in account currency
daily_profit_target - Daily profit target (optional stop)
max_daily_trades - Maximum number of trades per day
weekly_loss_limit - Maximum weekly loss limit
max_chain_loss_percent - Maximum loss per reentry chain (standard: 8%)
7. CHAIN MANAGEMENT PARAMETERS
Generation & Chain Controls:

max_reentry_generations - Maximum reentries allowed (default: 3)
stop_after_consecutive_losses - Stop after X losses in row
stop_after_drawdown_percent - Stop if chain drawdown exceeds X%
max_chain_duration_hours - Force stop after X hours
Emergency Stop Parameters:

emergency_stop_loss_percent - Emergency stop at X% account loss
correlation_emergency_stop - Stop if correlation exceeds X
drawdown_emergency_stop - Stop if drawdown exceeds X%
consecutive_loss_emergency - Emergency stop after X losses
max_trades_per_hour - Limit trades per hour
max_trades_per_minute - Limit trades per minute
cool_down_after_loss_streak - Cool down after X losses
cool_down_duration_minutes - Duration of cool down
force_break_after_hours - Force break after X hours trading
forced_break_duration_minutes - Duration of forced break
Parameter Set Information:

parameter_set_id - Unique identifier (required)
name - Human-readable name (required)
description - Detailed description
version - Version number
active - Whether set is active for trading
created_date - Creation timestamp
updated_date - Last modification timestamp
created_by - Creator identifier
backtest_verified - Has been backtested
live_verified - Has been live tested

12. READ-ONLY CALCULATED PARAMETERS
These are calculated by the system but visible to users:
Position Sizing Results:

calculated_lot_size - Actual lot size used
actual_risk_percent - Final risk percentage
risk_amount_dollars - Dollar amount being risked

Performance Tracking:

total_executions - Times parameter set was used
successful_executions - Number of profitable trades
total_pnl - Total profit/loss generated
last_execution - Last time used
avg_execution_time_ms - Average execution time
**********End global parameters ************

TRADE EXECUTION PARAMETERS, I think these are the parameters should be a part of the parameter sets that are called by the unique combination of Original or re entry variables. These variables can be combined and multiple ways to create parameter sets These parameter sets are attached to a unique  combination Of variables for either original or reentry trades These parameter sets are what Python sends to MQL for to execute based on the parameter sets After that execution occurs and that trade closes the results of that trade are sent back to Python from MQL4 How those results fall into re entry variables either causes no or calls another possibly the exact same set of parameters to be sent to MQL4 for execution  




Entry Order Types & Settings:

entry_order_type - "MARKET", "PENDING", or "STRADDLE"
market_slippage_pips - Maximum acceptable slippage for market orders
market_retry_attempts - Number of retry attempts on market order failure
market_retry_delay_ms - Delay between retry attempts

Pending Order Configuration:

pending_order_type - BUY_STOP, SELL_STOP, BUY_LIMIT, SELL_LIMIT
pending_distance_pips - Distance from current price
pending_expiration_minutes - Order expiration time
pending_price_method - "FIXED", "ATR", "SUPPORT_RESISTANCE"
atr_distance_multiplier - ATR multiplier for distance calculation

Straddle Order Configuration:

straddle_distance_pips - Distance for both legs
straddle_buy_order_type - Order type for buy leg
straddle_sell_order_type - Order type for sell leg
straddle_expiration_minutes - Expiration for both legs
straddle_auto_cancel_opposite - Auto-cancel unfilled leg
straddle_cancel_delay_seconds - Delay before canceling
straddle_asymmetric - Allow different distances
straddle_buy_distance_pips - Buy leg specific distance
straddle_sell_distance_pips - Sell leg specific distance
straddle_equal_lot_sizes - Equal sizes for both legs
straddle_buy_lot_ratio - Buy leg size ratio
straddle_sell_lot_ratio - Sell leg size ratio

4. STOP LOSS & TAKE PROFIT PARAMETERS
Stop Loss Configuration:

stop_loss_pips - Fixed SL distance (required)
stop_loss_method - "FIXED", "ATR_MULTIPLE", "PERCENT"
atr_stop_multiplier - ATR multiplier for dynamic SL
max_stop_loss_pips - Maximum allowed SL distance

Take Profit Configuration:

take_profit_pips - Fixed TP distance (required)
take_profit_method - "FIXED", "RR_RATIO", "ATR_MULTIPLE"
risk_reward_ratio - Risk to reward ratio
partial_tp_levels - Percentage levels for partial closes

Trailing Stop Settings:

use_trailing_stop - Enable/disable trailing
trailing_stop_pips - Trailing distance
trailing_step_pips - Step size for updates
trailing_start_pips - Profit level to start trailing

5. REENTRY EXECUTION PARAMETERS
Size & Position Adjustments:

size_multiplier - Base size multiplier for reentries
size_adjustment_method - "MULTIPLY", "ADD_LOTS", "FIBONACCI"
fibonacci_sequence - Sequence for Fibonacci sizing
max_reentry_size_multiplier - Cap on size increases
progressive_sizing - Increase/decrease size each generation
progressive_multiplier - Progressive size adjustment factor
size_cap_per_generation - Size caps by generation level

Timing & Delays:

base_delay_seconds - Base delay before reentry
progressive_delay - Increase delay each generation
delay_multiplier - Delay multiplication factor
max_delay_minutes - Maximum delay allowed
random_delay_range - Random variation in delay
entry_offset_pips - Price offset for reentry
use_limit_orders_for_reentry - Use limits vs market for reentries
limit_order_offset_pips - Limit order distance
8. ENTRY CONDITIONS & FILTERS
Market Entry Requirements:

confidence_threshold - Minimum confidence to enter
max_spread_pips - Maximum spread allowed
entry_delay_seconds - Delay before entering after signal
slippage_tolerance_pips - Maximum acceptable slippage