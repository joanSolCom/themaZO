<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Demo ThemaZO Thematicity Parser</title>
  <meta name="description" content="Demo for the thematicity parser ThemaZO">
  <meta name="author" content="Juan Soler">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css">
  <link rel="stylesheet" href="css/index.css">

</head>

<body>
  	<h1>
  		ThemaZO
  	</h1>
  	
  	<div class="container-fluid">
  		<div class="md-form">
			  <textarea id="form5" class="md-textarea form-control" rows="3" placeholder="Write something here..."></textarea>
		</div>

	  <button id="submitButton" class="btn btn-primary">Submit</button>

  	</div>

  	<ul class="nav nav-pills">
	
	  <li class="nav-item">
	  		<a class="nav-link active" data-toggle="pill" href="#home">Syntactic Tree</a>
	  </li>
	  
	  <li class="nav-item">
	  		<a class="nav-link" data-toggle="pill" href="#menu1">Thematicity</a>
	  </li>
	
	</ul>

	<div class="tab-content">
	  <div class="tab-pane container active" id="home">
	  		<div id="graphContainer" class="result"></div>
	  </div>
	  <div class="tab-pane container" id="menu1">
		  	<h3>Thematicity</h3>
	  </div>
	  
	</div>


  	  

	<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="  crossorigin="anonymous"></script>    
	<script src ="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"/>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script src="js/index.js"></script>

</body>
</html>