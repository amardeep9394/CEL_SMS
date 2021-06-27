%#disp.tpl

<html>
<head><link rel='stylesheet' type='text/css' href='/static/stylesheet.css'></head>
	<body>
		<div align=center>
			<h2> {{title}} </h2>
			<table id="mytable">
			<tr><th>System ID:</th><th colspan=3>{{sid}}</th></tr>
			<tr><th rowspan=2> TS_ID </th> <th colspan=2> Last updated at </th><th rowspan=2> DP_INFO </th></tr>
			<tr><th>Date</th><th>Time</th></tr>
			%for r in rv:
				<tr><td><a href="#" onclick="getId(this);"> {{r}} </a></td> <td>{{rv[r]['date']}} </td><td> {{rv[r]['time']}}</td>
				%if 'dp' in rv[r]:
					<td>
					%for i in rv[r]['dp']:
						<a href="#" onclick="getdp(this);" id="testlink">{{i}}</a>
					%end
					</td>
				%else:
					<td></td>
				%end
				</tr>
			%end
			</table>
		</div>

	</body>
<script>
function  getId(element) {

	//alert(document.getElementById('frame3').src);
	var table = document.getElementById("mytable"); 
	var src = "http://127.0.0.1:8080/history_result/"
	//x = document.getElementById("date").innerHTML

	//var msdac_table = document.getElementById("mytablemsdac"); 
	//var msdac_id = msdac_table.rows[1].cells[0].innerHTML
	var ts =table.rows[element.parentNode.parentNode.rowIndex].cells[0].innerHTML
	var sys_id = table.rows[0].cells[1].innerHTML
	var ts_num = ts.match(/\d+/)+'T';
	//alert(sys_id);
	//alert(ts);
	//alert(ts_num);
	var url = src+sys_id+"/"+ts_num+"/one_ts"	//alert(url);
	//alert(url);
	//document.getElementById('contents1').style.cssText = '';
	//document.getElementById('contents4').style.cssText = '';
	//document.getElementById("frame4").setAttribute("src", url);
	//alert(url);
	window.open(url);
	
	//alert(document.getElementById('frame4').src);
	
}
function  getdp(element) {

	//alert(document.getElementById('frame3').src);
	//var table = document.getElementById("mytable3"); 
	var src = "/history_result/"
	//x = document.getElementById("date").innerHTML

	var msdac_table = document.getElementById("mytable"); 
	var msdac_id = msdac_table.rows[0].cells[1].innerHTML;
	//alert(msdac_id);
	//var ts =table.rows[element.parentNode.parentNode.rowIndex].cells[element.parentNode.parentNode.rowIndex].innerHTML
	//alert(ts);
	//var ts_num = ts.match(/\d+/);
	var dp_id = element.innerHTML;
	//alert(dp_id);
	//var url = src+table.rows[0].cells[1].innerHTML+"/"+x+"/"+ts+"/one_ts"
	var url = src+msdac_id+"/"+dp_id+"/one_dp"
	//alert(url);
	//document.getElementById('contents1').style.cssText = '';
	//document.getElementById('contents4').style.cssText = '';
	//document.getElementById("frame4").setAttribute("src", url);
	window.open(url);
	
	//alert(document.getElementById('frame4').src);
	
}
</script>
</html>
