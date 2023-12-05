# Kwenta-TUI

Live Market Dashboards for Kwenta

## Features

- Strategy Plugin System
- Live Market Updates
- Run in Web and Terminal
- Cross platform

## Installation

To run this project you will need the following:

- Python 3.9+
- RPC Node (Free ones work, see examples)
- Wallet with a Kwenta Smart Margin Account (An empty account is provided)
  Install the following required packages:

\*Recommended to install in a python virtual environment to constrain the packages to the project.

```bash
  git clone https://github.com/Kwenta/kwenta-tui.git
  cd kwenta-tui
  cd dashboard_only
  #Optional venv
  python -m venv kwentatui
  ./kwentatui/scripts/activate

  #REQUIRED
  pip install textual requests kwenta web3 pandas aiohttp
```

## Usage/Examples

### Run Kwenta Dashboard (~1 second refresh time)

```
python .\kwenta_tui_dashboard.py --provider_rpc 'https://optimism.llamarpc.com'
```

### Run Dashboard with strategies enabled. (~8 second refresh time as strat prices are refreshed)

```
python .\kwenta_tui_dashboard.py --provider_rpc 'https://optimism.llamarpc.com' --enable_strats True
```

### Run Dashboard with strategies enabled, and wallet_address specified (No different from the above)

```
python .\kwenta_tui_dashboard.py --provider_rpc 'https://optimism.llamarpc.com' --enable_strats True --wallet_address '0x1234abcdefg'
```

## Strategies

I have included some basic strategies by default here for use. If you would like to add/change what is there, here is how.

#### kwenta_strats.py

- Add Strategy as Function
- Update the run_strat method with the function call and parameters

#### kwenta_actions.py

- Update _strat_filtered_keys_ variable (at top of file) with new key names from run_strat()

This will add new outputs to the datatable automatically.

#### _Strategies are run during pricing pull, if they are heavy, price refresh will be slow!_

## FAQ

#### Why would I use this?

There is a large amount of alpha in the default varient of this dashboard. You will have to figure it out.

#### Why isn't my terminal launching?

If you are on Windows make sure you are using PowerShell 7 (probably have to download it)

Double check your pip install and make sure everything is installed correctly.

Double check you have web3 version 6.0.0 +

## Support

I frequent the Kwenta Discord Dev Channel. https://discord.com/invite/kwentaio

If you have any questions feel free to ask there.

## Roadmap

- I am currently working on a version which will have trading included in the terminal, watch this project for updates.
- Graphs Maybe
- Better web integration as textual-web improves
