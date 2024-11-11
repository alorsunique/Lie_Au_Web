import os
from pathlib import Path

import pandas as pd


def catalog_create(catalog_file):
    if not catalog_file.exists():
        model_list = []
        dataframe = pd.DataFrame(model_list, columns=['Model', 'Download Status'])
        dataframe.to_excel(catalog_file, sheet_name='Catalog', index=False)


def catalog_read(catalog_file):
    dataframe = pd.read_excel(catalog_file)
    model_dict = dict(zip(dataframe['Model'], dataframe['Download Status']))
    return model_dict


def catalog_show(catalog_file):
    dataframe = pd.read_excel(catalog_file)
    print(dataframe.to_string())


def add_model(catalog_file, model_name, download_status):
    dataframe = pd.read_excel(catalog_file)
    dataframe_list = dataframe.values.tolist()

    if model_name in dataframe['Model'].values:
        print("Model already present")
    else:
        if download_status == 1:
            dataframe_list.append([model_name, 1])
        else:
            dataframe_list.append([model_name, 0])

    dataframe_list = sorted(dataframe_list, key=lambda x: x[0])

    if catalog_file.exists():
        os.remove(catalog_file)

    dataframe = pd.DataFrame(dataframe_list, columns=['Model', 'Download Status'])
    dataframe.to_excel(catalog_file, sheet_name='Catalog', index=False)


def remove_model(catalog_file, model_name):
    dataframe = pd.read_excel(catalog_file)
    dataframe_list = dataframe.values.tolist()
    copy_list = dataframe_list.copy()

    if model_name in dataframe['Model'].values:
        potential_rows = dataframe[dataframe['Model'] == model_name]
        potential_list = potential_rows.values.tolist()

        for entry in potential_list:
            if entry in copy_list:
                dataframe_list.remove(entry)
    else:
        print(f"{model_name} not in database")

    dataframe_list = sorted(dataframe_list, key=lambda x: x[0])

    if catalog_file.exists():
        os.remove(catalog_file)

    dataframe = pd.DataFrame(dataframe_list, columns=['Model', 'Download Status'])
    dataframe.to_excel(catalog_file, sheet_name='Catalog', index=False)


def flip_status(catalog_file, model_name):
    dataframe = pd.read_excel(catalog_file)
    dataframe_list = dataframe.values.tolist()
    copy_list = dataframe_list.copy()

    if model_name in dataframe['Model'].values:
        potential_rows = dataframe[dataframe['Model'] == model_name]
        potential_list = potential_rows.values.tolist()

        if potential_list[0][1] == 1:
            dataframe_list.remove(potential_list[0])
            dataframe_list.append([model_name, 0])
        else:
            dataframe_list.remove(potential_list[0])
            dataframe_list.append([model_name, 1])

    else:
        print(f"{model_name} not in database")

    dataframe_list = sorted(dataframe_list, key=lambda x: x[0])

    if catalog_file.exists():
        os.remove(catalog_file)

    dataframe = pd.DataFrame(dataframe_list, columns=['Model', 'Download Status'])
    dataframe.to_excel(catalog_file, sheet_name='Catalog', index=False)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("beibusosu_resource_path.txt", "r") as beibusosu_resources_text:
        beibusosu_resources_dir = Path(str(beibusosu_resources_text.readline()).replace('"', ''))

    catalog_path = beibusosu_resources_dir / "Catalog.xlsx"

    catalog_create(catalog_path)

    while True:
        catalog_show(catalog_path)

        print("\n--------------------------------\n")

        print("\n0. Exit Loop")
        print("1. Add Model")
        print("2. Remove Model")
        print("3. Flip Status")

        choice = str(input("Choice: "))

        if choice == "0":
            break
        elif choice == "1":
            model_name = str(input("Input Model Name: "))
            add_model(catalog_path, model_name, 0)
        elif choice == "2":
            model_name = str(input("Input Model Name: "))
            remove_model(catalog_path, model_name)
        elif choice == "3":
            model_name = str(input("Input Model Name: "))
            flip_status(catalog_path, model_name)
        else:
            print("Did not catch that")
