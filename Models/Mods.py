import pandas as pd
import numpy as np


class Mods:
    def __init__(self):
        self.raw_data = None
        self.data = None
        self.skills = None

        self.l_backend = ["JavaScript", "SQL", "NoSQL", "Node.js", "Express.js","Koa.js", "Hapi.js", "AngularJS", "Reactjs", "jQuery", "Nginx"]
        self.l_frontend = ["JavaScript", "HTML","CSS", "REST", "Reactjs", "SASS", "Webpack", "Gitlab"]
        self.l_embarque = ["C", "C++", "Linux", "Embedded_C++", "Embedded_C"]
        self.l_tech_jee = ["Java", "JEE", "Microservices", "Integration_continue", "Docker", "AWS"]
        self.l_fullstack = ["Node.js", "JavaScript", "AngularJS","jQuery", "HTML", "CSS", "MongoDB", "MySQL"]
        self.l_jee = ["Java", "JEE", "Spring", "SOA", "SOAP", "REST", "Microservices", "GIT", "SVN", "Confluence", "Spring", "Java"]
        self.l_symfony = ["PHP", "Symfony", "GIT", "Architecture_RESTful"]
        self.l_drupal = ["PHP", "CMS", "HTML", "Drupal", "HTML", "CSS", "MySQL", "Symfony", "JavaScript", "GIT"]
        self.l_product_owner = ["Scrum", "Testing"]

        self.backend = ["self.l_backend", "self.d_backend"]
        self.frontend = ["self.l_frontend", "self.d_frontend"]
        self.embarque = ["self.l_embarque", "self.d_embarque"]
        self.tech_jee = ["self.l_tech_jee", "self.d_tech_jee"]
        self.fullstack = ["self.l_fullstack", "self.d_fullstack"]
        self.jee = ["self.l_jee", "self.d_jee"]
        self.symfony = ["self.l_symfony", "self.d_symfony"]
        self.drupal = ["self.l_drupal", "self.d_drupal"]
        self.product_owner = ["self.l_product_owner", "self.d_product_owner"]

        self.map_backend = {
            'AngularJS': 1,            'C++': 1,            'C': 1,            'Express.js': 3,            'JavaScript': 1,            'jQuery': 1,            'Koa.js': 1,            'Hapi.js': 1,            'Nginx': 1,            'Node.js': 3,            'NoSQL': 2,            'Reactjs': 1,            'SQL': 3        }

        self.map_frontend = {            'CSS': 3,            'Gitlab': 1,            'HTML': 3,            'JavaScript': 3,            'Reactjs': 3,            'REST': 3,            'SASS': 1,            'Webpack': 1        }

        self.map_embarque = {            'C': 2,            'C++': 2,            'Linux': 3,            'Embedded_C': 3,            'Embedded_C++': 3        }

        self.map_tech_jee = {            'Java': 3,            'JEE': 3,            'Microservices': 3,            'Integration_continue': 3,            'Docker': 3,            'AWS': 3        }

        self.map_fullstack = {            'Node.js': 3,            'JavaScript': 3,            'AngularJS': 3,            'Ext.js': 3,            'jQuery': 2,            'HTML': 2,            'CSS': 2,            'MongoDB': 2,            'MySQL': 2        }

        self.map_jee = {            'Confluence': 1,            'GIT': 2,            'Java': 3,            'JEE': 3,            'Microservices': 3,            'REST': 1,            'SOAP': 1,            'SOA': 1,            'Spring': 3,            'SVN': 2        }

        self.map_symfony = {            'PHP': 2,            'Symfony': 2,            'Architecture_RESTful': 3,            'GIT': 3        }

        self.map_drupal = {            'PHP': 3,            'CMS': 1,            'Drupal': 3,            'HTML': 1,            'CSS': 1,            'MySQL': 1,            'Symfony': 2,            'JavaScript': 2,            'GIT': 2        }

        self.map_product_owner = {            'Scrum': 3,            'Testing': 3        }

        self.d_backend = None
        self.d_frontend = None
        self.d_embarque = None
        self.d_tech_jee = None
        self.d_fullstack = None
        self.d_jee = None
        self.d_symfony = None
        self.d_drupal = None
        self.d_product_owner = None

        self.l_prof = ["self.l_backend", "self.l_frontend", "self.l_embarque", "self.l_tech_jee",
                       "self.l_fullstack", "self.l_jee", "self.l_symfony", "self.l_drupal", "self.l_product_owner"]
        
        self.scores = None
        self.idx = None
        
    def fit(self,data):

        self.raw_data = data.copy(deep=True)
        self.data = data
        l = []
        for i in range(len(self.data)):
            for j in self.data["skills"][i][0]:
                l.append(j)
                l = list(set(l))
        
        self.skills = l

        for s in self.skills:
            self.data[s]=0
        
        for i in range(len(self.data)):
            for s in self.data["skills"][i][0]:
                self.data[s][i] = self.data["skills"][i][1][self.data["skills"][i][0].index(s)]
            

    def extract_profile(self, profile,cols=[]):
        ll = []
        for i in self.skills:
            if i not in eval(profile[0]):
                ll.append(i)
        ll.append("skills")
        
        n_data = self.data.copy(deep=True)
        n_data = n_data.drop(columns = ["url","name","location"])
        n_data = n_data.drop(columns = ll)

        #We can remove this when we add it 
        # n_data = n_data.drop(columns=[
        #                      "certifications", "nbre_languages", "honors", "organizations", "nbre_projet"])
        cols2 = ["certifications", "nbre_languages", "honors", "organizations", "nbre_projet","Tenure"]
        cols3 = []
        for i in cols2:
            if i not in cols:
                cols3.append(i)
        
        n_data = n_data.drop(columns = cols3)        
        
        exec(profile[1]+"= n_data")
    
    def k_best(self, profile, k, colz=[]):
        score_t = [[]]
        self.extract_profile(profile=profile,cols=colz)
        dats = eval(profile[1])

        for i in range(len(dats.columns)):
            score_t[0].append(2)

        from sklearn.neighbors import NearestNeighbors
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(dats)
        score,idx = nbrs.kneighbors(score_t)
        print("Scores : ",*score)
        print("Indexes :",*idx)
        self.scores = score
        self.idx = idx
        #return score,idx  
    
    def show_raw(self):
        return self.raw_data.iloc[self.idx[0],:]
    
    def show_raw_profile(self):
        tab = self.raw_data
        tab["Profil Conseillé"] = tab.index
        tab.index = np.array(tab.index.to_series().apply(
            lambda x: '<a href="displ/{0}">Afficher</a>'.format(x)))
        tab["Profil Conseillé"] = tab["Profil Conseillé"].apply(
            lambda x: '<a href="prof/{0}">Score par profil</a>'.format(x))
        tab = tab.drop(columns=["skills", "certifications", "nbre_languages",
                                "honors", "organizations", "nbre_projet", "Tenure"])
        return tab
    
    def show_raw_clean(self):
        tab = self.raw_data.iloc[self.idx[0], :].drop(
            columns=["skills", "location", "certifications", "nbre_languages", "honors", "organizations", "nbre_projet", "Tenure"])
        tab["Rang"]=0
        s=0
        for i in self.idx[0]:
            s+=1
            tab.at[i,"Rang"]=s
        tab.index = np.array(tab.index.to_series().apply(
            lambda x: '<a href="displ/{0}">Afficher</a>'.format(x)))
        return tab

    def show(self):
        return self.d_backend.iloc[self.idx[0],:]

    def get_profile(self,idx):
        # If a problem occurs in this function please check the names in the definition (skills names)

        n_data = self.data.copy(deep=True)
        n_data = n_data.drop(columns=["url", "name", "location","skills"])

        #We can remove this when we add it
        n_data = n_data.drop(columns=[
                             "certifications", "nbre_languages", "honors", "organizations", "nbre_projet"])
        
        s = []
        for i in self.l_prof:
            ss = 0
            for j in eval(i):
                ss = ss + n_data.iloc[idx][j]
            s.append(ss)
        
        for i in range(len(self.l_prof)):
            print(self.l_prof[i]," : ",s[i])
    
    def get_profile_clean(self, idx):
        # If a problem occurs in this function please check the names in the definition (skills names)

        n_data = self.data.copy(deep=True)
        n_data = n_data.drop(columns=["url", "name", "location", "skills"])

        #We can remove this when we add it
        n_data = n_data.drop(columns=[
                             "certifications", "nbre_languages", "honors", "organizations", "nbre_projet"])

        s = []
        for i in self.l_prof:
            ss = 0
            for j in eval(i):
                ss = ss + n_data.iloc[idx][j]
            s.append(ss)

        dic = {}
        for i in range(len(self.l_prof)):
            dic[self.l_prof[i]] = s[i]
            #print(self.l_prof[i], " : ", s[i])
        return dic
            












        

    
    


    


       
