var network;
var globalDATA;

$(document).ready(function(){

	$.ajaxSetup({async: false});  
  	manageTestButton();
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
			createGraph(globalDATA, currentGraph-1);
		}	
	});

	$("#next").click(function(){
		var currentGraph = parseInt($('#idGraph').attr("name"));
		if($( this ).css( "background-color" ) == "rgb(0, 0, 0)")
		{
			createGraph(globalDATA, currentGraph+1);
		}
	});
}

function manageTestButton()
{

	$("#testButton").click(function(){
	  	$("#pillWrapper").show();
	  	$("#tabContent").show();

	  	var height = $( window ).height();
	  	console.log(height)
	  	height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 20;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#header").hide()
	    $.getJSON( "http://127.0.0.1:5000/getTestConll?callback=?", function( dataJSON ) {
		    createGraph(dataJSON);
		});

		$.getJSON( "http://127.0.0.1:5000/getTestThematicity?callback=?", function( dataJSON ) {
		    displayThem(dataJSON);
		});
		$("#myonoffswitch").prop("checked",false);
  	});
}

function manageSubmitButton()
{

	$("#submitButton").click(function(){

		$("#pillWrapper").show();
		$("#tabContent").show();

	  	var height = $( window ).height();
	  	console.log(height)
	  	height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 20;
	  	$("#graphContainer").height(height);
	  	$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);

	  	$("#header").hide()

	  	var text =  $('textarea#inputBox').val();
	  	var data = {"text": text};

	    $.post( "http://127.0.0.1:5000/getConll", data ,function( dataJSON ) {
		    createGraph(dataJSON, 0);
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
    node.label = hyper;
    node.group = 0;
    node.title = "hyper";
    nodes.push(node);

    var THEME_OFFSET = 100;
    var RHEME_OFFSET = 1000;

	for(var i = 0 ; i< components.length; i++)
	{
		var nodeTheme = {};
	    nodeTheme.id = i+THEME_OFFSET;
	    nodeTheme.label = components[i][0];
	    nodeTheme.group = 1;
	    nodeTheme.title = "Theme";
	    nodeTheme.shape="triangle";
	    nodeTheme.scaling = {label:{enabled:true}};
	    nodes.push(nodeTheme);

	    if( i < components.length-1)
	    {
		    var nodeRheme = {};
		    nodeRheme.id = i+RHEME_OFFSET;
		    nodeRheme.label = components[i][1];
		    nodeRheme.group = 2;
		    nodeRheme.title = "Rheme";
		    nodeRheme.shape="triangle";
	    	nodeRheme.scaling = {label:{enabled:true}};
	    	nodes.push(nodeRheme);

		}
	}

	for(var j = 1; j< distances.length; j++)
	{
		var edgeTheme = {};
		edgeTheme.from = j-1+THEME_OFFSET;
		edgeTheme.to = j+THEME_OFFSET
		edgeTheme.label = String(distances[j][0].toFixed(2));
		edgeTheme.font = {align: 'top'};
		edgeTheme.arrows = "from";
		edges.push(edgeTheme);

		var edgeRheme = {};
		edgeRheme.from = j-1+RHEME_OFFSET;
		edgeRheme.to = j+THEME_OFFSET
		edgeRheme.label = String(distances[j][1].toFixed(2));
		edgeRheme.font = {align: 'top'};
		edgeRheme.arrows = "from";
		edges.push(edgeRheme);
/*
		var edgeHyper = {};
		edgeHyper.from = j+THEME_OFFSET
		edgeHyper.to = 0;
		edgeHyper.label = String(distances[j][2]);
		edgeHyper.font = {align: 'top'};
		edges.push(edgeHyper);*/
	}


	var container = document.getElementById('themProgContainer');
    var data = {
        nodes: nodes, 
        edges: edges
    };
    console.log(data);
    var options = {

	  physics: false
	};
    networkThem = new vis.Network(container, data, options);
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
	  	
  	}
  	else
  	{
  		var height = $( window ).height();
  		height = height - $("#pillWrapper").height() - $(".onoffswitch").height() - 50;
  		$("#graphContainer").height(height);
  		$("#themContainer").height(height);
	  	$("#themProgContainer").height(height);

  	}
  	//network.fit();
  });
}


function createGraph(dataJSON, i) 
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

		$( "#themContainer" ).append("<h3>Sentence Number "+(p+1)+"</h3><span id='sent_"+p+"'></span>");
		
		$(currentSentSelector).append("<span id=ann_in>"+sentence+"</span><br/>");

		var ann_selector = currentSentSelector + " " + "#ann_in";
		$(ann_selector).highlight(sentence,{className:"proposition badge badge-pill badge-dark"});


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
					$(currentSentSelector).append("<br/>");
				}

				var text = "";
				for(var k = from; k<=to;k++)
				{
					text+= tokens[k] + " "
				}
				text = $.trim(text);
				console.log(text);
				$(ann_selector).highlight(text,{className:className, wordsOnly: true});
			}
			

		}
		$(currentSentSelector).append("<br/>");
	}
	$( "#themContainer" ).css({"overflow":"auto", "overflow-x":"none"});
	
}