import ifcopenshell

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')

# Функция для извлечения информации о дверях
def get_doors_info(ifc_file):
    doors_info = []

    # Получение всех элементов IfcDoor (двери)
    doors = ifc_file.by_type('IfcDoor')

    for door in doors:
        door_name = getattr(door, 'Name', 'Unnamed Door')
        door_global_id = getattr(door, 'GlobalId', 'N/A')
        door_type = getattr(door, 'ObjectType', 'N/A')
        door_description = getattr(door, 'Description', 'N/A')

        # Извлечение размеров двери (ширина и высота)
        door_width = None
        door_height = None

        for rel_defines in door.IsDefinedBy:
            if rel_defines.is_a('IfcRelDefinesByProperties'):
                property_set = rel_defines.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    if property_set.Name == 'Pset_DoorCommon':
                        for property in property_set.HasProperties:
                            if property.Name == 'OverallWidth':
                                door_width = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'OverallHeight':
                                door_height = property.NominalValue.wrappedValue if property.NominalValue else None

        doors_info.append({
            'Name': door_name,
            'GlobalId': door_global_id,
            'Type': door_type,
            'Description': door_description,
            'Width': door_width,
            'Height': door_height
        })

    return doors_info

# Получение информации о дверях
doors_info = get_doors_info(ifc_file)

# Вывод информации
if doors_info:
    print(f"Количество дверей в проекте: {len(doors_info)}")
    for idx, door in enumerate(doors_info, start=1):
        print(f"\nДверь {idx}:")
        print(f"  Название: {door['Name']}")
        print(f"  GlobalId: {door['GlobalId']}")
        print(f"  Тип: {door['Type']}")
        print(f"  Описание: {door['Description']}")
        print(f"  Ширина: {door['Width']} мм" if door['Width'] else "  Ширина: N/A")
        print(f"  Высота: {door['Height']} мм" if door['Height'] else "  Высота: N/A")
else:
    print("Двери не найдены.")