"""
Mini Trading Bot - Educational Paper Trading Simulation
This bot trades on historical data using a simple moving average crossover strategy.
NO REAL MONEY IS INVOLVED - This is for learning purposes only.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


class PaperTradingBot:
    """Simple trading bot that simulates trading on historical data"""
    
    def __init__(self, initial_capital=1000, symbol="BTC-USD", start_date=None, end_date=None):
        """
        Initialize the bot
        
        Args:
            initial_capital: Starting amount of money (default: $1000)
            symbol: Asset to trade (default: Bitcoin)
            start_date: Start date for historical data
            end_date: End date for historical data
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.portfolio_value = initial_capital
        self.symbol = symbol
        self.position = 0  # How much of the asset we own
        self.trades = []  # Record of all trades
        
        # Set default dates (last 1 year)
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)
            
        self.start_date = start_date
        self.end_date = end_date
        
        # Fetch historical data
        print(f"📊 Fetching {self.symbol} data from {start_date.date()} to {end_date.date()}...")
        self.data = yf.download(self.symbol, start=start_date, end=end_date, progress=False)
        
        if self.data.empty:
            raise ValueError(f"No data found for {symbol}")
        
        # Calculate moving averages
        self._calculate_indicators()
        
    def _calculate_indicators(self):
        """Calculate technical indicators (moving averages)"""
        # Short-term moving average (20 days)
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        # Long-term moving average (50 days)
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
    def _should_buy(self, index):
        """
        Determine if we should buy
        Strategy: Buy when short MA crosses above long MA (Golden Cross)
        """
        if index < 50:  # Need enough data for indicators
            return False
            
        # Check if we have a position already
        if self.position > 0:
            return False
            
        # Buy signal: SMA_20 crosses above SMA_50
        prev_sma20 = self.data['SMA_20'].iloc[index - 1]
        prev_sma50 = self.data['SMA_50'].iloc[index - 1]
        curr_sma20 = self.data['SMA_20'].iloc[index]
        curr_sma50 = self.data['SMA_50'].iloc[index]
        
        # Golden cross pattern
        if prev_sma20 <= prev_sma50 and curr_sma20 > curr_sma50:
            return True
        return False
    
    def _should_sell(self, index):
        """
        Determine if we should sell
        Strategy: Sell when short MA crosses below long MA (Death Cross)
        """
        if index < 50:
            return False
            
        # Only sell if we own the asset
        if self.position == 0:
            return False
            
        # Sell signal: SMA_20 crosses below SMA_50
        prev_sma20 = self.data['SMA_20'].iloc[index - 1]
        prev_sma50 = self.data['SMA_50'].iloc[index - 1]
        curr_sma20 = self.data['SMA_20'].iloc[index]
        curr_sma50 = self.data['SMA_50'].iloc[index]
        
        # Death cross pattern
        if prev_sma20 >= prev_sma50 and curr_sma20 < curr_sma50:
            return True
        return False
    
    def run(self):
        """Run the bot on historical data"""
        print(f"\n🤖 Starting bot with ${self.initial_capital} capital...\n")
        
        for index in range(len(self.data)):
            date = self.data.index[index].date()
            price = self.data['Close'].iloc[index]
            
            # Check buy signal
            if self._should_buy(index):
                amount_to_invest = self.cash * 0.95  # Invest 95% of cash
                self.position = amount_to_invest / price
                self.cash -= amount_to_invest
                
                trade = {
                    'date': date,
                    'type': 'BUY',
                    'price': price,
                    'amount': self.position,
                    'cost': amount_to_invest
                }
                self.trades.append(trade)
                print(f"✅ BUY  - {date} @ ${price:.2f} | Bought {self.position:.6f} {self.symbol}")
            
            # Check sell signal
            elif self._should_sell(index):
                proceeds = self.position * price
                profit_loss = proceeds - self.trades[-1]['cost']
                profit_loss_pct = (profit_loss / self.trades[-1]['cost']) * 100
                
                trade = {
                    'date': date,
                    'type': 'SELL',
                    'price': price,
                    'amount': self.position,
                    'proceeds': proceeds,
                    'profit_loss': profit_loss,
                    'profit_loss_pct': profit_loss_pct
                }
                self.trades.append(trade)
                
                print(f"🔴 SELL - {date} @ ${price:.2f} | Profit/Loss: ${profit_loss:.2f} ({profit_loss_pct:.2f}%)")
                
                self.cash += proceeds
                self.position = 0
            
            # Calculate current portfolio value
            if self.position > 0:
                self.portfolio_value = self.cash + (self.position * price)
            else:
                self.portfolio_value = self.cash
        
        # Sell any remaining position at the end
        if self.position > 0:
            final_price = self.data['Close'].iloc[-1]
            final_date = self.data.index[-1].date()
            proceeds = self.position * final_price
            self.cash += proceeds
            self.position = 0
            print(f"\n🔴 SELL (Final) - {final_date} @ ${final_price:.2f}")
        
        self.portfolio_value = self.cash
    
    def get_results(self):
        """Calculate and return bot performance metrics"""
        final_value = self.portfolio_value
        total_return = final_value - self.initial_capital
        return_percentage = (total_return / self.initial_capital) * 100
        
        # Calculate number of trades
        buy_count = sum(1 for t in self.trades if t['type'] == 'BUY')
        sell_count = sum(1 for t in self.trades if t['type'] == 'SELL')
        
        # Calculate winning trades
        winning_trades = sum(1 for t in self.trades if t['type'] == 'SELL' and t['profit_loss'] > 0)
        losing_trades = sum(1 for t in self.trades if t['type'] == 'SELL' and t['profit_loss'] < 0)
        
        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'return_percentage': return_percentage,
            'total_trades': buy_count,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': (winning_trades / sell_count * 100) if sell_count > 0 else 0,
        }
        
        return results
    
    def print_summary(self):
        """Print bot performance summary"""
        results = self.get_results()
        
        print("\n" + "="*60)
        print("📈 TRADING BOT SUMMARY")
        print("="*60)
        print(f"Symbol: {self.symbol}")
        print(f"Period: {self.start_date.date()} to {self.end_date.date()}")
        print(f"\nInitial Capital: ${results['initial_capital']:,.2f}")
        print(f"Final Value: ${results['final_value']:,.2f}")
        print(f"Total Return: ${results['total_return']:,.2f} ({results['return_percentage']:.2f}%)")
        print(f"\nTotal Trades: {results['total_trades']}")
        print(f"Winning Trades: {results['winning_trades']}")
        print(f"Losing Trades: {results['losing_trades']}")
        print(f"Win Rate: {results['win_rate']:.2f}%")
        print("="*60 + "\n")


def main():
    """Main function - Run the bot"""
    # Create bot instance
    bot = PaperTradingBot(
        initial_capital=1000,
        symbol="BTC-USD",  # Bitcoin in USD
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2024, 8, 27)
    )
    
    # Run the bot on historical data
    bot.run()
    
    # Print results
    bot.print_summary()


if __name__ == "__main__":
    main()
