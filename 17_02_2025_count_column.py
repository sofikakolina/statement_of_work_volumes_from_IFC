import ifcopenshell

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')

# Функция для вычисления объема объекта на основе его геометрии
def calculate_volume_from_geometry(shape):
    if shape.is_a('IfcExtrudedAreaSolid'):
        # Получаем профиль (площадь) и высоту экструзии
        profile = shape.SweptArea
        depth = shape.Depth

        # Вычисляем площадь профиля (упрощенно, предполагая, что это прямоугольник)
        if profile.is_a('IfcRectangleProfileDef'):
            width = profile.XDim
            height = profile.YDim
            area = width * height
            return area * depth  # Объем = площадь * глубина
        else:
            # Для других типов профилей можно добавить расчет
            return None
    elif shape.is_a('IfcBoundingBox'):
        # Вычисляем объем для ограничивающего прямоугольника
        x = shape.XDim
        y = shape.YDim
        z = shape.ZDim
        return x * y * z
    elif shape.is_a('IfcMappedItem'):
        # Обработка IfcMappedItem (например, для повторяющихся элементов)
        return None  # Пока пропускаем такие элементы
    elif shape.is_a('IfcBooleanResult'):
        # Обработка булевых операций (например, вычитание или объединение)
        return None  # Пока пропускаем такие элементы
    else:
        # Для других типов геометрии можно добавить расчет
        return None

# Функция для получения информации о колоннах и расчета объема
def get_columns_info(ifc_file):
    columns_info = []

    # Получение всех элементов IfcColumn (колонны)
    columns = ifc_file.by_type('IfcColumn')

    element = ifc_file.by_type('IfcColumn')[0]  # Пример элемента
    if element.Representation is not None:
        print("Элемент имеет геометрию.")
    else:
        print("Элемент не имеет геометрии.")





    for column in columns:
        column_name = getattr(column, 'Name', 'Unnamed Column')
        column_global_id = getattr(column, 'GlobalId', 'N/A')

        # Получение материалов, связанных с колонной
        materials = []
        for rel in getattr(column, 'HasAssociations', []):
            if rel is not None and rel.is_a('IfcRelAssociatesMaterial'):
                material = rel.RelatingMaterial
                if material.is_a('IfcMaterial'):
                    materials.append(material.Name)
                elif material.is_a('IfcMaterialLayerSet'):
                    for layer in material.MaterialLayers:
                        if hasattr(layer, 'Material'):
                            materials.append(layer.Material.Name)

        # Получение геометрического представления колонны
        volume = None
        if column.IsDefinedBy:
            for relation in column.IsDefinedBy:
                if hasattr(relation, 'RelatingPropertyDefinition'):
                    prop_def = relation.RelatingPropertyDefinition
                    if prop_def.is_a("IfcElementQuantity"):
                        for quantity in prop_def.Quantities:
                            if quantity.is_a("IfcQuantityVolume"):
                                volume = quantity.VolumeValue

        # Если объем не удалось вычислить, используем значение по умолчанию
        if volume is None:
            volume = 1.0  # м³ (значение по умолчанию)

        columns_info.append({
            'Name': column_name,
            'GlobalId': column_global_id,
            'Materials': materials,
            'Volume': volume
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
        print(f"  Объем бетона: {column['Volume']:.3f} м³")
else:
    print("Колонны не найдены.")