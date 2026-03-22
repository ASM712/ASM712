class TradingEngine:
    def __init__(self):
        self.portfolio = {}  # Dictionary to hold the assets and their quantities
        self.trades = []  # List to track trades

    def execute_trade(self, action, asset, quantity, price):
        if action not in ['BUY', 'SELL']:
            raise ValueError('Action must be BUY or SELL')
        if action == 'BUY':
            self.portfolio[asset] = self.portfolio.get(asset, 0) + quantity
        elif action == 'SELL':
            if self.portfolio.get(asset, 0) < quantity:
                raise ValueError('Not enough asset to sell')
            self.portfolio[asset] -= quantity
        self.trades.append({'action': action, 'asset': asset, 'quantity': quantity, 'price': price})

    def calculate_portfolio_value(self, current_prices):
        total_value = 0
        for asset, quantity in self.portfolio.items():
            total_value += current_prices.get(asset, 0) * quantity
        return total_value

    def track_trades(self):
        return self.trades

    def manage_portfolio(self, rsi_signals):
        for asset, signal in rsi_signals.items():
            if signal == 'BUY':
                # Example trade execution logic - adjust as necessary
                self.execute_trade('BUY', asset, 1, current_prices[asset])
            elif signal == 'SELL':
                self.execute_trade('SELL', asset, 1, current_prices[asset])
