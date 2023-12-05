from __future__ import annotations
from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal 
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    RichLog,
    Static,
    Switch,
)
from textual import on, work
from kwenta import Kwenta
from web3 import Web3
import kwenta_actions as actions 
import asyncio
import time
import queue
from textual.worker import Worker, get_current_worker
from textual.logging import TextualHandler
import logging
logging.basicConfig(level=logging.ERROR,handlers=[TextualHandler()],)
import argparse

class Body(Container):
    pass

class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Switch(value=self.app.dark)
        yield Static("Dark mode toggle", classes="label")

    def on_mount(self) -> None:
        self.watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self) -> None:
        self.query_one(Switch).value = self.app.dark

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.app.dark = event.value


class SectionTitle(Static):
    pass

class Section(Container):
    pass

class Column(Container):
    pass


'''
Main Class where work is done. 
If you want to add new sort keys, add a binding, and add a new sort key sort_keys
'''
class kwentatui(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_queue = queue.Queue()
    CSS_PATH = "tui.tcss"
    TITLE = f"Kwenta Markets TUI | Remember to Breathe."
    current_sort_key = 'price_drift_percent'    
    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Dark mode"),
        ("f1", "app.toggle_class('RichLog', '-hidden')", "Logs"),
        ("f2", "sort_table('price_drift_percent')", "Sort Price Diff"),
        ("f3", "sort_table('pyth_price')", "Sort Price"),
        ("f4", "sort_table('pyth_ema_trend')", "Sort EMA"),
        Binding("ctrl+q", "app.quit", "Quit", show=True, priority=True),
    ]
    def action_sort_table(self, sort_key: str) -> None:
        self.current_sort_key = sort_key
        table = self.query_one("#markets", DataTable)
        #enable if top of table should be important
        if table:
            table.clear()
            self.gen_markets_table(table, self.current_sort_key)
            
    def add_note(self, renderable: RenderableType) -> None:
        self.query_one(RichLog).write(renderable)

    def compose(self) -> ComposeResult:
        yield Container(
            # Sidebar(classes="-hidden"),
            Header(show_clock=True),
            Body(
                Column(
                    Section(
                        SectionTitle("Markets"),
                        DataTable(id='markets'),
                    ),
                    classes="location-widgets location-first",
                ),
            ),
            RichLog(classes="-hidden", wrap=True, highlight=True, markup=True),
        )
        yield Footer()

    ############################################################
    ### MARKETS DATA TABLE                      ################
    ############################################################
    sort_keys = {
        'asset': 0,
        'pyth_price': 1,
        'chainlink_price': 2,
        'price_drift_percent': 3,
        'pyth_oracle': 4,
        'big_drift': 5,
        'pyth_ema_trend': 6,
        'big_ema_drift': 7,
        'ema_drift_direction': 8,
    }

    #creates the data table
    def draw_markets_table(self, id: str):
        table = self.query_one(f"#{id}", DataTable)
        table.cursor_type = "row"

        #assume all keys are same
        sample_market = all_market_data[0]
        for key in sample_market.keys():
            table.add_column(key.replace('_', ' ').title(), key=key)

        table.zebra_stripes = True
        self.gen_markets_table(table, self.current_sort_key)

    #creates all the rows from data for data table
    def gen_markets_table(self, table: DataTable, current_sort_key: str):
        rows = [tuple(market.get(key, None) for key in market)
                for market in all_market_data]
        
        # Sort rows by the current sort key
        sort_index = self.sort_keys[current_sort_key]
        rows.sort(key=lambda x: abs(x[sort_index]), reverse=True)

        for row in rows:
            table.add_row(*row, key=row[0])
    
    #updates data table live based on asset row/column coords
    def update_markets_table(self, table: DataTable):
        for market in all_market_data:
            for key, value in market.items():
                table.update_cell(row_key=market['asset'], column_key=key, value=value)

    def set_sort_key(new_sort_key):
        global current_sort_key
        current_sort_key = new_sort_key

    #continuously gets queue data spit out by the pyth process and updates the table
    async def monitor_queue(self):
        while True:
            if not self.data_queue.empty():
                global all_market_data
                self.update_market_data(self.data_queue)
                all_market_data = self.data_queue.get()
                table = self.query_one("#markets", DataTable)
                self.update_markets_table(table)
                self.add_note(f"Market Pricing Data Updated. {time.strftime('%H:%M:%S')}")
                
            await asyncio.sleep(.5)  # Adjust the sleep time for faster pull. RPC will be LOADED
    
    #worker to create pricing thread. Will run in background (pulls from actions)
    @work(exclusive=True, thread=True)
    async def update_market_data(self,q):
        worker = get_current_worker()
        if not worker.is_cancelled:
            try:
                data = await actions.pyth_process_market_pricing()
                q.put(data)
            except Exception as e:
                pass  

    def on_mount(self) -> None:
        self.add_note("Kwenta TUI is running")
        try:
            # first init of all markets
            markets_table = self.draw_markets_table('markets')
            self.update_market_data(self.data_queue)
            asyncio.create_task(self.monitor_queue())
            self.screen.set_focus(markets_table)
        except Exception as e:
            self.add_note(e)

#program pre-starter
# Input Args
parser = argparse.ArgumentParser(description='Kwenta TUI')
parser.add_argument('--provider_rpc', type=str, default=None)
parser.add_argument('--wallet_address', type=str, default='0xa0a17E374191e7342726f3a702732F68A56af3Ab')
parser.add_argument('--enable_strats', type=bool, default=False)

args = parser.parse_args()
provider_rpc = args.provider_rpc
wallet_address = Web3.to_checksum_address(args.wallet_address)
enable_strats = args.enable_strats
web3 = Web3(Web3.HTTPProvider(provider_rpc))
print(f'Populating Pyth Market Data...')
account = Kwenta(provider_rpc=provider_rpc, wallet_address=wallet_address)
app = kwentatui()

if __name__ == "__main__":
    print(f'KWENTUI STARTING *May take a couple seconds*\nLOADING LOTS OF DATA....')
    if provider_rpc is None:
        print("Please provide a provider rpc.")
        exit()
    allmarket_listings = actions.init_markets()
    global all_market_data
    all_market_data = asyncio.run(actions.pyth_process_market_pricing())
    app.run()