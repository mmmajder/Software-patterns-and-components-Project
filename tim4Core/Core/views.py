import json

from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from jsonpickle import encode, decode

from Core.models import Graph


def index(request):
    return render(request, 'index.html', get_plugins_dict())


@csrf_exempt
def set_selected_loader(request, loader_plugin_id):
    request.session["loader_id"] = loader_plugin_id
    return render(request, 'index.html', get_plugins_dict())


@csrf_exempt
def set_selected_visualiser(request, visualiser_plugin_id: str):
    request.session["visualiser_id"] = visualiser_plugin_id
    return render(request, 'index.html', get_plugins_dict())


def load_graph(request, file_name):
    loader_plugin_id = request.session["loader_id"]
    loader_plugins = apps.get_app_config("Core").loader_plugins
    for i in loader_plugins:
        if i.identifier() == loader_plugin_id:
            graph = i.load(file_name)
            apps.get_app_config("Core").graph = graph
            request.session["graph"] = encode(graph, keys=True)


@csrf_exempt
def file_picker(request):
    if request.method == 'POST':
        loader_plugin_id = request.session["loader_id"]
        if loader_plugin_id is None:
            return redirect('index')
        try:
            file = request.FILES['file_field']
        except:
            return redirect('index')

        with open('tempFile', 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        try:
            load_graph(request, 'tempFile')
        except:
            request.session['file_status'] = 'Invalid file'
        return redirect('index')


@csrf_exempt
def get_node_by_id(request):
    graph = decode(request.session["graph"], keys=True)
    id = request.GET['id']

    node = graph.get_node_by_id(id)
    children_ids = []
    for child in node.children:
        children_ids.append(child.id)

    node_parsed = {
        'id': node.id,
        'children_ids': children_ids,
        'attributes': node.attributes
    }

    return HttpResponse(json.dumps(node_parsed), content_type='application/json')


@csrf_exempt
def get_root_nodes(request):
    graph = decode(request.session["graph"], keys=True)
    # root_ids = {'root_ids': graph.get_root_node_ids()}
    root_ids = list(graph.get_root_node_ids())

    return HttpResponse(json.dumps(root_ids), content_type='application/json')


@csrf_exempt
def get_path_to_node(request):
    graph = decode(request.session["graph"], keys=True)
    id = request.GET['id']
    path = graph.get_path_to_node_from_roots(id)

    return HttpResponse(json.dumps(path), content_type='application/json')


@csrf_exempt
def view_graph(request):
    graph = decode(request.session["graph"], keys=True)
    html = ""
    visualiser_plugin_id = request.session["visualiser_id"]
    if visualiser_plugin_id is None:
        return
    visualiser_plugins = apps.get_app_config("Core").visualiser_plugins
    for i in visualiser_plugins:
        if i.identifier() == visualiser_plugin_id:
            html = i.visualise(graph)
            break
    request.session["graph_html"] = html
    return HttpResponse(json.dumps({'graph_html': html}), content_type='application/json')


@csrf_exempt
def search_graph(request, param):
    original_graph = apps.get_app_config("Core").graph
    if not original_graph:
        return bad_request('Graph is empty!')

    print(param)
    print(original_graph)
    if param == "null":
        request.session["graph"] = encode(original_graph, keys=True)
        return view_graph(request)

    searched_graph = search(original_graph, param)
    print(searched_graph)
    if not searched_graph:
        return bad_request('Graph is empty!')

    request.session["graph"] = encode(searched_graph, keys=True)
    return view_graph(request)


@csrf_exempt
def filter_graph(request, param):
    filtered_graph = filter(apps.get_app_config("Core").graph, param)
    print(decode(request.session["graph"], keys=True))
    print(filtered_graph)
    if not filtered_graph:
        return bad_request('Input is not valid!')
    apps.get_app_config("Core").graph = filtered_graph
    request.session["graph"] = encode(filtered_graph)
    return view_graph(request)


def get_plugins_dict():
    visualiser_plugins = apps.get_app_config("Core").visualiser_plugins
    loader_plugins = apps.get_app_config("Core").loader_plugins

    return {'visualiser_plugins': visualiser_plugins, 'loader_plugins': loader_plugins, 'graph_html': ''}


# search

def find_invalid_nodes(nodes, search_param):
    list_to_remove = []

    for node in nodes:
        found = False
        for key, value in node.attributes.items():
            if str(search_param).lower() in str(key).lower() or str(search_param).lower() in str(value).lower():
                found = True
        if not found:
            list_to_remove.append(node.id)

    return list_to_remove


def search(graph, search_param):
    list_to_remove = find_invalid_nodes(graph.get_nodes(), search_param)
    return graph.remove_nodes_by_id(list_to_remove)


def bad_request(message):
    response = HttpResponse(message)
    response.status_code = 400
    return response


# filter

def valid_node(x, operator, value):
    x = is_float(x)
    value = is_float(value)
    try:
        if operator == '==':
            return x == value
        if operator == '!=':
            return x != value
        if operator == '>':
            return x > value
        if operator == '<':
            return x < value
        if operator == '>=':
            return x >= value
        return x <= value
    except:
        return False


def is_float(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return str(x).lower()
    return a


def filter(graph, input):
    print(graph)
    attribute, operator, value = get_filter_params(input)
    if operator == 'error':
        return Graph()
    deleting_ids = []
    for node in graph.get_nodes():
        node_attribute = has_attribute(node, attribute)
        if not node_attribute or not valid_node(node_attribute, operator, value):
            deleting_ids.append(node.id)
    print(deleting_ids)
    for id in deleting_ids:
        graph.remove_node(id)
    return graph


def has_attribute(node, attribute):
    for a in node.attributes.keys():
        if attribute == a:
            return node.attributes[a]
        if attribute.lower() == a.lower():
            return node.attributes[a]
    return None


def get_filter_params(input):
    if len(input.split('==')) == 2:
        return split_params(input, '==')
    if len(input.split('!=')) == 2:
        return split_params(input, '!=')
    if len(input.split('<=')) == 2:
        return split_params(input, '<=')
    if len(input.split('>=')) == 2:
        return split_params(input, '>=')
    if len(input.split('<')) == 2:
        return split_params(input, '<')
    if len(input.split('>')) == 2:
        return split_params(input, '>')
    return '', 'error', ''


def split_params(input, operator):
    tokens = input.split(operator)
    attribute = tokens[0].strip()
    value = tokens[1].strip()
    if attribute == '' or value == '':
        return '', 'error', ''
    return attribute, operator, value
