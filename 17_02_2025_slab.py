import ifcopenshell
import ifcopenshell.geom
import numpy as np

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')
ifc_file = ifcopenshell.open('Renga.ifc')

# Функция для расчета объема по геометрии
def calculate_volume(geometry):
    """Вычисляет объем объекта по его геометрии."""
    verts = np.array(geometry.verts).reshape(-1, 3)  # Вершины
    faces = np.array(geometry.faces).reshape(-1, 3)  # Грани

    volume = 0.0
    for face in faces:
        # Получаем вершины для текущей грани
        v0, v1, v2 = verts[face]
        # Вычисляем объем тетраэдра, образованного гранью и началом координат
        volume += np.dot(v0, np.cross(v1, v2)) / 6.0

    return abs(volume)  # Возвращаем абсолютное значение объема

# Функция для извлечения информации о перекрытиях и расчета их объема
def get_slabs_info_with_volume(ifc_file):
    slabs_info = []

    # Получение всех элементов IfcSlab (перекрытия)
    slabs = ifc_file.by_type('IfcSlab')

    for slab in slabs:
        slab_name = getattr(slab, 'Name', 'Unnamed Slab')
        slab_global_id = getattr(slab, 'GlobalId', 'N/A')
        slab_type = getattr(slab, 'ObjectType', 'N/A')
        slab_description = getattr(slab, 'Description', 'N/A')

        # Извлечение материалов, связанных с перекрытием
        materials = []
        for rel in getattr(slab, 'HasAssociations', []):
            if rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)

        # Получение геометрических данных перекрытия и расчет объема
        volume = 0.0
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, slab)
            if geometry:
                volume = calculate_volume(geometry.geometry)
        except Exception as e:
            print(f"Ошибка при обработке перекрытия {slab_name}: {e}")

        slabs_info.append({
            'Name': slab_name,
            'GlobalId': slab_global_id,
            'Type': slab_type,
            'Description': slab_description,
            'Materials': materials,
            'Volume': volume
        })

    return slabs_info

# Получение информации о перекрытиях
slabs_info = get_slabs_info_with_volume(ifc_file)

# Вывод информации
if slabs_info:
    print(f"Количество перекрытий в проекте: {len(slabs_info)}")
    for idx, slab in enumerate(slabs_info, start=1):
        print(f"\nПерекрытие {idx}:")
        print(f"  Название: {slab['Name']}")
        print(f"  GlobalId: {slab['GlobalId']}")
        print(f"  Тип: {slab['Type']}")
        print(f"  Описание: {slab['Description']}")
        print(f"  Материалы: {', '.join(slab['Materials']) if slab['Materials'] else 'N/A'}")
        print(f"  Объем: {slab['Volume']:.2f} м³")
else:
    print("Перекрытия не найдены.")