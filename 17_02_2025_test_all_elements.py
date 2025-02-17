import ifcopenshell
import pandas as pd

# Загрузка IFC-файла
ifc_file = ifcopenshell.open('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')

# Создание списка для хранения данных
data = []

# Перебор всех элементов в IFC-файле
for element in ifc_file.by_type('IfcProduct'):
    element_info = {
        'Type': element.is_a(),
        'GlobalId': element.GlobalId,
        'Name': element.Name if hasattr(element, 'Name') else None,
        'Description': element.Description if hasattr(element, 'Description') else None,
        'Volume': None
    }

    # Проверка наличия атрибута Representation и его значения
    if hasattr(element, 'Representation') and element.Representation is not None:
        for rep in element.Representation.Representations:
            if rep.is_a('IfcShapeRepresentation'):
                for item in rep.Items:
                    if item.is_a('IfcExtrudedAreaSolid'):
                        if hasattr(item, 'SweptArea'):
                            if item.SweptArea.is_a('IfcRectangleProfileDef'):
                                length = item.Depth
                                width = item.SweptArea.XDim
                                height = item.SweptArea.YDim
                                element_info['Volume'] = length * width * height
                            # Добавьте другие типы профилей по необходимости

    data.append(element_info)

# Создание DataFrame
df = pd.DataFrame(data)

# Экспорт в Excel
df.to_excel('volume_statement.xlsx', index=False)

print("Ведомость объемов работ успешно экспортирована в volume_statement.xlsx")