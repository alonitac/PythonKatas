import tarfile
import tempfile
import unittest
from datetime import date
from katas.files_backup import files_backup
import os
import shutil


def create_temp_dir_with_content():
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, 'example.txt')
    with open(file_path, 'w') as file:
        file.write('Bla Bla')

    return temp_dir


class TestFilesBackupL1(unittest.TestCase):
    def test_files_backup(self):
        dir_path = create_temp_dir_with_content()
        expected_file_name = f'backup_{os.path.basename(dir_path)}_{date.today()}.tar.gz'
        backup_file_name = files_backup(dir_path)

        # Verify the backup file name
        self.assertEqual(backup_file_name, expected_file_name)

        # Verify the backup file exists
        self.assertTrue(os.path.exists(backup_file_name))

        with tarfile.open(backup_file_name, 'r:gz') as tar:
            extracted_content = tar.extractfile('example.txt').read().decode('utf-8')

        with open(os.path.join(dir_path, 'example.txt'), 'r') as original_file:
            original_content = original_file.read()

        self.assertEqual(extracted_content, original_content)

        os.remove(backup_file_name)
        shutil.rmtree(dir_path)


if __name__ == '__main__':
    unittest.main()
