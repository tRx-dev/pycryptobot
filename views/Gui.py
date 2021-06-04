from datetime import datetime
from rich.console import Console
from rich.table import Table, Column
from rich import print
from rich.layout import Layout
from rich.panel import Panel

# Init rich console
console = Console()

class Gui():
    def __init__(self) -> None:
        pass

    # Create  header
    def create_header(version) -> Panel:
        """Display header"""

        grid = Table.grid(expand=True)
        grid.add_column(justify='left')
        grid.add_column(justify='right')
        grid.add_row(
            '[b]PyCryptoBot[b]',
            version
        )
        return Panel(grid)

    # Create  footer
    def create_footer(exchange, time) -> Panel:
        """Display header"""

        grid = Table.grid(expand=True)
        grid.add_column(justify='left')
        grid.add_column(justify='right')
        grid.add_row(
            '[b]Current Exchange:[/b] ' + exchange,
            time
        )
        return Panel(grid)    

    # Create small info panel
    def create_small_info_panel(value, title, color) -> Panel:
        """Display small info panel"""
        
        grid = Table.grid(expand=True)
        grid.add_column(justify='center', ratio = 1)
        grid.add_row(
            '[b]' + value + ' [/b]'
        )
        return Panel(grid, border_style=color, title='[b]' + title + '[/b]')

    # Create info panel
    def create_info_panel(high, low, open) -> Panel:
        '''Create Info panel'''

        crypto_24h_panel = Table.grid(expand=True)
        crypto_24h_panel.add_column('High', justify='center')
        crypto_24h_panel.add_column('Low', justify='center')
        crypto_24h_panel.add_column('Value', justify='center')
        crypto_24h_panel.add_row('[b]High[/b]', '[b]Low[/b]', '[b]Open[/b]')
        crypto_24h_panel.add_row('[green]' + str(high) + ' EUR', '[red]' + str(low) + ' EUR', '[cyan]' + str(open) + ' EUR')

        highlow_table = Table.grid(expand=True)
        highlow_table.add_row(
            Panel(crypto_24h_panel, title='24H High/Low'),
        )

        return Panel(highlow_table, title='[b]Information[/b]')    

    # Create settings panel
    def create_settings_panel(settings, title, color) -> Panel:
        '''Create Settings panel'''

        settings_panel = Table.grid(expand=True)
        settings_panel.add_column('Settings', justify='center')
        settings_panel.add_row('\n')
        settings_panel.add_row('[b]Sell Upper: [/b]' + str(settings[0]))
        settings_panel.add_row('[b]Sell Lower: [/b]' + str(settings[1]))
        settings_panel.add_row('[b]Trailing Stop Loss: [/b]' + str(settings[2]))
        settings_panel.add_row('[b]Sell At Loss: [/b]' + str(settings[3]))
        settings_panel.add_row('[b]Sell At Resistance: [/b]' + str(settings[4]))
        settings_panel.add_row('[b]Trade Bull Only: [/b]' + str(not settings[5]))
        settings_panel.add_row('[b]Buy Near High: [/b]' + str(not settings[6]))
        settings_panel.add_row('[b]Use Buy MACD: [/b]' + str(not settings[7]))
        settings_panel.add_row('[b]Use Buy OBV: [/b]' + str(not settings[8]))
        settings_panel.add_row('[b]Use Buy Elder-Ray: [/b]' + str(not settings[9]))
        settings_panel.add_row('[b]Sell Fibonacci Low: [/b]' + str(not settings[10]))
        settings_panel.add_row('[b]Sell Lower Pcnt: [/b]' + str(not settings[11]))
        settings_panel.add_row('[b]Sell Upper Pcnt: [/b]' + str(not settings[11]))
        settings_panel.add_row('[b]Candlestick Reversal: [/b]' + str(not settings[12]))
        settings_panel.add_row('[b]Telegram: [/b]' + str(not settings[13]))
        settings_panel.add_row('[b]Log: [/b]' + str(not settings[14]))
        settings_panel.add_row('[b]Tracker: [/b]' + str(not settings[15]))
        settings_panel.add_row('[b]Auto restart Bot: [/b]' + str(settings[16]))
        settings_panel.add_row('[b]Max Buy Size: [/b]' + str(settings[17]))

        return Panel(settings_panel, border_style=color, title='[b]' + title + '[/b]')    

    # Create win loss panel        
    def create_buy_sell_panel(margin, profit, action, last_action, title, color) -> Panel:
        '''Display win or loss amount'''
        grid = Table.grid(expand=True)
        grid.add_column(justify='center')

        grid.add_row('\n[b]Last Action[/b]')
        if last_action == 'SELL':
            grid.add_row('[b]SELL[/b]', style='green')
        elif last_action == 'BUY':
            grid.add_row('[b]BUY[/b]', style='red')
        elif last_action == 'WAIT':
            grid.add_row('[b]WAIT[/b]', style='yellow')
        else:
            grid.add_row('[b]NONE[/b]', style='white')            

        grid.add_row('\n[b]Action[/b]')
        if action == 'SELL':
            grid.add_row('[b]SELL[/b]', style='green')
        elif action == 'BUY':
            grid.add_row('[b]BUY[/b]', style='red')
        elif action == 'WAIT':
            grid.add_row('[b]WAIT[/b]', style='yellow')
        else:
            grid.add_row('[b]NONE[/b]', style='white')

        grid.add_row('\n[b]Margin[/b]')
        grid.add_row(str(margin))

        grid.add_row('\n[b]Profit[/b]')
        grid.add_row(str(profit))

        return Panel(grid, border_style=color, title='[b]' + title + '[/b]')

    # Init dashboard
    def create_layout() -> Layout:
        '''Define the layout'''

        layout = Layout(name='root')

        layout.split(
            Layout(name='padding', size=1),
            Layout(name='header', size=3),
            Layout(name='main'),
            Layout(name='footer', size=3)
        )

        layout['main'].split_row(
            Layout(name='side'),
            Layout(name='body', ratio=3, minimum_size=60)
        )

        layout['body'].split(
            Layout(name='info'),
            Layout(name='buy_sell_status')
        )

        layout['side'].split(
            Layout(name='current_market', size=3),
            Layout(name='current_price', size=3),
            Layout(name='granularity', size=3),
            Layout(name='bull_bear', size=3),
            Layout(name='settings_info')
        )

        return layout

    def render_gui(layout):
        console.print(layout)