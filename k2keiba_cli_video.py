import logging
import os.path
import json

import k2kparser.result as pr
import k2kvideo.rpa as rpa
import k2kvideo.ocr as ocr

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

def capture_race(race_id):

    if os.path.isdir('./pic/{}'.format(race_id.replace('/','-'))) :
        logging.info('Exist')
        while(True):
            selected = input('This race capture already exists, overwrite(y/n)')
            if selected == 'n':
                return
            elif selected == 'y':
              break
            else:
              pass

    rpa_ins = rpa.RpaJRAVideoFireFox()

    for i in range(2):
        try:
            logger.info('Race ID : {}'.format(race_id))
            rpa_ins.start_automated_process(race_id)
            break
        except rpa.RpaJRAVideoPlayFail:
            logger.warning('RpaJRAVideoPlayFail')

def read_time(race_id):
    p = pr.ParserResultRace('/JRADB/accessS.html', race_id)
    race = p.parse()

    if race['place'] in ['東京', '新潟', '中京']:
        rcw = True
    else:
        rcw = False

    ocr_ins = ocr.RpaJRAVideoReadTime(race_id, rcw=rcw)
    snaps = ocr_ins.find_snap_shop(race['laps'])
    print(snaps)

    output = {
        'name' : race['name'],
        'snaps': []
    }

    output['snaps'].append({
        'tag' : 'start',
        'file': snaps[0]['file'],
        'ts': snaps[0]['ts'],
        'time': snaps[0]['time'],
        'lap': 'start'
    })
    snaps.pop(0)

    start_distance = 200 - race['distance'] % 200

    for i, snap in enumerate(snaps):
        output['snaps'].append({
            'tag': str(start_distance) + 'm',
            'file': snap['file'],
            'ts': snap['ts'],
            'time': snap['time'],
            'lap': race['laps'][i]
        })
        start_distance += 200

    output['snaps'][-1]['tag'] = 'goal'

    return output



def result_place(place_info):
    #print(place_info)

    pk = pr.ParserResultKaisai(place_info['param']['url'], place_info['param']['param'])
    result = pk.parse()

    #print(result)

    max = len(result['races'])

    selected = -1

    fmt = 'var app = new Vue({' \
          'el: "#app",' \
          'data: '

    while(selected < max):
        for i, race in enumerate(result['races']):
            print('[{:2d}]{:2d}R : {} ({}, {})'.format(i, race['index'],
                                                  race['name'], race['param']['url'], race['param']['param']))

        selected = input_in_range(max)

        if selected >= max:
            pass
        else:
            race_id = result['races'][selected]['param']['param']
            capture_race(race_id)
            output = read_time(race_id)

            with open('frontend/index.js', 'w') as f:
                json_data = json.dumps(output, indent=4)
                f.write(fmt + json_data + '});')

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


if __name__ == '__main__':
    logging.config.fileConfig('logging.ini',disable_existing_loggers=False )
    logger = logging.getLogger(__name__)

    logger.info('cli')

    result_top('/JRADB/accessS.html', 'pw01sli00/AF')
