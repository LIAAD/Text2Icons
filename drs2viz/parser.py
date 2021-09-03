import os
import re
import ast

from pathlib import Path

import process_actors as process_actors
import hftransformers as hftransformers
import googletranslate as googletranslate
from Dictionary import *

DRS_TAGS = {'events': '» EVENTS',
            'actors': '» ACTORS',
            'relations': '» RELATIONS'}

DRS_DIR = '../drs_files'
SENTENCES_DIR = '../sentences/'
TRANSLATIONS_DIR = '../translations'

def natural_sort(lst): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(lst, key = alphanum_key)


def remove_quotes(text):
    return text.replace('"', '')

def get_drs_files():
    return natural_sort([os.path.join(DRS_DIR, f) for f in os.listdir(DRS_DIR) if (os.path.isfile(os.path.join(DRS_DIR, f)) and '_drs.txt' in f)])


def get_drs_str(drs_file):
    with open(drs_file, 'r') as drs_file:
        drs = drs_file.read()

    # Remove # from drs
    drs = drs.replace('# ', '')

    return drs


def get_entities(drs):
    events = drs.split(DRS_TAGS['events'])[1].split(DRS_TAGS['actors'])[0]
    actors = drs.split(DRS_TAGS['actors'])[1].split(DRS_TAGS['relations'])[0]
    relations = drs.split(DRS_TAGS['actors'])[
        1].split(DRS_TAGS['relations'])[1]

    return events, actors, relations


# EVENTS

def get_events_list(events):
    events_list = events.split('\n\n')

    return events_list

def get_events_dict(events_list):
    # Refactor this v
    '''
    returns a dictionary {event_tag: event_type}
    '''
    arrow_pattern = ' -> '
    events_dict_aux = {}

    for event in events_list:
        event_split = event.split(arrow_pattern)

        e = event_split[0]

        e_label = e[e.find("(")+1:e.find(")")]
        e = e.replace(e_label, '').replace(' ()', '').replace('\n', '')

        if not e:
            continue

        events_dict_aux[e] = e_label

    # Ensure that events are ordered by their tags
    events_dict = {}
    for event_tag in natural_sort(events_dict_aux.keys()):
        events_dict[event_tag] = events_dict_aux[event_tag]

    return events_dict


# ACTORS

def get_actors_list(actors):
    actors = os.linesep.join([s for s in actors.splitlines() if s])
    actors_list = actors.splitlines()
    return actors_list


def get_actors_dict(actors_list):
    '''
    returns a dictionary {actor_tag: actor_name}
    '''
    arrow_pattern = ' -> '
    actors_dict_aux = {}

    for actor in actors_list:
        actor_split = actor.split(arrow_pattern)
        actors_dict_aux[actor_split[0]] = actor_split[1]

    # Ensure that actors are ordered by their tags
    actors_dict = {}
    for actor_tag in natural_sort(actors_dict_aux.keys()):
        actors_dict[actor_tag] = actors_dict_aux[actor_tag]

    return actors_dict


# RELATIONS

def get_relations_list(relations):
    relations = os.linesep.join([s for s in relations.splitlines() if s])
    relations_list = relations.splitlines()
    return relations_list


def get_relations_triplets(relations_list):
    '''
    returns a triplet (actor1, relation, actor2)
    '''
    dash_pattern = ' - '

    relations_triplets = []
    for relation in relations_list:
        relation_split = relation.split(dash_pattern)
        relation_triplet = (
            relation_split[0], relation_split[1], relation_split[2])
        relations_triplets.append(relation_triplet)

    return relations_triplets


def get_relations_per_events(relations_triplets, actors_dict, events_dict):

    # dict {'Ex': [('Ty', 'type'), ...]}
    relations_per_events = {}

    for r in relations_triplets:
        # Get only relations between actors and events
        if r[0] in actors_dict and r[2] in events_dict:
            if r[2] in relations_per_events:
                relations_per_events[r[2]].append((r[0], r[1]))
            else:
                relations_per_events[r[2]] = [(r[0], r[1])]
        elif r[0] in events_dict and r[2] in actors_dict:
            if r[0] in relations_per_events:
                relations_per_events[r[0]].append((r[2], r[1]))
            else:
                relations_per_events[r[0]] = [(r[2], r[1])]

    return relations_per_events


def explode_relations_per_events(relations_per_events):

    # dict {'Ex': [('Ty', 'type'), ...]}
    relations_per_events_exploded = {}
    seen = []
    for ev, rels in relations_per_events.items():
        for rel in rels:
            for rel_aux in rels:
                # If iterating over same event relation and if there is more than one relation, skip
                if (rel == rel_aux and len(rels) > 1):
                    continue
                
                dummy_triplet = (rel[0], ev, rel_aux[0])

                exists = False
                for r in seen:
                    # If triplet exists in events_relations, do not append
                    triplet_to_check = (r[0], r[1], r[2])
                    if sorted(triplet_to_check) == sorted(dummy_triplet):
                        exists = True
                        break
                
                if not exists:
                    relations_per_events_exploded.setdefault(ev, []).append((rel[0], rel[1] + '/' + rel_aux[1], rel_aux[0]))
                    seen.append(dummy_triplet)

    return relations_per_events_exploded


def get_non_event_relations(relations_triplets, events_relations, actors_dict, events_dict):

    non_event_relations = []
    for r in relations_triplets:
        # Get only opposite of relations between actors and events (relations between actors)
        # Written this way to match other function
        if not ((r[0] in actors_dict and r[2] in events_dict) or (r[0] in events_dict and r[2] in actors_dict)):
            # Ignore pronominal relations as they do not introduce useful information
            if r[1] != 'pronominal':
                # Ignore relations between events
                if r[0] not in events_dict and r[2] not in events_dict:
                    non_event_relations.append(r)

    return non_event_relations


def get_redundant_dict(relations_triplet, events_dict):
    '''
    returns a dict 
    whose keys are a actors, and the values are lists of equivalent actors (sameHead, objIdentity, synonymy)
    eg: {'actor_x: ['actor_y', 'actor_z']}
    '''
    
    redundant_dict_aux = {}

    for rel in relations_triplet:
        source = rel[0]
        r = rel[1]
        target = rel[2]

        # Ignore if self relation
        if source == target:
            continue
        
        # Ignore if relation includes event
        if source in events_dict or target in events_dict:
            continue
        
        # Ignore if relation does not imply redundancy
        if r != 'sameHead' and r != 'objIdentity' and r != 'synonymy':
            continue

        if target in redundant_dict_aux:
            if source not in redundant_dict_aux[target]:
                redundant_dict_aux[target].append(source)
        else: redundant_dict_aux[target] = [source]
        
    # Simplify
    for tag in list(redundant_dict_aux.keys()):
        # Gets keys from dict in which tag appears as value of those keys
        key_in_value = [key for key, value in redundant_dict_aux.items() if tag in value]

        for k in key_in_value:
            redundant_dict_aux[k].extend(redundant_dict_aux[tag])
        
        # If tag was a redundant actor, remove it from dict
        if len(key_in_value) > 0:
            del redundant_dict_aux[tag]

    # Order actors by their tags
    redundant_dict = {}
    for actor_tag in natural_sort(redundant_dict_aux.keys()):
        redundant_dict[actor_tag] = natural_sort(sorted(set(redundant_dict_aux[actor_tag]), key=redundant_dict_aux[actor_tag].index))

    return redundant_dict


def resolve_redundancy(redundant_dict, actors_dict, relations_triplets):
    '''
    change actors_dict and relations_triplets by removing redundant actors
    '''
    for actor_1, redund_list in redundant_dict.items():
        
        for actor_aux in redund_list:
            # Add redundant actor to original actor in actor_dict
            actors_dict[actor_1] = actors_dict[actor_1] + ', ' + actors_dict[actor_aux]

            # Change reference from actor_aux to actor_1 in relations
            for i, rel in enumerate(relations_triplets):
                if rel[0] == actor_aux:
                    rel = list(rel)
                    rel[0] = actor_1
                    relations_triplets[i] = tuple(rel)
                if rel[2] == actor_aux:
                    rel = list(rel)
                    rel[2] = actor_1
                    relations_triplets[i] = tuple(rel)
               
    # Delete redundant actors from actors_dict
    for act, redund_list in redundant_dict.items():
        for redund_actor in redund_list:
            try:
                del actors_dict[redund_actor]
            except KeyError as ke:
                #print('Actor ' + str(ke) + ' already removed')
                pass
    
    relations_triplets = [rel for rel in relations_triplets if not ((rel[0] == rel[2]) and (rel[1] == 'sameHead' or rel[1] == 'synonymy' or rel[1] == 'objIdentity'))]

    return actors_dict, relations_triplets


def create_mscgen(actors_dict, events_dict, events_relations, non_event_relations):

    # Begin mscgen string
    msc_string = 'msc {\nwordwraparcs=true, hscale="1";\n'

    # Build actors mscgen
    for i, (tag, actor) in enumerate(actors_dict.items()):
        msc_string += tag + ' [label="' + remove_quotes(actor) + '"]'
        if i < len(actors_dict) - 1:
            msc_string += ', '
        else:
            msc_string += ';\n\n'

    # Build relations mscgen
    
    # Events relations
    for ev, rels in events_relations.items():

        for i, rel_triplet in enumerate(rels):
            msc_string += rel_triplet[0] + '=>' + rel_triplet[2] + ' [label="' + remove_quotes(events_dict[ev]) + ' (' + rel_triplet[1] + ')' + '"];'
            # if i == 0:
            #     msc_string += ' [label="' + remove_quotes(events_dict[ev]) + '(' + rel_triplet[1] + ')' + '"]'
            # else:
            #     msc_string += ' [label="' + rel_triplet[1] + '"]'
            
        #     if i < len(rels)-1:
        #         msc_string += ',\n' 

        # msc_string += ';\n'

    # Non events relations
    for rel_triplet in non_event_relations:
        msc_string += rel_triplet[0] + '=>' + rel_triplet[2] + \
                ' [label="' + rel_triplet[1] + '"];\n'
    
    # Close mscgen string
    msc_string += '}'

    return msc_string


def print_dict(data):
    for k, v in data.items():
        print(k + ': ' + str(v))
    print()

def print_list(data):
    for elem in data:
        print(elem)
    print()

def parse_drs(drs_file, debug=False):
    try:
        drs = get_drs_str(drs_file)
        print('Parsing file: ' + drs_file + '\n')
    except FileNotFoundError as e:
        print(e)
        return 'msc {}'

    events, actors, relations = get_entities(drs)
    
    # Events
    events_list = get_events_list(events)
    events_dict = get_events_dict(events_list)
    
    # Actors
    actors_list = get_actors_list(actors)
    actors_dict = get_actors_dict(actors_list)
    
    # Relations
    relations_list = get_relations_list(relations)
    relations_triplets = get_relations_triplets(relations_list)
    
    if debug:
        print('===== ORIGINAL ELEMENTS FROM DRS ===== \n')

        print('EVENTS: ')
        print_dict(events_dict)

        print('ACTORS: ')
        print_dict(actors_dict)

        print('RELATIONS: ')
        print_list(relations_triplets)


    # Resolve actors redundancy
    redundant_dict = get_redundant_dict(relations_triplets, events_dict)
    actors_dict, relations_triplets = resolve_redundancy(redundant_dict, actors_dict, relations_triplets)

    # Resolve chain relations
    relations_per_events = get_relations_per_events(relations_triplets, actors_dict, events_dict)
    events_relations = explode_relations_per_events(relations_per_events)

    non_event_relations = get_non_event_relations(relations_triplets, events_relations, actors_dict, events_dict)
    
    if debug:

        print('===== PROCESSING ===== \n')

        print('REDUNDANT ACTORS: ')
        print_dict(redundant_dict)

        print('ACTORS: ')
        print_dict(actors_dict)

        print('RELATIONS: ')
        print_list(relations_triplets)

        print('RELATIONS PER EVENT: ')
        print_dict(events_relations)

        print('NON EVENT RELATIONS: ')
        print_list(non_event_relations)


    print('===== ELEMENTS TO DISPLAY ===== \n')

    print('ACTORS: ')
    print_dict(actors_dict)

    print('EVENTS: ')
    print_dict(events_dict)

    print('RELATIONS PER EVENTS: ')
    print_dict(events_relations)

    print('NON EVENT RELATIONS: ')
    print_list(non_event_relations)

    return actors_dict, events_dict, events_relations, non_event_relations


def get_msc_data(drs_file, debug=False):

    actors_dict, events_dict, events_relations, non_event_relations = parse_drs(drs_file)

    msc_string = create_mscgen(actors_dict, events_dict, events_relations, non_event_relations)

    print('MSCGEN STRING: ')
    print(msc_string)
    print()

    return msc_string


def get_graph_data(drs_file, debug=False):

    actors_dict, events_dict, events_relations, non_event_relations = parse_drs(drs_file)
    
    # Events relations
    event_relations = []
    for ev, rels in events_relations.items():
        for i, rel_triplet in enumerate(rels):
            event_relations.append((rel_triplet[0], remove_quotes(events_dict[ev]) + ' (' + rel_triplet[1] + ')', rel_triplet[2]))

    return actors_dict, non_event_relations, event_relations

### ICON VISUALIZATION ###

## ACTORS
def get_actors_data(drs_file, debug=False):
    actors_dict_pt, events_dict_pt, events_relations_pt, non_event_relations_pt = parse_drs(drs_file)

    # translate actor descriptions
    actors_dict_en = check_translation(drs_file, actors_dict_pt)

    # filter the actors dictionary to have only specific descriptions of the actors
    actors_filtered_en = process_actors.filter_actors(actors_dict_en.copy())

    actors_list = []
    for key, val in actors_filtered_en.items():
        actors_list.append(val)

    # get actors in each event - IDs
    actors_in_event = get_actors_in_event(events_relations_pt.copy(),events_dict_pt.copy())
    # get actors in each event - descriptions
    actors_in_event_des = get_dict_descriptions(actors_in_event.copy(), actors_filtered_en.copy(), events_dict_pt.copy())

    return actors_dict_pt, actors_dict_en, actors_filtered_en, actors_in_event, actors_list, events_dict_pt, actors_in_event_des

def get_actors_in_event(events_rel, events_dict, debug=False):
    '''
    returns a dictionary {event_tag: actors_tags}
    '''
    data_by_event = {}
    data_by_event_f = {}
    
    for key, value in events_rel.items():
        actors_list = []
        for rel in value:
            x,y = rel[0], rel[-1]
            if x not in actors_list:
                actors_list.append(x)
            if y not in actors_list:
                actors_list.append(y)
        data_by_event[key] = actors_list

    # order by event occurrence
    for key, value in events_dict.items():
        if key in data_by_event.keys():
            data_by_event_f[key] = data_by_event[key]
        else:
            continue

    return data_by_event_f

def searchName(id, dict, debug=False):
    for key, value in dict.items():
        if key == id:
            name = value
    return name

def get_dict_descriptions(dict1, dict2, dict3, debug=False):
    dict_des = {}

    for key, value in dict1.items():
        list = []
        for v in value:
            list.append(searchName(v,dict2))
        dict_des[searchName(key,dict3)] = list

    return dict_des

## ICONS
# icons data for actors dictionary and tuples
def get_icons_data(dict, debug=False):
    icons_data = []
    tuples = []
    d = Dictionary()
    d.updateIcons()
    
    for key, value in dict.items():
        if not value:
            continue
        img_path = d.searchImgName(value)
        if img_path != '':
            icons_data.append(img_path)
            tup = value, img_path
            tuples.append(tup)

    return icons_data, tuples

# icons data for actors in dictionary
def get_icons_data_img(dict, debug=False):
    '''
    returns a dictionary {dict_key: actors_image_path}
    '''
    icons_data = {}

    for key, value in dict.items():
        actors = []
        for actor in value:
            if not actor:
                continue 
            
            img_path = search_icon(actor,'most')
            # uncomment one of the lines below to search for opposite icons and comment on the previous one
            #img_path = search_opposite_icon(actor,'least')  # search for the least similar icon
            #img_path = search_opposite_icon(actor,'2most')  # search for the second most similar icon

            if img_path != '':
                if img_path not in actors:
                    actors.append(img_path)
        
        icons_data[key] = actors

    return icons_data  

# seach icon in dictionary, if match not found, add new icon automatically
def search_icon(actor,icon_type, debug=False):
    d = Dictionary()
    d.updateIcons()

    img_path = d.searchImgName(actor)

    if img_path != '':
        return img_path

    else:
        d.search2Add(actor,'auto',icon_type)
        img_path = d.searchImgName(actor)
        return img_path

# seach for opposite icons automatically
# saving in the opposites dictionary, for evaluation purposes only
def search_opposite_icon(actor,icon_type, debug=False):
    d = Dictionary()
    d.updateOpposites()

    d.search2Add(actor,'opposite',icon_type)
    img_path = d.searchImgNameOp(actor,icon_type)

    return img_path


## get news file name
def split_at(file, delimiter, n, type):
    words = file.split(delimiter)
    if type == 'before':
        return delimiter.join(words[:n])
    elif type == 'after':
        return delimiter.join(words[n:])

def get_news_name(drs_file):
    news_name = split_at(drs_file, '/', 2, 'after')
    news_name = split_at(news_name, '_', 3, 'before')
    return news_name


## TRANSLATIONS - of actors descriptions
def get_file_t(path, drs_file):
    path = r"{}".format(path)
    all_files = glob.glob(path + '/*_translation.txt')

    return all_files

def read_file(filename):
    with open(filename, encoding="utf8") as f:
        content = f.read()

    return content

# write to output file
def write_translation(actors_dict_en, out_file):
    with open(out_file, 'w') as f:
        try:
            print(actors_dict_en, file=f)
        except Exception as e:
            print('Exception while writing TRANSLATIONS\n')
            print(e)

# save translation to folder, creates output dir if does not exist
def save_translation(drs_file, actors_dict_en):
    Path(TRANSLATIONS_DIR).mkdir(parents=True, exist_ok=True)

    news_name = get_news_name(drs_file)
    output_file_name = news_name + '_translation.txt'
    
    output_file = os.path.join(TRANSLATIONS_DIR, output_file_name)
    write_translation(actors_dict_en, output_file)

def check_translation(drs_file, actors_dict_pt, debug=False):
    '''
    returns a dictionary {actor_tag: actor_translation}
    '''
    files = get_file_t(TRANSLATIONS_DIR, drs_file)
    actors_dict_en = {}

    for f in files:
        if get_news_name(drs_file) == get_news_name(f):
            actors_dict_en = read_file(f)
            return ast.literal_eval(actors_dict_en)
    
    # Hugging Face Transformers
    #actors_dict_en = hftransformers.toEnglish(actors_dict_pt)

    # Google Translate API
    actors_dict_en = googletranslate.toEnglish(actors_dict_pt)

    #save to translations
    save_translation(drs_file, actors_dict_en)
    
    return actors_dict_en


## SENTENCES
def get_file(path, drs_file):
    news_name = get_news_name(drs_file)
    path = r"{}".format(path)
    file = glob.glob(path + news_name + "_sentences.txt")

    return file[0]

def get_sentences_str(sentences_file):
    with open(sentences_file, 'r') as sentences_file:
        sentences = sentences_file.readlines()
    sentences = [s.strip().replace('\n', '') for s in sentences]

    return sentences

def get_sentences_dict(sentences):
    '''
    returns a dictionary {sentences_tag: sentences_type}
    '''
    sentences_dict = {}

    for s in sentences:
        tmp = s.split(' ', 1)
        sentences_dict[tmp[0]] = tmp[1]

    return sentences_dict

def parse_sentences(drs_file, debug=False):
    sentences_file = get_file(SENTENCES_DIR, drs_file)
    sentences = get_sentences_str(sentences_file)
    sentences_dict = get_sentences_dict(sentences)

    return sentences_dict

def find_word(text, search):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)

   if len(result)>0:
      return True
   else:
      return False

def get_actors_in_sentences(sentences_dict,actors_dict_pt, debug=False):
    '''
    returns a dictionary {sentences_tag: actors_tags}
    '''
    actors_in_sentences = {}

    for s_id,s in sentences_dict.items():
        actors_list = []

        for a_id,a in actors_dict_pt.items():
            list = a.split(", ")

            for elem in list:
                if find_word(s,elem):
                    if a_id not in actors_list:
                        actors_list.append(a_id)

        actors_in_sentences[s_id] = actors_list

    return actors_in_sentences