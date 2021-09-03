import os
import json
from flask import Flask, render_template, request, url_for
import parser as parser

app = Flask(__name__)

BRAT_ANN_DIR = '../brat2drs/text_2_story_new'
BRAT_TEXT2STORY_URL = 'https://nabu.dcc.fc.up.pt/brat/#/text_2_story_new/'

@app.route('/brat2viz', methods=['GET', 'POST'])
def brat2viz():
    drs_files = parser.get_drs_files()

    selected_drs = request.form.get('select_drs')

    if selected_drs:
        drs_file = selected_drs
    else:
        drs_file = drs_files[0]

    selected_vis = request.form.get('select_vis')
    
    common_file_name = drs_file.split('/')[-1].split('_drs')[0]

    brat_url = BRAT_TEXT2STORY_URL + common_file_name

    print('DRS file:', drs_file)

    if selected_vis == 'ann_text':
        vis = 'ann_text'
        ann_file = os.path.join(BRAT_ANN_DIR, common_file_name + '.ann')
        with open(ann_file, 'r') as fp:
            ann_text = fp.readlines()
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, text=ann_text)

    elif selected_vis == 'drs_text':
        vis = 'drs_text'
        with open(drs_file, 'r') as fp:
            drs_text = fp.readlines()
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, text=drs_text)

    elif selected_vis == 'msc':
        vis = 'msc'
        msc = parser.get_msc_data(drs_file)
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, msc=msc)

    elif selected_vis == 'graph':
        vis = 'graph'
        actors, non_ev_rels, ev_rels = parser.get_graph_data(drs_file)
        actors = json.dumps(actors)
        non_ev_rels = json.dumps(non_ev_rels)
        ev_rels = json.dumps(ev_rels)
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, actors=actors, non_ev_rels=non_ev_rels, ev_rels=ev_rels)

    elif selected_vis == 'icons':
        vis = 'icons'
        actors_dict_pt, actors_dict_en, actors_filtered, actors_in_event, actors_list, events_dict, actors_in_event_des = parser.get_actors_data(drs_file)
        icons_data, tuples = parser.get_icons_data(actors_filtered)
        actors_in_event_img = parser.get_icons_data_img(actors_in_event_des)
        sentences = parser.parse_sentences(drs_file)
        actors_in_sentences = parser.get_actors_in_sentences(sentences,actors_dict_pt)
        actors_in_sentences_des = parser.get_dict_descriptions(actors_in_sentences,actors_filtered,sentences)
        actors_in_sentences_img = parser.get_icons_data_img(actors_in_sentences_des)
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, actors_dict_pt=actors_dict_pt, actors_dict_en=actors_dict_en, actors_filtered=actors_filtered, actors_in_event=actors_in_event, actors_list=actors_list, tuples=tuples, icons_data=icons_data,events_dict=events_dict,actors_in_event_des=actors_in_event_des,actors_in_event_img=actors_in_event_img,sentences=sentences,actors_in_sentences=actors_in_sentences,actors_in_sentences_img=actors_in_sentences_img)

    # Default
    else:
        vis = 'news_text'
        news_file = os.path.join(BRAT_ANN_DIR, common_file_name + '.txt')
        with open(news_file, 'r') as fp:
            news_text = fp.readlines()
        return render_template('index.html', drs_files=drs_files, selected_drs=drs_file, brat_url=brat_url, selected_vis=vis, text=news_text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5055, debug=True)
