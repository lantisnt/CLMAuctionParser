from io import TextIOWrapper
import sys
import pprint
from datetime import datetime
from savedvariables_parser import SavedVariablesParser

guild = "alliance mirageraceway addon development"
previousTimestamp = ""

def GetSV(string: str) -> dict:
    return SavedVariablesParser().parse_string(string)

def ParseSV(source: TextIOWrapper) -> list:
    sv = GetSV(source.read())
    return sv["CLM2_DB"][guild]["personal"]["auctionHistory"]["stack"]

def BuildBidInfo(bids: dict, names: dict, upgraded: dict) -> str:
    bidInfo = {}
    if bids is not None:
        for name, value in bids.items():
            if not bidInfo.get(name):
                bidInfo[name] = {}
            bidInfo[name]['value'] = value
    if names is not None:
        for name, value in names.items():
            if not bidInfo.get(name):
                bidInfo[name] = {}
            bidInfo[name]['type'] = value
    if upgraded is not None:
        for name, value in upgraded.items():
            if not bidInfo.get(name):
                bidInfo[name] = {}
            bidInfo[name]['upgraded'] = value

    rows = ""
    template = [
        '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td></td><td></td></tr>',
        '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td><a href="https://www.wowhead.com/wotlk/item={3}" target="_blank">{3}</a></td><td></td></tr>',
        '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td><a href="https://www.wowhead.com/wotlk/item={3}" target="_blank">{3}</a></td><td><a href="https://www.wowhead.com/wotlk/item={4}" target="_blank">{4}</a></td></tr>',
    ]
    for name, info in bidInfo.items():
        type = info.get('type') if info.get('type') != None else ""
        value = info.get('value') if info.get('value') != None else ""
        upgraded = info.get('upgraded')
        if upgraded is None:
            rows += template[0].format(name, type, value)
        else:
            if len(upgraded) == 0:
                rows += template[0].format(name, type, value)
            if len(upgraded) == 1:
                rows += template[1].format(name, type, value, upgraded[0])
            if len(upgraded) == 2:
                rows += template[2].format(name, type, value, upgraded[0], upgraded[1])

    return rows

def BuildAuctionInfo(info: dict) -> str:
    auction = ""
    global previousTimestamp
    timestamp = datetime.fromtimestamp(info['time']).strftime("%d %B %Y")
    if previousTimestamp != timestamp:
        auction += '<h1>{0}</h1>'.format(timestamp)
        previousTimestamp = timestamp
    itemId = info['id']
    bids = BuildBidInfo(info.get('bids'), info.get('names'), info.get('upgraded'))

    auction += '<h2><a href="https://www.wowhead.com/wotlk/item={0}" data-wh-icon-size="medium" target="_blank">{0}</a></h2>'.format(itemId)
    auction += '<table>' + bids + '</table>'

    return auction


def OutputHTML(source: list, target: TextIOWrapper) -> None:
    header = open("input/template_begin.html", 'r').read()
    footer = open("input/template_end.html", 'r').read()

    body = ""
    for auction in source:
        body += BuildAuctionInfo(auction)

    target.write(header)
    target.write(body)
    target.write(footer)
    

def main() -> int:
    with open("input/ClassicLootManager.lua", 'r') as source:
        with open("output/AuctionHistory.html", 'w') as target:
            OutputHTML(ParseSV(source), target)
    return 0

if __name__ == '__main__':
    sys.exit(main())