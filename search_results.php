<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="search_results.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <title>Search Results</title>
  </head>

  
  <body>
    
    <!-- CHECK IF SEARCH FIELD IS EMPTY -->
<script>
function validateForm() {
  var s = document.forms["search-results"]["search"].value;

  if (s == "" || s == null) {
    alert("You cannot leave this field empty if you want to search something!");
    return false;
  }
}
</script>
    
    <!-- MAIN -->
    <main class="background-search">

      <form  class="search" name="search-results" action="search_results.php" onsubmit="return validateForm()" method="POST">
          <div class="search-box">
            <input type="text" name="search" placeholder="SEARCH RESULTS" minlength="4"/>
            <button type="submit" name="submit-search"><i class="fa fa-search"></i></button>
          </div>
      </form>
      <div class = "results-container">
      
      </div>

    </main>
  </body>
</html>
