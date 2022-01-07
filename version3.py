import pandas as pd
import numpy as np

from datetime import datetime
from pytz import timezone


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

#=======================================================================================================================

commonPath = 'D:\office\Git\Scripts\Telemetry\TelemetryBadDataExtractor'

df1 = pd.read_csv(commonPath+'\srap2_scadaanalogdump_28092021_15_19_22.csv' ,skiprows=6)
df1.drop(df1.columns[[0, 7]], axis = 1, inplace = True)
#print(df1)
df1.dropna(subset = ['Key'], inplace = True)
#print(df1)

df2 = pd.read_csv(commonPath+'\srap2_scadastatusdump_28092021_15_19_22.csv',skiprows=6)
df2.drop(df2.columns[[0, 7]], axis = 1, inplace = True)
#print(df2)
df2.dropna(subset = ['Key'], inplace = True)
#print(df2)
frames = [df1, df2]
#result = pd.concat(frames)
result = df1.append(df2)
#print(result)
result.dropna(subset = ["Key"], inplace=True)
#print(result)


result['StationID'] = result['Key']
result['Point Type'] = result['Key']
result['Point Type Name'] = result['Key']
result['record'] = np.arange(len(result))
#result(index_col = 'record')Jan@2022
#print(result)
result = result.set_index('record')
master = pd.read_excel(commonPath+'\MasterStationNameList.xlsx')


#=======================================================================================================================



print(result)
for ind in result.index:
    x = result['Key'].values[ind]
    y = x[1:2]
    x = x[2:5]
    result.loc[ind,'StationID'] = x
    result.loc[ind,'Point Type'] = y
    result.loc[ind,'Point Type Name'] = y
    #print(result['Key'][ind])

result.groupby(by ='StationID' )
#print(result)

##master = pd.read_excel('D:\SCADA Project\TELEMETRY FORMAT\MasterStationNameList.xlsx')
#print(master)




# result['Quality'] = result["Quality"].astype(str)
# result["Quality"].replace("4", "Non-Update", regex=True)


#=======================================================================================================================

data_types_dict = {'Quality': str}
result = result.astype(data_types_dict)

 # 0: Good 
result["Quality"] = result["Quality"].replace("0.0", "Good", regex=True)
# 1 : Questionable
result["Quality"] = result["Quality"].replace("1.0", "Questionable", regex=True)
# 2 : Substitution (Accum only)
result["Quality"] = result["Quality"].replace("2.0", "Substitution (Accum only)", regex=True)
# 4 : Non-Update
result["Quality"] = result["Quality"].replace("4.0", "Non-Update", regex=True)
# 8 : Reasonability (Analog only)
result["Quality"] = result["Quality"].replace("8.0", "Reasonability (Analog only)", regex=True)
# 16: Manual Entry
result["Quality"] = result["Quality"].replace("16.0", "Manual Entry", regex=True)
# 32: Drift (Analog only)
result["Quality"] = result["Quality"].replace("32.0", "Drift (Analog only)", regex=True)
# 64: Estimation Error
result["Quality"] = result["Quality"].replace("64.0", "Estimation Error", regex=True)
# 128: Flatline (Analog only)
result["Quality"] = result["Quality"].replace("128.0", "Flatline (Analog only)", regex=True)
#print(type(result['Quality']))

#=======================================================================================================================


data_types_dict = {'Point Type Name': str}
result = result.astype(data_types_dict)

#Analog
result["Point Type Name"] = result["Point Type Name"].replace("3", "Analog", regex=True)
#Status
result["Point Type Name"] = result["Point Type Name"].replace("2", "Status", regex=True)
#SOE/Status
result["Point Type Name"] = result["Point Type Name"].replace("1", "SOE/Status", regex=True)

#=======================================================================================================================


#result['SystemTimeSec'] = pd.to_datetime(result['SystemTimeSec'], unit='s').dt.strftime("%H:%M:%S")
result['SystemTimeSec'] = pd.to_datetime(result['SystemTimeSec'], unit='s').dt.strftime("%m/%d/%Y, %H:%M:%S")

print("Sample Time",result['SystemTimeSec'].values[0])

#=======================================================================================================================

result['RTU ID'] = ''
result['IEC point'] = ''

#=======================================================================================================================



#print(result)

fepdump = pd.read_csv(commonPath+'\srfep1_fepdump_25122021_15_00_00.csv',skiprows=6)
fepdump.rename(columns = {'Key':'SCADAKey'}, inplace = True)

print(type(fepdump['pRTU']))
# data_types_dict = {'pRTU': int}
# fepdump = fepdump.astype(data_types_dict)

# data_types_dict = {'pRTU': str}
# fepdump = fepdump.astype(data_types_dict)

data_types_dict = {'SCADA_Key': str}
fepdump = fepdump.astype(data_types_dict)
#fepdump['SCADA_Key'] = fepdump['SCADA_Key'].str.replace('.0',' ')


data_types_dict = {'pRTU': str}
fepdump = fepdump.astype(data_types_dict)
fepdump['pRTU'] = fepdump['pRTU'].str.replace('.0','')
fepdump['SCADA_Key'] = fepdump['SCADA_Key'].str[:7]    #.replace('.0',' ')

print(fepdump)

#d.read_csv('')
# result.rename(columns = {'Key':'SCADA_Key'}, inplace = True)
# data_types_dict = {'SCADA_Key': str}
# result = result.astype(data_types_dict)
# result['pRTU'] = 2

# print(result)
# print(fepdump)
# fepdump = pd.merge(result, fepdump, how="left", on=["SCADA_Key", "pRTU"])
# print(fepdump)


#Code to convert seconds to time in hours 
#print("Time in hours:",convert(result['SystemTimeSec'].values[1]))


#Code to dump in excel

with pd.ExcelWriter(commonPath+'\output.xlsx') as writer:
    for ind2 in master.index:
        #print(result. loc[result['StationID'] == str(master['STATION NAME'].values[ind2])])
        tempdf = (result.loc[result['StationID'] == str(master['STATION NAME'].values[ind2])]).copy()
        tempdf['S No'] = np.arange(len(tempdf))
        #tempdf.index = np.arange(1, len(tempdf))
        tempdf['Station Name'] = str(master['STATION NAAME'].values[ind2])
        tempdf['pRTU'] = master['RTU ID'].values[ind2]
        data_types_dict = {'pRTU': str}
        tempdf = tempdf.astype(data_types_dict)

        tempdf['IEC Addres'] = ''
        tempdf.rename(columns = {'Key':'SCADA_Key'}, inplace = True)
        data_types_dict = {'SCADA_Key': str}
        tempdf = tempdf.astype(data_types_dict)
        tempdf['SCADA_Key'] = tempdf['SCADA_Key'].str[1:]    #.replace('.0',' ')
        
        tempdf = pd.merge(tempdf, fepdump, how="left", on=["SCADA_Key", "pRTU"])
        
        print(tempdf)
        #tempdf.rename(columns = {'Name':'Point Name'}, inplace = True)
        
        tempdf = tempdf[['S No','SystemTimeSec','StationID','Station Name','SCADA_Key','Name','Point Type','Point Type Name','Quality','pRTU','IntParms' ]]
        tempdf.rename(columns = {'IntParms':'IEC Addres'}, inplace = True)
        #del tempdf['record']
        # (result. loc[result['StationID'] == str(master['STATION NAME'].values[ind2])]).to_excel(writer,
        #          sheet_name= str(master['STATION NAAME'].values[ind2]))  
        tempdf.to_excel(writer,
                 sheet_name= str(master['STATION NAAME'].values[ind2]), index = False) 
        
        del tempdf
        #print("\n")

