import pandas as pd


# Take two dfs and merge them into merge-df
df1 = pd.read_csv('D:\SCADA Project\TELEMETRY FORMAT\srap2_scadaanalogdump_28092021_15_19_22.csv',skiprows=6)
#df1.drop(['C', 'D'], axis = 1)
df1.drop(df1.columns[[0, 7]], axis = 1, inplace = True)

#print(df1)
df2 = pd.read_csv('D:\SCADA Project\TELEMETRY FORMAT\srap2_scadastatusdump_28092021_15_19_22.csv',skiprows=6)
df2.drop(df2.columns[[0, 7]], axis = 1, inplace = True)


#print(df2)
frames = [df1, df2]
#result = pd.concat(frames)
result = df1.append(df2)
result.dropna(subset = ["Key"], inplace=True)
#print(result)
#result.to_csv('scadatest1.csv')

#df3 = result.loc[result['Key'] == '3820013']

#print(df3)
result['StationID'] = ''

stationid = []

test = []
for ind in result.index:
    x = result['Key'].values[ind]
    #x = str(x)
    #x = float(x)
    test.append(x)
    #y = x[2:5]
    stationid.append(result['Key'].values[ind])
    
    #result.loc[ind,'StationID'] = y

result['StationID'] = stationid
#print(stationid)




#result.to_csv('scadatest1.csv')




# for ind in result.index: #range(len(result)) :     #result.index:
#      x = str(result['Key'].values[ind]) #str(result.loc[ind,'Key'])
#      #print("Value of X",x)#x = str(result['Key'][ind])
#      #print(x)
#      #print(x[1:4])
#      y = x[2:5]
#      result.loc[ind,'StationID'] = y
#      #result['StationID'][ind] = y
#      #result.insert(6, "StationID", y, True)
#      if(y=='820'):
#          #print(result.iloc[ind])
#          #print(x)
#          df3 = df3.append(result.iloc[ind])

#result.to_csv('scadatest1.csv')
#print(result)
#print(df3)
#df3.to_csv('820.csv')


i = int(0)
print(result)
# for ind3 in range(29639):
#     print(result['Key'][ind3],test[ind3],result['StationID'][ind3])
# for ind2 in result.index:
#     x1 = result['Key'].values[ind2]
#     #x1 = x1[2:5]
#     y1 = result['StationID'].values[ind2]
#     print(x1,"    ",y1)
    # if(x1.find(y1)>=0):
    #     i=i+1
    #     print("Found",x1,"    ",y1,i)

