import ifcopenshell


def calculate_stair_volume(ifc_file_path):
    model = ifcopenshell.open(ifc_file_path)
    stairs = model.by_type("IfcStair")
    total_volume = 0

    for stair in stairs:
        volume = 0

        # Проверяем, есть ли объем в количественных свойствах
        if stair.IsDefinedBy:
            for relation in stair.IsDefinedBy:
                if hasattr(relation, 'RelatingPropertyDefinition'):
                    prop_def = relation.RelatingPropertyDefinition
                    if prop_def.is_a("IfcElementQuantity"):
                        for quantity in prop_def.Quantities:
                            if quantity.is_a("IfcQuantityVolume"):
                                volume = quantity.VolumeValue

        # Если объем не найден в свойствах, пробуем вычислить из геометрии
        if volume == 0 and hasattr(stair, 'Representation') and stair.Representation:
            for rep in stair.Representation.Representations:
                if rep.is_a("IfcShapeRepresentation"):
                    for item in rep.Items:
                        if item.is_a("IfcExtrudedAreaSolid"):
                            base_area = item.SweptArea.AreaValue if hasattr(item.SweptArea, 'AreaValue') else 0
                            height = item.Depth if hasattr(item, 'Depth') else 0
                            volume = base_area * height
                        elif item.is_a("IfcBooleanResult"):
                            print(f"{stair.Name} использует булеву операцию, объем может быть сложнее.")
                        elif item.is_a("IfcMappedItem"):
                            print(f"{stair.Name} использует IfcMappedItem, возможно дублирование геометрии.")
                        elif item.is_a("IfcSolidModel"):
                            print(f"{stair.Name} представлена как SolidModel, попробуйте другое ПО для анализа.")

        print(f"Лестница {stair.Name}: объем = {volume} м³")
        total_volume += volume

    print(f"Общий объем всех лестниц: {total_volume} м³")
    return total_volume


# Укажите путь к вашему IFC файлу
ifc_file_path = ('TIM-analytic_tools_MGUU_VC_cource-main/DataExamples/AR_WIP_348_ALL_KI_SP_R21_отсоединено_ifc_4.ifc')
calculate_stair_volume(ifc_file_path)
