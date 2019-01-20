import logging
from optparse import OptionParser

import k2kparser.top as pt
import k2kparser.den as pd
import k2kparser.result as pr
import k2kparser.result_params as prp

def print_delimiter(tag):
    print('--- {} ---'.format(tag))

def input_in_range(max):
    selected = -1

    while(selected < 0):
        selected_raw = input('[0 - {}] >> '.format(max))
        try :
            selected = int(selected_raw)
        except ValueError:
            selected = -1

    return selected

def shutuba_place(place_info):
    #print(place_info)

    pk = pd.ParserDenKaisai(place_info['param']['url'], place_info['param']['param'])
    result = pk.parse()

    #print(result)

    for race in result['races']:
        print('[{:2d}R]{} ({}, {})'.format(race['index'], race['name'], race['param']['url'], race['param']['param']))

    print()

def shutuba_day(day_info):
    #print(day_info)

    max = len(day_info['kaisai'])

    selected = -1

    while(selected < max):
        print_delimiter('出馬表 競馬場選択(' + day_info['date'] + ')')
        for i, kaisai in enumerate(day_info['kaisai']):
            print('[{}] : {}'.format(i, kaisai['place']))

        print('[{}] : 戻る'.format(max))

        selected = input_in_range(max)

        if selected >= max:
            pass
        else:
            shutuba_place(day_info['kaisai'][selected])

def shutuba_top(url, param):
    #print('shutuba : {} / {}'.format(url, param))

    p = pd.ParserDenTop(url, param)
    kaisai_list = p.parse()

    #print(kaisai_list)

    print_delimiter('出馬表 開催日選択')

    max = len(kaisai_list)
    for i, date in enumerate(kaisai_list):
        print('[{}] : {}'.format(i, date['date']))

    print('[{}] : 戻る'.format(max))

    selected = input_in_range(max)

    if selected >= max:
        pass
    else:
        shutuba_day(kaisai_list[selected])

    #logger.debug(selected)

def result_place(place_info):
    #print(place_info)

    pk = pr.ParserResultKaisai(place_info['param']['url'], place_info['param']['param'])
    result = pk.parse()

    #print(result)

    for race in result['races']:
        print('[{:2d}R]{} ({}, {})'.format(race['index'], race['name'], race['param']['url'], race['param']['param']))

    print()

def result_day(day_info):
    #print(day_info)

    max = len(day_info['kaisai'])

    selected = -1

    while(selected < max):
        print_delimiter('レース結果 競馬場選択(' + day_info['date'] + ')')
        for i, kaisai in enumerate(day_info['kaisai']):
            print('[{}] : {}'.format(i, kaisai['place']))

        print('[{}] : 戻る'.format(max))

        selected = input_in_range(max)

        if selected >= max:
            pass
        else:
            result_place(day_info['kaisai'][selected])


def result_top(url, param):
    p = pr.ParserResultTop(url, param)
    kaisai_list = p.parse()

    max = len(kaisai_list)

    selected = -1

    while(selected < max):
        print_delimiter('レース結果 開催日選択')

        for i, date in enumerate(kaisai_list):
            print('[{}] : {}'.format(i, date['date']))

        print('[{}] : 戻る'.format(max))

        selected = input_in_range(max)

        if selected >= max:
            pass
        else:
            result_day(kaisai_list[selected])

def top_menu():
    p = pt.ParserTop()
    params = p.parse()

    table = {
        'kaisai' : {
            'tag':'開催情報',
            'availability': False
        },
        'shutuba': {
            'tag':'出馬表',
            'availability': True,
            'func': shutuba_top
        },
        'odds': {
            'tag': 'オッズ',
            'availability': False
        },
        'result': {
            'tag': 'レース結果',
            'availability': True,
            'func': result_top
        },
        'haraimodoshi': {
            'tag': '払い戻し',
            'availability': False
        },
        'tokubetu': {
            'tag': '特別登録馬',
            'availability': False
        }
    }

    max = len(params)
    selected = -1

    while(selected < max):
        print_delimiter('トップメニュー')

        for i, item in enumerate(params):
            print('[{}] : {}'.format(i,table[item['tag']]['tag']))

        print('[{}] : 終了'.format(max))
        selected_raw = input('[0 - 5] >> ')

        #print(selected_raw)
        try :
            selected = int(selected_raw)
        except ValueError:
            selected = -1

        if selected >= 0 and selected < max:
            #print(params[selected])
            item = table[params[selected]['tag']]
            if 'func' in item:
                item['func'](params[selected]['params']['url'], params[selected]['params']['param'])
            else:
                print('{}は未サポートです'.format(item['tag']))

            print()


def main():
    usage = 'usage: %prog'

    parser = OptionParser(usage=usage)
    options, args = parser.parse_args()
    if options == {}:
        top_menu()
    else:
        print(options)

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini',disable_existing_loggers=False )
    logger = logging.getLogger(__name__)

    logger.info('cli')

    main()