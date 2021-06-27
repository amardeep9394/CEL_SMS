%# disp_table.tpl
<html>
<head>
<meta http-equiv="refresh" content="5">
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'> 
</head>

<body>
<!--<div align="center">
<h2 id= "t2" align="center">MSDAC INFORMATION</h2>
<table id="mytable2" >
  <tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
  </tr>
  %for i in range(cases):
     <tr>
      %for r in rows:
	%if r == "No. of DP":
		%if rows["Status"][i] == "OK":
			<td><a href="" onclick="getdp(this);">{{rows[r][i]}}</a></td>
		%else:
			<td><a href="" onclick="getdp(this);"><font color="red">{{rows[r][i]}}</font></a></td>
		%end
	%elif r == "No. of TS":
		%if rows["Status"][i] == "OK":
			<td><a href="" onclick="getId(this);">{{rows[r][i]}}</a></td>
		%else:
			<td><a href="" onclick="getId(this);"><font color="red">{{rows[r][i]}}</font></a></td>
		%end
	%elif r == "Status":
		%if  rows[r][i] == "OK":
			<td> {{rows[r][i]}} </td>
		%else:
			<td  id = "ts">{{rows[r][i]}}</td>
		%end
	%else:
		<td>{{rows[r][i]}} </td>
	%end
      %end
     </tr>
  %end
</table>
</div>-->


<div align=center>
<h2 id= "t2" align="center">MSDAC INFORMATION</h2>
<table id="mytable2">
<tr>
<th rowspan=2 bgcolor=#0582b4><font color="white"> S. No</th> <th rowspan=2 bgcolor=#0582b4><font color="white"> System ID </th> <th colspan=6 bgcolor=#0582b4><font color="white"> TS Status </th>
</tr>
<tr><th bgcolor=red > OCCUPIED </th> <th bgcolor=green> CLEAR </th> <th bgcolor=white>RESET</th><th bgcolor=yellow> PREP</th><th bgcolor=orange>ERROR</th><th bgcolor=#0582b4><font color="white">Total</th></tr>
% i = 1
%for sid in tscn:
<tr>
	<td> {{i}} </td>
	% i = i + 1
	<td> {{sid}} </td>
	<td><a href="/tsd/OCCUPIED/{{sid}}"> {{tscn[sid]['occupied']}} </td>
	<td><a href="/tsd/UNOCCUPIED/{{sid}}"> {{tscn[sid]['clear']}} </td>
	<td><a href="/tsd/RESET/{{sid}}"> {{tscn[sid]['reset']}} </td>
	<td> <a href="/tsd/PREPARATORY RESET/{{sid}}">{{tscn[sid]['prep']}}</a> </td>
	<td> <a href="/tsd/ERROR/{{sid}}">{{tscn[sid]['error']}} </a></td>
	<td> {{tscn[sid]['total']}} </td>
</tr>
%end
</table>
</div>



</body>
<script>
function  getId(element) {

	var table = document.getElementById("mytable2"); 
	//alert(element.parentNode.parentNode.rowIndex);
	//alert(element.parentNode.cellIndex);
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML);

	var src = "/page2/"

	var url =src+table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML.slice(0, -1)+"/ts"
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[2].innerHTML.slice(0, -1))
	//document.getElementById('contents2').style.cssText = '';
	//alert(url);
	window.open(url);
	//window.location.target = "_blank";
	//document.getElementById("frame2").setAttribute("href", url);
	//document.getElementById("frame2").setAttribute("target", "_blank");
}

function  getdp(element) {

	var table = document.getElementById("mytable2"); 
	//alert(element.parentNode.parentNode.rowIndex);
	//alert(element.parentNode.cellIndex);
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML);

	var src = "/page2/"

	var url =src+table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML.slice(0, -1)+"/dp"
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[2].innerHTML.slice(0, -1))
	//document.getElementById('contents2').style.cssText = '';
	window.open(url);
	//document.getElementById("frame2").setAttribute("href", url);
}
</script>
<script>
var span = document.getElementById('ts'),
    text = span.innerHTML.split('').map(function(el) {
        return '<span class="char-' + el.toLowerCase() + '">' + el + '</span>';
    }).join('');
  
span.innerHTML = text;
</script>
</html>

