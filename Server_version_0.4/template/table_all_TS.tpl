%# table_all_TS.tpl
<html>
<head><title>Welcome::CEL SMS (Server Monitoring System)</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>
<body>
<div style=" margin-top: 20px;" align="center" >
<table id="mytablemsdac" >
  <tr>
    %for r in rows1:
      <th>{{r}}</th>
    %end
  </tr>
  %for i in range(cases1):
     <tr>
      %for r in rows1:
	%if r == "No. of DP":
		%if rows1["Status"][i] == "OK":
			<td>{{rows1[r][i]}}</td>
		%else:
			<td><font color="red">{{rows1[r][i]}}</font></td>
		%end
	%elif r == "No. of TS":
		%if rows1["Status"][i] == "OK":
			<td>{{rows1[r][i]}}</td>
		%else:
			<td><font color="red">{{rows1[r][i]}}</font></td>
		%end
	%elif r == "Status":
		%if  rows1[r][i] == "OK":
			<td> {{rows1[r][i]}} </td>
		%else:
			<td  id = "ts">{{rows1[r][i]}}</td>
			
		%end
	%else:
		<td>{{rows1[r][i]}} </td>
	%end
      %end
     </tr>
  %end
</table>
</div>
<div style=" margin-top: 25px;"align="center">
<h2 align="center">TS INFORMATION</h2>

<table id="mytable3">
  

  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
  %for i in range(cases):
     <tr>
      %for r in rows:
	%if r == "TS Status":
		%if rows["TS Status"][i] == "ERROR":
			<td id = "sts" bgcolor = "#faacb9"><font color= #c4062c><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "PREPARATORY RESET":
			<td><font color= #e79911><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "RESET":
			<td><font color= #6d6456><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "UNOCCUPIED":
			<td><font color= #059b32><b>{{rows[r][i]}}</font> </td>
		%elif rows["TS Status"][i] == "OCCUPIED":
			<td><font color= #ed4264><b>{{rows[r][i]}}</font> </td>
		%else:
			<td>{{rows[r][i]}}</td>
		%end

	%elif r == "TS Name":
		<td><a href="#" onclick="getId(this);">{{rows[r][i]}}</a></td>
	%else:
		<td>{{rows[r][i]}}</td>
	%end
      %end
     </tr>
  %end
</table>
</div>
</body>
<script>
function  getId(element) {

	//alert(document.getElementById('frame3').src);
	var table = document.getElementById("mytable3"); 
	var src = "/history_result/"
	//x = document.getElementById("date").innerHTML

	var msdac_table = document.getElementById("mytablemsdac"); 
	var msdac_id = msdac_table.rows[1].cells[0].innerHTML
	var ts =table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML
	var ts_num = ts.match(/\d+/);
	//alert(ts_num);
	var url = src+msdac_id+"/"+ts_num+"T"+"/one_ts"	//alert(url);
	//document.getElementById('contents1').style.cssText = '';
	//document.getElementById('contents4').style.cssText = '';
	//document.getElementById("frame4").setAttribute("src", url);
	window.open(url);
	
	//alert(document.getElementById('frame4').src);
	
}
</script>
</html>
