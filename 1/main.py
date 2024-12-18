import os
import zipfile
import configparser


class ShellEmulator:
    def __init__(self, config_path):
        self.fs_archive = None
        self.hostname = None
        self.username = None
        self.load_config(config_path)
        self.current_dir = ""
        self.fs_root = "virtual_fs"

    def load_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        self.username = config.get("Settings", "username")
        self.hostname = config.get("Settings", "hostname")
        self.fs_archive = config.get("Settings", "fs_archive")

    def extract_fs(self):
        with zipfile.ZipFile(self.fs_archive, 'r') as zip_ref:
            zip_ref.extractall(self.fs_root)

    def run(self):
        self.extract_fs()
        while True:
            cmd = input(
                f"{self.username}@{self.hostname}:{'/' if not self.current_dir else '/' + self.current_dir}$ ").strip()
            if cmd == "exit":
                break
            self.execute_command(cmd)

    def execute_command(self, cmd):
        parts = cmd.split()
        if not parts:
            return
        command, *args = parts

        if command == "ls":
            self.ls()
        elif command == "cd":
            self.cd(args)
        elif command == "pwd":
            self.pwd()
        elif command == "rmdir":
            self.rmdir(args)
        else:
            print(f"Unknown command: {command}")

    def ls(self):
        path = os.path.join(self.fs_root, self.current_dir)
        try:
            for entry in os.listdir(path):
                print(entry)
        except FileNotFoundError:
            print("Directory not found.")

    def cd(self, args):
        if not args:
            print("cd: missing operand")
            return
        new_dir = os.path.normpath(os.path.join(self.current_dir, args[0]))
        path = os.path.join(self.fs_root, new_dir)

        abs_path = os.path.abspath(path)
        abs_fs_root = os.path.abspath(self.fs_root)
        if not abs_path.startswith(abs_fs_root):
            self.current_dir = ""
            return

        if os.path.isdir(path):
            relative_path = os.path.relpath(path, self.fs_root)
            self.current_dir = "" if relative_path == "." else relative_path
        else:
            print(f"cd: {args[0]}: No such file or directory")

    def pwd(self):
        print(f"/{self.current_dir}" if self.current_dir else "/")

    def rmdir(self, args):
        if not args:
            print("rmdir: missing operand")
            return
        path = os.path.join(self.fs_root, self.current_dir, args[0])
        try:
            os.rmdir(path)
        except FileNotFoundError:
            print(f"rmdir: {args[0]}: No such file or directory")
        except OSError:
            print(f"rmdir: {args[0]}: Directory not empty or other error")


if __name__ == "__main__":
    emulator = ShellEmulator("config.ini")
    emulator.run()
