var itemIds = -1;
var rootIds = [];

function getNewItemId(){
    itemIds++;

    return itemIds;
}

function createItem(ul, nodeId){
    $.ajax({
        type: "GET",
        url: "/node",
        data: {"id": nodeId},
        async: false,
        error: function(data){
            alert(data);
        },
        success: function(node) {
            let newItemId = getNewItemId();
            $(ul).append(getItemHtml(node, newItemId));
            addItemListener(node, newItemId);
        }
    });
}

function createRoot(rootId){
    rootIds.push(rootId)
    createItem($("#tree"), rootId)
}

function createRoots(){
    $("#tree").empty();

    $.ajax({
        type: "GET",
        url: "/rootNodes",
        async: false,
        success: function(root_ids) {
            for (rootId of root_ids)
                createRoot(rootId)
        },
        error: function(data){
            alert(data);
        }
    });
}

function getItemHtml(node, itemId){
    return `
    <li class="childrenNotOpened" name="${node.id}" id="${itemId}"><i id="arrow${itemId}" class="far fa-arrow-alt-circle-right"></i> ${node.id}</li>
    `
}

function getAttributeItemHtml(attributeKey, attributeValue){
    return `
    <li>- ${attributeKey} : ${attributeValue}</li>
    `
}

function addAttributes(ul, node){
    for (var key in node.attributes){
        if (key != "id")
            $(ul).append(getAttributeItemHtml(key, node.attributes[key]))
    }
}

function addChildren(ul, node){
    if (node.children_ids != 0){
        for (childrenId of node.children_ids){
            createItem(ul, childrenId)
        }
    }
}

function createItemChildren(node, itemId){
    let nodeItem = $("#" + itemId);
    $(nodeItem).after(`<ul id="${itemId}_children"></ul>`);
    let ul = $(`#${itemId}_children`);
    addAttributes(ul, node)
    addChildren(ul, node)
}

function setChildrenOpenClasses(nodeItem, arrow){
    nodeItem.removeClass("childrenNotOpened");
    nodeItem.addClass("childrenOpened");
    arrow.removeClass("fa-arrow-alt-circle-right");
    arrow.addClass("fa-arrow-alt-circle-down");
}

function setChildrenNotOpenClasses(nodeItem, arrow){
    nodeItem.addClass("childrenNotOpened");
    nodeItem.removeClass("childrenOpened");
    arrow.removeClass("fa-arrow-alt-circle-down");
    arrow.addClass("fa-arrow-alt-circle-right");
}

function areChildrenClosed(nodeItem){
    let classList = nodeItem.attr("class");

    return classList.includes("childrenNotOpened")
}

function openChildren(nodeItem, arrow, node, itemId){
    setChildrenOpenClasses(nodeItem, arrow)
    createItemChildren(node, itemId);
}

function closeChildren(nodeItem, arrow, itemId){
    setChildrenNotOpenClasses(nodeItem, arrow)
    $(`#${itemId}_children`).remove();
}

function addItemListener(node, itemId){
    let nodeItem = $("#" + itemId);
    let arrow = $("#arrow" + itemId);

    $(nodeItem).click(function(){
        var nodeClickedOnTreeviewEvent = new CustomEvent('nodeClickedOnTreeview', {
            detail: {
                'id':node.id
            }
        });
        document.dispatchEvent(nodeClickedOnTreeviewEvent);
        if (areChildrenClosed(nodeItem)){
            openChildren(nodeItem, arrow, node, itemId);
        } else {
            closeChildren(nodeItem, arrow, itemId);
        }
    })

    if (rootIds.includes(node.id)){
        $(document).on('removeRootChildren', function(){
            if (!areChildrenClosed(nodeItem))
                closeChildren(nodeItem, arrow, itemId);
        });
    }
}

function openNode(wantedNodeId){
    $.ajax({
        type: "GET",
        url: "/pathToNode",
        async: false,
        data: {"id": wantedNodeId},
        success: function(path) {
            var removeRootChildrenEvent = new Event('removeRootChildren');
            document.dispatchEvent(removeRootChildrenEvent);

            for (nodeId of path){
                /* get itemIds, nodeItems, arrows and simulate their opening */
                itemId = $(`li[name="${nodeId}"]`).attr('id')
                let nodeItem = $("#" + itemId);
                let arrow = $("#arrow" + itemId)
                $.ajax({
                    type: "GET",
                    url: "/node",
                    data: {"id": nodeId},
                    async: false,
                    error: function(data){
                        alert(data);
                    },
                    success: function(node) {
                        openChildren(nodeItem, arrow, node, itemId);
                    }
                });
            }
        },
        error: function(data){
            alert(data);
        }
    });
}

$(document).on('nodeClicked', function(event){
    let id = event.detail.id
    openNode(id);
})