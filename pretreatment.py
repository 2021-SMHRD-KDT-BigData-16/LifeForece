def Pretreatment(test_df):

    import pandas as pd
    import numpy as np
    from tqdm.notebook import tqdm
    import pickle
    import copy

    test_df3 = test_df.copy()
    # test 데이터
    
    test_df3 = test_df3.replace(-1, np.NaN)
    
    first_index = test_df3.drop_duplicates('p_id').index
    
    colss=test_df3.columns
    cols=[]
    
    for i in range (2,colss.size):
        cols.append(colss[i])
        
    with open(file='./median_dict.pkl', mode='rb') as f:
        median_dict=pickle.load(f)
    
    for col in cols:
        for i in first_index:
            if np.isnan(test_df3.loc[i,col])==True:
                test_df3.loc[i, col] = median_dict[col]
        test_df3[col] = test_df3[col].fillna(method='ffill')
    # test 데이터

    test_df4 = test_df3.drop(['rec_time'], axis=1)

    maxlen = 70
    # zero-padding 함수

    def zero_padding(dataframe, maxlen):
        maxlen = maxlen
        df4 = dataframe
        col_len = len(df4.columns)
        data = []
        # 기본정보는 zero_padding에 모두 동일하게 적용되어야 함으로 따로 취급한다. 나머지는 모두 0.0으로 채운다.
        basic_col = 'p_id, age, ICUtype, male, female'
        basic_col_list = basic_col.split(', ')
        basic_col_indexer = df4.columns.get_indexer(basic_col_list)
        basic_col_indexer

        for p_id in df4.p_id.drop_duplicates().to_numpy():
            if len(df4[df4.p_id == p_id]) >= maxlen:
                dummy = df4[df4.p_id == p_id].to_numpy().tolist()
                data.append(dummy[:maxlen])
            else:
                length = len(df4[df4.p_id == p_id])
                base = np.zeros((maxlen, col_len))
                for idx in basic_col_indexer:
                    base[:, idx] = df4[df4.p_id == p_id].iloc[0, idx]
                # print(base.shape)
                dummy = df4[df4.p_id == p_id].to_numpy()
                # print(dummy.shape)
                base[-length:] = dummy
                # print(base.shape)
                # base[:length, 0] = pid
                # base[:length, -1] = dummy[0, -1]
                data.append(base.tolist())
        return data

    test_data = zero_padding(test_df4, maxlen)
    test_data = np.array(test_data)
    test_data = test_data.reshape((-1, len(test_df4.columns)))
    test_df5 = pd.DataFrame(test_data, columns=test_df4.columns)

    from sklearn.preprocessing import MinMaxScaler

    with open(file='./minmax.pickle', mode='rb') as f:
        minmax = pickle.load(f)

    test_df5_1 = test_df5.drop(
        columns=['p_id', 'age', 'ICUtype', 'male', 'female'])

    test_df5_2 = minmax.transform(test_df5_1)
    test_df5_2 = pd.DataFrame(test_df5_2, columns=test_df5_1.columns)
    test_df5_2.insert(0, 'p_id', test_df5['p_id'])
    test_df5_2.insert(1, 'age', test_df5['age'])
    test_df5_2.insert(3, 'ICUtype', test_df5['ICUtype'])
    test_df5_2['male'] = test_df5['male']
    test_df5_2['female'] = test_df5['female']
    test_df5 = test_df5_2

    test_df5['ICUtype_1.0'] = 0
    test_df5['ICUtype_2.0'] = 0
    test_df5['ICUtype_3.0'] = 0
    test_df5['ICUtype_4.0'] = 0

    for i in range(1, 5):
        if test_df5['ICUtype'][0] == float(i):
            test_df5[f'ICUtype_{i}.0'] = 1.0

    test_df6 = test_df5.drop(columns=['ICUtype'])

    return test_df6
