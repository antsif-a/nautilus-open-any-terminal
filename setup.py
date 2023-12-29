#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install as _install

PO_FILES = "locale/*/LC_MESSAGES/nautilus-open-any-terminal.po"


def create_mo_files():
    mo_files = []
    prefix = Path("src")

    for po_path in Path(prefix).glob(PO_FILES):
        mo = po_path.with_suffix(".mo")

        subprocess.run(["msgfmt", "-o", str(mo), str(po_path)], check=True)
        mo_files.append(str(mo.relative_to(prefix)))

    return mo_files


class InstallCommand(_install):
    def run(self):
        _install.run(self)

        # Install Nautilus Python extension
        print("== Installing Nautilus Python extension")
        src_file = Path("src/nautilus_open_any_terminal.py")
        dst_dir = Path(self.install_data) / "share/nautilus-python/extensions"
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_file = dst_dir / src_file.name
        self.copy_file(src_file, dst_file)
        print("== Done!")

        # Install language files
        print("== Installing language files")
        for po_path in Path("nautilus_open_any_terminal").glob(PO_FILES):
            src_file = po_path.with_suffix(".mo")
            original_folder = src_file.relative_to("nautilus_open_any_terminal").parent
            dst_dir = Path(self.install_data) / "share" / original_folder
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst_file = dst_dir / src_file.name
            self.copy_file(src_file, dst_file)
        print("== Done!")

        # Install GSettings Schema
        print("== Installing GSettings Schema")
        src_file = Path("./src/schemas/com.github.stunkymonkey.nautilus-open-any-terminal.gschema.xml")
        dst_dir = Path(self.install_data) / "share/glib-2.0/schemas"
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_file = dst_dir / src_file.name
        self.copy_file(src_file, dst_file)
        print(f"== Done! Run 'glib-compile-schemas {dst_dir}' to compile the schema.")


setup(
    package_data={"nautilus-open-any-terminal": create_mo_files()},
)
