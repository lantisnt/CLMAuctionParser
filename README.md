# CLMAuctionParser

## Requirements
Python v3.8+
## Installation
1. git clone repository
2. python -m venv ./venv
3. source venv/bin/activate
4. pip -r requirements.txt

## Usage
1. python -m venv ./venv
2. Copy `ClassicLootManager.lua` Saved Variable from: `<wow install directory>\_classic_\WTF\Account\<account id>\SavedVariables\<addon name>.lua` to `input/`
3. Run **python3 parser.py** to find out which guilds do you have. Using `global` does not work.
4. Run **python3 parser.py --guild X**
5. See result in `output/AuctionHistory.html`

