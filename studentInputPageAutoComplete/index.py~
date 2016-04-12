#!/usr/bin/python
# -*- coding: utf-8 -*-

#important to support utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import cgi
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

def buildStudentInputPage(cours_query):
	i=0
	htmlstart="""<!DOCTYPE html>
	<html lang="he">
		<link rel="stylesheet" type="text/css" href="style.css">
	  <body>
	  <div id="form-main">
		<div align="right">
		  <p class="titletext">:הרשמה</p>
		</div>
		<div id="form-div">
		  <div align="right">
		    <p class="text1">:הזן עיר מגורים</p>
		  </div>
		<form class="form" id="form1" action="/dbHandler" method="post" onsubmit="return validateForm()">
		  <input name="city" type="text" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input3" placeholder="עיר" id="city" />
		  <div align="right">
		    <p class="text1">:הזן קורסים וציונים</p>
		  </div>
		  

		    <div class="inputline">
		      <input type="button" id="buttonadd" value="הוסף קורס" />
		    </div>
		    <div id="cloneme0" class="cloneme">


		      <input name="name" type="text" list="courses" class="validate[required,custom[onlyLetter],length[0,100]] feedback-input" placeholder="שם קורס" id="name" autocomplete="off"/>



		      <input name="grade" type="number" class="validate[required,custom[email]] feedback-input2" min="0" max="100" id="grade" placeholder="ציון" />
		      <input type="button" id="buttondel0" class="buttondel" value="X" />
			  
		    </div>
		


		
		
		    <div align="right" id=cventry>
		      <p class="text1" >:אופציונלי-הזן קורות חיים</p>
		    </div>
		    <input name="cv" type="file" id="cv" />
		    <div class="submit">
		      <input type="submit" value="שלח" id="button-blue" />
		      <div class="ease"> </div>
		    </div>
			<datalist id="courses" hidden>"""
	htmlbody=''
	
	for course in cours_query:
		i=i+1
		htmlbody+=
		"""<option value="""+str(course.course_name)+""" data-id="1">"""
		
	htmlend="""</datalist>
		  </form>
		</div>
		<div class="validation-result hidden"></div>
			<script type="text/javascript" src="jquery-2.2.3.js"></script>
		<script type="text/javascript" src="script.js"></script>
	  </div>

	  </body>

	</html>"""

	html=htmlstart+htmlbody+htmlend
	return html
