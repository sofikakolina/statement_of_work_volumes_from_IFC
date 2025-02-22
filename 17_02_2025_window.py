import ifcopenshell
import re
import ifcopenshell.geom

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')


def extract_dimensions_from_object_type(object_type):
    """
    Извлекает ширину и высоту из строки ObjectType, где размеры указаны в формате "ширина x высота".
    Поддерживает форматы:
    - 900 x 2000 мм
    - 1350x2200(h)
    - 1500х1500/600h

    :param object_type: Строка, содержащая размеры.
    :return: Кортеж (ширина, высота) или (None, None), если размеры не найдены.
    """
    if object_type:
        # Используем регулярное выражение для поиска размеров
        match = re.search(r'(\d+)\s*[xхX*]\s*(\d+)', object_type)
        if match:
            width = float(match.group(1))
            height = float(match.group(2))
            return width, height
    return None, None
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
        window_width, window_height = extract_dimensions_from_object_type(window_type)
        has_geometry = False
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, window)
            if geometry:
                has_geometry = True
        except Exception as e:
            print(f"Ошибка при обработке геометрии крыши {window_name}: {e}")

        if (has_geometry):
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
