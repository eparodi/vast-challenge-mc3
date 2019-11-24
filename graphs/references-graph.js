
function loadJSON(file, callback) {   
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', file, false);
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            callback(JSON.parse(xobj.responseText));
          }
    };
    xobj.send(null);  
}

var nodes, edges, network;

loadJSON('graph/nodes.json', (response) => {
    nodes = response;
})

loadJSON('graph/edges.json', (response2) => {
    edges = response2;
})

function draw() {
    var container = document.getElementById('mynetwork');
    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        nodes: {
            shape: "dot",
            scaling: {
                customScalingFunction: function(min, max, total, value) {
                    return value / total;
                },
                min: 5,
                max: 150
            }
        }
    };
    
    // initialize your network!
    network = new vis.Network(container, data, options);
}

window.addEventListener("load", () => {
    draw();
});
