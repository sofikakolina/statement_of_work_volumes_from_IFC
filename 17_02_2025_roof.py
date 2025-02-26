import ifcopenshell
import ifcopenshell.geom

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')
ifc_file = ifcopenshell.open('Renga.ifc')

# Функция для извлечения информации о крыше и материалах
def get_roof_info(ifc_file):
    roofs_info = []

    # Получение всех элементов IfcRoof (крыши)
    roofs = ifc_file.by_type('IfcRoof')

    for roof in roofs:
        roof_name = getattr(roof, 'Name', 'Unnamed Roof')
        roof_global_id = getattr(roof, 'GlobalId', 'N/A')
        roof_type = getattr(roof, 'ObjectType', 'N/A')
        roof_description = getattr(roof, 'Description', 'N/A')

        # Извлечение материалов, связанных с крышей
        materials = []
        for rel in getattr(roof, 'HasAssociations', []):
            if rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)

        # Проверка наличия геометрии у крыши
        has_geometry = False
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, roof)
            if geometry:
                has_geometry = True
        except Exception as e:
            print(f"Ошибка при обработке геометрии крыши {roof_name}: {e}")


        if (has_geometry):
            roofs_info.append({
                'Name': roof_name,
                'GlobalId': roof_global_id,
                'Type': roof_type,
                'Description': roof_description,
                'Materials': materials,
                'HasGeometry': has_geometry
            })

    return roofs_info

# Получение информации о крыше
roofs_info = get_roof_info(ifc_file)

# Вывод информации
if roofs_info:
    print(f"Количество крыш в проекте: {len(roofs_info)}")
    for idx, roof in enumerate(roofs_info, start=1):
        print(f"\nКрыша {idx}:")
        print(f"  Название: {roof['Name']}")
        print(f"  GlobalId: {roof['GlobalId']}")
        print(f"  Тип: {roof['Type']}")
        print(f"  Описание: {roof['Description']}")
        print(f"  Материалы: {', '.join(roof['Materials']) if roof['Materials'] else 'N/A'}")
        print(f"  Наличие геометрии: {'Да' if roof['HasGeometry'] else 'Нет'}")
else:
    print("Крыши не найдены.")