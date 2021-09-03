import json 
import alg as alg

with open('news_info_google.json', 'r') as j:
    news_data_google = json.load(j)

with open('news_info_hugging.json', 'r') as k:
    news_data_hugg = json.load(k)

def countA(data):
    list = []
    ta = 0   # total number of actors
    tc = 0   # total number of well-defined
    tw = 0   # total number of wrongly defined 
    tu = 0   # total number of undefined

    for news in data:
        a = 0   # number of actors
        c = 0   # number of well-defined
        w = 0   # number of wrongly defined 
        u = 0   # number of undefined

        # dict of actor descriptions
        original = data[news][0]

        # dict of correct most specific actor descriptions
        c_res = data[news][1]

        # dict after being processed by the algorithm (most specific descriptions)
        a_res = alg.filter_actors(original)

        # check for wrong and undefined descriptions
        for actor in original:
            a = a + 1
            if a_res[actor] == '':
                u = u + 1
            elif a_res[actor] != c_res[actor]:
                w = w + 1
        
        c = a - w - u

        ta = ta + a
        tc = tc + c
        tw = tw + w
        tu = tu + u

        list.append((news,a,c,w,u))

    list.append(('Total',ta,tc,tw,tu))

    print(list)

print("Google Translate Results:")
countA(news_data_google)
print("Hugging Face Transformers Results:")
countA(news_data_hugg)