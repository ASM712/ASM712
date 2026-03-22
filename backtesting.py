from data_fetcher import DataFetcher
from rsi_calculator import RSICalculator
import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.portfolio = {}
        self.positions = {}
        self.trades = []
        self.daily_values = [initial_balance]
        self.data_fetcher = DataFetcher()
        self.rsi_calculator = RSICalculator()
    
    def backtest(self, ticker, days=60):
        """Backtest trading strategy on historical data"""
        prices = self.data_fetcher.get_historical_data(ticker, days=days)
        
        if prices is None:
            return None
        
        for i in range(self.rsi_calculator.period, len(prices)):
            historical_prices = prices[:i+1]
            current_price = prices[i]
            
            analysis = self.rsi_calculator.analyze(historical_prices)
            signal = analysis['signal']
            
            # Execute trade
            if signal == "BUY" and self.balance > current_price:
                quantity = int(self.balance * 0.1 / current_price)
                if quantity > 0:
                    self.balance -= quantity * current_price
                    self.portfolio[ticker] = quantity
                    self.positions[ticker] = current_price
                    self.trades.append({
                        'action': 'BUY',
                        'price': current_price,
                        'quantity': quantity
                    })
            
            elif signal == "SELL" and self.portfolio.get(ticker, 0) > 0:
                quantity = self.portfolio[ticker]
                self.balance += quantity * current_price
                profit = quantity * (current_price - self.positions[ticker])
                self.trades.append({
                    'action': 'SELL',
                    'price': current_price,
                    'quantity': quantity,
                    'profit': profit
                })
                del self.portfolio[ticker]
            
            # Track daily value
            portfolio_value = self.balance
            for tick, qty in self.portfolio.items():
                portfolio_value += qty * current_price
            self.daily_values.append(portfolio_value)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self):
        """Calculate backtest performance metrics"""
        final_value = self.daily_values[-1]
        total_return = final_value - self.initial_balance
        roi = (total_return / self.initial_balance) * 100
        
        # Calculate win rate
        wins = sum(1 for trade in self.trades if trade.get('profit', 0) > 0)
        total_trades = len([t for t in self.trades if t['action'] == 'SELL'])
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        # Calculate max drawdown
        cumulative = np.array(self.daily_values)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = np.min(drawdown) * 100
        
        return {
            'initial_balance': self.initial_balance,
            'final_balance': final_value,
            'total_return': total_return,
            'roi': roi,
            'total_trades': total_trades,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown
        }

def main():
    print("=" * 60)
    print("AUTO TRADING BOT - BACKTESTING")
    print("=" * 60)
    
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    for ticker in tickers:
        print(f"\nBacktesting {ticker}...")
        engine = BacktestEngine(initial_balance=10000)
        metrics = engine.backtest(ticker, days=90)
        
        if metrics:
            print(f"\n{ticker} Results:")
            print(f"  Initial Balance: ${metrics['initial_balance']:.2f}")
            print(f"  Final Balance: ${metrics['final_balance']:.2f}")
            print(f"  Total Return: ${metrics['total_return']:.2f}")
            print(f"  ROI: {metrics['roi']:.2f}%")
            print(f"  Total Trades: {metrics['total_trades']}")
            print(f"  Win Rate: {metrics['win_rate']:.2f}%")
            print(f"  Max Drawdown: {metrics['max_drawdown']:.2f}%")

if __name__ == "__main__":
    main()