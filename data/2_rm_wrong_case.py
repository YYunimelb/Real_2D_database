import json
import os
import pandas as pd
import re
import math


def formula_test(json_path = 'layered_materials.json'):
    def parse_formula(formula):
        elements_and_counts = re.findall('([A-Z][a-z]*)(\d*)', formula)
        return {element: int(count) if count else 1 for element, count in elements_and_counts}
    def read_formula(path = "POSCAR"):
        with open(path) as f:
            lines = f.readlines()
            elements = lines[5].split()
            number = lines[6].split()
            formula = ""
            for i, element in enumerate(elements):
                formula +=elements[i]
                formula +=number[i]
            return formula


    # 先将json文件读入为一个Python对象
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 提取所需的信息
    filtered_data = []
    wrong_data = []
    i = 0
    other_case = []
    for entry in data:
        i += 1
        formula = entry.get('formula')
        initial_3D_formula = entry.get('initial_3D_formula')
        if not initial_3D_formula:
            initial_3D_formula = entry.get('initial_3D_bulk_formula')

        if not formula or not initial_3D_formula:
            path = f"3D_structure/POSCAR{entry['ID']}"
            if os.path.exists(path):
                initial_3D_formula = read_formula(path =path )
            else:
                continue

        formula_dict = parse_formula(formula)
        initial_3D_formula_dict = parse_formula(initial_3D_formula)

        # 判断元素数量是否为倍数关系
        ratios = []

        if set(formula_dict.keys()) != set(initial_3D_formula_dict.keys()):
            wrong_data.append(entry)
            continue  # 如果元素种类不一样，则跳过此项
        else:
            for element, count in formula_dict.items():
                if element not in initial_3D_formula_dict:
                    wrong_data.append(entry)
                    break
                ratio = initial_3D_formula_dict[element] / count
                ratios.append(ratio)
            else:  # 如果没有提前结束循环
                # 判断所有元素的比例是否接近
                if all(math.isclose(ratios[0], ratio, rel_tol=1e-6) for ratio in ratios):
                    filtered_data.append(entry)
                else:
                    wrong_data.append(entry)

    # 将提取的信息保存到一个新的json文件
    with open('pass_formula_2.json', 'w') as f:
        json.dump(filtered_data, f, indent=4)

    with open('wrong_formula.json', 'w') as f:
        json.dump(wrong_data, f, indent=4)

    print(f"pass_formula: {len(filtered_data)}")
    print(f"wrong_formula: {len(wrong_data)}")
    print(f"no_formula: {len(other_case)}")
    print(f"sum = {i}")

formula_test(json_path = 'with_structure_1.json')





