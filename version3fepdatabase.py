import pandas as pd
import numpy as np

from datetime import datetime
from pytz import timezone
# from datetime import datetime
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
#Database
import psycopg2,pdb
import ftplib






def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

#=======================================================================================================================
#Fep code



current_date = datetime.now()

ftp_server = ftplib.FTP('10.0.100.25', 'control', 'rscc080')
ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/FEP_DUMP')
fep_file_name = 'srfep1_fepdump_'+current_date.strftime('%d%m%Y_%H_00')
ls = []
ftp_server.retrlines('LIST *'+fep_file_name+'*', ls.append)

filename = ls[0].split(' ')[-1]
wrfile = open('fep.csv','wb')
ftp_server.retrbinary('RETR '+filename,wrfile.write)

wrfile.close()

ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/ANALOG_DUMP')
analog_file_name = 'srap1_scadaanalogdump_'+current_date.strftime('%d%m%Y_%H_00')
ls = []
ftp_server.retrlines('LIST *'+analog_file_name+'*', ls.append)

filename = ls[0].split(' ')[-1]
wrfile = open('analog.csv','wb')
ftp_server.retrbinary('RETR '+filename,wrfile.write)

wrfile.close()

ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/DIGITAL_DUMP')
status_file_name = 'srap1_scadastatusdump_'+current_date.strftime('%d%m%Y_%H_00')
ls = []
ftp_server.retrlines('LIST *'+status_file_name+'*', ls.append)

filename = ls[0].split(' ')[-1]
wrfile = open('status.csv','wb')
ftp_server.retrbinary('RETR '+filename,wrfile.write)

wrfile.close()

ftp_server.close()


#=======================================================================================================================
#commonPath = 'D:\office\Git\Scripts\Telemetry\TelemetryBadDataExtractor'
commonPath = 'E:\\TelemetryMessageApp\\TelemetryBadDataExtractor'


df1 = pd.read_csv(commonPath+'\\analog.csv' ,skiprows=6)

df1.drop(df1.columns[[0, 7]], axis = 1, inplace = True)
#print(df1)
df1.dropna(subset = ['Key'], inplace = True)
#print(df1)

df2 = pd.read_csv(commonPath+'\\status.csv',skiprows=6)
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
result['Point Type No'] = result['Key']
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
    result.loc[ind,'Point Type No'] = y
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
print(type(result['SystemTimeSec']))
result['SystemTimeSec'] = result['SystemTimeSec'] + 19800
result['SystemTimeSec'] = pd.to_datetime(result['SystemTimeSec'], unit='s').dt.strftime("%m/%d/%Y, %H:%M:%S")

print("Sample Time",result['SystemTimeSec'].values[0])

# local_timezone = tzlocal.get_localzone() # get pytz tzinfo
# utc_time =  datetime.strptime(result['SystemTimeSec'].values[0], "%m-%d-%Y %H:%M:%S")#datetime.strptime("2011-01-21 02:37:21", "%Y-%m-%d %H:%M:%S")
# local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)




#=======================================================================================================================

result['RTU ID'] = ''
result['IEC point'] = ''

#=======================================================================================================================



#print(result)

fepdump = pd.read_csv(commonPath+'\\fep.csv',skiprows=6)
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
        #print(tempdf['SCADA_Key'])
        tempdf = tempdf.astype(data_types_dict)
        tempdf['SCADA_Key'] = tempdf['SCADA_Key'].str[1:]    #.replace('.0',' ')
        #print(tempdf['SCADA_Key'])

        tempdf = pd.merge(tempdf, fepdump, how="left", on=["SCADA_Key", "pRTU"])
        data_types_dict = {'IntParms': str}
        tempdf = tempdf.astype(data_types_dict)
        tempdf['IntParms'] = tempdf['IntParms'].str[:-2] 



        print(tempdf.columns)
        #tempdf.rename(columns = {'Name':'Point Name'}, inplace = True)
#==================================================================================================================================================
        
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="1234",
                                          host="localhost",
                                          port="5432",
                                          database="Telemetrydb")
            cursor = connection.cursor()
            print(tempdf['IntParms'])
            for ind3 in tempdf.index:
                #  postgres_insert_query = """ INSERT INTO station_point_table (station_id,scada_key, iec_address,point_id) VALUES (%s,%s,%s,%s)"""
                postgres_insert_query = """ INSERT INTO station_point_table (station_id,scada_key, iec_address,point_id) VALUES (%s,%s,%s,%s)"""
                record_to_insert = (int(tempdf['pStation'].values[ind3]), str(tempdf['SCADA_Key'].values[ind3]), str(tempdf['IntParms'].values[ind3]),int(tempdf['Point Type No'].values[ind3]))
   
                cursor.execute(postgres_insert_query, record_to_insert)
            #  postgres_insert_query = """ INSERT INTO station_point_table (station_id,scada_key, iec_address,point_id) VALUES (%s,%s,%s,%s)"""
    #         record_to_insert = (7, 'F', 'G',8)
    # # postgres_insert_query = """ INSERT INTO Station_P (Station_Id,SCADA_Key, IEC_Address,Point_Id) VALUES (%s,%s,%s,%s)"""
    # # record_to_insert = (1, 'B', 'C',2)
    #         cursor.execute(postgres_insert_query, record_to_insert)



            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully Station_Point_Table into  table")

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into Station_Point_Table table", error)

        finally:
    # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


#======================================================================================================================


        
        tempdf = tempdf[['S No','SystemTimeSec','Station Name','IntParms','SCADA_Key','Name','Point Type Name','Quality' ]]
        tempdf.rename(columns = {'IntParms':'IEC Addres'}, inplace = True)
        tempdf.rename(columns = {'SystemTimeSec':'Time Stamp'}, inplace = True)
        tempdf.rename(columns = {'SCADA_Key':'SCADA Key'}, inplace = True)
        tempdf.rename(columns = {'Name':'Point Name'}, inplace = True)
        tempdf.rename(columns = {'Point Type Name':'Point Type'}, inplace = True)

        #tempdf.replace(columns = {'Point Type':'Point Type1'}, inplace = True)
        #del tempdf['record']
        # (result. loc[result['StationID'] == str(master['STATION NAME'].values[ind2])]).to_excel(writer,
        #          sheet_name= str(master['STATION NAAME'].values[ind2]))  
        #print("This is new tempdf",tempdf['IEC Addres'])
        tempdf.to_excel(writer,
                 sheet_name= str(master['STATION NAAME'].values[ind2]), index = False) 
        
    #     try:
    #         connection = psycopg2.connect(user="postgres",
    #                                       password="1234",
    #                                       host="localhost",
    #                                       port="5432",
    #                                       database="Telemetrydb")
    #         cursor = connection.cursor()

    #         for ind3 in tempdf.index:
    #             postgres_insert_query = """ INSERT INTO station_point_table2 (station_id,scada_key, iec_address,point_id) VALUES (%s,%s,%s,%s)"""
    #             record_to_insert = (int(tempdf['STATION NAAME'].values[ind3]), str(tempdf['SCADA Key'].values[ind3]), str(tempdf['IEC Addres'].values[ind3]),6)
   
    #             cursor.execute(postgres_insert_query, record_to_insert)

    #         connection.commit()
    #         count = cursor.rowcount
    #         print(count, "Record inserted successfully Station_Point_Table into  table")

    #     except (Exception, psycopg2.Error) as error:
    #         print("Failed to insert record into Station_Point_Table table", error)

    #     finally:
    # # closing database connection.
    #         if connection:
    #             cursor.close()
    #             connection.close()
    #             print("PostgreSQL connection is closed")
    




        del tempdf
        #print("\n")



# from datetime import datetime
# import pytz    # $ pip install pytz
# import tzlocal # $ pip install tzlocal

# local_timezone = tzlocal.get_localzone() # get pytz tzinfo
# utc_time = datetime.strptime("2011-01-21 02:37:21", "%Y-%m-%d %H:%M:%S")
# local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
