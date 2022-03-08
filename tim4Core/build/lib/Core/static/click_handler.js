var previouslyClickedNodeId = null

function colorToWhitePreviousNode(){
    if (previouslyClickedNodeId)
    colorNode(previouslyClickedNodeId, 'white');
}

function colorNode(id, color){
    $($("#node_" + id).children('circle')[0]).attr('fill', color);
    $($("#n" + id).children('rect')[0]).attr('fill', color);
}

function perforcClickAction(event){
    let id = event.detail.id
    colorToWhitePreviousNode();
    colorNode(id, 'red');
    writeDetails(id);
    previouslyClickedNodeId = id;
}

function writeDetails(id){
    $.ajax({
        type: "GET",
        url: "/node",
        data: {"id": id},
        async: false,
        error: function(data){
            alert(data);
        },
        success: function(node) {
            let detailedViewList = $("#detailed-view-list");
            $(detailedViewList).empty();

            let attributes = node.attributes
            for (let attributeKey in attributes){
                    $(detailedViewList).append(`<li>- ${attributeKey} : ${attributes[attributeKey]}</li>`)
            }
        }
    });
}

$(document).on('nodeClicked', function(event){
    perforcClickAction(event)
})

$(document).on('nodeClickedOnTreeview', function(event){
    perforcClickAction(event)
})