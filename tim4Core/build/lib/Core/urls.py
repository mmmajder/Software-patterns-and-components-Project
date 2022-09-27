from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('loaderSelection/<str:loader_plugin_id>', views.set_selected_loader, name='load_plugin'),
    path('visualiserSelection/<str:visualiser_plugin_id>', views.set_selected_visualiser, name='visual_plugin'),

    path('file', views.file_picker, name="file"),
    path('viewGraph', views.view_graph, name='viewGraph'),  # added

    path('search/<str:param>', views.search_graph, name='search'),
    path('filter/<str:param>', views.filter_graph, name='filter'),

    path('node', views.get_node_by_id, name="node"),
    path('rootNodes', views.get_root_nodes, name="rootNodes"),
    path('pathToNode', views.get_path_to_node, name="pathToNode"),
]
