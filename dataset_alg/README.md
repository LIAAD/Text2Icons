# Evaluate the algorithm that finds the most specific description of an ACTOR

Dataset built to facilitate the evaluation of the algorithm, allowing to run several examples of news stories at the same time.

1) **news2json.py** creates two datasets with the information of a news set containing the ACTOR's descriptions and the respective more specific correct descriptions:
    - **news_info_google.json**, using translations obtained with the Google Translate API;
    - **news_info_hugg.json**, using translations obtained with the Hugging Face Transformers;

2) **process.py** runs the algorithm, stored in **alg.py**, and compares the result returned by the algorithm with the correct result stored in the datasets. 


For each news story are counted:
- the number of ACTORs present in each news story;
- the number of well defined ACTORs by the algorithm;
- the number of wrongly defined ACTORs by the algorithm;
- the number of undefined ACTORs by the algorithm;
- the total number of all previous counts.