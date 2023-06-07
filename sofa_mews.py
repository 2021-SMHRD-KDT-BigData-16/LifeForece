import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

def pre_treat(test_df):
    test_df = test_df.replace(-1, np.NaN)

    with open(file='./median_dict.pkl', mode='rb') as f:
            median_dict=pickle.load(f)

    first_index = test_df.drop_duplicates('p_id').index

    colss=test_df.columns
    cols=[]
    for i in range (2,colss.size):
        cols.append(colss[i])        

    test_df3 = test_df.copy()
    # test 데이터
    for col in cols:
        for i in first_index:
            if np.isnan(test_df3.loc[i,col])==True:
                test_df3.loc[i, col] = median_dict[col]
        test_df3[col] = test_df3[col].fillna(method='ffill')

    return test_df3

def calculate_mews(respiratory_rate, heart_rate, systolic_bp, temperature):
    
    mews = 0
    
    # Respiratory Rate
    if respiratory_rate >= 30:
        mews += 3
    elif respiratory_rate >= 21:
        mews += 2
    elif respiratory_rate >= 15:
        mews += 1
    elif respiratory_rate < 9:
        mews += 2
    
    # Heart Rate
    if heart_rate >= 130:
        mews += 3
    elif heart_rate >= 111:
        mews += 2
    elif heart_rate >= 101:
        mews += 1
    elif heart_rate >= 41 and heart_rate <= 50:
        mews += 1
    elif heart_rate < 40:
        mews += 2
    
    # Systolic Blood Pressure
    if systolic_bp <=70:
        mews += 3
    elif systolic_bp <= 80:
        mews += 2
    elif systolic_bp <= 100:
        mews += 1
    elif systolic_bp >= 200:
        mews += 2
    
    # Temperature
    if temperature < 35 or temperature >= 38.5:
        mews += 2
    
    
    return mews

def calculate_sofa(gcs, PaO2, FiO2, mbp, platelet_count, bilirubin, Creatinine):
    score = 0

    # Glasgow Coma Scale (GCS) score
    if gcs < 6:
        score += 4
    elif gcs < 10:
        score += 3
    elif gcs < 13:
        score += 2
    elif gcs < 15:
        score += 1
    
    respiratory = PaO2/FiO2
    
    # Respiratory rate score
    if respiratory <= 100:
        score += 4
    elif respiratory<= 200:
        score += 3
    elif respiratory <= 300:
        score += 2
    elif respiratory <= 400:
        score += 1

    # Platelet count score
    if platelet_count <= 20:
        score += 4
    elif platelet_count <= 50:
        score += 3
    elif platelet_count <= 100:
        score += 2
    elif platelet_count <= 150:
        score += 1

    # Bilirubin score 
    if bilirubin < 1.2:
        score += 0
    elif bilirubin < 2:
        score += 1
    elif bilirubin < 6:
        score += 2
    elif bilirubin < 12:
        score += 3
    else:
        score += 4
        
    # Renal Creatinine
    if Creatinine > 5:
        score += 4
    elif Creatinine >= 3.5:
        score += 3
    elif Creatinine >= 2.0:
        score += 2
    elif Creatinine >= 1.2:
        score += 1
        
    # Mean arterial pressure (MAP) score
    if mbp < 70:
        score += 1
    
    return score

def save_mews(test_df):
    mews_scores=[]
    cols = ['RR', 'HR', 'SBP', 'BT']
    for i in tqdm(test_df.index):
        data = test_df.loc[i, cols].values
        mews_score = calculate_mews(data[0], data[1], data[2], data[3])
        mews_scores.append(mews_score)
    test_df["MEWS"] = mews_scores
    
    return test_df['MEWS'].max()


def save_sofa(test_df):
    sofa_scores=[]
    cols = ['GCS', 'PaO2', 'FiO2', 'MBP','Platelets', 'Bilirubin', 'Creatinine']
    for i in tqdm(test_df.index):
        data = test_df.loc[i, cols].values
        sofa_score = calculate_sofa(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        sofa_scores.append(sofa_score)
    test_df["SOFA"] = sofa_scores
    
    return test_df['SOFA'].max()


