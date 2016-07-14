#!/usr/bin/python
# -*- coding: utf-8 -*-

#important to support utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import cgi
import urllib
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

#function that builds an error page given a message
def errorPage(errormsg):
	html="""
	<!DOCTYPE html>
	<html lang="he">
	<link rel="stylesheet" type="text/css" href="/LogInForBarak/style.css">
	 
	<body>
		<div align="center">
			<p class="text1">"""
	html+=errormsg
	html+=	"""
		</p>
		</div>
	</body>
	<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
	<script type="text/javascript" src="/UnauthorizedToolbar/loadToolbar.js"></script>  
	</html>	
	"""

	return html

#Methods to build the companyQueryResultsPage and StudentOffersPage

def buildQueryResultsPage(q,ad_id,ad):
	i=0
	adFlag = 0
	
	if (ad_id!=None):
		adFlag = 1
	
	
	htmlstart= """<!DOCTYPE html>
	<html>
	
	<link rel="stylesheet" type="text/css" href="companyQueryResultsPage/style.css">
	<body>
	
  <div align="right">
    <p class="titletext">:שליחת משרה</p>
  </div>"""
	if (adFlag == 0):
		htmlstart+=	"""<div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" onsubmit="return validateForm()" action="/messageSend?ad_id=-1" method="post">"""
	else:
		htmlstart+=	"""<div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" onsubmit="return validateForm()" action="/messageSend?ad_id="""+ad_id+"""" method="post">"""
		
	htmlstart+="""  <div align="right">
        <p class="text1">:שם החברה</p>
        <input name="companyName" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" """ 
      
	if (adFlag == 0):
		htmlstart+="""placeholder="שם" """
	else:
		htmlstart+= """value=" """ + ad.message.compName + "\""  
	  
	htmlstart+= """id="companyName" /></div>"""

	htmlstart+=  """<div align="right">
        <p class="text1">:מייל החברה</p>
        <input name="companyMail" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" """
	
	if (adFlag == 0):
		htmlstart+="""placeholder="מייל" """
	else:
		htmlstart+= """value=" """ + ad.message.compMail + "\""
		

	htmlstart+= """id="name" /> </div>"""

	htmlstart+= """<div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" """ 
		
	if (adFlag == 0):
		htmlstart+="""placeholder="משרה" """
	else:
		htmlstart+= """value=" """ + ad.message.jobName + "\""
		
		
	htmlstart+=""" id="jobId" /></div>"""

	htmlstart+="""<div align="right">
        <p class="text1">:תאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" """

	if (adFlag == 0):
		htmlstart+="""placeholder="פרטים על המשרה..">"""
	else:
		htmlstart+= """>""" + ad.message.cont 

	htmlstart+= """</textarea>"""
        
           
	htmlstart+="""  </div>
	<div align="right" > <p class="medtitletextpadded">:בחר מועמדים</p> </div>

      <div id="scroll" style="overflow-y: scroll; height:600px;">"""
	  
	htmlbody=''
	hasCv=False
	
	for student in q:
		i=i+1
		hasCv=False
		if (student.cv_blob_key != None) :
			hasCv=True
		
		if(adFlag!=0):
			if(student.user_id in ad.sentId):
				htmlbody+="""<div class="form-element2" align="right">"""
			else:
				htmlbody+="""<div class="form-element" align="right">"""
		else:
			htmlbody+="""<div class="form-element" align="right" >"""
			
			
		
		htmlbody+="""
			<table dir="rtl" style="width:100%">
			<tr>
			<td><b>זמינות: </b></td>
			<td><b>שנה:</b> </td>
			<td><b>אזור: </b></td>
			<td><b>קורות חיים:</b></td>
			<td><b>גיליון ציונים:</b></td>
			<td><b>גיט: </b></td>
			<td><b>בחר: </b></td>
			</tr>
			<td>
			"""+availTranslate(student.availability).decode('utf-8', 'ignore')+"""
			</td>
			<td>
			"""+yearTranslate(student.year).decode('utf-8', 'ignore')+"""
			</td>
			<td>
			"""+residenceTranslate(student.residence).decode('utf-8', 'ignore')+"""
			</td>
			<td>
			"""
		if (hasCv) :
			htmlbody+="""
			  <button type="button" onclick="window.open('getCV?user_id="""+str(student.user_id)+ """')" id="Cvbutton" """+str(i)+""" class="Cvbutton">הצג</button>
			  </td><td>"""
			  
		else :
			htmlbody+="""לא צורף</td><td>"""  
		
		htmlbody+="""
		<button type="button" onclick="window.open('gradeSheet?user_id="""+str(student.user_id)+ """')" id="Cvbutton" """+str(i)+""" class="Cvbutton">הצג</button>
		</td><td>"""
		
		
		if (student.git!=""):	
			htmlbody+="""
			<a href="http://www."""+ student.git.decode('utf-8', 'ignore')+""" "> חשבון גיט</a>
			"""
		else:
			htmlbody+="""לא הוזן"""
		
		htmlbody+="""</td><td>
			<input type="checkbox" id="studentselect" """+str(i)+""" class="checkbox" 
			value="""+str(student.user_id)+"""></td>
		</tr></table></div>"""
	
	htmlend="""
      </div>
		
      <label for="select-all" class="textsmallpad">בחר הכל</label>
      <input type="checkbox" name="select-all" id="select-all" />
      <div class="submit">
        <input type="submit" value="שלח משרה" id="button-blue" />

      </div>
    </form>

  </div>
  </body>
  	<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
	<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
	<script type="text/javascript" src="companyQueryResultsPage/script.js"></script>
	
	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html
		
def buildStudentOffersPage(conv_query, user_id):
	i=0
	htmlstart= """<!DOCTYPE html>
	<html>
	
	<link rel="stylesheet" type="text/css" href="StudentOffersPage/style.css">
	<body>
	<script type="text/javascript" src="StudentOffersPage/jquery-2.2.3.js" defer></script>
	<script type="text/javascript" src="StudentToolbar/loadToolbar.js" defer></script>
	<script type="text/javascript"  src="StudentOffersPage/script.js" defer></script>
  <div >
    <p class="titletext"  >:ההצעות שלי</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הצעות שקיבלת</p>  </div>
  


      <div id="scroll">"""
	  
	htmlbody=''
	
	for conver in conv_query:
		for message in conver.message:
			if(message.receiver.identity == user_id):
				#send = Student.query(Student.id==message.sender.identity).get()
				#send = users.User(_user_id = message.sender.identity)
				i=i+1
				htmlbody+="""

				        <div class="form-element" ; align="right">
		
						<div align="right">
							<button type="button" id="button"""+str(i)+"""" class="button">הצג פרטים</button>
							<p class="text">"""+str(message.compMail)+"""</p>
							<p class="text">:מייל</p>
							<p class="text">"""+str(message.compName)+"""</p>
							<p class="text">:שם חברה</p>
							<p class="text">"""+str(message.jobName)+"""</p>
							<p class="text">:שם משרה</p>
						</div>
				
						<div class="form-extra" id="extra"""+str(i)+"""""; align="right">

						<p class="text" id="extra1" >""" +str(message.cont)+ """</p>


						</div>
				</div>"""
	
	emptypage="""
            </div>

    <div align="right"> <p class="medtitletext" id="empty">...טרם קיבלת הצעות</p>  </div>

  </div>"""

	htmlend = """
  </body>
	
	
	
	
	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html


def buildStudentInputPage(course_query):
	i=0
	message=""" This is my statement one.\n;This is my statement2"""
	htmlstart="""<!DOCTYPE html>
	<html lang="he">
		<link rel="stylesheet" type="text/css" href="studentInputPage/style.css">
		

	  <body>
		<script type="text/javascript" src="studentInputPage/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/StudentToolbar/loadToolbarInputPage.js"></script>
	  <div id="form-main">
		<div align="right">
		  <p class="titletext">:הרשמה</p>
		</div>
		<div id="form-div">
	
		<form class="form" id="form1" onsubmit="return validateForm()" action="/dbHandler" method="post" enctype="multipart/form-data">
		  <div>
			  <p class="text2" id="element1">:הזן אזור מגורים</p>
 				<select name="residence" id="element2" dir="rtl" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input4" placeholder="אזור" id="residence">
				<option value=0>(לא נבחר אזור)</option>
				<option value=1> תל אביב</option>
				<option value=2> הרצליה-רמת השרון</option>
				<option value=3> ר"ג-גבעתיים</option>
				<option value=4> ראשל"צ-חולון-בת ים</option>
				<option value=5> אשדוד</option>
				<option value=6> רחובות-נס ציונה</option>
				<option value=7> פתח תקווה והסביבה</option>
				<option value=8> רעננה-כפ"ס-הוד השרון</option>
				<option value=9> ראש העין והסביבה</option>
				<option value=10> בקעת אונו</option>
				<option value=11> בני ברק-גבעת שמואל</option>
				<option value=12> שוהם והסביבה</option>
				<option value=13> רמלה-לוד</option>
				<option value=14> מודיעין והסביבה</option>
				<option value=15> נתניה והסביבה</option>
				<option value=16> השרון</option>
				
			  </select>
		  </div>
		  
		  <div align="right" id="gradeentry">
		    <p class="text1">:הזן קורסים וציונים</p>
		  </div>
		  
		    <div class="inputline">
		      <input type="button" id="buttonadd" value="הוסף קורס" />
		    </div>
		    <div id="cloneme0" class="cloneme">
		      <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name" />
		      <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder="ציון" />
		      <input type="button" id="buttondel0" class="buttondel" value="הסר" />
			  
		    </div>
		

		    <div id="avgEntry" >
				<p class="text2" id="element1">:הזן ממוצע כללי</p> 

				<input name="average" type="number" class="average" id="element2" min="60" max="100" id="average" placeholder="ממוצע" />			  
			</div>
			<div>
			  <p class="text2" id="element1">:שנת לימודים</p>
 				<select name="year" id="element2" dir="rtl" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="year">
				<option value=0>(לא נבחר )</option>
				<option value=1> 'א</option>
				<option value=2> 'ב</option>
				<option value=3> 'ג</option>
				<option value=4> 'ד</option>
			  </select>
		  </div>
			
			<br><br><br><br>
			<div>
			  <p class="text2" id="element1">:הזן סוג משרה</p>
			  <select name="availability" id="element2" dir="rtl" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="availability">
				<option value=0>(לא נבחר סוג)</option>
				<option value=1> חצי משרה</option>
				<option value=2> משרה מלאה</option>
				
			  </select>
			</div>
			
			<br><div align="right" id="cventry">
		      <p class="text2" id="element1" >:אופציונלי-הזן קורות חיים</p>
			  <input name="cv" type="file" id="element2" class="file" accept=".pdf,.doc,.txt,.docx" id="cv" />
		    </div>
			
			
			<br><div id="gitEntry" >
				<p class="text2" id="element1">:אופציונלי - הזן חשבון גיט</p><br><br>

				<input name="git" type="text" class="git" id="git" placeholder="" />			  
			</div>
			
			
			<br><br><br>
		    <div class="getEmailNotification" align="right">
			  <label for="getEmailNotification" class="textsmallpad">לחץ כאן במידה והינך מעוניין לקבל עדכון במייל לגבי הצעת משרה</label>
			  <input type="checkbox" value="True" name="getEmailNotification" id="getEmailNotification" class="checkbox" >
			</div>
			
			<div id="info">
			<a class="ui-btn ui-btn-inline ui-corner-all ui-icon-info ui-btn-icon-right" data-rel="dialog" id="masterTooltip" title=" """+message+""" ">פרטיות</a>			

			</div>
			
		    <div class="submit">
		      <input type="submit" value="שלח" id="button-blue" />
		      <div class="ease"> </div>
		    </div>
			<datalist id="courses" hidden>"""
	htmlbody=''
	
	for course in course_query:
		i=i+1
		htmlbody+="""<option> """+  str(course.course_name) + """</option> data-id="1" """
		
	htmlend="""</datalist>
		  </form>
		</div>
		<div class="validation-result hidden"></div>
			
		
	  </div>
	  </body>


		<script type="text/javascript" src="studentInputPage/script.js"></script>

	<link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">
	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html

def residenceTranslate(num):
	return{
		1: "תל אביב",
		2: "הרצליה-רמת השרון",
		3: 'ר"ג-גבעתיים',
		4: 'ראשל"צ-חולון-בת ים',
		5: "אשדוד והסביבה",
		6: "רחובות-נס ציונה",
		8: 'רעננה-כפ"ס-הוד השרון',
		7: "פתח תקווה והסביבה",
		9: "ראש העין והסביבה",
		10: "בקעת אונו",
		11: "בני ברק-גבעת שמואל",
		12: "שוהם והסביבה",
		13: "רמלה-לוד",
		14: "מודיעין והסביבה",
		15: "נתניה והסביבה",
		16: "השרון"
	} .get(num, "לא הוזן")
	
def yearTranslate(num):
	return{
		1: "א",
		2: "ב",
		3: "ג",
		4: "ד",
	} .get(num, "לא הוזן")	
	
def availTranslate(num):
	return{
		1: "חצי משרה",
		2: "משרה מלאה",
	} .get(num, "לא הוזן")

def buildSearchParameters(ad_query):
	
	dynFlag = 0
	if (ad_query==1):
		dynFlag = 2
	elif(ad_query==None):
		logging.info("dynamic not recognized")
		dynFlag = 0
	else:
		logging.info("dynamic recognized")
		dynFlag = 1
	
	logging.info(dynFlag)
	
	htmlMain = """
			<div align="right">
			<p class="text1">:ציון מינימלי בקורס</p>
		  </div>
			<div class="inputline">
			  <input type="button" id="buttonadd" value="הוסף קורס" />
			</div>"""
	htmlbody =""		
	if (dynFlag==1 and len(ad_query.aQuery.student_courses)>0):
		j = 0
		for crs in ad_query.aQuery.student_courses:
			if (crs!=None):
				htmlbody+= """
				  <div id="cloneme""" + str(j) + """" class="cloneme">
				  <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" value='""" + str(crs.course.course_name) + """' id="name" />
				  <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" value='""" + str(crs.grade) + """' />
				  <input type="button" id="buttondel""" + str(j) + """" class="buttondel" onclick= "b(this.id)" value="X" />
				 </div>"""
				j+=1
	else:
		htmlbody+= """<div id="cloneme0" class="cloneme">
			  <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name"  />
			  <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder="ציון" />
			  <input type="button" id="buttondel0" class="buttondel" onclick= "b(this.id)" value="הסר" />
			</div>"""
	
	htmlbody+= """<div align="right" id="bysubject">
			  <p class="text1">:ממוצע מינימלי באשכול</p>
			</div>
			<div class="inputline">
			  <input type="button" id="buttonaddtwo" value="הוסף אשכול" />
			</div>"""
			
	
	if (dynFlag==1):
		k = 0	
		for crs in ad_query.aQuery.ctypes:
			if (crs!=None):
				htmlbody+="""<div id="clonemetwo""" + str(k) + """" class="clonemetwo">
				<select name="ctype" id="ctype""" + str(k) + """"  class="validate[required,custom[onlyLetter],length[0,100]] feedback-input5"  id="ctype">
				<option value=""" + str(ad_query.aQuery.ctypes[k]) + """>(לא נבחר אשכול)</option>
				<option value=1>מתמטיקה</option>
				<option value=2>תכנות</option>
				<option value=3>תאוריות מדעי המחשב</option>
				<option value=4>אבטחת מידע</option>
				<option value=5>מדעי המידע</option>
				<option value=6>רשתות</option>
				<option value=7>ביואינפורמטיקה</option>
			  </select>
			  
			  <input name="ctype_avg" type="number" class="validate[required,custom[email]] feedback-input6" min="60" max="100" id="ctype_avg" value=""" + str(ad_query.aQuery.ctype_avgs[k]) + """ />
			  <input type="button" id="buttondeltwo""" + str(k) + """" class="buttondeltwo" onclick= "btwo(this.id)" value="הסר" />
			</div>"""
				k +=1
		
	else:
		htmlbody+= """<div id="clonemetwo0" class="clonemetwo">
				<select name="ctype" id="ctype" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input5"  id="ctype">
				<option selected="selected"  value=0>(לא נבחר אשכול)</option>
				<option value=1>מתמטיקה</option>
				<option value=2>תכנות</option>
				<option value=3>תאוריות מדעי המחשב</option>
				<option value=4>אבטחת מידע</option>
				<option value=5>מדעי המידע</option>
				<option value=6>רשתות</option>
				<option value=7>ביואינפורמטיקה</option>
			  </select>
	
			  <input name="ctype_avg" type="number" class="validate[required,custom[email]] feedback-input6" min="60" max="100" id="ctype_avg" placeholder="ממוצע" />
			  <input type="button" id="buttondeltwo0" class="buttondeltwo" value="הסר" />
			</div>"""
			
	htmlbody+=	"""<div align="right" id=avgentry>
			  <p class="text1">:ממוצע תואר מינימלי</p>
			  <input name="avg" type="number" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" min="60" max="100" id="avg" """
	
	if (dynFlag==1):
		htmlbody+="""value='""" + str(ad_query.aQuery.avg) + """'"""
	else:
		htmlbody+="""placeholder="ממוצע" """
		
	htmlbody+="""/>	</div>

		<div align="right">

			<p class="text1">:אזור מגורים</p>
		  <select name="residence" id="residence" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input4" align="right" id="validateFormcity" />"""
		  
	if(dynFlag==1):	
		htmlbody+="""<option value=""" + str(ad_query.aQuery.residence) + """> כל האזורים</option>"""
	else:
		htmlbody+="""<option value=0> כל האזורים</option>"""
	
	htmlbody+="""
		<option value=1> תל אביב</option>
		<option value=2> הרצליה-רמת השרון</option>
		<option value=3> ר"ג-גבעתיים</option>
		<option value=4> ראשל"צ-חולון-בת ים</option>
		<option value=5> אשדוד</option>
		<option value=6> רחובות-נס ציונה</option>
		<option value=7> פתח תקווה והסביבה</option>
		<option value=8> רעננה-כפ"ס-הוד השרון</option>
		<option value=9> ראש העין והסביבה</option>
		<option value=10> בקעת אונו</option>
		<option value=11> בני ברק-גבעת שמואל</option>
		<option value=12> שוהם והסביבה</option>
		<option value=13> רמלה-לוד</option>
		<option value=14> מודיעין והסביבה</option>
		<option value=15> נתניה והסביבה</option>
		<option value=16> השרון</option>
		</select></div>"""
	
		
	htmlYear = """<br><br><div align="right" >
			  <p class="text1" id="element1">:שנת לימודים</p>
 				<select name="year" id="year" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="year">"""
	if(dynFlag==1):	
		htmlYear+="""<option value=""" + str(ad_query.aQuery.year) + """>(לא נבחר)</option>"""
	else:
		htmlYear+="""<option value=0>(לא נבחר)</option>"""
		
	htmlYear+="""<option value=1> א</option>
				<option value=2> ב</option>
				<option value=3> ג</option>
				<option value=4> ד</option>
			  </select>
		  </div>"""
	
	htmlAvail = """<br><br>
			<div align="right" >
			  <p class="text1" id="element1">:סוג משרה</p>
			  <select name="availability" id="availability" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="availability">"""
	if(dynFlag==1):	
		htmlAvail+="""<option value=""" + str(ad_query.aQuery.availability) + """>(לא נבחר סוג)</option>"""
	else:
		htmlAvail+="""<option value=0>(לא נבחר סוג)</option>"""	

	htmlAvail+="""<option value=1> חצי משרה</option>
				<option value=2> משרה מלאה</option>
				
			  </select>
			</div>"""
	htmlEmail = ""
	if (dynFlag>0):
		htmlEmail+= """<div class="getEmailNotification" align="right">
			  <label for="getEmailNotification" class="textsmallpad">שלח לי עדכון כאשר יש מועמדים חדשים למשרה</label>
			  <input type="checkbox" value="True" name="getEmailNotification" id="getEmailNotification" class="checkbox" """
		
		if(dynFlag==1):
			if(ad_query.aQuery.scheduler == True):
				htmlEmail+= """checked"""
		
		htmlEmail+= """> </div>"""		
	
	return htmlMain +htmlbody+ htmlYear +htmlAvail + htmlEmail

def buildCourseList(course_query):
	i = 0
	htmlbody="""<div><datalist id="courses" hidden>"""
	
	for course in course_query:
		i=i+1
		htmlbody+="""<option> """+  str(course.course_name) + """</option data-id="1"> \n"""
	
	htmlbody+= """</datalist>"""
	
	return htmlbody
	
def buildCompanyQuery(course_query):
	i=0
	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="companyQueryFormPage/style.css">
	  <body>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
		
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:חיפוש מועמדים</p>
		</div>
		<div id="form-div">
		<form class="form" id="form1" onsubmit="return validateForm()" action="/companyQueryResultsPage" method="post">"""

	htmlQueryParam = buildSearchParameters(None)

	htmlButt ="""<p class="text1" dir="rtl">
	לתשומת לבכם: שאילתא ריקה תניב את כל הסטודנטים הרשומים באתר כרגע</p>
	
	<div class="submit">
			  <input type="submit" value="חפש" id="button-blue" />
			  <div class="ease"></div>"""
	
	htmlCourseList = buildCourseList(course_query)	  
	
	
	htmlend="""	
	</form> </div></div>
	  </body>
	  <script type="text/javascript" src="/companyQueryFormPage/script.js"></script>
	  </html>"""
	
	
	html=htmlstart+ htmlQueryParam +htmlButt + htmlCourseList + htmlend
	return html

def buildStudentEditPage(student, course_query):
	hasCv=False
	
	htmlstart="""﻿<!DOCTYPE html>
	<html lang="he">
	<link rel="stylesheet" type="text/css" href="studentEditPage/style.css">
	<script type="text/javascript" src="studentEditPage/jquery-2.2.3.js"></script>
	<body>
	
	<script type="text/javascript" src="/StudentToolbar/loadToolbar.js"></script>
	<div id="form-main">
	<div align="right">
		<p class="titletext">:הפרטים שלי</p>
	</div>
	<div id="form-div">
		<div align="right" dir="rtl">
			<p class="text1">מספר צפיות בקורות החיים שלי: """+ str(student.cv_view_cnt)\
			+ """</p>
			<p class="text1">מספר צפיות בגיליון הציונים שלי: """+ str(student.gradesheet_view_cnt)\
			+ """</p>
			<p class="text1">אזור מגורים:</p>
		</div>
	<form class="form" id="form1" action="/dbHandler" method="post" onsubmit="return validateForm()" enctype="multipart/form-data">
	<select name="residence" id="residence" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input3" align= "right" dir="rtl" />
		<option value=""" + str(student.residence) + """>(לא נבחר אזור)</option>
		<option value=1> תל אביב</option>
		<option value=2> הרצליה-רמת השרון</option>
		<option value=3> ר"ג-גבעתיים</option>
		<option value=4> ראשל"צ-חולון-בת ים</option>
		<option value=5> אשדוד</option>
		<option value=6> רחובות-נס ציונה</option>
		<option value=7> פתח תקווה והסביבה</option>
		<option value=8> רעננה-כפ"ס-הוד השרון</option>
		<option value=9> ראש העין והסביבה</option>
		<option value=10> בקעת אונו</option>
		<option value=11> בני ברק-גבעת שמואל</option>
		<option value=12> שוהם והסביבה</option>
		<option value=13> רמלה-לוד</option>
		<option value=14> מודיעין והסביבה</option>
		<option value=15> נתניה והסביבה</option>
		<option value=16> השרון</option>
	</select>"""

	htmlbody = """<div align="right"> 
					<p class="text1">:הקורסים שלי</p>
      			  </div>
		<div class="inputline">
          <input type="button" id="buttonadd" value="הוסף קורס" />
        </div>"""
	j = 0
	for crs in student.student_courses:

		if (crs!=None):
			htmlbody+= """
			<div id="cloneme""" + str(j) + """" class="cloneme">
			  <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" value='""" + str(crs.course.course_name) + """' id="name" />
			  <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" value='""" + str(crs.grade) + """' />
			  <input type="button" id="buttondel""" + str(j) + """" class="buttondel" onclick= "b(this.id)" value="X" />
			 </div>"""
			j+=1

	if (student.cv_blob_key != None) :
			hasCv=True

	if(hasCv):
		htmlcv = """<div align="right" id=cventry>
					<p class="text3" id="element1">:קורות החיים שהזנת</p>"""
		
		htmlcv += """<button type="button" onclick="location.href='getMyCV'" id="Cvbutton" class="Cvbutton">הצג</button>"""
		
		htmlcv += """<div>
    				<p class="text4">:החלפת קורות חיים</p>
    				<input name="cv" type="file"  class="file" accept=".pdf,.doc,.txt,.docx" id="cv"/>
    			 </div>"""
	else:
    				htmlcv = """<div>
    				<p class="text4">:הזנת קורות חיים</p>
    				<input name="cv" type="file"  class="file" accept=".pdf,.doc,.txt,.docx" id="cv"/>"""

	htmlAvg = """<div align="right" id="avgEntry" >
					<p class="text2" id="element1">:ממוצע כללי </p> 
					<input name="average" type="number" class="average" id="element2" min="60" max="100" id="average" value='""" + str(student.avg) + """' />			  
				 </div>"""
	htmlYear = """<div>
					<p class="text2" id="element1">:שנת לימודים</p>
 				    <select name="year" id="year" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" dir="rtl" >
						<option value=""" + str(student.year) + """>(לא נבחר )</option>
						<option value=1> א'</option>
						<option value=2> ב'</option>
						<option value=3> ג'</option>
						<option value=4> ד'</option>
			  		</select>
		  		  </div>"""
	
	htmlAvail = """<br>
			<div>
			  <p class="text2" id="element1">:סוג משרה</p>
			  <select name="availability" id="availability" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" dir="rtl">
				<option value=""" + str(student.availability) + """>(לא נבחר סוג)</option>
				<option value=1> חצי משרה</option>
				<option value=2> משרה מלאה</option>
				
			  </select>
			</div>"""

	htmlGit = """<div id="gitEntry" >
					<br><br><p class="text2" id="element1">:חשבון גיט</p>
					<input name="git" type="text" class="git" id="git" placeholder="" value= '""" + str(student.git) + """' />			  
				 </div>"""
	htmlMail = """<br><br><br><br><div class="getEmailNotification" align="right">
			  		<label for="getEmailNotification" class="textsmallpad">שלח לי עדכון במייל לגבי הצעות שקיבלתי</label>
			  <input type="checkbox" value="True" name="getEmailNotification" id="getEmailNotification" class="checkbox" """
	

	if(student.allow_emails == True):
		htmlMail+="""checked"""
	
	htmlMail+="""> </div>"""
	
	htmlRecOffers = """<br><br><div class="receiveOffers" align="right">
			  <label for="receiveOffers" class="textsmallpad">מצאתי משרה, אל תשלח לי הודעות בינתיים</label>
			  <input type="checkbox" value="True" name="receiveOffers" id="receiveOffers" class="checkbox" """
	

	logging.info(student.needs_job)
	#inverting values
	if(student.needs_job != True): 
    
		htmlRecOffers+="""checked"""
	
	htmlRecOffers+="""> </div>"""
	
	
	htmlButt = """<div class="submit">
          <input type="submit" form="form1" value="שמור" id="button-blue" />
          <div class="ease"> <br> <br></div>
        </div>"""

	

	htmlDlist= """<datalist id="courses" hidden>"""
	i = 0 
	for course in course_query:
		i=i+1
		htmlDlist+="""<option data-id="1" > """+  str(course.course_name) + """</option> \n"""
		
	htmlEndForm="""</datalist>
      </form> 
    </div>	
  """
	htmlEnd = """</div></body> 
	<script type="text/javascript" src="studentEditPage/script.js"></script>
  </html>"""
  
	htmlDel = """<div><button type="button" onclick="delClick()" id="delButton" class="delButton">הסר פרופיל</button> </div>"""

	html=htmlstart + htmlbody + htmlAvg +htmlYear + htmlAvail + htmlcv +htmlGit +htmlMail + htmlRecOffers + htmlButt +"<br>"+"<br>"+htmlDlist +htmlEndForm + htmlDel + htmlEnd
	return html

	
def buildAdPage(course_query):

	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="createAd/style.css">
	  <body>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
		<form class="form" id="form1" onsubmit="return validateForm()" action="/processAd?ad_id=-1" method="post">
		
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:בניית משרה</p>
		</div>
		<div id="form-div">"""
	
	htmlSearchParam = buildSearchParameters(1)
	
	htmlbody = buildCourseList(course_query)
	
	htmlAdDesc  = """<div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="jobId" />
      </div>

      <div align="right">
        <p class="text1">:תאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" class="note" dir="rtl" placeholder="פרטים על המשרה.." id="note"></textarea>
		<br><br><div align="right">
		  <p class="text1">:פרמטרים לחיפוש</p>
		</div>"""
	htmlFreq = """<div>
			  <p class="text1" id="element1">:תדירות עדכון</p>
 				<select name="freq" id="freq" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" dir="rtl" >
				<option value=0">(לא נבחר )</option>
				<option value=1> 24 שעות</option>
				
			  </select>
		  </div>"""
	
	htmlButt ="""  <p class="text1" id="element1" dir="rtl">
	לתשומת לבכם: 
	על מנת שסטודנטים יוכלו לראות את ההודעה יש להיכנס לתוצאות
	החיפוש ולשלוח אותה. </p>
	
	<div class="submit">
			  <input type="submit" value="צור מודעה" id="button-blue" />
			  <div class="ease"></div>"""
			  
	htmlend="""	</fodrm> </div></div>
		
	  </body>
	  <script type="text/javascript" src="/createAd/script.js"></script>
	  </html>"""
	  
	html=htmlstart+htmlAdDesc +htmlSearchParam +htmlButt +htmlbody + htmlend
	return html

def EditAdPage(course_query,ad_query,ad_id):

	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="editAd/style.css">
	  <body>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
		<form class="form" id="form1" onsubmit="return validateForm()" action="/processAd?ad_id="""+ad_id+"""" method="post">
	
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:עריכת משרה</p>
		</div>
		<div id="form-div">"""
	
	htmlSearchParam = buildSearchParameters(ad_query)
	
	htmlbody = buildCourseList(course_query)
	
	htmlAdDesc  = """<div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" value='""" + ad_query.message.jobName + """' id="jobId" />
      </div>

      <div align="right">
        <p class="text1">:תאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" id="note" dir="rtl">"""+ ad_query.message.cont +"""</textarea>
		<br><br><div align="right">
		  <p class="text1">:פרמטרים לחיפוש</p>
		</div>"""
	
	htmlButt =""" <p class="text1" id="element1" dir="rtl">
	לתשומת לבכם: 
	על מנת שסטודנטים יוכלו לראות את ההודעה יש להיכנס לתוצאות
	החיפוש ולשלוח אותה. </p>
	
	<div class="submit">
			  <input type="submit" value="ערוך מודעה" id="button-blue" />
			  <div class="ease"></div>"""
			  
	htmlend="""	</form> </div></div>
		
	  </body>
	  <script type="text/javascript" src="/editAd/script.js"></script>
	  </html>"""
	  
	html=htmlstart+htmlAdDesc +htmlSearchParam +htmlbody +htmlButt + htmlend
	return html

def buildCurrentAdsPage(ad_query):
	logging.info("entered buildCurrentAdsPage")
	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="currentAds/style.css">
	  <body>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:המשרות שלי</p>
		</div>
		<div id="form-div">"""
	
	htmlbody=""
	
	i = 0 
	for ad in ad_query:
		htmlbody+="""<div class="form-element" align="right">
			<p class="text1">"""+str(ad.message.jobName) + """</p>
			<br><br><p class="text2" >"""+str(ad.message.cont)+"""</p></div>
			<br><br><div><button type="button2" id="button2" onclick="location.href='deleteAd?ad_id="""+str(i)+ """'" id="showRes" class="showRes">מחק</button>
			<button type="button" id="button" onclick="location.href='editAd?ad_id="""+str(i)+ """'" " id="editAd" class="editAd">ערוך משרה</button></div>
			<button type="button" id="button" onclick="location.href='showAdResults?ad_id="""+str(i)+ """'" id="showRes" class="showRes">הצג תוצאות</button>			
			<br><br>"""
		i+=1
			
		
	htmlend="""</div>
		
	  </body>
	  <script type="text/javascript" src="/currentAds/script.js"></script>
	  </html>"""
	  
	html=htmlstart+htmlbody + htmlend
	return html

def buildCompanySignUp():
	html="""<!DOCTYPE html>
	<html lang="he">
		<link rel="stylesheet" type="text/css" href="companySignUp/style.css">
		

	  <body>
		<script type="text/javascript" src="companySignUp/jquery-2.2.3.js"></script>
	  	<script type="text/javascript" src="/signUpToolbar/loadToolbar.js"></script>
		

		<div id="form-main">
	
		<div id="form-div">

		<div align="right"> <p class="pink">מטרת האתר היא לסייע לקשר בין מעסיקים לסטודנטים למדעי המחשב מאוניברסיטת תל אביב. האתר מאפשר לסטודנטים להעלות לאתר את הקורסים שלמדו וקורות חיים ומאפשר למעסיקים לחפש את הסטודנטים שמתאימים למשרות שברצונם להציע   </p><br></div>

		<div align="right"> <p class="cyan">על מנת להשתמש באתר כמעסיק יש צורך בתהליך הרשמה קצר. נא מלא את השדות שלמטה ולאחר מכן לחץ על "הרשם". בסיום תהליך ההרשמה הבקשה תשלח לתהליך אישור קצר שבסיומו יהיה ניתן להתחבר לאתר ולהתחיל לחפש סטודנטים </p></div>
	
		<form class="form" id="form1" onsubmit="return validateForm()" action="/signUpHandler" method="post" enctype="multipart/form-data">

<div align="right">
				<p class="text1" id="element1">תפקיד</p><br><br>

				<input name="role" type="text" class="role" id="role" placeholder="" /> </div>

<div align="right">
				<p class="text1" id="element1">שם חברה/מעסיק</p><br><br>

				<input name="compName" type="text" class="compName" id="compName" placeholder="" /></div>

<div align="right">
				<p class="text1" id="element1">מייל לשם כניסה לאתר (עם סיומת (@gmail.com</p><br><br>

				<input name="mailAdd" type="text" class="mailAdd" id="mailAdd" placeholder="" /></div>"""



	htmlButt ="""<div class="submit">
			  <input type="submit" value="הרשם" id="button-blue" />
			  <div class="ease"></div>"""

	htmlEnd = """</div></div></form> </body>
	<script type="text/javascript" src="/companySignUp/script.js"></script></html>
	<link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css">"""

	return html + htmlButt + htmlEnd

	
#function that dynamically builds help page depending on
#type of user and login state

def buildHelpPage(isStudent, isCompany):
	
	html="""
	<!DOCTYPE html>
	<html lang="he">
		<link rel="stylesheet" type="text/css" href="/HelpPage/style.css">
	 <body>
		<div id="form-main">
			<div id="form-div">
			<div align="right">
	"""
	if (isStudent and isCompany):
		html+="""
		<p class="student"> :אם הינך סטודנט</p>
		"""
	if (isStudent): 
		html+="""
		<p class="red" dir="rtl">
		1. הזן פרטים 
		<img src="/HelpPictures/HelpPic1.png" height="600" width="500" vspace="10">
		<br>
		2. המתן לקבלת הצעה
		<img src="/HelpPictures/HelpPic2.png" height="300" width="500" vspace="10">
		<br>
		3. הצעות עבודה חדשות יופיעו באתר כך
		(תוכל לבחור לקבל עדכונים על כך במייל)
		<img src="/HelpPictures/HelpPic3.png" height="300" width="500" vspace="10">
		<br>
		</div>
		"""
	html+="""<div align="right">"""
	
	if (isCompany==True and isStudent==True):
		html+="""
		
		<p class="company"> :אם הינך מעסיק</p>
		"""
	if (isCompany):
		html+="""
		<p class="red" dir="rtl">
		1. בנה משרה
		<img src="/HelpPictures/HelpPic4.png" height="350" width="500" vspace="10">
		<br>
		2. באפשרותך לצפות בסטודנטים מתאימים למשרה או לערוך אותה
		<img src="/HelpPictures/HelpPic5.png" height="150" width="500" vspace="10">
		<br>
		3. בחר מועמדים מרשימת המועמדים המתאימים ושלח להם את המשרה
		<br>
		(תוכל לבחור לקבל עדכונים למייל כאשר נרשמים לאתר סטודנטים חדשים המתאימים למשרה)
		<img src="/HelpPictures/HelpPic6.png" height="300" width="500" vspace="10">
		</div>
		"""
		
	html+="""</div>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/HelpPage/decideToolbar.js"></script>
		</body>
		</html>
		"""
	return html
	
#function that builds gradesheet page given student id
def buildGradeSheetPage(student):
	hasCv=False
	
	htmlstart="""﻿<!DOCTYPE html>
	<html lang="he">
	<link rel="stylesheet" type="text/css" href="gradeSheet/style.css">
	<script type="text/javascript" src="studentEditPage/jquery-2.2.3.js"></script>
	<body>
	
	<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
	<div id="form-main">
	<div align="right">
		<p class="titletext">:פרטי הסטודנט</p>
	</div>
	<div id="form-div">
		"""

	htmlbody = """<div align="right"> 
					<p class="text1">:גיליון ציונים</p>
      			  </div>
		"""
	j = 0
	htmlbody+="""<table dir="rtl" align="right" class="text3"
		border=1 width=100%>"""
	for crs in student.student_courses:
		
		if (crs!=None):
			htmlbody+= """<tr><td> 
			"""+ str(crs.course.course_name) + """
			</td> <td> """+ str(crs.grade) + """</td> </tr>
			 """
	
	htmlbody+="""</table>"""
	
	if (student.cv_blob_key != None) :
			hasCv=True
	
	if(hasCv):
		htmlbody+= """<div align="right" id=cventry>
				<p class="text1" id="element1">:קורות החיים שהוזנו"""
		
		htmlbody+= """<button type="button" align="left"
		onclick="window.open('getCV?user_id=""" \
		+str(student.user_id)+ """ ')"
		id="Cvbutton" class="Cvbutton">הצג</button>"""
		
	htmlbody+="""<div align="right">
			<p class="text1">אזור מגורים:
			""" + residenceTranslate(student.residence) + """
		</p>
		
			<p class="text1">ממוצע כללי:  
			""" + str(student.avg) + """
		</p>
			<p class="text1">סוג משרה:  
			""" + availTranslate(student.availability) + """
		</p>
		
			<p class="text1">שנת לימודים:  
			""" + yearTranslate(student.year) + """
		</p></div>"""
	if (student.hasgit):
		htmlbody+="""
		<div align="right">
			<p class="text1">גיט:  
			<a href="http://www."""+ student.git.decode('utf-8', 'ignore')+"""
			"> חשבון גיט</a>
		</p></div>"""
	
	htmlEnd = """</div></div></body> 
	</html>"""
  
	html=htmlstart + htmlbody+"<br>"+"<br>"  + htmlEnd
	
	return html

