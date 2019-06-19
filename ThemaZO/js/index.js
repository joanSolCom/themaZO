var network;


$(document).ready(function(){
  

  $("#testButton").click(function(){
  	var height = $( window ).height();
  	console.log(height)
  	height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 20;
  	$("#graphContainer").height(height);
  	$("#themContainer").height(height);
  	$("#header").hide()
    $.getJSON( "http://127.0.0.1:5000/getConll?callback=?", function( dataJSON ) {
	    createGraph(dataJSON);
	});

	$.getJSON( "http://127.0.0.1:5000/getThematicity?callback=?", function( dataJSON ) {
	    displayThem(dataJSON);
	});
	$("#myonoffswitch").prop("checked",false);
  });

  $("#myonoffswitch").click(function(){
  	$("#header").toggle();
  	console.log($(this).is(":checked"));
  	if($(this).is(":checked"))
  	{
  		var height = $( window ).height();
	  	height = height - $("#header").height() - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
	  	console.log(height)
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	
  	}
  	else
  	{
  		var height = $( window ).height();
	  	console.log(height)
  		height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
  		$("#graphContainer").height(height);
  		$("#themContainer").height(height);
  	}
  	network.fit();
  });


});


function createGraph(dataJSON) 
{
	var obj = $.parseJSON(dataJSON);
	var tokens = obj["sentences"][3]["tokens"];

	var nodes = [];
	var edges = [];

	/**
		Create nodes
	**/
	for (var i = 0; i < tokens.length; i++) {
	    console.log(tokens[i]);
	    var pieces = tokens[i].split("\t");
	    var node = {};
	    node.id = pieces[0];
	    node.label = pieces[1];
	    node.group = pieces[3][0];
	    node.title = pieces[3];
	    nodes.push(node);

	    if(node.id != pieces[5])
	    {
	    	var edge = {};
	    	edge.from = pieces[5];
	    	edge.to = node.id;
	    	edge.label = pieces[4];
	    	edge.arrows = "to";
	    	edges.push(edge);
	    }
	}	


	var container = document.getElementById('graphContainer');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        layout:{  
          "hierarchical":{  
            "nodeSpacing":150,
            "sortMethod" : 'directed'
          }
        }
    };
    network = new vis.Network(container, data, options);
}

function displayThem(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	var sentence = obj["sentences"][3]["text"];
	var them = obj["sentences"][3]["components"];
	var tokens = obj["sentences"][3]["tokens"]

	$( "#themContainer" ).html("");
	
	var dictHighlight = {};

	$( "#themContainer" ).append(sentence+"<br/>");

	for (var j = 0; j < them.length; j++) 
	{
		$( "#themContainer" ).append("<span id=ann_"+j+">"+sentence +"</span><br/>");
		for(var n = 0; n < them[j].length; n++)
		{
			var from = them[j][n][0] - 1;
			var to = them[j][n][1] - 1;
			var label = them[j][n][2];
			var className;
			if(label[0] == "P")
			{
				className = "proposition badge badge-pill badge-dark";
			}
			else if(label[0] == "R")
			{
				className = "rheme badge badge-pill badge-danger";
			}
			else if(label[0] == "S")
			{
				className = "specifier badge badge-pill badge-warning";
			}
			else
			{
				className = "theme badge badge-pill badge-success";
			}

			var text = "";
			for(var k = from; k<=to;k++)
			{
				text+= tokens[k] + " "
			}
			text = $.trim(text);
			console.log(text);
			$("#ann_"+j).highlight(text,{className:className});
		}
		
	}
}