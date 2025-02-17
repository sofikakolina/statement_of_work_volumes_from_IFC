import ifcopenshell

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')

# Функция для получения информации о колоннах
def get_columns_info(ifc_file):
    columns_info = []

    # Получение всех элементов IfcColumn (колонны)
    columns = ifc_file.by_type('IfcColumn')

    for column in columns:
        column_name = getattr(column, 'Name', 'Unnamed Column')
        column_global_id = getattr(column, 'GlobalId', 'N/A')

        # Получение материалов, связанных с колонной
        materials = []
        for rel in getattr(column, 'HasAssociations', []):
            if rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)

        columns_info.append({
            'Name': column_name,
            'GlobalId': column_global_id,
            'Materials': materials
        })

    return columns_info

# Получение информации о колоннах
columns_info = get_columns_info(ifc_file)

# Вывод информации
if columns_info:
    print(f"Количество колонн в проекте: {len(columns_info)}")
    for idx, column in enumerate(columns_info, start=1):
        print(f"\nКолонна {idx}:")
        print(f"  Название: {column['Name']}")
        print(f"  GlobalId: {column['GlobalId']}")
        print(f"  Материалы: {', '.join(column['Materials']) if column['Materials'] else 'N/A'}")
else:
    print("Колонны не найдены.")