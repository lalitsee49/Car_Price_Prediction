from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


#standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    
    Fuel_Type_Diesel=0
    Fuel_Type_LPG=0
    
    if request.method == 'POST':
        Year = int(request.form['Year'])
        car_age = 2021-Year
        Kilometers_Driven=int(request.form['Kilometers_Driven'])
        Mileage=float(request.form['Mileage'])
        Power=float(request.form['BHP'])
        Seats=float(request.form['Seats'])
        
        Owner_Type_Second=request.form['Owner']
        if(Owner_Type_Second=='Second'):
            Owner_Type_Second=1
            Owner_Type_Third=0
            Owner_Type_Fourth_and_Above=0
                
        elif(Owner_Type_Second=='Third'):
            Owner_Type_Second=0
            Owner_Type_Third=1
            Owner_Type_Fourth_and_Above=0
            
        else:
            Owner_Type_Second=0
            Owner_Type_Third=0
            Owner_Type_Fourth_and_Above=1
        
        Fuel_Type_Petrol=request.form['Fuel Type']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=0
                
        elif(Fuel_Type_Petrol=='LPG'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=1
            
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Type_LPG=0
            
        
        Transmission_Manual=request.form['Transmission Type']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
            
        prediction=model.predict([[Kilometers_Driven,Mileage,Power,Seats,car_age,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Transmission_Manual,Owner_Type_Fourth_and_Above,Owner_Type_Second,Owner_Type_Third]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="Based on details submitted your car's selling price is {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)