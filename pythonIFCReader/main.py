from _general import mguu_cource_tools
import ifcopenshell as _ifc

ifc_file = _ifc.open(mguu_cource_tools.get_example_file_path("Renga_House.ifc"))
ifc_project =  ifc_file.by_type("IfcProject")[0]
# print(str(ifc_project.get_info()))

window_uuid = "1lG7A9IimhR$$PamwmLlhY"
ifc_window = ifc_file.by_guid(window_uuid)
print(ifc_window)

print("get invers")
elems_inverse = ifc_file.get_inverse(ifc_window)
for elems_inv in elems_inverse:
    print(elems_inv.is_a())

print("get travers")
elems_travers = ifc_file.traverse(ifc_window, 2)
for elems_trav in elems_travers:
    print(elems_trav.is_a())