<html>
  <head><title>Home Page</title>
<link rel='stylesheet' type='text/css' href='/static/stylesheet1.css'>
  </head>
  <body>
	<!--<div class="logout"><a href = "#" onclick="document.getElementById('id02').style.display='block'">Register User</a></div>-->
    <center>
      <img src="/static/cel.png" alt="Image Not Found" style="width:304px;height:228px;">
    </center>
    <marquee><h2>Welcome To CEL Server Monitoring System</h2></marquee>
	
    <div class="wrapper">
      <button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Login</button>
    </div>
    <div id="id01" class="modal">
      <form class="modal-content animate" action="/home" name='myform'>
        <div class="imgcontainer">
          <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
          <img src="/static/login2.png" alt="image not found" class="avatar">
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
          	<td><label><b>login As</b></label></td>
          	<td><select  name="systype" id="mycmb" onchange="enabledisabletext()">
          			<option value="Select">Select</option>
          			<option value="Admin">Admin</option>
          			<option value="User">User</option>
          			<option value="Helpdesk">Helpdesk</option>
          			</select>
            </td>
	  </tr>
	  <tr>
          	<td><label><b>Region</b></label></td> 
          	<td><input type="text" placeholder="Enter Region" name="region" required ></td>
	  </tr>
	  
          	
	 </table>
   <td><button type="submit">Login</button></td>
    
        </div>
       
      </form>
    </div>
<div id="id02" class="modal">
      <form class="modal-content animate" action="/registeruser">
        <div class="imgcontainer">
          <span onclick="document.getElementById('id02').style.display='none'" class="close" title="Close Modal">&times;</span>
          <img src="/static/register.png" alt="image not found" class="avatar">
        </div>
        <div class="container">
          <label><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="uname" required>
          <label><b>Password</b></label>
          <input type="password" placeholder="Enter Password" name="pwd" required >
          <label><b>Region</b></label>
          <input type="text" placeholder="Enter Region" name="region"  >
          <button type="submit">Register</button>
        </div>
       
      </form>
    </div>
	<div align = "center"><label><b>{{lbl}}</b></label></div>
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
function enabledisabletext()
{	
	//alert(document.myform.mycmb.value);
	if(document.myform.mycmb.value=='Admin' || document.myform.mycmb.value=='Select')
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

</body>
</html>

