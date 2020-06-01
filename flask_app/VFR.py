import pandas as pd
import pickle as pkl
from sklearn.neighbors import NearestNeighbors
import numpy as np

def extract_profile(prof,l):
    ll = []
    for i in l:
        if i not in prof:
            ll.append(i)
    ll.append("skills")
    return ll



def profilw(e,profile,l):


    switcher={
                "web_back_end":["JavaScript","SQL","NoSQL","Node.js","Express.js","Koa.js","Hapi.js","AngularJS","Reactjs","jQuery","Nginx"],
                "Developpeur Front-End":["JavaScript","HTML","CSS","REST","Reactjs","SASS","GIT","AngularJS","jQuery","Nginx"],
                "Développeur PHP/Symfony":["PHP","Symfony","Architecture_RESTful","GIT"],
                3:'Wednesday',
                4:'Thursday',
                5:'Friday',
                6:'Saturday'
             }


    back = e.copy(deep=True)
    back = back.drop(columns=["url","name","location","experiences"])
    back = back.drop(columns=extract_profile(switcher.get(profile,"Invalid profile"),l))
    back = back.drop(columns=["certifications","nbre_languages","honors","organizations","nbre_projet"])
    back["Tenure"]= back["Tenure"].apply(lambda x : 5*x)
    return back


def Model_ONE_IA(n_neighbor,backv):
    nbrs = NearestNeighbors(n_neighbors=n_neighbor,algorithm='ball_tree').fit(backv)
    a = np.full(shape=backv.shape[1],fill_value=2)
    #print(nbrs.kneighbors([a]))
    return nbrs.kneighbors([a])
