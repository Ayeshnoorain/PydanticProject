from pydantic import BaseModel, field_validator
from typing import List
import os
from pathlib import Path

class FileListValidator(BaseModel):
    filenames: List[str]
    base_directory: str

    def validate_files_exist(self):
        for filename in self.filenames:
            full_path = os.path.join(self.base_directory, filename)
            #print(full_path)
            if not os.path.exists(full_path):
                raise ValueError(f"File {full_path} does not exist")

    def validate_filename_convention(self):
        required_prefix = "Current_7_VAS_AreaOfInterest"
        non_conforming_filenames = [
            filename for filename in self.filenames if not filename.startswith(required_prefix)
        ]
        if non_conforming_filenames:
            # Raise an error listing all non-conforming filenames
            raise ValueError(
                f"Files do not follow the required naming convention: {', '.join(non_conforming_filenames)}")



def main(directory_path):
    path = Path(directory_path)
    filenames = [item.name for item in path.iterdir() if item.is_file()]


    try:
        file_list = FileListValidator(filenames=filenames,base_directory=directory_path)
        file_list.validate_files_exist()
        file_list.validate_filename_convention()
        print("Validation passed. All files exist and conform to the naming convention.")
    except ValueError as e:
        print(f"Error {e}")


if __name__ == "__main__":
    directory_path = r'C:\Users\ayesha.noorain\PycharmProjects\PydanticProject\P99704\Logo distinctiveness'
    main(directory_path)
