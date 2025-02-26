import ifcopenshell
import ifcopenshell.geom
import re

# Загрузка IFC файла
ifc_file = ifcopenshell.open('КолдинТЭ_2-2_revit.ifc')
# ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')
ifc_file = ifcopenshell.open('Renga.ifc')


def extract_dimensions_from_object_type(object_type):
    if object_type:
        # Используем регулярное выражение для поиска размеров
        match = re.search(r'(\d+)\s*[xX*]\s*(\d+)', object_type)
        if match:
            width = float(match.group(1))
            height = float(match.group(2))
            return width, height
    return None, None


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
        # Извлечение размеров двери (ширина и высота) из ObjectType
        door_width, door_height = extract_dimensions_from_object_type(door_type)
        # Проверка наличия геометрии
        has_geometry = False
        settings = ifcopenshell.geom.settings()
        try:
            geometry = ifcopenshell.geom.create_shape(settings, door)
            if geometry:
                has_geometry = True
        except Exception as e:
            print(f"Ошибка при обработке геометрии двери {door_name}: {e}")
        if (door_width!=None or door_height!=None):
            doors_info.append({
                'Name': door_name,
                'GlobalId': door_global_id,
                'Type': door_type,
                'Description': door_description,
                'Width': door_width,
                'Height': door_height,
                'HasGeometry': has_geometry
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
        print(f"  Ширина: {door['Width']} мм" if door['Width'] is not None else "  Ширина: N/A")
        print(f"  Высота: {door['Height']} мм" if door['Height'] is not None else "  Высота: N/A")
        print(f"  Наличие геометрии: {'Да' if door['HasGeometry'] else 'Нет'}")
else:
    print("Двери не найдены.")