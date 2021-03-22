from flask import Flask , render_template , request
import pandas as pd
import pickle
app =Flask(__name__,template_folder='templates')
route="/"
@app.route(route,methods = ["GET","POST"])
def home():
    wind_col=['E','ENE','ESE','N','NE','NNE','NNW','NW','S','SE','SSE','SSW','SW','W','WNW','WSW']
    rain_tod_col=["Yes","No"]
    var="Veuillez entrer les valeurs"
    prediction=""
    if request.method == "POST":
        with open("best_models_per_loc","rb") as file:
            data=pickle.load(file)
        with open("list_col","rb") as file:
            list_col=pickle.load(file)
        location= request.form.get("location")
        date= request.form.get("Date")
        MinTemp_= request.form.get("MinTemp")
        MaxTemp_= request.form.get("MaxTemp")
        Rainfall_= request.form.get("Rainfall")
        WindGustDir_= request.form.get("WindGustDir")
        WindGustSpeed_= request.form.get("WindGustSpeed")
        WindDir9am_= request.form.get("WindDir9am")
        WindDir3pm_= request.form.get("WindDir3pm")
        WindSpeed9am_= request.form.get("WindSpeed9am")
        WindSpeed3pm_= request.form.get("WindSpeed3pm")
        Humidity9am_= request.form.get("Humidity9am")
        Humidity3pm_= request.form.get("Humidity3pm")
        Pressure9am_= request.form.get("Pressure9am")
        Pressure3pm_= request.form.get("Pressure3pm")
        Temp9am_= request.form.get("Temp9am")
        Temp3pm_= request.form.get("Temp3pm")
        RainToday_= request.form.get("RainToday")
        try:
            sc=data[location]["scaler"]
            model=data[location]["estimator"]
            col=list_col[location]
        except:
            return render_template("html_test.html",returned="location non existante,merci de verifier")
        try:
            month={1:"Janvier",2:"Fevrier",3:"Mars",4:"Avril",5:"Mai",6:"Juin",7:"Juillet",8:"Aout",9:"Septembre",10:"Octobre",11:"Novembre",12:"Decembre"}
            date=pd.Series(pd.to_datetime(date,format="%Y-%m-%d").month).map(month)[0]
            date=[[date]]
            df=pd.DataFrame(date,columns=["Month"])
        except:
            return render_template("html_test.html",returned="date format doit etre YYY-MM-DD")
        if WindGustDir_ in wind_col:
            df["WindGustDir"]=WindGustDir_
        else:
            return render_template("html_test.html",returned="WindGustDir doit etre dans:"+str(wind_col))
        if WindDir9am_ in wind_col:
            df["WindDir9am"]=WindDir9am_
        else:
            return render_template("html_test.html",returned="WindDir9am doit etre dans:"+str(wind_col))
        if WindDir3pm_ in wind_col:
            df["WindDir3pm"]=WindDir3pm_
        else:
            return render_template("html_test.html",returned="WindDir3pm_ doit etre dans:"+str(wind_col))
        if RainToday_ in rain_tod_col:
            df["RainToday"]=RainToday_
        else:
            return render_template("html_test.html",returned="RainToday_ doit etre dans:"+str(rain_tod_col))
        try:
            df["MinTemp"]=float(MinTemp_)
        except:
            return render_template("html_test.html",returned="MinTemp doit etre de type float")
        try:
            df["MaxTemp"]=float(MaxTemp_)
        except:
            return render_template("html_test.html",returned="MaxTemp doit etre de type float")
        try:
            df["Rainfall"]=float(Rainfall_)
        except:
            return render_template("html_test.html",returned="Rainfall doit etre de type float")
        try:
            df["WindGustSpeed"]=float(WindGustSpeed_)
        except:
            return render_template("html_test.html",returned="WindGustSpeed doit etre de type float")
        try:
            df["WindSpeed9am"]=float(WindSpeed9am_)
        except:
            return render_template("html_test.html",returned="WindSpeed9am doit etre de type float")
        try:
            df["WindSpeed3pm"]=float(WindSpeed3pm_)
        except:
            return render_template("html_test.html",returned="WindSpeed3pm doit etre de type float")
        try:
            df["Humidity9am"]=float(Humidity9am_)
        except:
            return render_template("html_test.html",returned="Humidity9am_ doit etre de type float")
        try:
            df["Humidity3pm"]=float(Humidity3pm_)
        except:
            return render_template("html_test.html",returned="Humidity3pm doit etre de type float")
        try:
            df["Humidity3pm"]=float(Humidity3pm_)
        except:
            return render_template("html_test.html",returned="Humidity3pm doit etre de type float")
        try:
            df["Pressure9am"]=float(Pressure9am_)
        except:
            return render_template("html_test.html",returned="Pressure9am doit etre de type float")
        try:
            df["Pressure3pm"]=float(Pressure3pm_)
        except:
            return render_template("html_test.html",returned="Pressure3pm_ doit etre de type float")
        try:
            df["Temp9am"]=float(Temp9am_)
        except:
            return render_template("html_test.html",returned="Temp9am_ doit etre de type float")
        try:
            df["Temp3pm"]=float(Temp3pm_)
        except:
            return render_template("html_test.html",returned="Temp3pm doit etre de type float")
        df=df[['MinTemp','MaxTemp','Rainfall','WindGustDir','WindGustSpeed','WindDir9am','WindDir3pm','WindSpeed9am','WindSpeed3pm','Humidity9am','Humidity3pm','Pressure9am','Pressure3pm','Temp9am','Temp3pm','RainToday','Month']]
        df=pd.get_dummies(df)
        for c in col:
          if c not in df.columns:
               df[c] = 0
        df=df[col]
        print(df)
        X = data[location]["scaler"].transform(df)
        prediction=data[location]["estimator"].predict(X)
        print("prediction:",prediction)
        if prediction == 1:
            var="Il va pleuvoir demain en "+location
        elif prediction == 0:
            var="Il ne va pas pleuvoir demain en "+location
    return render_template("html_test.html",returned=var)
        
            
    
if __name__ == "__main__":
    app.run(debug=True)
