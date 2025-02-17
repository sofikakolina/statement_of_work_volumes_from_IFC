import ifcopenshell
import ifcopenshell.geom
import numpy as np

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')

# Функция для расчета площади полигона
def calculate_polygon_area(vertices):
    """Вычисляет площадь полигона по его вершинам."""
    x = vertices[:, 0]
    y = vertices[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Функция для извлечения материалов из стен
def extract_materials_from_walls(ifc_file):
    materials_from_walls = []

    # Получение всех элементов IfcWall (стены)
    walls = ifc_file.by_type('IfcWall')

    for wall in walls:
        wall_name = getattr(wall, 'Name', 'Unnamed Wall')

        # Получение геометрических данных стены
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, wall)
            if geometry:
                # Проверка наличия атрибутов verts и faces
                if hasattr(geometry, 'geometry') and hasattr(geometry.geometry, 'verts') and hasattr(geometry.geometry, 'faces'):
                    verts = np.array(geometry.geometry.verts).reshape(-1, 3)  # Вершины стены
                    faces = np.array(geometry.geometry.faces).reshape(-1, 3)  # Грани стены

                    # Вычисление площади одной стороны стены
                    area = 0.0
                    for face in faces:
                        # Получаем вершины для текущей грани
                        face_verts = verts[face]
                        # Вычисляем площадь грани
                        area += calculate_polygon_area(face_verts[:, :2])  # Используем только X и Y координаты

                    # Получение материалов, связанных с текущей стеной
                    for rel in getattr(wall, 'HasAssociations', []):
                        if rel.is_a('IfcRelAssociatesMaterial'):
                            material = rel.RelatingMaterial

                            # Обработка различных типов материалов
                            if material.is_a('IfcMaterial'):
                                # Если материал напрямую связан со стеной
                                materials_from_walls.append({
                                    'Wall': wall_name,
                                    'Material': material.Name,
                                    'Thickness': 'N/A',
                                    'Area': area
                                })
                            elif material.is_a('IfcMaterialLayerSet'):
                                # Если материал представлен как набор слоев
                                for layer in material.MaterialLayers:
                                    if hasattr(layer, 'Material'):
                                        materials_from_walls.append({
                                            'Wall': wall_name,
                                            'Material': layer.Material.Name,
                                            'Thickness': getattr(layer, 'LayerThickness', 'N/A'),
                                            'Area': area
                                        })
                            elif material.is_a('IfcMaterialLayerSetUsage'):
                                # Если материал представлен как использование набора слоев
                                layer_set = material.ForLayerSet
                                for layer in layer_set.MaterialLayers:
                                    if hasattr(layer, 'Material'):
                                        materials_from_walls.append({
                                            'Wall': wall_name,
                                            'Material': layer.Material.Name,
                                            'Thickness': getattr(layer, 'LayerThickness', 'N/A'),
                                            'Area': area
                                        })
                            elif material.is_a('IfcMaterialProfileSet'):
                                # Если материал представлен как набор профилей
                                for profile in material.MaterialProfiles:
                                    if hasattr(profile, 'Material'):
                                        materials_from_walls.append({
                                            'Wall': wall_name,
                                            'Material': profile.Material.Name,
                                            'Thickness': 'N/A',
                                            'Area': area
                                        })
                            elif material.is_a('IfcMaterialProfileSetUsage'):
                                # Если материал представлен как использование набора профилей
                                profile_set = material.ForProfileSet
                                for profile in profile_set.MaterialProfiles:
                                    if hasattr(profile, 'Material'):
                                        materials_from_walls.append({
                                            'Wall': wall_name,
                                            'Material': profile.Material.Name,
                                            'Thickness': 'N/A',
                                            'Area': area
                                        })
                            elif material.is_a('IfcMaterialConstituentSet'):
                                # Если материал представлен как набор компонентов
                                for constituent in material.MaterialConstituents:
                                    if hasattr(constituent, 'Material'):
                                        materials_from_walls.append({
                                            'Wall': wall_name,
                                            'Material': constituent.Material.Name,
                                            'Thickness': 'N/A',
                                            'Area': area
                                        })
                else:
                    print(f"Геометрия стены {wall_name} не содержит данных о вершинах и гранях.")
        except Exception as e:
            print(f"Ошибка при обработке стены {wall_name}: {e}")

    return materials_from_walls

# Извлечение данных
materials_from_walls = extract_materials_from_walls(ifc_file)

# Вывод данных
if materials_from_walls:
    print("Материалы из стен:")
    for material_info in materials_from_walls:
        wall_name = material_info.get('Wall', 'N/A')
        material_name = material_info.get('Material', 'N/A')
        thickness = material_info.get('Thickness', 'N/A')
        area = material_info.get('Area', 'N/A')

        if thickness != 'N/A':
            print(f"Материал: {material_name}, Толщина: {thickness}, Площадь: {area:.2f} м²")
        else:
            print(f"Материал: {material_name}, Площадь: {area:.2f} м²")
else:
    print("Материалы не найдены.")

print(len(materials_from_walls))