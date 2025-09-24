"""
- From folder "metadata_PEP"  extract _GSE.soft and _GSM.soft
- Create separate metadata JSON files for document and entity node
- Use domain-specific metadata format of file, if available, else fill backup metadata schema and add uncovered entries ("data/extracted_data/metadata/")
"""

from language_model.chat_client_factory import client_selector
from utils.helper import save_json, find_docs_in_folder


def extract_metadata(metadata_dir, data_dir, output_path):
    print(output_path)
    documents = find_docs_in_folder(metadata_dir, data_dir)
    dataset_counter = 1
    sample_counter = 1
    for i, doc in enumerate(documents):
        response = client_selector("metadata_extraction", doc)
        # Save the schema
        if response:
            try:
                if response.get("dataset"):
                    if isinstance(response.get("dataset"), list):
                        data = response.get("dataset")[0]
                    else:
                        data = response.get("dataset")
                    save_json(
                        f"{output_path}/dataset_{dataset_counter}.json",
                        data,
                    )
                    dataset_counter += 1
                if response.get("samples"):
                    if isinstance(response.get("samples"), list):
                        data = response.get("samples")[0]
                    else:
                        data = response.get("samples")
                    save_json(
                        f"{output_path}/sample_{sample_counter}.json",
                        data,
                    )
                    sample_counter += 1
                else:
                    print("Wrong format:", response)
            except Exception as e:
                print("Error in create_initial_schema:", e)
