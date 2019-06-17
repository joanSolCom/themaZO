$(document).ready(function(){
  

  $("#submitButton").click(function(){
    $.getJSON( "http://127.0.0.1:5000/getConll?callback=?", function( dataJSON ) {
	    console.log(dataJSON);
	    createGraph(dataJSON);
	});
  });


});


function createGraph(dataJSON) 
{
	var obj = $.parseJSON(dataJSON);
	var tokens = obj["sentences"][0]["tokens"];

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