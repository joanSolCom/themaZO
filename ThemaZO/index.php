<?php require "header.php" ?>
 	  
  	  <div id="textAreaWrapper">
	  	  <div>
		  	<textarea id="inputBox" class="md-textarea" rows="3" placeholder="Write something here..."></textarea>
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

		  <li class="nav-item pill-3">
		  		<a class="nav-link" data-toggle="pill" href="#menu2">Thematic Progression</a>
		  </li>
		
		</ul>
	</div>

	<div id="tabContent" class="tab-content">
	  <div class="tab-pane container active" id="home">
	  		<div id="graphContainer" class="result">
	  			

	  		</div>
	  		<div id="pageButtons">
				<button id="previous" class="round">&#8249;</a>
				<button id="next" class="round">&#8250;</a>	  		
	  		</div>
	  </div>
	  <div class="tab-pane container" id="menu1">
		  	<div id="themContainer" class="result">
		  	</div>
	  </div>

	  <div class="tab-pane container" id="menu2">
		  	<div id="themProgContainer" class="result">
		  	</div>
	  </div>
	  
	</div>



<?php require "footer.php" ?>