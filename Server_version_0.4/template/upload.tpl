<html>
<head><title>Welcome::CEL SMS (Server Monitoring System)</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>
<body>
<h2 >System ID : {{ID}}</h2>
<h2>Region : {{reg}}</h2>
<div class="export"><a href = "#" onclick="exportTableToCSV('{{ID}}_{{reg}}_TS.csv');" >Export To CSV</a></div>
<div class="print"><a href = "#" onclick= "printpage()">Print</a></div>
<div class="dp_info"><a href = "#" onclick="getId(this);">DP Details</a></div>
<div class="config_info"><a href = "#" onclick="config();">Config Details</a></div>


<div class = "ts">
<h2 align="center">TS INFORMATION</h2>
<table class ="uploadts" id = "uploadts" align= "center">
<tr>
    %for r in rows1:
      <th>{{r}}</th>
    %end
</tr>
%for i in range(cases1):
	<tr>
		 %for r in rows1:
			%if r == "TS Status":
				%if rows1["TS Status"][i] == "ERROR":
					<td id = "sts" bgcolor = "#faacb9"><font color= #c4062c><b>{{rows1[r][i]}}</font> </td>
				%elif rows1["TS Status"][i] == "PREPARATORY RESET":
					<td><font color= #e79911><b>{{rows1[r][i]}}</font> </td>
				%elif rows1["TS Status"][i] == "RESET":
					<td><font color= #6d6456><b>{{rows1[r][i]}}</font> </td>
				%elif rows1["TS Status"][i] == "UNOCCUPIED":
					<td><font color= #059b32><b>{{rows1[r][i]}}</font> </td>
				%elif rows1["TS Status"][i] == "OCCUPIED":
					<td><font color= #ed4264><b>{{rows1[r][i]}}</font> </td>
				%else:
					<td>{{rows1[r][i]}}</td>
				%end
			%else:
				<td>{{rows1[r][i]}}</td>
			%end
		%end
		
	</tr>
%end
</table>
</div>
<div id="id01" class="modal">
	<form class="modal-content animate" action= "/export_csv" target = "", method = "post" enctype = "multipart/form-data">
		

		<div class="container">
			<table>
				
			      	<tr>
					<td><label><b>Successfully Exported to CSV</b></label></td>
			      		
				</tr>
				
			</table>
			<input  class = "search" type="submit" value="OK"/>
			
      
		</div>
	</form>
</div>

<script>
function printpage(){
window.print();}

function  getId(element) 
{
var src = "./dp_info"
window.open(src);
}
function config(){
var src ="./config_info"
window.open(src);
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}


function exportTableToCSV(filename) {
    alert("HI"+document.getElementById("uploadts"));
    var csv = [];
    var rows = document.querySelectorAll("#uploadts tr"); // set the selector to select the data from specific ID of a table
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}

function getTableId(node) {
    var element = node;
    while (element.tagName.toLowerCase() !== 'table') {
        element = element.parentNode;
    }
    return element.id;
}
</script>
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


</body>
</html>
