# Write JSON news data to json file 
  
import json 
  
# data to write (ACTORs descriptions) - translation with google translate
data_google = {"news_cm_1_drs.txt":[{'T1': 'A man, the thief, the burglar, The thief', 'T3': 'a couple, who, them, the victims, both, the, the couple', 'T6': 'a car, the car, where', 'T9': 'a pistol', 'T10': 'Liberty avenue', 'T11': 'Lisbon', 'T12': 'The crime', 'T16': 'about 400 euros', 'T20': 'Tuesday afternoon', 'T21': 'Rossio', 'T29': 'them, the, the couple', 'T30': 'a camcorder', 'T31': 'two watches'},
                                    {'T1': 'thief', 'T3': 'victim', 'T6': 'car', 'T9': 'pistol', 'T10': 'liberty avenue', 'T11': 'lisbon', 'T12': 'crime', 'T16': 'euro', 'T20': 'afternoon', 'T21': 'rossio', 'T29': 'couple', 'T30': 'camcorder', 'T31': 'watch'}],
        
        "news_cm_2_drs.txt":[{'T1': 'The President of France, François Hollande, Hollande', 'T4': 'today', 'T5': 'all of Europe, Europe, France, Europe', 'T7': 'the attacks, the attacks', 'T8': 'this morning', 'T9': 'Brussels, Brussels', 'T14': 'the necessary provisions in view of the seriousness of the threat', 'T15': 'January', 'T17': 'France, her, her, France', 'T20': 'last november', 'T21': 'target of terrorist attacks', 'T28': 'strengthening the fight against terrorism', 'T30': 'today', 'T31': 'a Council of Ministers'},
                             {'T1': 'françois hollande', 'T4': 'today', 'T5': 'france', 'T7': 'attack', 'T8': 'morning', 'T9': 'brussels', 'T14': 'provisions', 'T15': 'january', 'T17': 'france', 'T20': 'november', 'T21': 'attack', 'T28': 'fight', 'T30': 'today', 'T31': 'council'}],
        
        "news_cm_3_drs.txt":[{'T1': 'Thieves', 'T3': '500 cows, all', 'T4': 'a livestock farm', 'T5': 'New Zealand', 'T6': 'the owner, the man, the farmer', 'T8': 'for weeks', 'T10': 'the herd, 1300 heads', 'T11': 'early july', 'T14': 'just over 800', 'T16': 'The police, officers', 'T18': 'the theft, theft', 'T20': 'few clues', 'T30': 'now'},
                             {'T1': 'thief', 'T3': 'cow', 'T4': 'farm', 'T5': 'new zealand', 'T6': 'farmer', 'T8': 'week', 'T10': 'herd', 'T11': 'july', 'T14': 'over', 'T16': 'police', 'T18': 'theft', 'T20': 'clue', 'T30': 'now'}],
        
        "news_cm_4_drs.txt":[{'T1': 'The Secretary General, Secretary General', 'T2': 'Homeland Security System, Homeland Security System', 'T3': 'all security forces, All Security Forces and Services, yours, your', 'T4': 'Counter-Terrorism Coordination Unit, Counter-Terrorism Coordination Unit', 'T5': 'the events, the events', 'T6': 'Brussels, Brussels, The city of Brussels, capital of Belgium', 'T7': 'alert level', 'T8': 'Portugal', 'T14': 'all the necessary data', 'T17': 'the cabinet', 'T21': 'morning', 'T22': 'two attacks', 'T23': 'two explosions', 'T24': 'more two', 'T25': 'airport', 'T26': 'subway', 'T28': 'at least 21 dead', 'T29': 'dozens of injured', 'T30': 'today', 'T43': 'counterparts'},
                             {'T1': 'secretary genaral', 'T2': 'security system', 'T3': 'security forces', 'T4': 'counter-terrorism', 'T5': 'event', 'T6': 'brussels', 'T7': 'alert', 'T8': 'portugal', 'T14': 'data', 'T17': 'cabinet', 'T21': 'morning', 'T22': 'attack', 'T23': 'explosion', 'T24': 'more', 'T25': 'airport', 'T26': 'subway', 'T28': 'dead', 'T29': 'injured', 'T30': 'today', 'T43': 'counterpart'}],
        
        "news_cm_5_drs.txt":[{'T1': 'An armed man, the clumsy burglar, burglar', 'T2': 'a knife', 'T3': 'a gas station, Coastal Gas Station, local', 'T4': 'state of New Jersey, New Jersey', 'T5': 'employee, employee', 'T6': 'two dollars of gasoline, 1.9 euros', 'T11': 'The attempted assault, the adventure, assault', 'T13': 'Pennsville County', 'T16': 'imprisonment', 'T27': 'insignificant value'},
                             {'T1': 'burglar', 'T2': 'knife', 'T3': 'station', 'T4': 'new jersey', 'T5': 'employee', 'T6': 'dollar', 'T11': 'assault', 'T13': 'county', 'T16': 'imprisonment', 'T27': 'value'}],
        
        "news_cm_6_drs.txt":[{'T3': 'Brussels', 'T4': 'Prime Minister, Charles Michel, Charles Michel, Prime Minister', 'T5': 'Belgium', 'T7': 'Belgian security services, the competent authorities', 'T8': 'The government', 'T10': 'all efforts', 'T13': 'solemn ceremony', 'T14': 'the king Philip', 'T15': 'Queen Matilde', 'T16': 'government members', 'T17': 'the president, Jean-Claude Juncker', 'T20': 'the attacks, the attacks', 'T21': 'today', 'T31': 'full light', 'T32': 'The government and the competent authorities will make every effort to shed light on the attacks'},
                             {'T3': 'brussels', 'T4': 'charles michel', 'T5': 'belgium', 'T7': 'authority', 'T8': 'government', 'T10': 'effort', 'T13': 'ceremony', 'T14': 'king', 'T15': 'queen', 'T16': 'government', 'T17': 'jean-claude juncker', 'T20': 'attack', 'T21': 'today', 'T31': 'light', 'T32': 'authority'}],
        
        "news_destak_1_drs.txt":[{'T1': 'The secretary general, Jerónimo de Sousa, The communist leader, his', 'T2': 'PCP, the party', 'T5': 'today', 'T6': 'commitments, commitments', 'T25': 'the problem', 'T28': 'PCP, party'},
                                 {'T1': 'jerónimo de sousa', 'T2': 'PCP', 'T5': 'today', 'T6': 'commitment', 'T25': 'problem', 'T28': 'PCP'}],
        
        "news_destak_2_drs.txt":[{'T1': 'Maria Antónia Pinto de Matos, current director of the National Tile Museum, Maria Antónia Pinto de Matos', 'T4': 'director of the Museum of the Presidency of the Republic', 'T6': 'Diogo Gaspar, Diogo Gaspar, Diogo Gaspar, whose', 'T7': 'today', 'T10': 'September 30', 'T12': 'last summer', 'T13': 'various crimes, crimes', 'T14': 'suspicious, suspicious', 'T15': 'The appointment', 'T16': 'service commission', 'T19': 'influence traffic', 'T20': 'document forgery', 'T21': 'embezzlement', 'T22': 'use embezzlement', 'T23': 'economic participation in business', 'T24': 'Power abuse', 'T29': 'Republic Diary', 'T35': 'a position'},
                                 {'T1': 'maria antónia pinto de matos', 'T4': 'director', 'T6': 'diogo gaspar', 'T7': 'today', 'T10': 'september', 'T12': 'summer', 'T13': 'crime', 'T14': 'suspicious', 'T15': 'appointment', 'T16': 'commission', 'T19': 'traffic', 'T20': 'document', 'T21': 'embezzlement', 'T22': 'embezzlement', 'T23': 'economic', 'T24': 'power', 'T29': 'republic', 'T35': 'position'}]   
}

# data to write (ACTORs descriptions) - translation with hugging face transformers
data_hugg = {"news_cm_1_drs.txt":[{'T1': 'A man, the thief, the robber, the thief', 'T3': 'a couple, who, they, the victims, both, the, the couple', 'T6': 'a car, the car, where', 'T9': 'a gun.', 'T10': 'Avenue of Liberty', 'T11': 'Lisboa', 'T12': 'Crime', 'T16': 'About 400 euros', 'T20': 'Tuesday afternoon', 'T21': 'Red', 'T29': 'they, os, The couple', 'T30': 'a camera of filming', 'T31': 'two watches'},
                                  {'T1': 'thief', 'T3': 'victim', 'T6': 'car', 'T9': 'gun', 'T10': 'liberty avenue', 'T11': 'lisboa', 'T12': 'crime', 'T16': 'euro', 'T20': 'afternoon', 'T21': 'rossio', 'T29': 'couple', 'T30': 'camera', 'T31': 'watch'}],
             
             "news_cm_2_drs.txt":[{'T1': 'The President of France, François Hollande, Hollande', 'T4': 'today', 'T5': 'all Europe, Europe, France, Europe', 'T7': 'attacks, attacks', 'T8': 'this morning', 'T9': 'Brussels, Brussels', 'T14': 'the essential provisions in view of the seriousness of the threat', 'T15': 'January', 'T17': 'France, her, yours, France', 'T20': 'past November', 'T21': 'Target of terrorist attacks', 'T28': 'strengthening the fight against terrorism', 'T30': 'today', 'T31': 'a Council of Ministers'},
                                  {'T1': 'françois hollande', 'T4': 'today', 'T5': 'france', 'T7': 'attack', 'T8': 'morning', 'T9': 'brussels', 'T14': 'provisions', 'T15': 'january', 'T17': 'france', 'T20': 'november', 'T21': 'attack', 'T28': 'fight', 'T30': 'today', 'T31': 'council'}],
             
             "news_cm_3_drs.txt":[{'T1': 'Thieves', 'T3': '500 cows, all', 'T4': 'a livestock holding', 'T5': 'New Zealand', 'T6': 'the owner, the man, the farmer', 'T8': 'for weeks', 'T10': 'the herd, 1300 heads', 'T11': 'beginning of July', 'T14': 'just over 800', 'T16': 'The police, the agents.', 'T18': 'the theft, theft', 'T20': 'few clues', 'T30': 'Now'},
                                  {'T1': 'thief', 'T3': 'cow', 'T4': 'livestock', 'T5': 'new zealand', 'T6': 'farmer', 'T8': 'week', 'T10': 'herd', 'T11': 'july', 'T14': 'over', 'T16': 'police', 'T18': 'theft', 'T20': 'clue', 'T30': 'now'}],
             
             "news_cm_4_drs.txt":[{'T1': 'The Secretary-General, Secretary-General', 'T2': 'Internal Security System, Internal Security System', 'T3': 'all security forces, all security forces and services, yours', 'T4': 'Anti-terrorism Coordination Unit, Anti-terrorism Coordination Unit', 'T5': 'events, events', 'T6': 'Brussels, Brussels, The city of Brussels, capital of Belgium', 'T7': 'alert level', 'T8': 'Portugal', 'T14': 'all necessary data', 'T17': 'the office', 'T21': 'this morning', 'T22': 'two attacks', 'T23': 'two explosions', 'T24': 'two more', 'T25': 'airport', 'T26': 'metre', 'T28': 'at least 21 dead', 'T29': 'dozens of wounded', 'T30': 'today', 'T43': 'Congeners'},
                                  {'T1': 'secretary genaral', 'T2': 'security', 'T3': 'security forces', 'T4': 'anti-terrorism', 'T5': 'event', 'T6': 'brussels', 'T7': 'alert', 'T8': 'portugal', 'T14': 'data', 'T17': 'office', 'T21': 'morning', 'T22': 'attack', 'T23': 'explosion', 'T24': 'more', 'T25': 'airport', 'T26': 'metre', 'T28': 'dead', 'T29': 'wounded', 'T30': 'today', 'T43': 'congener'}],
             
             "news_cm_5_drs.txt":[{'T1': 'An armed man, the clumsy assailant, assailant', 'T2': 'a knife', 'T3': 'a gas pump, Coastal Gas Station, location', 'T4': 'State of New Jersey, New Jersey', 'T5': 'employee, employee', 'T6': 'two dollars of gasoline, 1.9 euros', 'T11': 'The attempted assault, the adventure, the assault', 'T13': 'municipality of Pennsville', 'T16': 'Prison sentence', 'T27': 'insignificant value'},
                                  {'T1': 'assailant', 'T2': 'knife', 'T3': 'station', 'T4': 'new jersey', 'T5': 'employee', 'T6': 'dollar', 'T11': 'assault', 'T13': 'pennsville', 'T16': 'prison', 'T27': 'value'}],
             
             "news_cm_6_drs.txt":[{'T3': 'Brussels', 'T4': 'The Prime Minister, Charles Michel, Charles Michel, the Prime Minister', 'T5': 'Belgium', 'T7': 'Belgian security services, competent authorities', 'T8': 'The government', 'T10': 'all efforts', 'T13': 'solemn ceremony', 'T14': 'King Philip', 'T15': 'Queen Matilde', 'T16': 'members of the Government', 'T17': 'the President, Jean-Claude Juncker', 'T20': 'the attacks, the attacks', 'T21': 'today', 'T31': 'full light', 'T32': 'The Government and the competent authorities will make every effort to shed light on the attacks'},
                                  {'T3': 'brussels', 'T4': 'charles michel', 'T5': 'belgium', 'T7': 'authority', 'T8': 'government', 'T10': 'effort', 'T13': 'ceremony', 'T14': 'king', 'T15': 'queen', 'T16': 'government', 'T17': 'jean-claude juncker', 'T20': 'attack', 'T21': 'today', 'T31': 'light', 'T32': 'authority'}],
             
             "news_destak_1_drs.txt":[{'T1': 'The Secretary-General, Jerome de Sousa, The Communist leader,', 'T2': 'PCP, the party', 'T5': 'today', 'T6': 'commitments, commitments', 'T25': 'the problem', 'T28': 'PCP, party'},
                                      {'T1': 'jerónimo de sousa', 'T2': 'PCP', 'T5': 'today', 'T6': 'commitment', 'T25': 'problem', 'T28': 'PCP'}],
             
             "news_destak_2_drs.txt":[{'T1': 'Maria Antónia Pinto de Matos, current director of the National Museum of Tiles, Maria Antónia Pinto de Matos', 'T4': 'Director of the Museum of the Presidency of the Republic', 'T6': 'Diogo Gaspar, Diogo Gaspar, Diogo Gaspar, whose', 'T7': 'today', 'T10': '30 September', 'T12': 'last summer', 'T13': 'various crimes, crimes', 'T14': 'suspicious, suspicious', 'T15': 'The appointment', 'T16': 'Committee of Service', 'T19': 'trade in influence', 'T20': 'falsification of the document', 'T21': 'peculate', 'T22': 'peculate for use', 'T23': 'economic participation in business', 'T24': 'abuse of power', 'T29': 'Journal of the Republic', 'T35': 'a position'},
                                      {'T1': 'maria antónia pinto de matos', 'T4': 'director', 'T6': 'diogo gaspar', 'T7': 'today', 'T10': 'september', 'T12': 'summer', 'T13': 'crime', 'T14': 'suspicious', 'T15': 'appointment', 'T16': 'committee', 'T19': 'trade', 'T20': 'falsification', 'T21': 'peculate', 'T22': 'peculate', 'T23': 'economic', 'T24': 'power', 'T29': 'journal', 'T35': 'position'}]
}

def jprint(obj):
    # formatted string of Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False)
    print(text)

# add info to JSON 
def write_json(data, file): 
    with open(file,'w') as j: 
        json.dump(data, j, indent=4, ensure_ascii=False) 


def process_data(data,file):
    write_json(data,file)

    with open(file, 'r') as j:
        news_data = json.load(j)

    jprint(news_data)

process_data(data_google,'news_info_google.json')
process_data(data_hugg,'news_info_hugging.json')