<?php require "header.php" ?>
 	  
  	  <div id="textAreaWrapper">
	  	  <div>
		  	<textarea class="md-textarea" rows="3" placeholder="Write something here..."></textarea>
		  </div>
		  <div id= "wrapperButtons">
			  <button id="submitButton" class="btn btn-primary">Submit</button>
			  <button id="testButton" class="btn btn-info">Test</button>
	      </div>
      </div>
    </div>
  	<div id="pillWrapper">
	  	<ul class="nav nav-pills">
		
		  <li class="nav-item pill-1">
		  		<a class="nav-link active" data-toggle="pill" href="#home">Syntactic Tree</a>
		  </li>
		  
		  <li class="nav-item pill-2">
		  		<a class="nav-link" data-toggle="pill" href="#menu1">Thematicity</a>
		  </li>
		
		</ul>
	</div>

	<div class="tab-content">
	  <div class="tab-pane container active" id="home">
	  		<div id="graphContainer" class="result">
	  			

	  		</div>
	  </div>
	  <div class="tab-pane container" id="menu1">
		  	<div id="themContainer"  class="result">
		  	</div>
	  </div>
	  
	</div>



<?php require "footer.php" ?>