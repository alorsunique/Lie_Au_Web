# Catalog for beibusosu
# Creates the Excel file to store the dataframe

import os
import time
from pathlib import Path

import pandas as pd


# Creates the catalog
def catalog_create(catalog_file):
    if not catalog_file.exists():
        model_list = []
        df = pd.DataFrame(model_list, columns=['Model', 'Download Status'])
        df.to_excel(catalog_file, sheet_name='Catalog', index=False)


def catalog_read(catalog_file):
    df = pd.read_excel(catalog_file)
    model_dict = dict(zip(df['Model'], df['Download Status']))
    return model_dict


# Shows the catalog
def catalog_show(catalog_file):
    df = pd.read_excel(catalog_file)
    print(df.to_string())


# Adds model to the catalog
def add_model(catalog_file, model_name, download_status):
    df = pd.read_excel(catalog_file)
    df_list = df.values.tolist()

    # Model is added here
    if model_name in df['Model'].values:
        print("Model already present")
    else:
        df_list.append([model_name, download_status])

    df_list = sorted(df_list, key=lambda x: x[0])

    # Removes the catalog file for the new update
    if catalog_file.exists():
        os.remove(catalog_file)

    df = pd.DataFrame(df_list, columns=['Model', 'Download Status'])
    df.to_excel(catalog_file, sheet_name='Catalog', index=False)


# Removes model from the catalog
def remove_model(catalog_file, model_name):
    df = pd.read_excel(catalog_file)
    df_list = df.values.tolist()
    reference_list = df_list.copy()

    if model_name in df['Model'].values:
        potential_rows = df[df['Model'] == model_name]
        potential_list = potential_rows.values.tolist()

        # Model is removed here
        for entry in potential_list:
            if entry in reference_list:
                df_list.remove(entry)
    else:
        print(f"{model_name} not in database")

    df_list = sorted(df_list, key=lambda x: x[0])

    # Removes the catalog file for the new update
    if catalog_file.exists():
        os.remove(catalog_file)

    df = pd.DataFrame(df_list, columns=['Model', 'Download Status'])
    df.to_excel(catalog_file, sheet_name='Catalog', index=False)


# Flips the status of a model
def flip_status(catalog_file, model_name):
    df = pd.read_excel(catalog_file)
    df_list = df.values.tolist()

    if model_name in df['Model'].values:
        potential_rows = df[df['Model'] == model_name]
        potential_list = potential_rows.values.tolist()

        # Model is flipped here
        if potential_list[0][1] == 1:
            df_list.remove(potential_list[0])
            df_list.append([model_name, 0])
        else:
            df_list.remove(potential_list[0])
            df_list.append([model_name, 1])

    else:
        print(f"{model_name} not in database")

    df_list = sorted(df_list, key=lambda x: x[0])

    # Removes the catalog file for the new update
    if catalog_file.exists():
        os.remove(catalog_file)

    df = pd.DataFrame(df_list, columns=['Model', 'Download Status'])
    df.to_excel(catalog_file, sheet_name='Catalog', index=False)


# Clears extra models
def clear_extra(catalog_file, beibusosu_resources_dir):
    df = pd.read_excel(catalog_file)
    folder_model_list = []

    # Takes note of the folders present
    for entry in beibusosu_resources_dir.iterdir():
        if entry.is_dir():
            folder_model_list.append(entry.name)

    drop_index_list = []

    # Takes note of the index of the rows to be dropped
    for index, row in df.iterrows():
        current_model = row["Model"]
        if current_model not in folder_model_list:
            drop_index_list.append(index)

    # Extra models are dropped here
    df = df.drop(drop_index_list)

    # Removes the catalog file for the new update
    if catalog_file.exists():
        os.remove(catalog_file)

    df = pd.DataFrame(df, columns=['Model', 'Download Status'])
    df.to_excel(catalog_file, sheet_name='Catalog', index=False)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    print(f"Project directory: {project_dir}")

    os.chdir(project_dir)

    with open("Beibusosu_Resource_Path.txt", "r") as beibusosu_resources_text:
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
        print("4. Clear Extra")

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
        elif choice == "4":
            clear_extra(catalog_path, beibusosu_resources_dir)
        else:
            print("Did not catch that")
        time.sleep(1)
