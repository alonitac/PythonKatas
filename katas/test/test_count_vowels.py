import os
import subprocess
import tempfile
import unittest
import katas.count_vowels as m

module_abs_path = os.path.abspath(m.__file__)


class TestCountVowelsL2(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'Hello world!')
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_count_from_string(self):
        script_command = f"python {module_abs_path} --string 'Hello world!'"
        process = subprocess.run(script_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.stdout.decode().strip()
        self.assertEqual(result, '3')

    def test_count_from_file(self):
        script_command = f"python {module_abs_path} --file {self.temp_file.name}"
        process = subprocess.run(script_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.stdout.decode().strip()
        self.assertEqual(result, '3')

    def test_count_from_url(self):
        script_command = f"python {module_abs_path} -u https://raw.githubusercontent.com/openai/openai-python/release-v0.28.1/LICENSE"
        process = subprocess.run(script_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = process.stdout.decode().strip()
        self.assertEqual(result, '333')

    def test_invalid_url(self):
        script_command = f"python {module_abs_path} -u https://!!$%#$%&&(&*)(*$%@!%#^&*(**(&.com"
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.run(script_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(context.exception.returncode, 1)

    def test_multiple_flags(self):
        script_command = f"python {module_abs_path} --file {self.temp_file.name} --string 'Hello world!'"
        with self.assertRaises(subprocess.CalledProcessError) as context:
            subprocess.run(script_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(context.exception.returncode, 1)


if __name__ == '__main__':
    unittest.main()
