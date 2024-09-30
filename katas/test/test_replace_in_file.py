import os
import subprocess
import tempfile
import unittest
import katas.replace_in_file as m


class TestReplaceInFileL1(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'Hello, old world!')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_main_content_replacement(self):
        module_abs_path = os.path.abspath(m.__file__)
        script_command = f"python {module_abs_path} {self.temp_file.name} old new"
        subprocess.run(script_command, shell=True, check=True)

        with open(self.temp_file.name, 'r') as file:
            modified_content = file.read()

        self.assertEqual(modified_content, 'Hello, new world!')


if __name__ == '__main__':
    unittest.main()
