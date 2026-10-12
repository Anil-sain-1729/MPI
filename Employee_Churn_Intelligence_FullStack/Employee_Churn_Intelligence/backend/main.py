from pathlib import Path
import json, joblib, pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"data"/"employee_churn_sample.csv"
ART=ROOT/"backend"/"artifacts"; ART.mkdir(exist_ok=True)
MODEL=ART/"employee_churn.joblib"; METRICS=ART/"metrics.json"
NUM=["Age","MonthlyIncome","DistanceFromHome","YearsAtCompany","YearsInCurrentRole","YearsSinceLastPromotion","YearsWithCurrManager","OverTime","JobSatisfaction","WorkLifeBalance","EnvironmentSatisfaction","JobInvolvement","TrainingTimesLastYear","NumCompaniesWorked"]
CAT=["Department","JobRole","BusinessTravel","MaritalStatus","EducationField"]
FEATURES=NUM+CAT
app=FastAPI(title="Employee Churn Intelligence API")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

def train():
    if MODEL.exists() and METRICS.exists(): return
    d=pd.read_csv(DATA); X=d[FEATURES]; y=d.Attrition.astype(str)
    xt,xv,yt,yv=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    prep=ColumnTransformer([
      ("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),NUM),
      ("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]),CAT)])
    pipe=Pipeline([("prep",prep),("model",RandomForestClassifier(n_estimators=200,class_weight="balanced",min_samples_leaf=3,random_state=42,n_jobs=-1))])
    pipe.fit(xt,yt); pred=pipe.predict(xv); classes=list(pipe.named_steps["model"].classes_)
    pp=pipe.predict_proba(xv)[:,classes.index("Yes")]
    m={"accuracy":round(float(accuracy_score(yv,pred)),3),"precision_yes":round(float(precision_score(yv,pred,pos_label="Yes",zero_division=0)),3),"recall_yes":round(float(recall_score(yv,pred,pos_label="Yes",zero_division=0)),3),"f1_yes":round(float(f1_score(yv,pred,pos_label="Yes",zero_division=0)),3),"roc_auc":round(float(roc_auc_score((yv=="Yes").astype(int),pp)),3),"note":"Synthetic demo data only; not real-world performance."}
    joblib.dump(pipe,MODEL); METRICS.write_text(json.dumps(m,indent=2))
@app.on_event("startup")
def startup(): train()

class Employee(BaseModel):
    Age:int=Field(35,ge=18,le=80); MonthlyIncome:float=Field(5000,ge=0)
    DistanceFromHome:int=5; YearsAtCompany:int=5; YearsInCurrentRole:int=3
    YearsSinceLastPromotion:int=1; YearsWithCurrManager:int=3; OverTime:int=Field(0,ge=0,le=1)
    JobSatisfaction:int=Field(3,ge=1,le=4); WorkLifeBalance:int=Field(3,ge=1,le=4)
    EnvironmentSatisfaction:int=Field(3,ge=1,le=4); JobInvolvement:int=Field(3,ge=1,le=4)
    TrainingTimesLastYear:int=2; NumCompaniesWorked:int=2
    Department:str="Research & Development"; JobRole:str="Research Scientist"
    BusinessTravel:str="Travel_Rarely"; MaritalStatus:str="Single"; EducationField:str="Life Sciences"

@app.get("/")
def root(): return {"app":"Employee Churn Intelligence","docs":"/docs"}
@app.get("/api/overview")
def overview():
    d=pd.read_csv(DATA); m=json.loads(METRICS.read_text())
    rates=d.groupby("Department").Attrition.apply(lambda x:round(100*(x=="Yes").mean(),1)).to_dict()
    yes=int((d.Attrition=="Yes").sum())
    return {"total":len(d),"attrition_count":yes,"attrition_rate":round(100*yes/len(d),1),"department_rates":rates,"metrics":m,"note":"Synthetic demo data."}
@app.post("/api/predict")
def predict(e:Employee):
    pipe=joblib.load(MODEL); row=pd.DataFrame([e.model_dump()])[FEATURES]
    classes=list(pipe.named_steps["model"].classes_); score=float(pipe.predict_proba(row)[0][classes.index("Yes")])
    hints=[]
    if e.OverTime: hints.append("Overtime is marked Yes")
    if e.JobSatisfaction<=2: hints.append("Low job-satisfaction rating")
    if e.WorkLifeBalance<=2: hints.append("Low work-life-balance rating")
    if e.YearsSinceLastPromotion>=4: hints.append("Several years since last promotion")
    if not hints: hints=["No simple rule-based indicator triggered"]
    return {"risk_percent":round(score*100,1),"predicted_class":"Higher estimated risk" if score>=.5 else "Lower estimated risk","indicators":hints,"caution":"Synthetic demo estimate only, not a fact or causal explanation. Never use for firing, hiring, promotion, pay, or other adverse employment decisions."}
