# Text2Icons

## Usage

It is recommended to run the project on a python virtual environment.

1) Install requirements.txt;
2) Download 'wiki-news-300d-1M-subword.bin' (https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.bin.zip) and save under *drs2viz*.

### BRAT2DRS

1) Change directory to *brat2drs*
2) Run **brat2drs.py**
            
    * Creates drs representations, under *drs_files*, from the files under *text_2_story_new*. 
    * Extracts sentences, under *sentences*, from the original news stories under *text_2_story_new*.

### DRS2VIZ

1) Change directory to *drs2viz*
2) Run npm init && npm install vis-network
4) Run **app.py**

    * Starts a flask server running the representations on http://localhost:5055/brat2viz


## Icon Visualization

The Icon Dictionary used for the Icon Visualization contains the classes and methods to search for icons to use in the visualization of the Text2Story pipeline.
Icons are searched by terms, adding a new icon when that term does not yet have an icon that represents it in the dictionary. 

### Dictionary Construction:
* **Semi-automatic:** User chooses the icon to be saved in the icon dictionary by selecting one from the list of corresponding icons obtained by searching the icon sources.

* **Automatic (used by default):** Choice made using fastText(https://fasttext.cc) models to obtain embeddings for any word. From the icon lists obtained from the searches in the icon sources, the cosine similarity between the searched term and each element of the lists is calculated to choose the icon that is most similar to the one searched for, so that it can be saved in the icon dictionary.

### Icon sources:

#### APIs

1) emojidex
    * https://developer.emojidex.com/#api
2) IconFinder
    * https://developer.iconfinder.com/reference/overview-1
3) Icons8
    * https://developers.icons8.com/docs/getting-started
4) OpenEmoji
    * Cannot save images;
    * https://emoji-api.com/#documentation
            
#### Datasets

1) Icons-50
    * https://www.kaggle.com/danhendrycks/icons50
2) ImageNet - using Tiny Imagenet(Stanford CS231N)
    * http://image-net.org/index

### Translation available with:

1) Hugging Face Transformers - https://github.com/huggingface/transformers

2) Google Translate API (used by default) - https://pypi.org/project/googletrans/

### Icon Information:
Information saved under *drs2viz/icon_info.json*, and the icon images under *drs2viz/static/icon_images*.
* **icon_info.json** -  File that stores information about the icons: 
    - *keyterm*, keyterm of the icon; 
    - *variants*, list of associated/synonymous terms;
    - *img*, the file name of the icon image;
    - *source*, indicates the source where the icon was fetched;
    - *icon_type*, indicates what type of icon was saved in relation to the search term (most similar).

## Search for opposite icons
For evaluation purposes, a dictionary of opposite icons was built automatically. The information is saved under *drs2viz/icon_opposite_info.json*, and the opposite icon images are saved under *drs2viz/static/opposites_images*.

* **icon_opposite_info.json** -  File that stores information about the opposite icons: 
    - *term*, searched term to get an opposite icon;
    - *keyterm*, keyterm of the opposite icon;
    - *img*, the file name of the opposite icon image;
    - *source*, indicates the source where the opposite icon was fetched;
    - *icon_type*, indicates what type of icon was saved in relation to the search term (least similar or second most similar).

To see the news stories with the opposite icons it is necessary to comment and uncomment code in the files: *drs2viz/parser.py* and *drs2viz/templates/icons.html* (described in the respective files what to do).