from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, Image
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import time
from datetime import datetime, timedelta
import traceback


PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
import pandas as pd


class PDFGenerator():
    def __init__(self, Message_No):
        self.Message_No = Message_No
        self.mesg_date = datetime.now()

    def myFirstPage(self, canvas, doc):
        header = "headerGrid.jpg"
        footer = "Footer.png"
        canvas.setTitle("SRLDC BENGALURU")
        canvas.saveState()
        canvas.drawImage(header, 5, PAGE_HEIGHT-170)
        canvas.saveState()
        # canvas.drawImage(footer, 0, 0)
        # canvas.saveState()
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        ptext = '<font size=12><b>Real Time Telemetry Discrepancy Report  </b></font>'
        paragraph1=Paragraph(ptext, centered)
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 0,PAGE_HEIGHT-193)
        msg_no=self.Message_No+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'
        msg_date=str(self.mesg_date.strftime('%d-%m-%Y %H:%M'))+' Hrs&nbsp&nbsp&nbsp&nbsp'
        ptext = '<font size=12><b>Message No: </b>%s <b>Date: </b>%s</font>' %( msg_no ,msg_date )
        paragraph1=Paragraph(ptext, styles["Normal"])
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 48,PAGE_HEIGHT-223)
        Pagespace='&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'  
        ptext = '<font size=9> %s Page %s </font>' %(Pagespace,doc.page )
        # ptext = '<font size=9> %s %s Page %s </font>' %(msg_date,Pagespace,doc.page )
        paragraph1=Paragraph(ptext, styles["Normal"])
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 48,87)
        canvas.restoreState()


    def myLaterPages(self, canvas, doc):
        header = "headerGrid.jpg"
        footer = "Footer.png"
        canvas.saveState()
        canvas.drawImage(header, 25, PAGE_HEIGHT-170)
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        ptext = '<font size=12><b>Real Time Telemetry Discrepancy Report  </b></font>'
        paragraph1=Paragraph(ptext, centered) 
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 0,PAGE_HEIGHT-193)
        msg_no=self.Message_No+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'
        msg_date=str(self.mesg_date.strftime('%d-%m-%Y %H:%M'))+' Hrs&nbsp&nbsp&nbsp&nbsp'
        ptext = '<font size=12><b>Message No: </b>%s <b>Date: </b>%s</font>' %( msg_no ,msg_date )
        paragraph1=Paragraph(ptext, styles["Normal"])
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 48,PAGE_HEIGHT-223)
        ptext = '<font size=10>Continued...</font>'
        paragraph1=Paragraph(ptext, styles["Normal"])
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 48,PAGE_HEIGHT-243)
        Pagespace='&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'  
        ptext = '<font size=9> %s Page %s </font>' %(Pagespace,doc.page )
        # ptext = '<font size=9> %s %s Page %s </font>' %(msg_date,Pagespace,doc.page )
        paragraph1=Paragraph(ptext, styles["Normal"])
        w, h = paragraph1.wrap(PAGE_WIDTH, 20)
        paragraph1.drawOn(canvas, 48,87)
        canvas.saveState()
        canvas.setFont('Times-Roman',9)




    def create_pdf_deviation(self, df, fileName='abc'):
        doc = SimpleDocTemplate(fileName+".pdf", pagesize=letter,
                                rightMargin=52,leftMargin=42,
                                topMargin=195,bottomMargin=50, Title='SRLDC BENGALURU')
        Story=[]
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        left = ParagraphStyle(name="left", alignment=TA_LEFT)
        right = ParagraphStyle(name="right", alignment=TA_RIGHT)
        justify =ParagraphStyle(name="justify", alignment=TA_JUSTIFY)
        Designation = "Dummy"
        ptext = '<font size=12><b>From: REMC, SRLDC </b></font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.1*inch))
        ptext = '<font size=12><b>To: Station In Charge </b></font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.1*inch))
        font_size = 11

        # #In every row three shift incharges
        liststates=[]
        temp=[]

        # stations = df.Station_Name.unique()

        ptext = "<font size=%s>%s</font>" % (font_size-1, '1')
        p = Paragraph(ptext, centered)
        temp.append(p)
        ptext = "<font size=%s>%s</font>" % (font_size-1, fileName)
        p = Paragraph(ptext, left)
        temp.append(p)
        

        ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        p = Paragraph(ptext, centered)
        temp.append(p)
        ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        p = Paragraph(ptext, left)
        temp.append(p)
        

        ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        p = Paragraph(ptext, centered)
        temp.append(p)
        ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        p = Paragraph(ptext, left)
        temp.append(p)
        liststates.append(temp)

        # for i in range(0, len(stations), 3):	    
        #     counter=0
        #     temp=[]
        #     while (counter<3):
        #         if(i+counter<len(stations)):
        #             ptext = "<font size=%s>%s</font>" % (font_size-1, i+counter+1)
        #             p = Paragraph(ptext, centered)
        #             temp.append(p)
        #             ptext = "<font size=%s>%s</font>" % (font_size-1, stations[i+counter])
        #             p = Paragraph(ptext, left)
        #             temp.append(p)
        #         else:
        #             ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        #             p = Paragraph(ptext, centered)
        #             temp.append(p)
        #             ptext = "<font size=%s>%s</font>" % (font_size-1, ' ')
        #             p = Paragraph(ptext, left)
        #             temp.append(p)
        #         counter+=1
        #     liststates.append(temp)
        table = Table(liststates, colWidths=[37, 133, 37, 133, 37, 133 ], repeatRows=1,)
        Story.append(table)
        Story.append(Spacer(0,0.2*inch))


        ptext = '<font size=11>Sir/Madam, </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.1*inch))

        ptext = '<font size=11>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp It has been observed that following data points are not updating at SRLDC REMC. </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.1*inch))

        ptext = '<font size=11>This is impacting grid visibility and forecasting of RE generation. </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.12*inch))

        # temp=[]
        # ptext = "<font size=%s><b>Type of Violation: %s</b></font>" % (font_size-1, 'Telemetry')
        # p = Paragraph(ptext, left)
        # temp.append(p)

        
        # IEGC_Clause = '4.6.2'
       

        # ptext = "<font size=%s><b>IEGC Clause: </b>%s</font>" % (font_size-1, IEGC_Clause)
        # p = Paragraph(ptext, left)
        # temp.append(p)
        # listiegcviolation=[]
        # listiegcviolation.append(temp)
        # table = Table(listiegcviolation, colWidths=[270, 250], repeatRows=1)
        # Story.append(table)
        # Story.append(Spacer(0,0.2*inch))

        # if(violationType=='Deviation'):
        #    pass
        # else:
        #     ptext = "<font size=%s><b>Grid Frequency: </b>%s</font>" % (font_size-1, frequency)
        #     p = Paragraph(ptext, left)
        #     Story.append(Paragraph(ptext, styles["Normal"]))
        #     Story.append(Spacer(1,0.2*inch))


        text_data = ["SL.No", "TimeStamp",  "Station Name", "IEC Address",
                                "SCADA Key", "Point Name", "Point Type", "Quality"
                                ]  
        d = []
        font_size = 8
        for text in text_data:
            ptext = "<font size=%s><b>%s</b></font>" % (font_size, text)
            p = Paragraph(ptext, centered)
            d.append(p)
        data = [d]
        line_num = 1
        formatted_line_data = []

        # status_category=3

        for x in range(0, len(df)):
            TimeStamp=df.iloc[x]['TimeStamp']
            StationName=df.iloc[x]['Station_Name']
            IECAddress=df.iloc[x]['iec_address']
            ScadaKey=df.iloc[x]['scada_key']
            PointName=df.iloc[x]['point_name']
            PointType=df.iloc[x]['Point_Name']
            Quality='Bad'
            

            # import pdb
            # pdb.set_trace()
            print(TimeStamp)

            ptext = "<font size=%s>%s</font>" % (font_size-1, str(x+1))
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, TimeStamp)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, StationName)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, IECAddress)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, ScadaKey)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, PointName)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, PointType)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            ptext = "<font size=%s>%s</font>" % (font_size-1, Quality)
            p = Paragraph(ptext, centered)
            formatted_line_data.append(p)

            data.append(formatted_line_data)
            formatted_line_data = []


        table = Table(data, colWidths=[37, 70,70,  70, 80, 80, 70], repeatRows=1,
                                            )
        table.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        data_len = len(data)
        for each in range(data_len):
            if each % 2 == 0:
                bg_color = colors.white
            else:
                bg_color = colors.whitesmoke
            table.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
        Story.append(table)
        Story.append(Spacer(0,0.2*inch))


        ptext = '<font size=11>Please Note that this is in violation of Indian Electricity Grid Code (IEGC) Clause 4.6.4 <i>“Reliable and efficient speech and data communication systems shall be provided to facilitate necessary communication and data exchange, and supervision/control of the grid by the RLDC, under normal and abnormal conditions. All users, STUs and CTU shall provide Systems to telemeter power system parameter such as flow, voltage and status of switches/ transformer taps etc. in line with interface requirements and other guideline made available by RLDC. The associated communication system to facilitate data flow up to appropriate data collection point on CTU’s system, shall also be established by the concerned user or STU as specified by CTU in Connection Agreement. All users/STUs in coordination with CTU shall provide the required facilities at their respective ends as specified in the Connection Agreement”</i> </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.12*inch))


        ptext = '<font size=11> It is here by requested to take immediate action in order to have complete visibility of the station/developer for reliable and secure System Operation.</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.12*inch))

        ptext = '<font size=11>-------------------------------------------End of the Message---------------------------------------- </font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,0.12*inch))


        # if(status_category==1):
        #     IECF_stmt='It is here by requested to take immediate action to strictly adhere to schedule drawl/generation for reliable/secure System Operation.'
        #     ptext = '<font size=10>%s <br />\n <br />\n </font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))
        #     IECF_stmt='Non-compliance of the RLDC direction would be a threat to grid security and shall be treated as violation of CERC Regulations / CEA Grid Standards / Electricity Act 2003. The same would be reported to CERC as per Cl. 1.5 of IEGC 2010 and amendments thereof.'
        #     ptext = '<font size=10>%s <br />\n <br />\n </font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))
        # elif(status_category==2):
        #     IECF_stmt='It is here by requested to take immediate action to strictly adhere to schedule drawl/generation for reliable/secure System Operation.'
        #     ptext = '<font size=10>%s <br />\n <br />\n </font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))
        #     IECF_stmt='SLDC(s) shall ensure proper load generation balance and correct operation of Automatic Demand Management Scheme(ADMS) as per approved logic in thier respective control area. The details of ADMS operation if any may please be informed.'
        #     ptext = '<font size=10>%s <br />\n <br />\n <br />\n <br />\n</font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))
        # else:
        #     IECF_stmt='It is here by requested to take immediate action in order to maintain the drawl/injection as per schedule(s) for reliable and secure System Operation.'
        #     ptext = '<font size=10>%s <br />\n <br />\n </font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))
        #     IECF_stmt='SLDCs shall ensure correct operation of Automatic Demand Management Scheme(ADMS) as per approved logic. The details of operation if any may please be intimated'
        #     ptext = '<font size=10>%s <br />\n <br />\n <br />\n <br />\n</font>' %( IECF_stmt)
        #     Story.append(Paragraph(ptext, justify))


        # if(Remarks is not None):
        #     ptext = "<font size=%s><b>Remarks:</b> %s.</font>" % (font_size, Remarks)
        #     Story.append(Paragraph(ptext, justify))
        #     Story.append(Spacer(0,0.2*inch))


        # if(username!='Dummy'):
        #     sign = ''+str(username)+'.png'
        #     im = Image(sign, 1.5*inch, 0.4*inch)
        #     im.hAlign = 'RIGHT'
        #     Story.append(im)
        #     Story[-1].keepWithNext = True


        # ptext = "<font size=10><b>%s</b></font>" % (str(firstname))
        # Story.append(Paragraph(ptext, right))
        # Story[-1].keepWithNext = True

        # ptext = "<font size=12><b>%s</b></font>" % ("Control Room")
        # Story.append(Paragraph(ptext, right))

        # #############COPY TO LIST##########################
        # Story[-1].keepWithNext = True
        # if(len(copyList)>0):
        #     ptext = '<font size=10><b>Copy to: </b></font>'
        #     Story.append(Paragraph(ptext, styles["Normal"]))
        #     Story.append(Spacer(1,0.1*inch))
        #     listcopy=[]
        #     index=0
        #     font_size = 10
        #     for i in range(0, len(copyList)):	    
        #         counter=0
        #         temp=[]
        #         ptext = "<font size=%s>%s</font>" % (font_size-1, i+1)
        #         p = Paragraph(ptext, centered)
        #         temp.append(p)
        #         ptext = "<font size=%s>%s</font>" % (font_size-1, copyList[i])
        #         p = Paragraph(ptext, left)
        #         temp.append(p)
        #         listcopy.append(temp)
        #     table = Table(listcopy, colWidths=[20,480 ])
        #     Story.append(table)

        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)


current_date = (datetime.now())




from TelemetryBadChecker import *



import psycopg2

try:


    connection = psycopg2.connect(      user="postgres",
                                    password="1234",
                                    host="localhost",
                                    port="5432",
                                    database="Telemetrydb"

            )
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM public."Station_Point_Table"  ')
    stationPointsDf = pd.DataFrame(cursor.fetchall(), columns=['station_id', 'scada_key', 'iec_address', 'point_id', 'point_name'])
    print(stationPointsDf)    

    cursor.execute('SELECT "Point_id", "Point_Name" FROM public."Point_Type_Table" ')
    pointTypeDf = pd.DataFrame(cursor.fetchall(), columns=["Point_id", "Point_Name"])
    pointTypeDf['Point_id']=pointTypeDf['Point_id'].astype(int)  

    cursor.execute('SELECT "Station_id", "Station_Name" FROM public."Station_Table" ')
    stationDf = pd.DataFrame(cursor.fetchall(), columns=["Station_id", "Station_Name"])
    stationDf['Station_id']=stationDf['Station_id'].astype(int)       

    def updateStationPointDf(prioritytime, colName):
        fileTime = prioritytime
        
        for index, row in stationPointsDf.iterrows():
            query = 'SELECT "quality" FROM public."Station_Point_Data" where "FileDate"={} and station_id={} and scada_key={}'.format("'"+fileTime.strftime("%Y-%m-%d %H:00")+"'", row['station_id'], row['scada_key'])
            cursor.execute(query)
            x= cursor.fetchone()
            try:
                if(int(x[0])!=0):
                    stationPointsDf[colName].iloc[index]=1
                else:
                    stationPointsDf[colName].iloc[index]=0
            except Exception as e:
                stationPointsDf[colName].iloc[index]=0
            else:
                pass
            finally:
                pass

    def updateTimeStamp(prioritytime):
        fileTime = prioritytime
        stationPointsDf['TimeStamp'] = ''
        for index, row in stationPointsDf.iterrows():
            query = 'SELECT "TimeInFile" FROM public."Station_Point_Data" where "FileDate"={} and station_id={} and scada_key={}'.format("'"+fileTime.strftime("%Y-%m-%d %H:00")+"'", row['station_id'], row['scada_key'])
            # import pdb
            # pdb.set_trace()
            cursor.execute(query)
            x= cursor.fetchone()
            try:
                stationPointsDf['TimeStamp'].iloc[index]=x[0]
            except Exception as e:
                stationPointsDf['TimeStamp'].iloc[index]=''
            else:
                pass
            finally:
                pass
            
            

    def getMessageNo(current_time, Type):
        try:
            query = 'SELECT "No" FROM public."MessageNoTracker" where "Year_Month"={} and "Type"={}'.format("'"+current_time.strftime("%Y_%b")+"'", "'"+Type+"'")
            cursor.execute(query)
            x= cursor.fetchone()

            if(x):
                message_no = x[0]+1
            else:
                query = 'INSERT INTO public."MessageNoTracker" ("Year_Month", "No", "Type") VALUES ({}, {}, {})'.format("'"+current_time.strftime("%Y_%b")+"'", '0', "'"+Type+"'")
                cursor.execute(query)
                connection.commit()
                message_no = 1
            return message_no
        except Exception as e:
            pass
        else:
            pass
        finally:
            pass

    def updateMessageNo(current_time, Type, No):
        try:
            query = 'UPDAT  FROM public."MessageNoTracker" SET "No"={} where "Year_Month"={} and "Type"={}'.format("'"+No+"'","'"+current_time.strftime("%Y_%b")+"'", "'"+Type+"'")
            cursor.execute(query)
            connection.commit()
           
        except Exception as e:
            connection.rollback()
        else:
            pass
        finally:
            pass
    

    stationPointsDf['Priority1'] = ''
    stationPointsDf['Priority2'] = ''
    stationPointsDf['Priority3'] = ''
    stationPointsDf['Priority4'] = ''


    # stationPointsDf['Priority1'] = 1
    # stationPointsDf['Priority2'] = 1
    # stationPointsDf['Priority3'] = 1
    # stationPointsDf['Priority4'] = 1

    # ##priority1 bit
    priority1Time = current_date
    # ###priority2 bit
    priority2Time = current_date-timedelta(hours=1)
    # ###priority3 bit
    priority3Time = current_date-timedelta(hours=2)
    # ###priority4 bit
    priority4Time = current_date-timedelta(hours=3)

    InsertToDatabase(priority1Time)
    InsertToDatabase(priority2Time)     
    InsertToDatabase(priority3Time)    
    InsertToDatabase(priority4Time)
    updateStationPointDf(priority1Time, 'Priority1')    
    updateStationPointDf(priority2Time, 'Priority2')
    updateStationPointDf(priority3Time, 'Priority3')
    updateStationPointDf(priority4Time, 'Priority4')

    updateTimeStamp(priority1Time)

    print(stationPointsDf)

    stationPointsDf['Priority'] = stationPointsDf['Priority1']*8+stationPointsDf['Priority2']*4+stationPointsDf['Priority3']*2+stationPointsDf['Priority4']*1
    badStationsDf = stationPointsDf[stationPointsDf['Priority']>=6]

    badStationsDf.rename(columns={'station_id':'Station_id'}, inplace=True)
    badStationsDf=pd.merge(badStationsDf, stationDf,on='Station_id')
    badStationsDf.rename(columns={'point_id':'Point_id'}, inplace=True)
    badStationsDf=pd.merge(badStationsDf, pointTypeDf,on='Point_id')

    
    

    for index,row in stationDf.iterrows():
        import pdb
        pdb.set_trace()
        df= badStationsDf[badStationsDf['Station_Name']==row['Station_Name']]
        df.reset_index(inplace=True)
        messageNo = getMessageNo(current_date, 'BT')
        pdfGen = PDFGenerator('SRLDC/BT/'+current_date.strftime('%Y')+'/'+current_date.strftime('%b')+'/'+str(messageNo))
        pdfGen.create_pdf_deviation(df, row['Station_Name'])
        updateMessageNo(current_date, 'BT', messageNo)
    ##################Updating MessageNo to be done...............

    print()

except Exception as e:
    print(traceback.format_exc())
else:
    pass
finally:
    cursor.close()
    connection.close()



# df = pd.read_excel('output - Copy.xlsx', sheet_name='SPRING WIND')

# df = df[df['Quality']!='Good']

# pdfGen = PDFGenerator()
# pdfGen.create_pdf_deviation(df)