import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

#Methods to build the companyQueryResultsPage and StudentOffersPage

def buildQueryResultsPage(q):
	i=0
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="style.css">
	<body>
	
  <div align="right">
    <p class="titletext">:שליחת משרה</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הזן משרה</p>  </div>
    <form class="form" id="form1" action="advanced.py" method="post">
      <div align="right">
        <p class="text1">:שם החברה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="שם" id="name" />
      </div>

      <div align="right">
        <p class="text1">:מייל החברה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="מייל" id="name" />
      </div>

      <div align="right">
        <p class="text1">:שם המשרה</p>
        <input name="name" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="משרה" id="name" />
      </div>

      <div align="right">
        <p class="text1">:תיאור המשרה</p>
        <textarea class="scrollabletextbox" name="note" dir="rtl" placeholder="פרטים על המשרה.."></textarea>
        
           
      </div>
	<div align="right" > <p class="medtitletextpadded">:בחר מועמדים</p> </div>

      <div id="scroll" style="overflow-y: scroll; height:450px;">"""
	  
	htmlbody=''
	
	for student in q:
		i=i+1
		htmlbody+="""

        <div class="form-element" ; align="right">

          <label for="studentselect"""+str(i)+""" class="textsmallpad">בחר</label>
          <input type="checkbox" id="studentselect"""+str(i)+""" class="texthugepad" value="select">
          <p class="text">לא צורף</p>
          <p class="textbigpad">:קורות חיים</p>
          <p class="text">"""+str(student.student.city)+"""</p>
          <p class="text">:עיר</p>

        </div>"""
	
	htmlend="""
      </div>

      <label for="select-all" class="textsmallpad">בחר הכל</label>
      <input type="checkbox" name="select-all" id="select-all" />
      <div class="submit">
        <input type="submit" value="שלח משרה" id="button-blue" />

      </div>
    </form>
	
	<script type="text/javascript" src="jquery-2.2.3.js"></script>
	<script type="text/javascript" src="script.js"></script>
  </div>
  <body>
	<html>"""

	html=htmlstart+htmlbody+htmlend
	return html
		
def buildStudentOffersPage():
	i=0
	htmlstart= """<!DOCTYPE html>
	<html>
	<link rel="stylesheet" type="text/css" href="style.css">
	<body>

  <div >
    <p class="titletext"  >:הפרופיל שלי</p>
  </div>

  <div id="form-div">
    <div align="right"> <p class="medtitletext">:הצעות שקיבלת</p>  </div>
  


      <div id="scroll">"""
	  
	htmlbody=''
	for obj in database:
		i=i+1
		htmlbody+="""

                <div class="form-element" ; align="right">
		
				<div align="right">
					<button type="button" id="button"""+i+"""" class="button">הצג פרטים</button>
					<p class="text">"""+obj.mail+"""</p>
					<p class="text">:מייל</p>
					<p class="text">"""+obj.companyName+"""</p>
					<p class="text">:שם חברה</p>
					<p class="text">"""+obj.jobName+"""</p>
					<p class="text">:שם משרה</p>
				</div>
				
				<div class="form-extra" id="extra"""+i+"""""; align="right">

				<p class="text" id="extra1" >"""+obj.description+"""</p>


				</div>
        </div>"""
	
	htmlend="""
            </div>

    <div align="right"> <p class="medtitletext" id="empty">...טרם קיבלת הצעות</p>  </div>

  </div>


  <body>
			<script type="text/javascript" src="jquery-2.2.3.js"></script>
	<script type="text/javascript" src="script.js"></script>
	<html>"""

	html=htmlstart+htmlbody+htmlend
	return html
	