from Models.Mods import Mods
import pickle as pkl
model = Mods()
import pandas as pd






def d_data_f():
    with open(r"finaldf_2.pkl", "rb") as input_file:
        data = pkl.load(input_file)
        
    model.fit(data=data)
    
    

    
def d_model(i,cols):
    switcher={
                "web_back_end": model.backend,
                "Developpeur Front-End":model.frontend,
                'embarque':model.embarque,
                'tech_jee':model.tech_jee,
                'fullstack':model.fullstack,
                'jee':model.jee,
                'symfony':model.symfony,
                'drupal':model.drupal,
                'product_owner':model.product_owner
        
             }
    
    return model.extract_profile(switcher.get(i,"Invalid day of week"),cols)



