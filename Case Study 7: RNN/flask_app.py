import pandas as pd
import pickle
import numpy as np
import json
from flask import jsonify,request

class flask_model:

    def __init__(self,model_file):
        self.model_file = model_file
        self.data = None
        self.output = None
        try:
            with open(model_file,'rb') as f:
                self.model = pickle.load(f)
        except:
            print(f'E:Given model name of {self.model_file} was not found')
            
    def load_data(self,json_data):
        try:
            self.data = pd.read_json(json_data,orient='records')
        except:
            self.data = pd.DataFrame([json_data])

    def predict(self):
        self.output = self.model.predict_proba(self.data)

    def make_return(self):
        name = np.argmax(self.output)
        species = ['setosa','versicolor','virginica']
        return jsonify(
            Probabilities =self.output.tolist(),
            Class = species[name]
        )

    new = flask_model('iris.model')

    @app.route('/')
    def hello():
        return ('Hello, world')
        
    @app.route('/predict'/methods=(['POST']))
    def test():
            content = request.get_data()
            new.load_data(content)
            new.predict()
            out = new.make_return()
            return out

    if __name__ == '__main__':
        app.rum(debug=True,host='0.0.0.0',port=1313)
