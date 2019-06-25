var network;
var globalDATA;
var networkThem;
var networkCoref;

$(document).ready(function(){

	$.ajaxSetup({async: false});  
  	manageOnOffSwitch();
  	manageSubmitButton();
  	manageNextPrevButtons();

});

function manageNextPrevButtons()
{

	$("#previous").click(function(){
		var currentGraph = parseInt($('#idGraph').attr("name"));

		if($( this ).css( "background-color" ) == "rgb(0, 0, 0)")
		{
			displayTree(globalDATA, currentGraph-1);
		}	
	});

	$("#next").click(function(){
		var currentGraph = parseInt($('#idGraph').attr("name"));
		if($( this ).css( "background-color" ) == "rgb(0, 0, 0)")
		{
			displayTree(globalDATA, currentGraph+1);
		}
	});
}


function manageSubmitButton()
{

	$("#submitButton").click(function(){

		$("#pillWrapper").show();
		$("#tabContent").show();

	  	var height = $( window ).height();
	  	height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 20;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);

	  	$("#header").hide()

	  	var text =  $('textarea#inputBox').val();
	  	var data = {"text": text};

	    $.post( "http://127.0.0.1:5000/getConll", data ,function( dataJSON ) {
		    displayTree(dataJSON, 0);
		    displayCorefs(dataJSON);
		    globalDATA = dataJSON;
		}, "json");

		$.post( "http://127.0.0.1:5000/getThematicity", function( dataJSON ) {
		    displayThem(dataJSON);
		}, "json");

		$.post( "http://127.0.0.1:5000/getThematicProgression", function( dataJSON ) {
		    displayThematicProgression(dataJSON);
		}, "json");
		
		$("#myonoffswitch").prop("checked",false);
  	});
}

function displayThematicProgression(dataJSON)
{

	var nodes = [];
	var edges = [];

	var obj = $.parseJSON(dataJSON);
	var components = obj["components"];
	var hyper = obj["hypernode"];
	var distances = obj["distances"];


	var node = {};
    node.id = 0;
    node.label = "First Sentence";
    node.group = 0;
    node.title = hyper;
    nodes.push(node);

    var THEME_OFFSET = 100;
    var RHEME_OFFSET = 1000;

	for(var i = 0 ; i< components.length; i++)
	{
		var nodeTheme = {};
	    nodeTheme.id = i+THEME_OFFSET;
	    nodeTheme.label = "Theme";
	    nodeTheme.group = 1;
	    nodeTheme.title = components[i][0];
	    nodeTheme.shape="circle";
	    nodes.push(nodeTheme);

	    if( i < components.length-1)
	    {
		    var nodeRheme = {};
		    nodeRheme.id = i+RHEME_OFFSET;
		    nodeRheme.label = "Rheme";
		    nodeRheme.group = 2;
		    nodeRheme.title = components[i][1];
		    nodeRheme.shape="circle";
	    	nodes.push(nodeRheme);

		}
	}

	for(var j = 1; j< distances.length; j++)
	{
		var edgeTheme = {};
		edgeTheme.from = j-1+THEME_OFFSET;
		edgeTheme.to = j+THEME_OFFSET
		
		if(distances[j][0] == "coref")
		{
			edgeTheme.label = "coref";
		}
		else if(distances[j][0] != -10)
		{
			edgeTheme.label = String(distances[j][0].toFixed(2));
		}

		edgeTheme.font = {align: 'top'};
		edgeTheme.arrows = "from";
		edges.push(edgeTheme);

		var edgeRheme = {};
		edgeRheme.from = j-1+RHEME_OFFSET;
		edgeRheme.to = j+THEME_OFFSET

		if(distances[j][1] != -10)
		{
			edgeRheme.label = String(distances[j][1].toFixed(2));
		}

		edgeRheme.font = {align: 'top'};
		edgeRheme.arrows = "from";
		edges.push(edgeRheme);

		if(distances[j][2] != -10)
		{
			var edgeHyper = {};
			edgeHyper.from = j+THEME_OFFSET
			edgeHyper.to = 0;
			edgeHyper.label = String(distances[j][2].toFixed(2));
			edgeHyper.font = {align: 'top'};
			edgeHyper.arrows = "to";
			edges.push(edgeHyper);
		}
		
	}


	var container = document.getElementById('themProgContainer');
    var data = {
        nodes: nodes, 
        edges: edges
    };
    var options = {

	};

    networkThem = new vis.Network(container, data, options);


  	$('#them a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
	  networkThem.fit();
	});


}


function manageOnOffSwitch()
{
	$("#myonoffswitch").click(function(){
  	$("#header").toggle();
  	if($(this).is(":checked"))
  	{
  		var height = $( window ).height();
	  	height = height - $("#header").height() - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);
  	}
  	else
  	{
  		var height = $( window ).height();
  		height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
  		$("#graphContainer").height(height);
  		$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);
	  	$("#corefContainer").height(height);

  	}
  	//network.fit();
  });
}


function displayTree(dataJSON, i) 
{
	if($("#idGraph").length == 0)
	{
		$("#home").append("<input type='hidden' id='idGraph' name='"+i+"' />");
	}
	else
	{
		$("#idGraph").attr("name",i);
	}

	var obj = $.parseJSON(dataJSON);
	var tokens = obj["sentences"][i]["tokens"];
	console.log(obj["corefs"]);

	var nodes = [];
	var edges = [];

	if(i - 1 >= 0)
	{
		$("#previous").css({"background-color":"black"});
	}
	else
	{
		$("#previous").css({"background-color":"grey"});
	}
	if(i+1 < obj["sentences"].length)
	{
		$("#next").css({"background-color":"black"});
	}
	else
	{
		$("#next").css({"background-color":"grey"});
	}

	/**
		Create nodes
	**/
	for (var i = 0; i < tokens.length; i++) {
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
    	
/*
    $("#synt").click(function(){
  		network.fit();
  	});
*/
  	$('#synt a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
 	  network.fit();

	});
}

function displayCorefs(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	var corefs = obj["corefs"];
	var nodes = [];
	var edges = [];
	/**
		Create nodes
	**/
	var idNode = 0;

	for (var i = 0; i < corefs.length; i++) 
	{
	    for(var j = 0; j < corefs[i].length; j++)
	    {
	    	console.log(idNode);
	    	var node = {};
		    node.id = idNode;
		    node.label = corefs[i][j];
		    node.group = j;
		    nodes.push(node);
		    idNode++;
	    }
	    idNode = idNode - corefs[i].length;
	    console.log("end loop",idNode);
	    for(var j = 0; j < corefs[i].length - 1; j++)
	    {
	    	var edge = {};
	    	edge.from = idNode;
	    	edge.to = idNode + 1;
	    	edge.arrows = "to";
	    	edges.push(edge);
	    	idNode++;
	    }
	    idNode++;
	    
	}	
	var container = document.getElementById('corefContainer');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {

    };
    networkCoref = new vis.Network(container, data, options);
    	
  	$('#coref a').on('click', function (e) {
	  e.preventDefault();
	  $(this).tab('show');
 	  networkCoref.fit();

	});

}

function displayThem(dataJSON)
{
	var obj = $.parseJSON(dataJSON);
	$( "#themContainer" ).html("");

	for(var p = 0; p<obj["sentences"].length; p++)
	{
		var sentence = obj["sentences"][p]["text"];
		var them = obj["sentences"][p]["components"];
		var tokens = obj["sentences"][p]["tokens"];


		var dictHighlight = {};
		var currentSentSelector = "#sent_"+p;

		$( "#themContainer" ).append("<br/><br/><h4>Sentence Number "+(p+1)+"</h3><span id='sent_"+p+"'></span>");
		
		$(currentSentSelector).append("<span id=ann_in>"+sentence+"</span><br/>");

		var ann_selector = currentSentSelector + " " + "#ann_in";
		$(ann_selector).highlight(sentence,{className:"proposition badge badge-pill badge-secondary"});


		for (var j = 0; j < them.length; j++) 
		{
			$(currentSentSelector).append("<span id=ann_"+j+">"+sentence +"</span><br/>");
			ann_selector = currentSentSelector + " #ann_" +j;

			for(var n = 0; n < them[j].length; n++)
			{
				var from = them[j][n][0] - 1;
				var to = them[j][n][1] - 1;
				var label = them[j][n][2];
				var className;
				if(label[0] == "P")
				{
					className = "proposition badge badge-pill badge-secondary";
				}
				else if(label[0] == "R")
				{
					className = "rheme badge badge-pill badge-info";
				}
				else if(label[0] == "S")
				{
					className = "specifier badge badge-pill badge-success";
				}
				else
				{
					className = "theme badge badge-pill badge-primary";
					$(currentSentSelector).append("<br/>");
				}

				var text = "";
				for(var k = from; k<=to;k++)
				{
					text+= tokens[k] + " "
				}
				text = $.trim(text);
				$(ann_selector).highlight(text,{className:className, wordsOnly: true});
			}
			

		}
		$(currentSentSelector).append("<br/>");
	}
	$( "#themContainer" ).css({"overflow":"auto", "overflow-x":"none"});
	
}