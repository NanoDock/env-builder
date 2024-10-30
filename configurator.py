#!/usr/bin/env python3

import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate NixOS configuration files for development environments.')
    parser.add_argument('-language', '--language', required=True, help='Programming language (e.g., python, nodejs, go, rust)')
    parser.add_argument('-version', '--version', required=True, help='Version of the programming language (e.g., 3.12.2)')
    parser.add_argument('-packages', '--packages', help='Path to a text file listing packages to install')
    args = parser.parse_args()
    return args

def read_packages(packages_file):
    if packages_file and os.path.exists(packages_file):
        with open(packages_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip()]
        return packages
    else:
        return []

def generate_nix_config(args, packages):
    language = args.language.lower()
    version = args.version
    content = ''

    if language == 'python':
        content = generate_python_nix(version, packages)
    elif language == 'nodejs' or language == 'node':
        content = generate_nodejs_nix(version, packages)
    elif language == 'go':
        content = generate_go_nix(version, packages)
    elif language == 'rust':
        content = generate_rust_nix(version, packages)
    # Add more languages here as needed
    else:
        print(f'Language "{language}" is not supported yet.')
        sys.exit(1)
    return content

def generate_python_nix(version, packages):
    python_version_attr = f'python{version.replace(".", "")}'
    # Check if the specified Python version is supported
    supported_versions = ['38', '39', '310', '311', '312']
    if python_version_attr not in [f'python{v}' for v in supported_versions]:
        print(f'Python version {version} is not supported.')
        sys.exit(1)

    pkgs_import = '<nixpkgs>'
    packages_list = ''
    if packages:
        packages_str = ' '.join([f'"{pkg}"' for pkg in packages])
        packages_list = f'[{packages_str}]'
    else:
        packages_list = '[]'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  python = pkgs.{python_version_attr};
in
pkgs.mkShell {{
  buildInputs = [
    (python.withPackages (ps: {packages_list}))
  ];
}}
'''
    return shell_nix

def generate_nodejs_nix(version, packages):
    nodejs_version_attr = f'nodejs-{version}'
    pkgs_import = '<nixpkgs>'
    packages_list = ''
    if packages:
        packages_str = ' '.join([f'"{pkg}"' for pkg in packages])
        packages_list = f'[{packages_str}]'
    else:
        packages_list = '[]'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [
    pkgs.{nodejs_version_attr}
    (pkgs.nodePackages.buildNodePackage {{
      name = "my-node-package";
      packageJson = {{
        name = "my-node-package",
        version = "1.0.0",
        dependencies = (pkgs.lib.fromJSON (pkgs.lib.generators.toJSON {{
          {', '.join([f'"{pkg}": "*" ' for pkg in packages])}
        }}));
      }};
    }})
  ];
}}
'''
    return shell_nix

def generate_go_nix(version, packages):
    go_version_attr = f'go_{version.replace(".", "_")}'
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.{go_version_attr} ];
}}
'''
    return shell_nix

def generate_rust_nix(version, packages):
    rust_channel = f'stable-{version}'
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ (pkgs.rustChannelOf{{ date = "{version}"; channel = "{rust_channel}"; }}.rust) ];
}}
'''
    return shell_nix

def main():
    args = parse_arguments()
    packages = read_packages(args.packages)
    nix_config_content = generate_nix_config(args, packages)

    with open('shell.nix', 'w') as f:
        f.write(nix_config_content)
    print('shell.nix has been generated.')

if __name__ == '__main__':
    main()