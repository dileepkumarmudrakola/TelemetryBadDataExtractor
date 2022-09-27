from datetime import datetime, timedelta
import ftplib
import psycopg2,pdb
import pandas as pd
import numpy as np
import traceback

commonPath = 'E:\\TelemetryMessageApp\\TelemetryBadDataExtractor'



def InsertToDatabase(current_date = datetime.now()):
	try:
		connection = psycopg2.connect(		user="postgres",
                              		password="1234",
                                    host="localhost",
                                    port="5432",
                                    database="Telemetrydb"

                              )
		cursor = connection.cursor()
		cursor.execute('SELECT "Station_id", "Station_Name", "RTU_id" FROM public."Station_Table" ORDER BY "Station_id" ASC ')
		stationDf = pd.DataFrame(cursor.fetchall(), columns=['Station_id', 'Station_Name', 'RTU_id'])
		print(stationDf)


		ftp_server = ftplib.FTP('10.0.100.25', 'control', 'rscc080')
		# return
		


		def readAnalogtoDf():
			analogDf = pd.read_csv(commonPath+'\\analog.csv' ,skiprows=6)
			analogDf.drop(analogDf.columns[[0, 7]], axis = 1, inplace = True)
			analogDf.dropna(subset = ['Key'], inplace = True)
			return analogDf

		def readStatustoDf():
			statusDf = pd.read_csv(commonPath+'\\status.csv',skiprows=6)
			statusDf.drop(statusDf.columns[[0, 7]], axis = 1, inplace = True)
			statusDf.dropna(subset = ['Key'], inplace = True)
			return statusDf

		def retrieveDataFromFtp(inputFileName, outputFileName):
			ls = []
			ftp_server.retrlines('LIST *'+inputFileName+'*', ls.append)
			filename = ls[0].split(' ')[-1]
			wrfile = open(outputFileName+'.csv','wb')
			ftp_server.retrbinary('RETR '+filename,wrfile.write)
			wrfile.close()

		def combineStatusAndAnalog(analogDf, statusDf):
			frames = [analogDf, statusDf]
			combinedAnalogStatusDf = analogDf.append(statusDf)
			combinedAnalogStatusDf.dropna(subset = ["Key"], inplace=True)
			combinedAnalogStatusDf['StationID'] = combinedAnalogStatusDf['Key']
			combinedAnalogStatusDf['Point Type No'] = combinedAnalogStatusDf['Key']
			combinedAnalogStatusDf['Point Type Name'] = combinedAnalogStatusDf['Key']
			combinedAnalogStatusDf['record'] = np.arange(len(combinedAnalogStatusDf))
			combinedAnalogStatusDf = combinedAnalogStatusDf.set_index('record')
			for ind in combinedAnalogStatusDf.index:
				x = combinedAnalogStatusDf['Key'].values[ind]
				y = x[1:2]
				x = x[2:5]
				combinedAnalogStatusDf.loc[ind,'StationID'] = x
				combinedAnalogStatusDf.loc[ind,'Point Type No'] = y
				combinedAnalogStatusDf.loc[ind,'Point Type Name'] = y
			# combinedAnalogStatusDf.groupby(by ='StationID' )
			data_types_dict = {'Quality': str}
			combinedAnalogStatusDf = combinedAnalogStatusDf.astype(data_types_dict)

			combinedAnalogStatusDf["Quality_id"] = combinedAnalogStatusDf["Quality"].str.replace('.0','')

			# 0: Good 
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("0.0", "Good", regex=True)
			# 1 : Questionable
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("1.0", "Questionable", regex=True)
			# 2 : Substitution (Accum only)
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("2.0", "Substitution (Accum only)", regex=True)
			# 4 : Non-Update
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("4.0", "Non-Update", regex=True)
			# 8 : Reasonability (Analog only)
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("8.0", "Reasonability (Analog only)", regex=True)
			# 16: Manual Entry
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("16.0", "Manual Entry", regex=True)
			# 32: Drift (Analog only)
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("32.0", "Drift (Analog only)", regex=True)
			# 64: Estimation Error
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("64.0", "Estimation Error", regex=True)
			# 128: Flatline (Analog only)
			combinedAnalogStatusDf["Quality"] = combinedAnalogStatusDf["Quality"].replace("128.0", "Flatline (Analog only)", regex=True)
			
			#=======================================================================================================================


			data_types_dict = {'Point Type Name': str}
			combinedAnalogStatusDf = combinedAnalogStatusDf.astype(data_types_dict)

			#Analog
			combinedAnalogStatusDf["Point Type Name"] = combinedAnalogStatusDf["Point Type Name"].replace("3", "Analog", regex=True)
			#Status
			combinedAnalogStatusDf["Point Type Name"] = combinedAnalogStatusDf["Point Type Name"].replace("2", "Status", regex=True)
			#SOE/Status
			combinedAnalogStatusDf["Point Type Name"] = combinedAnalogStatusDf["Point Type Name"].replace("1", "SOE/Status", regex=True)

			#=======================================================================================================================

			combinedAnalogStatusDf['SystemTimeSec'] = combinedAnalogStatusDf['SystemTimeSec'] + 19800
			combinedAnalogStatusDf['SystemTimeSec'] = pd.to_datetime(combinedAnalogStatusDf['SystemTimeSec'], unit='s').dt.strftime("%Y-%m-%d %H:%M")

			#=======================================================================================================================

			combinedAnalogStatusDf['RTU ID'] = ''
			combinedAnalogStatusDf['IEC point'] = ''

			#=======================================================================================================================


			return combinedAnalogStatusDf

		def readFepDf():
			fepdump = pd.read_csv(commonPath+'\\fep.csv',skiprows=6)
			fepdump.rename(columns = {'Key':'SCADAKey'}, inplace = True)
			data_types_dict = {'SCADA_Key': str}
			fepdump = fepdump.astype(data_types_dict)
			data_types_dict = {'pRTU': str}
			fepdump = fepdump.astype(data_types_dict)
			fepdump['pRTU'] = fepdump['pRTU'].str[:-2]
			fepdump['SCADA_Key'] = fepdump['SCADA_Key'].str[:7]    #.replace('.0',' ')
			#Export to excel
			return fepdump

		def inputsProcess(fileTime):
			fileEndName = fileTime.strftime('%d%m%Y_%H_00')
			print(fileEndName)
			ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/FEP_DUMP')
			fep_file_name = 'srfep1_fepdump_'+fileEndName
			retrieveDataFromFtp(fep_file_name, 'fep')
			ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/ANALOG_DUMP')
			analog_file_name = 'srap1_scadaanalogdump_'+fileEndName
			retrieveDataFromFtp(analog_file_name, 'analog')
			analogDf = readAnalogtoDf()
			ftp_server.cwd('/ftp/reports/REMC/SCADA_DUMP/DIGITAL_DUMP')
			status_file_name = 'srap1_scadastatusdump_'+fileEndName
			retrieveDataFromFtp(status_file_name, 'status')
			statusDf = readStatustoDf()
			combinedAnalogStatusDf = combineStatusAndAnalog(analogDf, statusDf)
			fepDf = readFepDf()


			cursor.execute('DELETE FROM public."Station_Point_Data" where "FileDate"={}'.format("'"+fileTime.strftime("%Y-%m-%d %H:00")+"'"))
			connection.commit()
			
			for index in stationDf.index:
				
				tempdf = (combinedAnalogStatusDf.loc[combinedAnalogStatusDf['StationID'] == str(stationDf['Station_id'].values[index])]).copy()
				
				tempdf['Station Name'] = str(stationDf['Station_Name'].values[index])
				tempdf['pRTU'] = stationDf['RTU_id'].values[index]
				data_types_dict = {'pRTU': str}
				tempdf = tempdf.astype(data_types_dict)

				tempdf['IEC Addres'] = ''
				tempdf.rename(columns = {'Key':'SCADA_Key'}, inplace = True)
				data_types_dict = {'SCADA_Key': str}
				tempdf = tempdf.astype(data_types_dict)
				tempdf['SCADA_Key'] = tempdf['SCADA_Key'].str[1:]    #.replace('.0',' ')

				

				tempdf = pd.merge(tempdf, fepDf, how="left", on=["SCADA_Key", "pRTU"])
				data_types_dict = {'IntParms': str}
				tempdf = tempdf.astype(data_types_dict)
				tempdf['IntParms'] = tempdf['IntParms'].str[:-2]
				# if('KAYAMKULAM SOLAR'==str(stationDf['Station_Name'].values[index])):
				# 	import pdb
				# 	pdb.set_trace()
				# 	print()

				# tempdf = tempdf[['SystemTimeSec','Station Name','IntParms','SCADA_Key','Name','Point Type Name','Quality' ]]
				tempdf.rename(columns = {'IntParms':'IEC Address'}, inplace = True)
				tempdf.rename(columns = {'SystemTimeSec':'Time Stamp'}, inplace = True)
				# tempdf.rename(columns = {'SCADA_Key':'SCADA Key'}, inplace = True)
				tempdf.rename(columns = {'Name':'Point Name'}, inplace = True)
				tempdf.rename(columns = {'Point Type Name':'Point Type'}, inplace = True)

				

				for eachIndex in tempdf.index:
					
					postgres_insert_query = 'INSERT INTO public."Station_Point_Table"(station_id, scada_key, iec_address, point_id, point_name) VALUES (%s, %s, %s, %s, %s)'
					record_to_insert = (int(tempdf['pStation'].values[eachIndex]), str(tempdf['SCADA_Key'].values[eachIndex]), str(tempdf['IEC Address'].values[eachIndex]),int(tempdf['Point Type No'].values[eachIndex]), str(tempdf['Point Name'].values[eachIndex]))
					
				

					try:
						cursor.execute(postgres_insert_query, record_to_insert)
						connection.commit()
					except Exception as e:
						connection.rollback()

					
					postgres_insert_query = 'INSERT INTO public."Station_Point_Data"("FileDate", "TimeInFile", station_id, scada_key, quality)VALUES (%s, %s, %s, %s, %s)'
					record_to_insert = (str(fileTime.strftime("%Y-%m-%d %H:00")), (tempdf['Time Stamp'].values[eachIndex]),int(tempdf['pStation'].values[eachIndex]), str(tempdf['SCADA_Key'].values[eachIndex]), int(tempdf['Quality_id'].values[eachIndex]))
					
					try:
						cursor.execute(postgres_insert_query, record_to_insert)
						connection.commit()
					except Exception as e:
						connection.rollback()						
					


		inputsProcess(current_date)
	except Exception as e:
		print(traceback.format_exc())
		print(e)
	finally:
		ftp_server.close()
		cursor.close()
		connection.close()


InsertToDatabase(datetime.now()-timedelta())