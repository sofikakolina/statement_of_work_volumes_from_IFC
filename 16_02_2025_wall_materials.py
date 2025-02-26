import ifcopenshell
import ifcopenshell.geom
import numpy as np

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')
ifc_file = ifcopenshell.open('Renga.ifc')

# Функция для расчета площади полигона
def calculate_polygon_area(vertices):
    """Вычисляет площадь полигона по его вершинам."""
    x = vertices[:, 0]
    y = vertices[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Функция для извлечения информации о стенах
def extract_wall_info(ifc_file):
    walls_info = []
    # Получение всех элементов IfcWall (стены)
    walls = ifc_file.by_type('IfcWall')
    for wall in walls:
        wall_name = getattr(wall, 'Name', 'Unnamed Wall')
        wall_global_id = getattr(wall, 'GlobalId', 'N/A')
        wall_type = getattr(wall, 'ObjectType', 'N/A')
        wall_description = getattr(wall, 'Description', 'None')
        # Получение материалов, связанных с текущей стеной
        materials = []
        for rel in getattr(wall, 'HasAssociations', []):
            if rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                # Обработка различных типов материалов
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)
                elif material.is_a('IfcMaterialLayerSetUsage'):
                    layer_set = material.ForLayerSet
                    for layer in layer_set.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)
                elif material.is_a('IfcMaterialProfileSet'):
                    for profile in material.MaterialProfiles:
                        if hasattr(profile, 'Material'):
                            materials.append(profile.Material.Name)
                elif material.is_a('IfcMaterialProfileSetUsage'):
                    profile_set = material.ForProfileSet
                    for profile in profile_set.MaterialProfiles:
                        if hasattr(profile, 'Material'):
                            materials.append(profile.Material.Name)
                elif material.is_a('IfcMaterialConstituentSet'):
                    for constituent in material.MaterialConstituents:
                        if hasattr(constituent, 'Material'):
                            materials.append(constituent.Material.Name)

        # Получение геометрических данных стены
        has_geometry = False
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, wall)
            if geometry:
                has_geometry = True
        except Exception as e:
            print(f"Ошибка при обработке стены {wall_name}: {e}")

        walls_info.append({
            'Name': wall_name,
            'GlobalId': wall_global_id,
            'Type': wall_type,
            'Description': wall_description,
            'Materials': materials,
            'HasGeometry': has_geometry
        })

    return walls_info

# Извлечение данных
walls_info = extract_wall_info(ifc_file)

# Вывод данных
if walls_info:
    for wall in walls_info:
        print(f"Стена:")
        print(f"  Название: {wall['Name']}")
        print(f"  GlobalId: {wall['GlobalId']}")
        print(f"  Тип: {wall['Type']}")
        print(f"  Описание: {wall['Description']}")
        print(f"  Материалы: {', '.join(wall['Materials']) if wall['Materials'] else 'N/A'}")
        print(f"  Наличие геометрии: {'Да' if wall['HasGeometry'] else 'Нет'}")
        print()
else:
    print("Стены не найдены.")
