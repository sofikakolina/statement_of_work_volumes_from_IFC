import ifcopenshell

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')

# Функция для извлечения параметров лестницы и расчета объема бетона
def calculate_concrete_volume_for_stairs(ifc_file):
    stairs_info = []
    railings_info = []

    # Получение всех элементов IfcStair и IfcStairFlight
    stairs = ifc_file.by_type('IfcStair') + ifc_file.by_type('IfcStairFlight')

    for stair in stairs:
        stair_name = getattr(stair, 'Name', 'Unnamed Stair')
        stair_global_id = getattr(stair, 'GlobalId', 'N/A')

        # Извлечение параметров лестницы из свойств (Pset_StairCommon)
        tread_length = None
        riser_height = None
        number_of_treads = None
        stair_width = None

        for rel_defines in stair.IsDefinedBy:
            if rel_defines.is_a('IfcRelDefinesByProperties'):
                property_set = rel_defines.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    if property_set.Name == 'Pset_StairCommon':
                        for property in property_set.HasProperties:
                            if property.Name == 'TreadLength':
                                tread_length = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'RiserHeight':
                                riser_height = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'NumberOfTreads':
                                number_of_treads = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'Width':
                                stair_width = property.NominalValue.wrappedValue if property.NominalValue else None

        # Если параметры не найдены, используем значения по умолчанию
        if tread_length is None:
            tread_length = 280  # мм (значение по умолчанию)
        if riser_height is None:
            riser_height = 172.63  # мм (значение по умолчанию)
        if number_of_treads is None:
            number_of_treads = 10  # (значение по умолчанию)
        if stair_width is None:
            stair_width = 1000  # мм (значение по умолчанию)

        # Преобразование в метры
        tread_length_m = tread_length / 1000
        riser_height_m = riser_height / 1000
        stair_width_m = stair_width / 1000

        # Расчет объема бетона
        volume = tread_length_m * stair_width_m * riser_height_m * number_of_treads

        stairs_info.append({
            'Name': stair_name,
            'GlobalId': stair_global_id,
            'TreadLength': tread_length,
            'RiserHeight': riser_height,
            'NumberOfTreads': number_of_treads,
            'StairWidth': stair_width,
            'Volume': volume
        })

    # Получение всех элементов IfcRailing (перила)
    railings = ifc_file.by_type('IfcRailing')

    for railing in railings:
        railing_name = getattr(railing, 'Name', 'Unnamed Railing')
        railing_global_id = getattr(railing, 'GlobalId', 'N/A')

        # Извлечение параметров перил из свойств (Pset_RailingCommon)
        railing_length = None
        railing_height = None
        railing_material = None

        for rel_defines in railing.IsDefinedBy:
            if rel_defines.is_a('IfcRelDefinesByProperties'):
                property_set = rel_defines.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    if property_set.Name == 'Pset_RailingCommon':
                        for property in property_set.HasProperties:
                            if property.Name == 'Length':
                                railing_length = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'Height':
                                railing_height = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'Material':
                                railing_material = property.NominalValue.wrappedValue if property.NominalValue else None

        # Если параметры не найдены, используем значения по умолчанию
        if railing_length is None:
            railing_length = 1000  # мм (значение по умолчанию)
        if railing_height is None:
            railing_height = 900  # мм (значение по умолчанию)
        if railing_material is None:
            railing_material = 'Не указан'

        railings_info.append({
            'Name': railing_name,
            'GlobalId': railing_global_id,
            'Length': railing_length,
            'Height': railing_height,
            'Material': railing_material
        })

    return stairs_info, railings_info

# Получение информации о лестницах и перилах
stairs_info, railings_info = calculate_concrete_volume_for_stairs(ifc_file)

# Вывод информации о лестницах
if stairs_info:
    print(f"Количество лестниц в проекте: {len(stairs_info)}")
    for idx, stair in enumerate(stairs_info, start=1):
        print(f"\nЛестница {idx}:")
        print(f"  Название: {stair['Name']}")
        print(f"  GlobalId: {stair['GlobalId']}")
        print(f"  Длина ступени: {stair['TreadLength']} мм")
        print(f"  Высота подступенка: {stair['RiserHeight']} мм")
        print(f"  Количество ступеней: {stair['NumberOfTreads']}")
        print(f"  Ширина лестницы: {stair['StairWidth']} мм")
        print(f"  Расчетный объем бетона: {stair['Volume']:.3f} м³")
else:
    print("Лестницы не найдены.")

# Вывод информации о перилах
if railings_info:
    print(f"\nКоличество перил в проекте: {len(railings_info)}")
    for idx, railing in enumerate(railings_info, start=1):
        print(f"\nПерила {idx}:")
        print(f"  Название: {railing['Name']}")
        print(f"  GlobalId: {railing['GlobalId']}")
        print(f"  Длина: {railing['Length']} мм")
        print(f"  Высота: {railing['Height']} мм")
        print(f"  Материал: {railing['Material']}")
else:
    print("\nПерила не найдены.")