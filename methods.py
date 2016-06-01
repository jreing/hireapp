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

def buildQueryResultsPage(q):
	i=0
	
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="companyQueryResultsPage/style.css">
	<body>
	
  <div align="right">
    <p class="titletext">:שליחת משרה</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" onsubmit="return validateForm()" action="/messageSend" method="post">

      <div align="right">
        <p class="text1">:שם החברה</p>
        <input name="companyName" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="שם" id="companyName" />
      </div>

      <div align="right">
        <p class="text1">:מייל החברה</p>
        <input name="companyMail" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="מייל" id="name" />
      </div>

      <div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="jobId" />
      </div>

      <div align="right">
        <p class="text1">:תיאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" placeholder="פרטים על המשרה.."></textarea>
        
           
      </div>
	<div align="right" > <p class="medtitletextpadded">:בחר מועמדים</p> </div>

      <div id="scroll" style="overflow-y: scroll; height:600px;">"""
	  
	htmlbody=''
	hasCv=False
	
	for student in q:
		i=i+1
		hasCv=False
		if (student.cv_blob_key != None) :
			hasCv=True
			
		htmlbody+="""
			<div class="form-element" align="right">"""
			
		if (hasCv) :
			htmlbody+="""
			  <label for="studentselect"""+str(i)+"""" class="textsmallpad">בחר</label>
			  <input type="checkbox" name="studentselect" id="studentselect" """+str(i)+""" class="checkbox" 
			  value="""+str(student.user_id)+""">
			  <button type="button" onclick="location.href='getCV?user_id="""+str(student.user_id)+ """'" id="Cvbutton" """+str(i)+""" class="Cvbutton">הצג</button>
			  <p class="textbigpad">:קורות חיים</p>"""
			  
		else :
			htmlbody+="""
			  <label for="studentselect"""+str(i)+""" class="textsmallpad">בחר</label>
			  <input type="checkbox" name="studentselect" id="studentselect" """+str(i)+""" class="checkbox" 
			  value="""+str(student.user_id)+""">
			  <p class="textbigasCvButton">לא צורף</p>
			  <p class="textbigpad">:קורות חיים</p>"""
			  
		htmlbody+="""
			<p class="text" >"""+availTranslate(student.availability).decode('utf-8', 'ignore')+"""</p>
			<p class="text">:זמינות</p>
			<p class="text" >"""+yearTranslate(student.year).decode('utf-8', 'ignore')+"""</p>
			<p class="text">:שנה</p>
			<p class="text" >"""+residenceTranslate(student.residence).decode('utf-8', 'ignore')+"""</p>
			<p class="text">:איזור</p>
			<p class="text" >"""+ student.git.decode('utf-8', 'ignore')+"""</p>
			<p class="text">:גיט</p>
			</div>"""	
			  	
	
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
				<option value=0>(לא נבחר איזור)</option>
				<option value=1> תל אביב</option>
				<option value=2> השרון</option>
				<option value=3> מרכז גוש דן</option>
				<option value=4> דרום גוש דן</option>
				<option value=5> אשדוד</option>
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
		2: "השרון",
		3: "מרכז גוש דן",
		4: "דרום גוש דן",
		5: "אשדוד"
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

def buildSearchParameters():
	htmlMain = """
		  
			<div align="right">
			<p class="text1">:ציון מינימלי בקורס</p>
		  </div>
			<div class="inputline">
			  <input type="button" id="buttonadd" value="הוסף קורס" />
			</div>
			<div id="cloneme0" class="cloneme">
			  <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name"  />
			  <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="60" max="100" id="grade" placeholder="ציון" />
			  <input type="button" id="buttondel0" class="buttondel" value="הסר" />
			</div>
			<div align="right" id="bysubject">
			  <p class="text1">:ממוצע מינימלי באשכול</p>
			</div>
			<div class="inputline">
			  <input type="button" id="buttonaddtwo" value="הוסף אשכול" />
			</div>
			<div id="clonemetwo0" class="clonemetwo">
			  <select name="ctype" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input5"  id="ctype">
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
			</div>
		
			<div align="right" id=avgentry>
			  <p class="text1">:ממוצע תואר מינימלי</p>
			  <input name="avg" type="number" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" min="60" max="100" placeholder="ממוצע" id="avg" />
			</div>

		<div align="right">

			<p class="text1">:איזור מגורים</p>
		  <select name="residence" id="element2" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input4" align="right" id="validateFormcity" />
				<option value=0> כל האזורים</option>
				<option value=1> תל אביב</option>
				<option value=2> השרון</option>
				<option value=3> מרכז גוש דן</option>
				<option value=4> דרום גוש דן</option>
				<option value=5> אשדוד</option>
			  </select></div>"""
	
	htmlYear = """<br><br><div align="right" >
			  <p class="text1" id="element1">:שנת לימודים</p>
 				<select name="year" id="yearElem" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="year">
				<option value=0>(לא נבחר)</option>
				<option value=1> א</option>
				<option value=2> ב</option>
				<option value=3> ג</option>
				<option value=4> ד</option>
			  </select>
		  </div>"""
	
	htmlAvail = """<br><br>
			<div align="right" >
			  <p class="text1" id="element1">:סוג משרה</p>
			  <select name="availability" id="availElem" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" id="availability">
				<option value=0>(לא נבחר סוג)</option>
				<option value=1> חצי משרה</option>
				<option value=2> משרה מלאה</option>
				
			  </select>
			</div>"""
			
	
	return htmlMain + htmlYear +htmlAvail

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

	htmlQueryParam = buildSearchParameters()

	htmlButt ="""<div class="submit">
			  <input type="submit" value="חפש" id="button-blue" />
			  <div class="ease"></div>"""
	
	htmlCourseList = buildCourseList(course_query)	  
	
	
	htmlend="""	</form> </div></div>
		
	  </body>
	  <script type="text/javascript" src="/companyQueryFormPage/script.js"></script>
	  </html>"""
	
	# htmlGit is not in use right now	
	htmlGit = """<div class="hasgit" align="right">
			  <label for="hasgit" class="textsmallpad">חפש סטודנט עם חשבון גיט</label>
			  <input type="checkbox" value="True" name="hasgit" id="hasgit" class="checkbox"> </div>"""
	
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
      <div align="right">
        <p class="text1">:אזור מגורים</p>
      </div>
	<form class="form" id="form1" action="/dbHandler" method="post" onsubmit="return validateForm()" enctype="multipart/form-data">
	<select name="residence" id="residence" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input3" align= "right" dir="rtl" />
				<option value=""" + str(student.residence) + """>(לא נבחר איזור)</option>
				<option value=1> תל אביב</option>
				<option value=2> השרון</option>
				<option value=3> מרכז גוש דן</option>
				<option value=4> דרום גוש דן</option>
				<option value=5> אשדוד</option>
			  </select>
      <div align="right">"""

	htmlbody = """<p class="text1">:הקורסים שלי</p>
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
	htmlcv = """<br><br><div align="right" id=cventry>
				<p class="text3" id="element1" >:קורות חיים</p>
        
		<div align="right">
		<input name="cv" type="file"  class="file" accept=".pdf,.doc,.txt,.docx" id="cv" />
		</div>"""
		
	if(hasCv):	
		htmlcv += """<div><button type="button" onclick="location.href='getMyCV'" id="Cvbutton" class="Cvbutton">הצג</button>
         </div>"""

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
	
	htmlAvail = """<br><br><br><br>
			<div>
			  <p class="text2" id="element1">:סוג משרה</p>
			  <select name="availability" id="availability" class="validate[required,custom	[onlyLetter],length[0,100]] feedback-input5" dir="rtl">
				<option value=""" + str(student.availability) + """>(לא נבחר סוג)</option>
				<option value=1> חצי משרה</option>
				<option value=2> משרה מלאה</option>
				
			  </select>
			</div>"""

	htmlGit = """<br><br><br><br><div id="gitEntry" >
				<p class="text2" id="element1">:חשבון גיט</p><br><br>
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
          <div class="ease"> </div>
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

	html=htmlstart + htmlbody + htmlAvg +htmlYear + htmlAvail + htmlcv +htmlGit +htmlMail + htmlRecOffers + htmlButt +htmlDlist +htmlEndForm + htmlDel + htmlEnd
	return html

	
def buildAdPage(course_query):

	htmlstart="""<!DOCTYPE html>
	<html>
		<link rel="stylesheet" type="text/css" href="createAd/style.css">
	  <body>
		<script type="text/javascript" src="/jquery/jquery-2.2.3.js"></script>
		<script type="text/javascript" src="/CompanyToolbar/loadToolbar.js"></script>
		<form class="form" id="form1" onsubmit="return validateForm()" action="/" method="post">
		
		<div id="form-main">
		<div align="right">
		  <p class="titletext">:בניית משרה</p>
		</div>
		<div id="form-div">"""
	
	htmlSearchParam = buildSearchParameters()
	
	htmlbody = buildCourseList(course_query)
	
	htmlAdDesc  = """<div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="jobId" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="jobId" />
      </div>

      <div align="right">
        <p class="text1">:תיאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" placeholder="פרטים על המשרה.."></textarea>
		<br><br><div align="right">
		  <p class="text1">:פרמטרים לחיפוש</p>
		</div>"""
	
	htmlButt ="""<div class="submit">
			  <input type="submit" value="צור מודעה" id="button-blue" />
			  <div class="ease"></div>"""
			  
	htmlend="""	</form> </div></div>
		
	  </body>
	  <script type="text/javascript" src="/createAd/script.js"></script>
	  </html>"""
	  
	html=htmlstart+htmlAdDesc +htmlSearchParam +htmlButt +htmlbody + htmlend
	return html

	