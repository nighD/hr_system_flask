from flask import Flask, render_template,request, url_for
import os
import json
import plotly
import xlrd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
import numpy as np
from scipy.stats import norm, skew
from scipy import stats
import statsmodels.api as sm
from flask import jsonify
from flask_cors import CORS
import pickle
from pandas.io.json import json_normalize
plotly.tools.set_credentials_file(username='nightD', api_key='0oUTeVklfkuokQa0s7mM')
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Load data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
df_sourcefile = pd.read_excel('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/data/WA_Fn-UseC_-HR-Employee-Attrition.xlsx', sheet_name=0)
df_HR = df_sourcefile.copy()

df_attrition_predict = pd.read_excel('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/data/unseen_attrition.xlsx', sheet_name=0)
df_attrition_predict_target = pd.read_excel('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/data/target_unseen_attrition.xlsx', sheet_name=0)

df_fraud_predict = pd.read_excel('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/data/unseen_fraud.xlsx', sheet_name=0)
df_fraud_predict_target = pd.read_excel('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/data/target_unseen_fraud.xlsx', sheet_name=0)

unseen_attrition = df_attrition_predict.copy()
unseen_target_attrition = df_attrition_predict_target.copy()

unseen_fraud = df_fraud_predict.copy()
unseen_target_fraud = df_fraud_predict_target.copy()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Load the model
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
model_attrition = pickle.load(open('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/model/attrition.pkl','rb'))
model_fraud = pickle.load(open('/Users/mac/Desktop/Night/RMIT VietNam After Mel/Sem 2/Capstone_Project_B/HR_Web_Based/test_flask/model/fraud.pkl','rb'))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get Unseen Data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/unseen_data')
def get_unseen_data():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "DataUnseen.json")
    data = json.load(open(json_url))
    return json.dumps(data)

@app.route('/unseen_data_attrition')
def get_attrition_unseen_data():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Attrition.json")
    data = json.load(open(json_url))
    return json.dumps(data)

@app.route('/unseen_data_fraud')
def get_fraud_unseen_data():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Fraud.json")
    data = json.load(open(json_url))
    return json.dumps(data)

@app.route('/unseen_target_attrition')
def get_attrition_unseen_target():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Target_Attrition.json")
    data = json.load(open(json_url))
    return json.dumps(data)

@app.route('/unseen_target_fraud')
def get_fraud_unseen_target():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Target_Fraud.json")
    data = json.load(open(json_url))
    return json.dumps(data)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Find Unseen Data By ID
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def CheckRange(s):
    try:
        a = int(s)
        if 0 < a and a < 69:
            return True
        else :
            return False
    except:
        return False
        
@app.route('/find_unseen_data/<id>')
def find_unseen_data(id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "DataUnseen.json")
    data = json.load(open(json_url))
    if RepresentsInt(id) :
        if CheckRange(id):
            return json.dumps(data[int(id)])
        else : 
            return "Out of Range"
    else :
        return "Not a Integer"


@app.route('/find_unseen_data_attrition/<id>')
def find_attrition_unseen_data(id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Attrition.json")
    data = json.load(open(json_url))
    if RepresentsInt(id) and CheckRange(id):
        return json.dumps(data[int(id)])
    else :
        return "Not a Integer"

@app.route('/find_unseen_data_fraud/<id>')
def find_fraud_unseen_data(id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Fraud.json")
    data = json.load(open(json_url))
    if RepresentsInt(id) and CheckRange(id):
        return json.dumps(data[int(id)])
    else :
        return "Not a Integer"

@app.route('/find_unseen_target_attrition/<id>')
def find_attrition_unseen_target(id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Target_Attrition.json")
    data = json.load(open(json_url))
    if RepresentsInt(id) and CheckRange(id):
        return json.dumps(data[int(id)])
    else :
        return "Not a Integer"

@app.route('/find_unseen_target_fraud/<id>')
def find_fraud_unseen_target(id):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Unseen_Target_Fraud.json")
    data = json.load(open(json_url))
    if RepresentsInt(id) and CheckRange(id):
        return json.dumps(data[int(id)])
    else :
        return "Not a Integer"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Predict
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/predict',methods=['POST'])
def predict():
    print (request.is_json)
    content = request.get_json(force=True)
    prediction = model_fraud.predict(np.array(json_normalize(content)))
    output = prediction[0]
    print(output)
    return "done"
    
@app.route('/predict_attrition/<id>')
def predict_attrition(id):
    if RepresentsInt(id) :
        if CheckRange(id):
            data_actual_attrition = unseen_attrition.iloc[int(id),:]
            actual_result_attrition = unseen_target_attrition.iloc[int(id),:]
            prediction_attrition = model_attrition.predict(np.array(data_actual_attrition).reshape(1, -1))
            output_attrition = prediction_attrition[0]
            x = {
                "Actual Result":int(np.array(actual_result_attrition)),
                "Predict Result":int(output_attrition)
            }
            y = json.dumps(x)

            return y
        else : 
            return "Out of Range"
    else :
        return "Not a Integer"

@app.route('/predict_fraud/<id>')
def predict_fraud(id):
    if RepresentsInt(id) :
        if CheckRange(id):
            data_actual_fraud = unseen_fraud.iloc[int(id),:]
            actual_result_fraud = unseen_target_fraud.iloc[int(id),:]
            prediction_fraud = model_fraud.predict(np.array(data_actual_fraud).reshape(1, -1))
            output_fraud = prediction_fraud[0]
            x = {
                "Actual Result":int(np.array(actual_result_fraud)),
                "Predict Result":int(output_fraud)
            }
            y = json.dumps(x)

            return y
        else : 
            return "Out of Range"
    else :
        return "Not a Integer"
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Comparison Result
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/comparison_target_attrition')
def compare_target_attrition():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Attrition.json") 
    # print(json_normalize(content))
    data = json.load(open(json_url))
    attrition_compare = json_normalize(data)
    content = attrition_compare['Actual Result'].value_counts()
    target = np.array(content.index)
    frequency = np.array(content.values)
    dic ={}
    dic['target']= target.tolist()
    dic['frequency'] = frequency.tolist()
    back = json.dumps(dic)
    return back

@app.route('/result_attrition')
def result_attrition():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Attrition.json") 
    # print(json_normalize(content))
    data = json.load(open(json_url))
    attrition_compare = json_normalize(data)
    content = attrition_compare['Compare Result'].value_counts()
    result = (content[0]/69)*100
    return str(result)

@app.route('/result_fraud')
def result_fraud():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Fraud.json") 
    # print(json_normalize(content))
    data = json.load(open(json_url))
    attrition_compare = json_normalize(data)
    content = attrition_compare['Compare Result'].value_counts()
    result = (content[0]/69)*100
    return str(result)

@app.route('/comparison_predict_attrition')
def compare_predict_attrition():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Predict_Attrition.json") 
    # print(json_normalize(content))
    data = json.load(open(json_url))
    attrition_compare = json_normalize(data)
    content = attrition_compare['Actual Result'].value_counts()
    target = np.array(content.index)
    frequency = np.array(content.values)
    dic ={}
    dic['target']= target.tolist()
    dic['frequency'] = frequency.tolist()
    back = json.dumps(dic)
    return back

@app.route('/comparison_target_fraud')
def compare_target_fraud():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Fraud.json")
    data = json.load(open(json_url))
    fraud_compare = json_normalize(data)
    content = fraud_compare['Actual Result'].value_counts()
    target = np.array(content.index)
    frequency = np.array(content.values)
    dic ={}
    dic['target']= target.tolist()
    dic['frequency'] = frequency.tolist()
    back = json.dumps(dic)
    return back

@app.route('/comparison_predict_fraud')
def compare_predict_fraud():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "JSON_File", "Comparision_Predict_Fraud.json")
    data = json.load(open(json_url))
    fraud_compare = json_normalize(data)
    content = fraud_compare['Actual Result'].value_counts()
    target = np.array(content.index)
    frequency = np.array(content.values)
    dic ={}
    dic['target']= target.tolist()
    dic['frequency'] = frequency.tolist()
    back = json.dumps(dic)
    return back


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get Columns Name and All data
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/get_columns_name')
def get_columns():
    columns = np.array(df_HR.columns).tolist()
    return json.dumps(columns)
@app.route('/get_data')
def get_datas():
    values = np.array(df_HR.values.tolist())
    columns = np.array(df_HR.columns).tolist()
    arrayRes = {}
    final = []
    for value in values:
        for key,element in enumerate(value):
            # print
            arrayRes[columns[key]]=element

        final.append(arrayRes)
    return json.dumps(final)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data Visualization (Distribution With Target)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/age_distribution')
def data_analysis_age():
    xaxis=np.arange(15, 65, 5)
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'Age']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'Age']
    x1 = np.array(x1)
    x2 = np.array(x2)
    group_labels = ['Active Employees', 'Ex-Employees']
    data = [x1,x2]
     # Create distplot with custom bin_size
    fig = ff.create_distplot(data, group_labels,curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Age Distribution in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[15, 60], dtick=5))
    fig['layout'].update(autosize = True)
    fig.layout['xaxis'].update(automargin= True)
    print()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/education_field')
def data_analysis_ef():
    df_EducationField = pd.DataFrame(columns=["Field", "% of Leavers"])
    i=0
    for field in list(df_HR['EducationField'].unique()):
        ratio = df_HR[(df_HR['EducationField']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['EducationField']==field].shape[0]
        df_EducationField.loc[i] = (field, ratio*100)
        i += 1
        print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_EF = df_EducationField.groupby(by="Field").sum()
    x1 = df_HR['EducationField'].unique()
    y1 = df_EF['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Education Field (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/gender_distribution')
def data_analysis_gender():
    df_Gender = pd.DataFrame(columns=["Gender", "% of Leavers"])
    i=0
    for field in list(df_HR['Gender'].unique()):
        ratio = df_HR[(df_HR['Gender']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['Gender']==field].shape[0]
        df_Gender.loc[i] = (field, ratio*100)
        i += 1
        print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_G = df_Gender.groupby(by="Gender").sum()
    x1 = df_HR['Gender'].unique()
    y1 = df_G['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Gender (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/marital_distribution')
def data_analysis_marital_status():
    df_Marital = pd.DataFrame(columns=["Marital Status", "% of Leavers"])
    i=0
    for field in list(df_HR['MaritalStatus'].unique()):
        ratio = df_HR[(df_HR['MaritalStatus']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['MaritalStatus']==field].shape[0]
        df_Marital.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_MF = df_Marital.groupby(by="Marital Status").sum()
    x1 = df_HR['MaritalStatus'].unique()
    y1 = df_MF['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Marital Status (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/distance_distribution')
def data_analysis_distance():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'DistanceFromHome']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'DistanceFromHome']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(
        title='Distance From Home Distribution in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 30], dtick=2))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    
@app.route('/department')
def data_analysis_department():
    df_Department = pd.DataFrame(columns=["Department", "% of Leavers"])
    i=0
    for field in list(df_HR['Department'].unique()):
        ratio = df_HR[(df_HR['Department']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['Department']==field].shape[0]
        df_Department.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_DF = df_Department.groupby(by="Department").sum()
    x1 = df_HR['Department'].unique()
    y1 = df_DF['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Department (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/busi_travel')
def data_analysis_business_travel():
    df_BusinessTravel = pd.DataFrame(columns=["Business Travel", "% of Leavers"])
    i=0
    for field in list(df_HR['BusinessTravel'].unique()):
        ratio = df_HR[(df_HR['BusinessTravel']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['BusinessTravel']==field].shape[0]
        df_BusinessTravel.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_BT = df_BusinessTravel.groupby(by="Business Travel").sum()
    x1 = df_HR['BusinessTravel'].unique()
    y1 = df_BT['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Business Travel (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/job_role')
def data_analysis_job_role():
    df_JobRole = pd.DataFrame(columns=["Job Role", "% of Leavers"])
    i=0
    for field in list(df_HR['JobRole'].unique()):
        ratio = df_HR[(df_HR['JobRole']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['JobRole']==field].shape[0]
        df_JobRole.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_JR = df_JobRole.groupby(by="Job Role").sum()
    x1 = df_HR['JobRole'].unique()
    y1 = df_JR['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Job Role (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/job_level')
def data_analysis_job_level():
    df_JobLevel = pd.DataFrame(columns=["Job Level", "% of Leavers"])
    i=0
    for field in list(df_HR['JobLevel'].unique()):
        ratio = df_HR[(df_HR['JobLevel']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['JobLevel']==field].shape[0]
        df_JobLevel.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_JL = df_JobLevel.groupby(by="Job Level").sum()
    x1 = df_HR['JobLevel'].unique()
    y1 = df_JL['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Job Level (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/job_involve')
def data_analysis_job_involvement():
    df_JobInvolvement = pd.DataFrame(columns=["Job Involvement", "% of Leavers"])
    i=0
    for field in list(df_HR['JobInvolvement'].unique()):
        ratio = df_HR[(df_HR['JobInvolvement']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['JobInvolvement']==field].shape[0]
        df_JobInvolvement.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_JI = df_JobInvolvement.groupby(by="Job Involvement").sum()
    x1 = df_HR['JobInvolvement'].unique()
    y1 = df_JI['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Job Involvement (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/training_lyear')
def data_analysis_training_lyear():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'TrainingTimesLastYear']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'TrainingTimesLastYear']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(
        title='Training Times Last Year metric in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 6], dtick=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/companies_worked')
def data_analysis_companies_worked():
    df_NumCompaniesWorked = pd.DataFrame(columns=["Num Companies Worked", "% of Leavers"])
    i=0
    for field in list(df_HR['NumCompaniesWorked'].unique()):
        ratio = df_HR[(df_HR['NumCompaniesWorked']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['NumCompaniesWorked']==field].shape[0]
        df_NumCompaniesWorked.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_NC = df_NumCompaniesWorked.groupby(by="Num Companies Worked").sum()
    x1 = df_HR['NumCompaniesWorked'].unique()
    y1 = df_NC['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Num Companies Worked (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/ys_at_company')
def data_analysis_years_at_company():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'YearsAtCompany']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'YearsAtCompany']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Years At Company in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 40], dtick=5))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/ys_in_role')
def data_analysis_years_in_role():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'YearsInCurrentRole']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'YearsInCurrentRole']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Years InCurrent Role in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 18], dtick=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/ys_last_promotion')
def data_analysis_years_last_promotion():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'YearsSinceLastPromotion']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'YearsSinceLastPromotion']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Years Since Last Promotion in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 15], dtick=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/total_work_years')
def data_analysis_total_work_years():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'TotalWorkingYears']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'TotalWorkingYears']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Total Working Years in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 40], dtick=5))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/ys_curr_mana')
def data_analysis_ys_curr_mana():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'YearsWithCurrManager']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'YearsWithCurrManager']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(
        title='Years With Curr Manager in Percent by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 17], dtick=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/wo_li_bala')
def data_analysis_work_life_balance():
    df_WorkLifeBalance = pd.DataFrame(columns=["WorkLifeBalance", "% of Leavers"])
    i=0
    for field in list(df_HR['WorkLifeBalance'].unique()):
        ratio = df_HR[(df_HR['WorkLifeBalance']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['WorkLifeBalance']==field].shape[0]
        df_WorkLifeBalance.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_WLB = df_WorkLifeBalance.groupby(by="WorkLifeBalance").sum()
    x1 = df_HR['WorkLifeBalance'].unique()
    y1 = df_WLB['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by WorkLifeBalance (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/over_time')
def data_analysis_over_time():
    df_OverTime = pd.DataFrame(columns=["OverTime", "% of Leavers"])
    i=0
    for field in list(df_HR['OverTime'].unique()):
        ratio = df_HR[(df_HR['OverTime']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['OverTime']==field].shape[0]
        df_OverTime.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_OT = df_OverTime.groupby(by="OverTime").sum()
    x1 = df_HR['OverTime'].unique()
    y1 = df_OT['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by OverTime (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/monthly_income')
def data_analysis_monthly_income():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'MonthlyIncome']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'MonthlyIncome']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Monthly Income by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[0, 20000], dtick=2000))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/percent_salary_hike')
def data_analysis_percent_salary_hike():
    # Add histogram data
    x1 = df_HR.loc[df_HR['Attrition'] == 'No', 'PercentSalaryHike']
    x2 = df_HR.loc[df_HR['Attrition'] == 'Yes', 'PercentSalaryHike']
    # Group data together
    hist_data = [x1, x2]
    group_labels = ['Active Employees', 'Ex-Employees']
    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels,
                            curve_type='kde', show_hist=False, show_rug=False)
    # Add title
    fig['layout'].update(title='Percent Salary Hike by Attrition Status')
    fig['layout'].update(xaxis=dict(range=[10, 26], dtick=1))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/stock_option_level')
def data_analysis_stock_option_level():
    df_StockOptionLevel = pd.DataFrame(columns=["StockOptionLevel", "% of Leavers"])
    i=0
    for field in list(df_HR['StockOptionLevel'].unique()):
        ratio = df_HR[(df_HR['StockOptionLevel']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['StockOptionLevel']==field].shape[0]
        df_StockOptionLevel.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_SOL = df_StockOptionLevel.groupby(by="StockOptionLevel").sum()
    x1 = df_HR['StockOptionLevel'].unique()
    y1 = df_SOL['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Stock Option Level (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/env_satis')
def data_analysis_env_satis():
    df_EnvironmentSatisfaction = pd.DataFrame(columns=["EnvironmentSatisfaction", "% of Leavers"])
    i=0
    for field in list(df_HR['EnvironmentSatisfaction'].unique()):
        ratio = df_HR[(df_HR['EnvironmentSatisfaction']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['EnvironmentSatisfaction']==field].shape[0]
        df_EnvironmentSatisfaction.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_Env = df_EnvironmentSatisfaction.groupby(by="EnvironmentSatisfaction").sum()
    x1 = df_HR['EnvironmentSatisfaction'].unique()
    y1 = df_Env['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Environment Satisfaction (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/job_satis')
def data_analysis_job_satis():
    df_JobSatisfaction = pd.DataFrame(columns=["JobSatisfaction", "% of Leavers"])
    i=0
    for field in list(df_HR['JobSatisfaction'].unique()):
        ratio = df_HR[(df_HR['JobSatisfaction']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['JobSatisfaction']==field].shape[0]
        df_JobSatisfaction.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_JS = df_JobSatisfaction.groupby(by="JobSatisfaction").sum()
    x1 = df_HR['JobSatisfaction'].unique()
    y1 = df_JS['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Job Satisfaction (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/relationship_satis')
def data_analysis_relationship_satis():
    df_RelationshipSatisfaction = pd.DataFrame(columns=["RelationshipSatisfaction", "% of Leavers"])
    i=0
    for field in list(df_HR['RelationshipSatisfaction'].unique()):
        ratio = df_HR[(df_HR['RelationshipSatisfaction']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['RelationshipSatisfaction']==field].shape[0]
        df_RelationshipSatisfaction.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_RS = df_RelationshipSatisfaction.groupby(by="RelationshipSatisfaction").sum()
    x1 = df_HR['RelationshipSatisfaction'].unique()
    y1 = df_RS['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Relationship Satisfaction (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/performance_rating')
def data_analysis_performance_rating():
    df_PerformanceRating = pd.DataFrame(columns=["PerformanceRating", "% of Leavers"])
    i=0
    for field in list(df_HR['PerformanceRating'].unique()):
        ratio = df_HR[(df_HR['PerformanceRating']==field)&(df_HR['Attrition']=="Yes")].shape[0] / df_HR[df_HR['PerformanceRating']==field].shape[0]
        df_PerformanceRating.loc[i] = (field, ratio*100)
        i += 1
        #print("In {}, the ratio of leavers is {:.2f}%".format(field, ratio*100))    
    df_PR = df_PerformanceRating.groupby(by="PerformanceRating").sum()
    x1 = df_HR['PerformanceRating'].unique()
    y1 = df_PR['% of Leavers'].get_values()
    data = [go.Bar(
        x=x1,
        y = y1,
        text = y1,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity= 0.4
    )]
    layout = go.Layout(title='Leavers by Performance Rating (%)')
    fig = go.Figure(data=data,layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON









    