<html>
<head><title>Welcome::CEL SMS (Server Monitoring System)</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>
<body>
<h2 align = "center">SYSTEM INFORMATION</h2>
<!--<div class="topsearch"><a href = "#" onclick="document.getElementById('id01').style.display='block'" >Search</a></div>-->

<div class="logout"><a href = "./" onclick="document.getElementById('id03').style.display='block'">Logout</a></div>
%if reg == "Admin":
	<div class="registeruser"><a href = "#" onclick="document.getElementById('id06').style.display='block'">Register User</a></div>
	
%end
%if reg == "Admin" or log =="Helpdesk":
	<div class="config"><a href = "#" onclick="document.getElementById('id05').style.display='block'">Insert New System</a></div>
%end
<div class="fileupload"><a href = "#" onclick="document.getElementById('id04').style.display='block'" >Upload File</a></div>

<table id="myTable" align = "center">
  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
  %for i in range(cases):
     <tr>
      %for r in rows:
	%if r == "System Type" and rows[r][i] == "MSDAC":
		
		<td ><a href="#" onclick="getId(this); ">{{rows[r][i]}}</a></td>
	
	%elif r == "System Type" and rows[r][i] == "HASSDAC":
		
		<td ><a href="#" onclick="getId(this); ">{{rows[r][i]}}</a></td>	
	%else:
		<td>{{rows[r][i]}} </td>
	%end
      %end
     </tr>
  %end
</table>
<div align = "center"><label><b>{{lbl}}</b></label></div>
<div id="contents1" style="display:none;" class="fixed" aling="centre" > 
        <iframe id="frame" src="" width="1300" height="400" frameborder="no" aling="centre"></iframe>
</div>
<div id="id01" class="modal">
	<form class="modal-content animate" action="/search_result" target = "_blank">
		<div class="imgcontainer">
			<span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
		</div>

		<div class="container">
			<table>
				<tr>
					<td><label><b>Location</b></label></td>
					<td><input type="text" placeholder="Enter Location" name="loc" ></td>
				</tr>
			      	<tr>
					<td><label><b>System ID</b></label></td>
			      		<td><input type="text" placeholder="Enter System ID" name="sysid" ></td>
				</tr>
				<tr>
			       		<td><label><b>Station Name</b></label></td>
			      		<td><input type="text" placeholder="Enter Station Name" name="stn" ></td>
				</tr>
				<tr>
					<td><label><b>System Type</b></label></td>
					<td><select  name="systype">
					 	  <option value="Select">Select</option>
						  <option value="MSDAC">MSDAC</option>
						  <option value="HASSDAC">HASSDAC</option>
						  <option value="SSDAC">SSDAC</option>
						</select></td>
				</tr>
				<tr>
					<td><label><b>System Status</b></label></td>
					<td><select  name="sysstatus">
					 	  <option value="Select">Select</option>
						  <option value="OK">OK</option>
						  <option value="UNKNOWN">UNKNOWN</option>
				  		</select></td>
				</tr>
			</table>
			<button class = "search" type="submit" >Search</button>
      
		</div>
	</form>
</div>
<div id="id06" class="modal">
      <form class="modal-content animate" action="/registeruser" name="myform">
        <div class="imgcontainer">
          <span onclick="document.getElementById('id06').style.display='none'" class="close" title="Close Modal">&times;</span>
          <img src="/static/register.png" alt="image not found" class="avatar">
        </div>
        <div class="container">
          <table>
	          <tr>
	          	<td><label><b>Username</b></label></td>
	          	<td><input type="text" placeholder="Enter Username" name="uname" required></td>
	          </tr>
	          <tr>
	          	<td><label><b>Password</b></label></td>
	          	<td><input type="password" placeholder="Enter Password" name="pwd" required ></td>
	          </tr>
	          <tr>
	          	<td><label><b>User Type</b></label></td>
          		<td><select  name="systype" id="mycmb" onchange="enabledisabletext()">
		  			<option value="Select">Select</option>
		  			<option value="Admin">Admin</option>
		  			<option value="User">User</option>
		  			<option value="Helpdesk">Helpdesk</option>
		  			</select>
	          </tr>
	          <tr>
	          	<td><label><b>Region</b></label></td>
	          	<td><input type="text" placeholder="Enter Region" name="region" required ></td>
	          </tr>

	          
	          	
	          
          </table>
          <button type="submit">Register</button>
        </div>
       
      </form>
    </div>

<div id="id02" class="modal">
	<form class="modal-content animate" action="/history_result" target = "_blank">
		<div class="imgcontainer">
			<span onclick="document.getElementById('id02').style.display='none'" class="close" title="Close Modal">&times;</span>
		</div>

		<div class="container">
			<table>
				<tr>
					<td><label><b>Start Date</b></label></td>
					<td>
                            <table  class="ds_box" cellpadding="0" cellspacing="0" id="ds_conclass" style="display: none;" border="1">
                                <tr>
                                    <td id="ds_calclass">
                                    </td>
                                </tr>
                            </table>
                            <input id="fromDate" onclick="ds_sh(this);" name='fromDate' readonly="readonly" style="cursor: text"/>

                        </td>
					
				</tr>
			      	<tr>
					<td><label><b>End Date</b></label></td>
					<td>
                            <table  class="ds_box" cellpadding="0" cellspacing="0" id="ds_conclass" style="display: none;" border="1">
                                <tr>
                                    <td id="ds_calclass">
                                    </td>
                                </tr>
                            </table>
                            <input id="fromDate" onclick="ds_sh(this);" name='endDate' readonly="readonly" style="cursor: text"/>

                        </td>
				</tr>
				<tr>
			       		<td><label><b>System ID</b></label></td>
			      		<td><input type="text" placeholder="Enter System ID" name="sysid" required></td>
				</tr>
			</table>
			<button class = "history" type="submit">Get History</button>
      
		</div>
	</form>
</div>
<div id="id04" class="modal">
	<form class="modal-content animate" action= "/generate_report" target = "_blank", method = "post" enctype = "multipart/form-data">
		<div class="imgcontainer">
			<span onclick="document.getElementById('id04').style.display='none'" class="close" title="Close Modal">&times;</span>
		</div>

		<div class="container">
			<table>
				
			      	<tr>
					<td><label><b>System ID</b></label></td>
			      		<td><input type="text" placeholder="Enter System ID" name="sysid" ></td>
				</tr>
				<tr>
			       		<td><label><b>Region</b></label></td>
			      		<td><input type="text" placeholder="Enter Region" name="region" ></td>
				</tr>
				<tr>
					<td><label><b>Select File</b></label></td>
					<td><input type="file" name="fileToUpload" id="fileToUpload"></td>
				</tr>
			</table>
			<input  class = "search" type="submit" value="Generate Report"/>
			
      
		</div>
	</form>
</div>
<div id="id05" class="modal">
	<form class="modal-content animate" action="/insert_details" name="myform1">
	<!--<form class="modal-content animate" action= "#" ,method = "post" enctype = "multipart/form-data" name="myform">-->
		<div class="imgcontainer">
			<span onclick="document.getElementById('id05').style.display='none'" class="close" title="Close Modal">&times;</span>
		</div>

		<div class="container">
			<table>
				<tr>
					<td><label><b>System ID</b></label></td>
			      		<td><input type="text" placeholder="Enter System ID" name="sysid" required></td>
				</tr>
			      	<tr>
					<td><label><b>Region</b></label></td>
			      		<td><input type="text" placeholder="Enter Region" name="reg" required></td>
				</tr>
				<tr>
			       		<td><label><b>Division</b></label></td>
			      		<td><input type="text" placeholder="Enter Division" name="div" required></td>
				</tr>
			      	<tr>
					<!--<td><label><b>System Type</b></label></td>
			      		<td><input type="text" placeholder="Enter System Type" name="systype" required></td>-->
					<td><label><b>System Type</b></label></td>
					<td><select  name="systype" id="mycmb1" onchange="enabledisabletext1()">
					 	  <option value="Select">Select</option>
						  <option value="MSDAC">MSDAC</option>
						  <option value="HASSDAC">HASSDAC</option>
						  <option value="SSDAC">SSDAC</option>
						</select></td>
				</tr>
				<tr>
			       		<td><label><b>Station Name</b></label></td>
			      		<td><input type="text" placeholder="Enter Station Name" name="stnname" required ></td>
				</tr>
			      	
				<tr>
			       		<td><label><b>Mobile No.</b></label></td>
			      		<td><input type="text" placeholder="Enter Mobile No." name="mobno" ></td>
				</tr>
			      	
				<tr>
			       		<td><label><b>TS_Details</b></label></td>
			      		<td><input type="text" placeholder="Enter TS_Details" name="nots" required></td>
				</tr>
				<tr>
					<td><label><b>DP_Details</b></label></td>
			      		<td><input type="text" placeholder="Enter DP_Details" name="nodp" required></td>
				</tr>
			</table>
			<input  class = "search" type="submit" value="Insert Details"/>
			
      
		</div>
	</form>
</div>
</body>
<script>
function  getId(element) {
	//<button class = "search" type="submit" onclick = "getId(this)">Generate Report</button>
    //alert(document.location.pathname);
	//alert("row" + element.parentNode.parentNode.rowIndex + " - column" + element.parentNode.cellIndex);
	//alert(document.getElementById('frame').src+"MSDAC");
	var src = "./"
	//alert(src);
	//alert(document.getElementById('frame').src);
	var url =""
	if (element.text == "MSDAC")
		url = src+"page1/MSDAC";
	else if(element.text == "HASSDAC")
		url = src+"page1/HASSDAC";
	else if(element.text == "SSDAC")
		url = src+"page1/SSDAC";

	document.getElementById('contents1').style.cssText = '';

	document.getElementById("frame").setAttribute("src", url);
	//alert(document.getElementById('frame').src+"MSDAC");
	//alert(url);
}
function enabledisabletext1()
{	
	//alert(document.myform.mycmb.value);
	if(document.myform1.mycmb1.value=='HASSDAC' || document.myform1.mycmb1.value=='SSDAC' || document.myform1.mycmb1.value =='Select')
	{
	//alert('name');
	document.myform1.nots.disabled=true;
	document.myform1.nodp.disabled=true;
	
	}
	else
	{
	document.myform1.nots.disabled=false;
	document.myform1.nodp.disabled=false;
	}
}
function enabledisabletext()
{	
	//alert(document.myform.mycmb.value);
	if(document.myform.mycmb.value =='Admin' || document.myform.mycmb.value =='Select')
	{
	//alert('name');
	document.myform.region.disabled=true;
	
	
	}
	else
	{
	document.myform.region.disabled=false;
	
	}
}
</script>
<script>
// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
</script>

<script>
// Get the modal
var modal = document.getElementById('id02');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
</script>

<script>
//Calennder
// Code begin...
// Set the initial date.
var ds_i_date = new Date();
ds_c_month = ds_i_date.getMonth() + 1;
ds_c_year = ds_i_date.getFullYear();

// Get Element By Id
function ds_getel(id) {
        return document.getElementById(id);
}

// Get the left and the top of the element.
//This Function display calender just below the input
function ds_getleft(el) {
        var tmp = el.offsetLeft;
        el = el.offsetParent
        while(el) {
            tmp += el.offsetLeft;
            el = el.offsetParent;
        }
        return tmp;
}
function ds_gettop(el) {
        var tmp = el.offsetTop;
        el = el.offsetParent
        while(el) {
            tmp += el.offsetTop;
            el = el.offsetParent;
        }
        return tmp;
}

// Output Element
var ds_oe = ds_getel('ds_calclass');
// Container
var ds_ce = ds_getel('ds_conclass');

// Output Buffering
var ds_ob = ''; 
function ds_ob_clean() {
        ds_ob = '';
}
function ds_ob_flush() {
        ds_oe.innerHTML = ds_ob;
        ds_ob_clean();
}
function ds_echo(t) {
        ds_ob += t;
}

var ds_element; // Text Element...

var ds_monthnames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']; // You can translate it for your language.

var ds_daynames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']; // You can translate it for your language.

// Calendar template
function ds_template_main_above(t) {
        return '<table cellpadding="3" cellspacing="1" class="ds_tbl">'
            + '<tr>'
            + '<td class="ds_head" style="cursor: pointer" onclick="ds_py();"><<</td>'
            + '<td class="ds_head" style="cursor: pointer" onclick="ds_pm();"><</td>'
            + '<td class="ds_head" style="cursor: pointer" onclick="ds_hi();" colspan="3">[Close]</td>'
            + '<td class="ds_head" style="cursor: pointer" onclick="ds_nm();">></td>'
            + '<td class="ds_head" style="cursor: pointer" onclick="ds_ny();">>></td>'
            + '</tr>'
            + '<tr>'
            + '<td colspan="7" class="ds_head">' + t + '</td>'
            + '</tr>'
            + '<tr>';
}

function ds_template_day_row(t) {
        return '<td class="ds_subhead">' + t + '</td>';
        // Define width in CSS, XHTML 1.0 Strict doesn't have width property for it.
}

function ds_template_new_week() {
        return '</tr><tr>';
}

function ds_template_blank_cell(colspan) {
        return '<td colspan="' + colspan + '"></td>'
}

function ds_template_day(d, m, y) {
        return '<td class="ds_cell" onclick="ds_onclick(' + d + ',' + m + ',' + y + ')">' + d + '</td>';
        // Define width the day row.
}

function ds_template_main_below() {
        return '</tr>'
            + '</table>';
}
// A function to show the calendar.
// This one draws calendar...
function ds_draw_calendar(m, y) {
        // First clean the output buffer.
        ds_ob_clean();
        // Here we go, do the header
        ds_echo (ds_template_main_above(ds_monthnames[m - 1] + ' ' + y));
        for (i = 0; i < 7; i ++) {
            ds_echo (ds_template_day_row(ds_daynames[i]));
        }
        // Make a date object.
        var ds_dc_date = new Date();
        ds_dc_date.setMonth(m - 1);
        ds_dc_date.setFullYear(y);
        ds_dc_date.setDate(1);
        if (m == 1 || m == 3 || m == 5 || m == 7 || m == 8 || m == 10 || m == 12) {
            days = 31;
        } else if (m == 4 || m == 6 || m == 9 || m == 11) {
            days = 30;
        } else {
            days = (y % 4 == 0) ? 29 : 28;
        }
        var first_day = ds_dc_date.getDay();
        var first_loop = 1;
        // Start the first week
        ds_echo (ds_template_new_week());
        // If sunday is not the first day of the month, make a blank cell...
        if (first_day != 0) {
            ds_echo (ds_template_blank_cell(first_day));
        }
        var j = first_day;
        for (i = 0; i < days; i ++) {
            // Today is sunday, make a new week.
            // If this sunday is the first day of the month,
            // we've made a new row for you already.
            if (j == 0 && !first_loop) {
                // New week!!
                ds_echo (ds_template_new_week());
            }
            // Make a row of that day!
            ds_echo (ds_template_day(i + 1, m, y));
            // This is not first loop anymore...
            first_loop = 0;
            // What is the next day?
            j ++;
            j %= 7;
        }
        // Do the footer
        ds_echo (ds_template_main_below());
        // And let's display..
        ds_ob_flush();
        // Scroll it into view.
        ds_ce.scrollIntoView();
}
// When user click on the date, it will set the content of t.
function ds_sh(t) {
	// Set the element to set...
        ds_element = t;
        // Make a new date, and set the current month and year.
        var ds_sh_date = new Date();
        ds_c_month = ds_sh_date.getMonth() + 1;
        ds_c_year = ds_sh_date.getFullYear();
        // Draw the calendar
        ds_draw_calendar(ds_c_month, ds_c_year);
        // To change the position properly, we must show it first.
        ds_ce.style.display = '';
        // Move the calendar container!
        the_left = ds_getleft(t);
        the_top = ds_gettop(t) + t.offsetHeight;
        ds_ce.style.left = the_left + 'px';
        ds_ce.style.top = the_top + 'px';
        // Scroll it into view.
        ds_ce.scrollIntoView();
}

// Hide the calendar.
function ds_hi() {
        ds_ce.style.display = 'none';
}

// Moves to the next month...
function ds_nm() {
        // Increase the current month.
        ds_c_month ++;
        // We have passed December, let's go to the next year.
        // Increase the current year, and set the current month to January.
        if (ds_c_month > 12) {
            ds_c_month = 1; 
            ds_c_year++;
        }
        // Redraw the calendar.
        ds_draw_calendar(ds_c_month, ds_c_year);
}

// Moves to the previous month...
function ds_pm() {
        ds_c_month = ds_c_month - 1; // Can't use dash-dash here, it will make the page invalid.
        // We have passed January, let's go back to the previous year.
        // Decrease the current year, and set the current month to December.
        if (ds_c_month < 1) {
            ds_c_month = 12; 
            ds_c_year = ds_c_year - 1; // Can't use dash-dash here, it will make the page invalid.
        }
        // Redraw the calendar.
        ds_draw_calendar(ds_c_month, ds_c_year);
}

// Moves to the next year...
function ds_ny() {
        // Increase the current year.
        ds_c_year++;
        // Redraw the calendar.
        ds_draw_calendar(ds_c_month, ds_c_year);
}

// Moves to the previous year...
function ds_py() {
        // Decrease the current year.
        ds_c_year = ds_c_year - 1; // Can't use dash-dash here, it will make the page invalid.
        // Redraw the calendar.
        ds_draw_calendar(ds_c_month, ds_c_year);
}

// Format the date to output.
function ds_format_date(d, m, y) {
        // 2 digits month.
        m2 = '00' + m;
        m2 = m2.substr(m2.length - 2);
        // 2 digits day.
        d2 = '00' + d;
        d2 = d2.substr(d2.length - 2);
        // DD/MM/YYYY
        return y + '-' + m2 + '-' + d2;
}

// When the user clicks the day.
function ds_onclick(d, m, y) {
        // Hide the calendar.
        ds_hi();
        // Set the value of it, if we can.
        if (typeof(ds_element.value) != 'undefined') {
            ds_element.value = ds_format_date(d, m, y);
            // Maybe we want to set the HTML in it.
        } else if (typeof(ds_element.innerHTML) != 'undefined') {
            ds_element.innerHTML = ds_format_date(d, m, y);
            // I don't know how should we display it, just alert it to user.
        } else {
            alert (ds_format_date(d, m, y));
        }
}

// And here is the end.
</script>

</html>


