import unittest
import os
from main import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("config.ini")
        self.emulator.fs_root = "test_virtual_fs"
        os.makedirs(self.emulator.fs_root, exist_ok=True)
        os.makedirs(os.path.join(self.emulator.fs_root, "dir1"), exist_ok=True)
        os.makedirs(os.path.join(self.emulator.fs_root, "dir2"), exist_ok=True)
        with open(os.path.join(os.path.join(self.emulator.fs_root, "dir2"), "file2.txt"), "w") as f:
            f.write("test file")
        with open(os.path.join(self.emulator.fs_root, "file1.txt"), "w") as f:
            f.write("test file")

    def tearDown(self):
        for root, dirs, files in os.walk(self.emulator.fs_root, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.emulator.fs_root)

    def test_ls(self):
        self.emulator.current_dir = ""
        self.emulator.ls()

    def test_cd_valid_directory(self):
        self.emulator.cd(["dir1"])
        self.assertEqual(self.emulator.current_dir, "dir1")

    def test_cd_invalid_directory(self):
        self.emulator.cd(["invalid_dir"])
        self.assertEqual(self.emulator.current_dir, "")

    def test_pwd_root(self):
        self.emulator.current_dir = ""
        self.emulator.pwd()

    def test_pwd_subdir(self):
        self.emulator.current_dir = "dir1"
        self.emulator.pwd()

    def test_rmdir_empty_directory(self):
        self.emulator.rmdir(["dir1"])
        self.assertFalse(os.path.exists(os.path.join(self.emulator.fs_root, "dir1")))

    def test_rmdir_non_empty_directory(self):
        self.emulator.rmdir(["dir2"])
        self.assertTrue(os.path.exists(os.path.join(self.emulator.fs_root, "dir2")))

    def test_rmdir_invalid_directory(self):
        self.emulator.rmdir(["nonexistent"])

if __name__ == '__main__':
    unittest.main()
