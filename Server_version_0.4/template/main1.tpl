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
	<h3 style="color:red;" align="center">Please Enter Correct Details !</h3>
    <div class="wrapper">
      <button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Login</button>
    </div>
    <div id="id01" class="modal">
      <form class="modal-content animate" action="/home">
        <div class="imgcontainer">
          <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
          <img src="/static/login2.png" alt="image not found" class="avatar">
        </div>
        <div class="container">
          <label><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="uname" required>
          <label><b>Password</b></label>
          <input type="password" placeholder="Enter Password" name="pwd" required>
          <label><b>Region</b></label>
          <input type="text" placeholder="Enter Region" name="region" required>
          <button type="submit">Login</button>
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
          <input type="text" placeholder="Enter Region" name="region" required >
          <button type="submit">Register</button>
        </div>
       
      </form>
    </div>
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

</body>
</html>

