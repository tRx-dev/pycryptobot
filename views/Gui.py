import threading
from threading import Timer
import time
import sched
from datetime import datetime
from numpy import exp
from rich import progress
from rich.console import Console
from rich.table import Row, Table, Column
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn

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
        return Panel(grid, border_style='bright_white')

    # Create  footer
    def create_footer(exchange, time_left, time_now) -> Panel:
        """Display header"""

        grid = Table.grid(expand=True)
        grid.add_column(justify='left')
        grid.add_column(justify='center')
        grid.add_column(justify='right')

        time_left_progress = Progress(
            TextColumn('{task.description}', justify='right'),
            BarColumn(),
            TextColumn(str(time_left.total_seconds() * 100).split(".")[0] + ' sec')
        )

        time_left_progress.add_task('[b]Update in:[/b] ', total=0.6)

        time_left_progress.advance(0, 0.6 - time_left.total_seconds())

        grid.add_row(
            '[b]Current Exchange:[/b] ' + exchange,
            time_left_progress,
            time_now
        )
        return Panel(grid, border_style='bright_white')    

    # Create small info panel
    def create_small_info_panel(value, title, color) -> Panel:
        """Display small info panel"""
        
        grid = Table.grid(expand=True)
        grid.add_column(justify='center', ratio = 1)
        if value == '':
            value = 'None'

        grid.add_row(
            '[b]' + value + ' [/b]'
        )
        return Panel(grid, border_style=color, title='[b]' + title + '[/b]')

    # Create info panel
    def create_info_panel(values) -> Panel:
        '''Create Info panel'''

        info_panel_close = Table.grid(expand=True)
        info_panel_close.add_column(justify='center')
        info_panel_close.add_row('[b]Close[/b]')
        info_panel_close.add_row(values[0])

        info_panel_ema = Table.grid(expand=True)
        info_panel_ema.add_column(justify='center')
        info_panel_ema.add_column(justify='center')
        info_panel_ema.add_row('[b]EMA12[/b]', '[b]EMA26[/b]')
        info_panel_ema.add_row(values[1], values[2])
        
        info_panel_sma = Table.grid(expand=True)
        info_panel_sma.add_column(justify='center')
        info_panel_sma.add_column(justify='center')
        info_panel_sma.add_row('[b]SMA20[/b]', '[b]SMA200[/b]')
        info_panel_sma.add_row(values[3], values[4])

        info_panel_above_below = Table.grid(expand=True)
        info_panel_above_below.add_column(justify='center')
        info_panel_above_below.add_column(justify='center')
        info_panel_above_below.add_column(justify='center')
        info_panel_above_below.add_column(justify='center')
        info_panel_above_below.add_row('[b]Crossing Above[/b]', '[b]Currently Above[/b]', '[b]Crossing Below[/b]', '[b]Currently Below[/b]')
        info_panel_above_below.add_row(Gui.true_false_color(values[5]), Gui.true_false_color(values[6]), Gui.true_false_color(values[7]), Gui.true_false_color(values[8]))

        info_panel_condition_ema = Table.grid(expand=True)
        info_panel_condition_ema.add_column(justify='center')
        info_panel_condition_ema.add_row(values[9])

        ema_sma_table = Table.grid(expand=True)
        ema_sma_table.add_row(
            Panel(info_panel_close, title='[b]Close', border_style='bright_cyan'),
            Panel(info_panel_ema, title='[b]EMA', border_style='bright_cyan'),
            Panel(info_panel_sma, title='[b]SMA', border_style='bright_cyan'),
        )

        info_panel_macd = Table.grid(expand=True)
        info_panel_macd.add_column(justify='center')
        info_panel_macd.add_column(justify='center')
        info_panel_macd.add_column(justify='center')
        info_panel_macd.add_column(justify='center')
        info_panel_macd.add_row('[b]MACD[/b]', '[b]Signal[/b]', '[b]Currently Above[/b]', '[b]Currently Below[/b]')
        info_panel_macd.add_row(values[10], values[11], Gui.true_false_color(values[12]), Gui.true_false_color(values[13]))

        info_panel_condition_macd = Table.grid(expand=True)
        info_panel_condition_macd.add_column(justify='center')
        info_panel_condition_macd.add_row(values[14])

        info_table = Table.grid(expand=True)
        info_table.add_row(ema_sma_table)
        info_table.add_row(Panel(info_panel_above_below, title='[b]EMA Above/Below[/b]', border_style='bright_cyan'))
        info_table.add_row(Panel(info_panel_condition_ema, title='[b]Condition EMA[/b]', border_style='bright_cyan'))
        info_table.add_row('\n\n')
        info_table.add_row(Panel(info_panel_macd, title='[b]MACD/Signal[/b]', border_style='bright_cyan'))
        info_table.add_row(Panel(info_panel_condition_macd, title='[b]Condition MACD/Signal[/b]', border_style='bright_cyan'))
                    
        return Panel(info_table, title='[b]Information[/b]')    

    def true_false_color(string) -> str:
        '''Check if option is true or false'''

        if string == 'True':
            return '[b][green]True[/green]'
        elif string == 'False':
            return '[b][red]False[/red]'
        else:
            return string

    # Create settings panel
    def create_settings_panel(settings, title, color) -> Panel:
        '''Create Settings panel'''

        settings_panel = Table.grid(expand=True)
        settings_panel.add_column('Settings', justify='center')
        settings_panel.add_row('\n')
        settings_panel.add_row('[b]Sell Upper: [/b]' + Gui.true_false_color(str(settings[0])))
        settings_panel.add_row('[b]Sell Lower: [/b]' + Gui.true_false_color(str(settings[1])))
        settings_panel.add_row('[b]Trailing Stop Loss: [/b]' + Gui.true_false_color(str(settings[2])))
        settings_panel.add_row('[b]Sell At Loss: [/b]' + Gui.true_false_color(str(settings[3])))
        settings_panel.add_row('[b]Sell At Resistance: [/b]' + Gui.true_false_color(str(settings[4])))
        settings_panel.add_row('[b]Trade Bull Only: [/b]' + Gui.true_false_color(str(not settings[5])))
        settings_panel.add_row('[b]Buy Near High: [/b]' + Gui.true_false_color(str(not settings[6])))
        settings_panel.add_row('[b]Use Buy MACD: [/b]' + Gui.true_false_color(str(not settings[7])))
        settings_panel.add_row('[b]Use Buy OBV: [/b]' + Gui.true_false_color(str(not settings[8])))
        settings_panel.add_row('[b]Use Buy Elder-Ray: [/b]' + Gui.true_false_color(str(not settings[9])))
        settings_panel.add_row('[b]Sell Fibonacci Low: [/b]' + Gui.true_false_color(str(not settings[10])))
        settings_panel.add_row('[b]Sell Lower Pcnt: [/b]' + Gui.true_false_color(str(not settings[11])))
        settings_panel.add_row('[b]Sell Upper Pcnt: [/b]' + Gui.true_false_color(str(not settings[11])))
        settings_panel.add_row('[b]Candlestick Reversal: [/b]' + Gui.true_false_color(str(not settings[12])))
        settings_panel.add_row('[b]Telegram: [/b]' + Gui.true_false_color(str(not settings[13])))
        settings_panel.add_row('[b]Log: [/b]' + Gui.true_false_color(str(not settings[14])))
        settings_panel.add_row('[b]Tracker: [/b]' + Gui.true_false_color(str(not settings[15])))
        settings_panel.add_row('[b]Auto restart Bot: [/b]' + Gui.true_false_color(str(settings[16])))
        settings_panel.add_row('[b]Max Buy Size: [/b]' + Gui.true_false_color(str(settings[17])))

        return Panel(settings_panel, border_style=color, title='[b]' + title + '[/b]')    

    # Create win loss panel        
    def create_status_panel(margin, profit, action, last_action, title, color) -> Panel:
        '''Display win or loss amount'''
        grid = Table.grid(expand=True)
        grid.add_column(justify='center')
        grid.add_column(justify='center')
        grid.add_column(justify='center')
        grid.add_column(justify='center')

        grid.add_row('[b]Last Action[/b]',
                    '[b]Action[/b]',
                    '[b]Margin[/b]',
                    '[b]Profit[/b]')

        if last_action == 'SELL':
            last_action_row = '[green][b]SELL[/b][/green]'
        elif last_action == 'BUY':
            last_action_row = '[red][b]BUY[/b][/red]'
        elif last_action == 'WAIT':
            last_action_row = '[yellow][b]WAIT[/b][/yellow]'
        else:
            last_action_row = '[white][b]NONE[/b][/white]'

        if action == 'SELL':
            action_row = '[green][b]SELL[/b][/green]'
        elif action == 'BUY':
            action_row = '[red][b]BUY[/b][/red]'
        elif action == 'WAIT':
            action_row = '[yellow][b]WAIT[/b][/yellow]'
        else:
            action_row = '[white][b]NONE[/b][/white]'

        if margin > 0:
            margin_str = '[green]' + str(margin) + '%'
        else:
            margin_str = '[red]' + str(margin) + '%'

        if profit > 0:
            profit_str = '[green]' + str(profit)
        else:
            profit_str = '[red]' + str(profit)

        grid.add_row(last_action_row,
                    action_row,
                    margin_str,
                    profit_str)

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
            Layout(name='status', size=4)
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

    def thread_gui(app, price, bullbeartext, margin, profit, state, schedule):
        layout = Gui.create_layout()
        while True:
            #print("test")
            layout['header'].update(Gui.create_header(app.getVersionFromREADME()))
            layout['current_price'].update(Gui.create_small_info_panel(str(price), 'Current Price', 'bright_green'))
            layout['current_market'].update(Gui.create_small_info_panel(app.getMarket(), 'Market', 'bright_green'))
            layout['granularity'].update(Gui.create_small_info_panel(app.printGranularity(), 'Granularity', 'bright_yellow'))
            layout['bull_bear'].update(Gui.create_small_info_panel(bullbeartext, 'Bull/Bear', 'bright_yellow'))
            layout['status'].update(Gui.create_status_panel(margin, profit, state.action, state.last_action, 'Status', 'bright_magenta'))

            settings = [app.sellUpperPcnt(), app.sellLowerPcnt(), app.trailingStopLoss(), app.allowSellAtLoss(), app.sellAtResistance(), app.disableBullOnly(), app.disableBuyNearHigh(), app.disableBuyMACD(), app.disableBuyOBV(), app.disableBuyElderRay(), app.disableFailsafeFibonacciLow(), app.disableFailsafeLowerPcnt(), app.disableProfitbankReversal(), app.disabletelegram, app.disableLog(), app.disableTracker(), app.autoRestart(), app.getBuyMaxSize()]
            layout['settings_info'].update(Gui.create_settings_panel(settings, 'Settings', 'bright_red'))

            #print(price)
                
            #info_values = [str(truncate(price)), str(truncate(float(df_last['ema12'].values[0]))), str(truncate(float(df_last['ema26'].values[0]))), str(truncate(float(df_last['sma20'].values[0]))), str(truncate(float(df_last['sma200'].values[0]))), str(ema12gtema26co), str(ema12gtema26), str(ema12ltema26co), str(ema12ltema26), condition_ema_txt, str(truncate(float(df_last['macd'].values[0]))), str(truncate(float(df_last['signal'].values[0]))), str(macdgtsignal), str(macdltsignal), condition_macd_txt]
            #layout['info'].update(Gui.create_info_panel(info_values))
                
            time_left = datetime.fromtimestamp(schedule.queue[0].time)
            time_left = time_left - datetime.now()
            layout['footer'].update(Gui.create_footer(app.getExchange(), time_left / 100, datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

            # Print GUI
            Gui.render_gui(layout)
            time.sleep(1)
