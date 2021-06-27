%# table_all_TS.tpl
<html>
<head>
<title>Welcome::CEL SMS (Server Monitoring System)</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>
<script type="text/javascript">

/* Paginate Table Script ©2008 John Davenport Scheuer
   as first seen in http://www.dynamicdrive.com/forums/
   username: jscheuer1 - This Notice Must Remain for Legal Use
   */

// you can init as many tables as you like in here by id: paginateTable('id', 0, num_max_rows);
paginateTable.init = function(){ // remove any not used
paginateTable('history_one_ts_table', 0, 10);
//paginateTable('test2', 0, 3);
};

////////////////////// Stop Editing //////////////////////

function paginateTable(table, way, max){
max? paginateTable.max[table] = max : max = paginateTable.max[table];
way = way == 1? 1 : way == -1? 0 : -1;
var r = document.getElementById(table).rows, i = 0;
for(i; i < r.length; ++i) // find current start point
 if(r[i].style.display != 'none')
  break;
for(i; i < r.length; ++i){ // continue on to find current end point
 if(r[i].style.display == 'none'){
  paginateTable.endPoint[table] = i;
  break;
 };
 paginateTable.endPoint[table] = 0; // if no end point found, table is 'virgin' or at end
};
if(way == 1 && r[r.length - 1].style.display != 'none') return; // table was already at the end and we tried to move forward
// if moving forward, start will be old end, else start will be old start - max or 0, whichever is greater:
paginateTable.startPoint[table] = way? paginateTable.endPoint[table] : Math.max( 0, paginateTable.startPoint[table] - max);
paginateTable.endPoint[table] = paginateTable.startPoint[table] + --max; // new end will be new start + max - 1
for (i = r.length - 1; i > -1; --i) // set display of rows based upon whether or not they are in range of the calculated start/end points
 r[i].style.display = i < paginateTable.startPoint[table] || i > paginateTable.endPoint[table]? 'none' : '';
};

paginateTable.startPoint = {};
paginateTable.endPoint = {};
paginateTable.max = {};

if(window.addEventListener)
window.addEventListener('load', paginateTable.init, false);
else if (window.attachEvent)
window.attachEvent('onload', paginateTable.init);

//////////////// End Paginate Table Script ///////////////

</script>
<body>
<h2 id="t4">{{TS_Name}} INFORMATION</h2>
<div class= "history_one_ts">
<table id="history_one_ts_table_header">
  <tr>
    <th colspan = "2">MSDAC ID</th>
    <th colspan = "3">{{ID}}</th>
  </tr>
  <tr>
    <th colspan = "2">TS Name</th>
    <th colspan = "3">{{TS_Name}}</th>
  </tr>
  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
</table>
<div>
<table id="history_one_ts_table">
  %for i in range(cases):
     <tr>
      %for r in rows:
	%if r == "S. No":
		<td width="109px";>{{rows[r][i]}}</td>

	%elif r == "TS Status":
		%if rows["TS Status"][i] == "ERROR":
			<td width="185px"; id = "sts" bgcolor = "#faacb9"><font color= #c4062c><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "PREPARATORY RESET":
			<td width="185px";><font color= #e79911><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "RESET":
			<td width="185px";><font color= #6d6456><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "UNOCCUPIED":
			<td width="185px";><font color= #059b32><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "OCCUPIED":
			<td width="185px";><font color= #ed4264><b>{{rows[r][i]}}</font> </td>
		%else:
			<td width="185px";>{{rows[r][i]}}</td>		
		%end
		
	%elif r == "Remark":
		<td width="157px";>{{rows[r][i]}}</td>
	%elif r == "Date":
		<td width="100px";>{{rows[r][i]}}</td>
	%elif r == "Time":
		<td width="0px";>{{rows[r][i]}}</td>
	%end
	%end
     </tr>
  %end
</table>
</div>
</div>
<div id = "page_btns">
  <input type="button" value="Previous" onclick="paginateTable('history_one_ts_table', -1);">
  <input type="button" value="Next" onclick="paginateTable('history_one_ts_table', 1);">
</div>
</body>
</html>


