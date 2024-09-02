from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from utils import functions 
app = Flask(__name__, template_folder='views')
print(os.path.abspath(os.getcwd()))
path_model= os.path.join('..', 'model', 'model_svm.pkl')

model = pickle.load(open(path_model, 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Pega os dados do formulário
    data = [
        float(request.form['balance_divided_creditlimit']),
        int(request.form['age']),
        float(request.form['DebtRatio']),
        float(request.form['MonthlyIncome']),
        int(request.form['NumberOfOpenCreditLinesAndLoans']),
        int(request.form['NumberOfTimes90DaysLate']),
        int(request.form['NumberRealEstateLoansOrLines']),
        int(request.form['number_times_latepay60-89']),
        int(request.form['NumberOfDependents'])
    ]
    print(data)
    data = np.array([data])
    
    

    
    prediction = model.predict(data)

    
    return render_template('result.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
