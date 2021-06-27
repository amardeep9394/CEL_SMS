<html>
<head><title>Welcome::CEL SMS (Server Monitoring System)</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet.css'>
</head>
<body>
<h2 >System ID : {{ID}}</h2>
<h2>Region : {{reg}}</h2>
<div class="export2"><a href = "#" onclick="exportTableToCSV('{{ID}}_{{reg}}_Config.csv');" >Export To CSV</a></div>
<div class="print"><a href = "#" onclick= "printpage()">Print</a></div>
<div class="cfg">
<h2 align="center">CONFIGURATION INFORMATION</h2>
<table id = "uploaddp">
<tr>
    %for r in rows:
      <th>{{r}}</th>
    %end
</tr>
%for i in range(cases):
	<tr>
		 %for r in rows:
			<td>{{rows[r][i]}}</td>
		%end
		
	</tr>
%end
</table>
</div>

<script>
function printpage(){
window.print();}


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
    //alert("HI"+document.getElementById("uploadts"));
    var csv = [];
    var rows = document.querySelectorAll("#uploaddp tr"); // set the selector to select the data from specific ID of a table
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}

</script>


</body>
</html>
