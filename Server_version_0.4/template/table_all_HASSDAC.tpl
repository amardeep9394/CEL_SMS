%# disp_table.tpl
<html>
<head>
<meta http-equiv="refresh" content="5">
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>

<body>
<h2 id= "t5">HASSDAC INFORMATION</h2>
<table id="hassdac_total_info" >
	<tr>
		%for r in rows:
			<th>{{r}}</th>
		%end
	</tr>
	%for i in range(cases):
		<tr>
		%for r in rows:
			%if r == "HASSDAC ID":
	   			<td><a href="" onclick="getId(this);">{{rows[r][i]}} </td>
			%else:
	    			<td>{{rows[r][i]}} </td>
			%end
	
     		%end
    		</tr>
	%end
</table>
</body>
<script>
function  getId(element) {

	//var table = document.getElementById("hassdac_total_info");
	var hassdac_table = document.getElementById("hassdac_total_info"); 
	var hassdac_id = hassdac_table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML//rows[1].cells[0].innerHTML
	var hassdac_num = hassdac_id.match(/\d+/);
	//alert(hassdac_num)
	//alert(element.parentNode.parentNode.rowIndex);
	//alert(element.parentNode.cellIndex);
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML);

	var src = "/page3/"

	//var url =src+hassdac_table.rows[element.parentNode.parentNode.rowIndex].cells[1].innerHTML+"/hassdac"
	var url =src+"HASSDAC"+hassdac_num+"/hassdac"
	//alert(table.rows[element.parentNode.parentNode.rowIndex].cells[2].innerHTML.slice(0, -1))
	//document.getElementById('contents2').style.cssText = '';
	//alert(url);
	window.open(url);
	//window.location.target = "_blank";
	//document.getElementById("frame2").setAttribute("href", url);
	//document.getElementById("frame2").setAttribute("target", "_blank");
}
</script>
</html>


