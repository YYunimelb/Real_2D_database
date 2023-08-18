import json
def json2POSCAR(json,header ="fa9f8c81-3c69-42fd-b5bf-abf658a90d95",path = "POSCAR"):
    cell = json["data"]['attributes']["cell"]
    sites = json["data"]['attributes']["sites"]
    atoms = {}
    for site in sites:
        element = site["kind_name"]
        position = site["position"]
        if element not in atoms:
            atoms[element] = []
        atoms[element].append(position)

    # 生成POSCAR格式字符串
    poscar = f"{header}\n1.0\n"
    for row in cell:
        poscar += f"{row[0]:.10f} {row[1]:.10f} {row[2]:.10f}\n"
    elements = " ".join(atoms.keys())
    elements_count = " ".join(str(len(atoms[element])) for element in atoms.keys())
    poscar += f"{elements}\n{elements_count}\nCartesian\n"

    for element in atoms.keys():
        for position in atoms[element]:
            poscar += f"{position[0]:.10f} {position[1]:.10f} {position[2]:.10f}\n"

    # 输出POSCAR格式字符串
    with open(path,"w") as f:
        f.write(poscar)
        f.close()


def get_json_from_unique_name(unique_name = "79638adc-333a-4152-9b87-a3158a5ee06e"):
    import requests
    url1 = f"https://aiida.materialscloud.org/mc2d/api/v4/nodes/{unique_name}/contents/attributes"
    res1 = requests.get(url=url1)
    data1 = res1.json()
    return data1

def add_outer_atoms(json_path = 'initial.json'):
    with_structure_1 = []
    with open(json_path, 'r') as f:
        data = json.load(f)
    for i, entry in enumerate(data):
        # get 3D unique name
        relaxed_3D_bulk_structure = entry.get('relaxed_3D_bulk_structure_df2')
        if not relaxed_3D_bulk_structure:
            relaxed_3D_bulk_structure = entry.get('relaxed_3D_bulk_structure_revpbe')
        if not relaxed_3D_bulk_structure:
            relaxed_3D_bulk_structure = entry.get('relaxed_3D_bulk_structure_rvv10')
        if not relaxed_3D_bulk_structure:
            print("No 3D structures")

        # get 2D unique name
        structure_unrelaxed_2D = entry.get("structure_unrelaxed_2D")
        if not structure_unrelaxed_2D:
            structure_unrelaxed_2D = entry.get("structure_2D")

        if not structure_unrelaxed_2D:
            print("No 2D structures")
        if structure_unrelaxed_2D and relaxed_3D_bulk_structure:
        # get the structure and save as POSCAR
            data = get_json_from_unique_name(unique_name=relaxed_3D_bulk_structure)
            json2POSCAR(data, header=relaxed_3D_bulk_structure, path=f"3D_structure/POSCAR{i}")

            data = get_json_from_unique_name(unique_name=structure_unrelaxed_2D)
            json2POSCAR(data, header=structure_unrelaxed_2D, path=f"2D_structure/POSCAR{i}")

        entry["ID"] = f"{i}"
        with_structure_1.append(entry)
        print(i)

        with open('with_structure_1.json', 'w') as f:
            json.dump(with_structure_1, f, indent=4)


add_outer_atoms(json_path = 'initial.json')


