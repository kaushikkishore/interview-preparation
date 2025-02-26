import os


def create_folder_structure():
    base_path = "dsa_preparation"

    # Main topic folders
    main_folders = [
        "01_arrays_and_strings",
        "02_linked_lists",
        "03_stacks_and_queues",
        "04_trees",
        "05_graphs",
        "06_hash_tables",
        "07_sorting_and_searching",
        "08_dynamic_programming",
        "09_greedy_algorithms",
        "10_backtracking",
        "11_advanced_topics",
    ]

    # Create base directory
    os.makedirs(base_path, exist_ok=True)

    # Create main folders
    for folder in main_folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Create README.md in each folder
        with open(os.path.join(folder_path, "README.md"), "w") as f:
            f.write(f"# {folder.split('_', 1)[1].replace('_', ' ').title()}\n\n")
            f.write("## Problems and Solutions\n\n")


if __name__ == "__main__":
    create_folder_structure()
