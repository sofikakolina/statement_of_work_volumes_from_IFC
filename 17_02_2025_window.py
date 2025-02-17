import ifcopenshell

# Загрузка IFC файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')

# Функция для извлечения информации об окнах
def get_windows_info(ifc_file):
    windows_info = []

    # Получение всех элементов IfcWindow (окна)
    windows = ifc_file.by_type('IfcWindow')

    for window in windows:
        window_name = getattr(window, 'Name', 'Unnamed Window')
        window_global_id = getattr(window, 'GlobalId', 'N/A')
        window_type = getattr(window, 'ObjectType', 'N/A')
        window_description = getattr(window, 'Description', 'N/A')

        # Извлечение размеров окна (ширина и высота)
        window_width = None
        window_height = None

        for rel_defines in window.IsDefinedBy:
            if rel_defines.is_a('IfcRelDefinesByProperties'):
                property_set = rel_defines.RelatingPropertyDefinition
                if property_set.is_a('IfcPropertySet'):
                    if property_set.Name == 'Pset_WindowCommon':
                        for property in property_set.HasProperties:
                            if property.Name == 'OverallWidth':
                                window_width = property.NominalValue.wrappedValue if property.NominalValue else None
                            elif property.Name == 'OverallHeight':
                                window_height = property.NominalValue.wrappedValue if property.NominalValue else None

        windows_info.append({
            'Name': window_name,
            'GlobalId': window_global_id,
            'Type': window_type,
            'Description': window_description,
            'Width': window_width,
            'Height': window_height
        })

    return windows_info

# Получение информации об окнах
windows_info = get_windows_info(ifc_file)

# Вывод информации
if windows_info:
    print(f"Количество окон в проекте: {len(windows_info)}")
    for idx, window in enumerate(windows_info, start=1):
        print(f"\nОкно {idx}:")
        print(f"  Название: {window['Name']}")
        print(f"  GlobalId: {window['GlobalId']}")
        print(f"  Тип: {window['Type']}")
        print(f"  Описание: {window['Description']}")
        print(f"  Ширина: {window['Width']} мм" if window['Width'] else "  Ширина: N/A")
        print(f"  Высота: {window['Height']} мм" if window['Height'] else "  Высота: N/A")
else:
    print("Окна не найдены.")