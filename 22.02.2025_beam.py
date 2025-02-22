import ifcopenshell
import ifcopenshell.geom
import numpy as np

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')

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

# Функция для извлечения информации о балках и расчета их объема
def get_beams_info_with_volume(ifc_file):
    beams_info = []

    # Получение всех элементов IfcBeam (балки)
    beams = ifc_file.by_type('IfcBeam')

    for beam in beams:
        beam_name = getattr(beam, 'Name', 'Unnamed Beam')
        beam_global_id = getattr(beam, 'GlobalId', 'N/A')
        beam_type = getattr(beam, 'ObjectType', 'N/A')
        beam_description = getattr(beam, 'Description', 'N/A')

        # Извлечение материалов, связанных с балкой
        materials = []
        for rel in getattr(beam, 'HasAssociations', []):
            if rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)

        # Получение геометрических данных балки и расчет объема
        volume = 0.0
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, beam)
            if geometry:
                volume = calculate_volume(geometry.geometry)
        except Exception as e:
            print(f"Ошибка при обработке балки {beam_name}: {e}")

        beams_info.append({
            'Name': beam_name,
            'GlobalId': beam_global_id,
            'Type': beam_type,
            'Description': beam_description,
            'Materials': materials,
            'Volume': volume
        })

    return beams_info

# Получение информации о балках
beams_info = get_beams_info_with_volume(ifc_file)

# Вывод информации
if beams_info:
    print(f"Количество балок в проекте: {len(beams_info)}")
    for idx, beam in enumerate(beams_info, start=1):
        if (beam['GlobalId'] == '1aznOgcD9Fp9cJ8_9mfQun'):
            print(f"\nБалка {idx}:")
            print(f"  Название: {beam['Name']}")
            print(f"  GlobalId: {beam['GlobalId']}")
            print(f"  Тип: {beam['Type']}")
            print(f"  Описание: {beam['Description']}")
            print(f"  Материалы: {', '.join(beam['Materials']) if beam['Materials'] else 'N/A'}")
            print(f"  Объем: {beam['Volume']:.2f} м³")
else:
    print("Балки не найдены.")