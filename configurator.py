#!/usr/bin/env python3

import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate NixOS configuration files and Dockerfile for development environments.')
    parser.add_argument('-language', '--language', required=True, help='Programming language (e.g., python, nodejs, deno, go, rust, swift, java, c++, dart, r)')
    parser.add_argument('-version', '--version', help='Version of the programming language (e.g., 3.12.2). If not specified, the latest version is used.')
    parser.add_argument('-packages', '--packages', help='Path to a text file listing packages to install')
    parser.add_argument('-framework', '--framework', help='Specific framework to include (e.g., nextjs)')
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
    framework = args.framework.lower() if args.framework else None
    content = ''

    if language == 'python':
        content = generate_python_nix(version, packages)
    elif language == 'nodejs' or language == 'node':
        content = generate_nodejs_nix(version, packages, framework)
    elif language == 'deno':
        content = generate_deno_nix(version)
    elif language == 'go':
        content = generate_go_nix(version)
    elif language == 'rust':
        content = generate_rust_nix(version)
    # Add other languages as needed
    else:
        print(f'Language "{language}" is not supported yet.')
        sys.exit(1)
    return content

def generate_python_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    packages_list = ''
    if packages:
        packages_str = ' '.join([f'"{pkg}"' for pkg in packages])
        packages_list = f'[{packages_str}]'
    else:
        packages_list = '[]'

    if version:
        python_version_attr = f'python{version.replace(".", "")}'
        python_definition = f'python = pkgs.{python_version_attr} or (throw "Python version {version} not found in nixpkgs");'
    else:
        python_definition = 'python = pkgs.python3;  # Latest Python 3 version'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  {python_definition}
in
pkgs.mkShell {{
  buildInputs = [
    (python.withPackages (ps: {packages_list}))
  ];
}}
'''
    return shell_nix

def generate_nodejs_nix(version, packages, framework):
    pkgs_import = '<nixpkgs>'

    if version:
        nodejs_version_attr = f'nodejs-{version}'
        node_definition = f'node = pkgs.{nodejs_version_attr} or (throw "Node.js version {version} not found in nixpkgs");'
    else:
        node_definition = 'node = pkgs.nodejs;  # Latest Node.js version'

    packages_list = ''
    if packages:
        packages_list = ' '.join(packages)
    if framework:
        packages_list += f' {framework}'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  {node_definition}
in
pkgs.mkShell {{
  buildInputs = [ node ];

  shellHook = ''
    mkdir -p node_env
    cd node_env
    npm init -y
    npm install {packages_list.strip()}
  '';
}}
'''
    return shell_nix

def generate_deno_nix(version):
    pkgs_import = '<nixpkgs>'
    if version:
        deno_definition = f'deno = pkgs.deno_{version.replace(".", "_")} or (throw "Deno version {version} not found in nixpkgs");'
    else:
        deno_definition = 'deno = pkgs.deno;  # Latest Deno version'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  {deno_definition}
in
pkgs.mkShell {{
  buildInputs = [ deno ];
}}
'''
    return shell_nix

def generate_go_nix(version):
    pkgs_import = '<nixpkgs>'
    if version:
        go_version_attr = f'go_{version.replace(".", "_")}'
        go_definition = f'go = pkgs.{go_version_attr} or (throw "Go version {version} not found in nixpkgs");'
    else:
        go_definition = 'go = pkgs.go;  # Latest Go version'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  {go_definition}
in
pkgs.mkShell {{
  buildInputs = [ go ];
}}
'''
    return shell_nix

def generate_rust_nix(version):
    pkgs_import = '<nixpkgs>'
    if version:
        rust_definition = f'rust = pkgs.rustup.override {{ defaultToolchain = "{version}"; }};'
    else:
        rust_definition = 'rust = pkgs.rustup;  # Latest Rust version'

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  {rust_definition}
in
pkgs.mkShell {{
  buildInputs = [ rust ];
}}
'''
    return shell_nix

def generate_dockerfile():
    dockerfile_content = '''
# Use the official Nix image
FROM nixos/nix

# Set the working directory
WORKDIR /app

# Copy the shell.nix file into the container
COPY shell.nix .

# Run nix-shell to set up the environment
RUN nix-shell --run "exit"

# Set the default command to enter the nix-shell
CMD ["nix-shell"]
'''
    return dockerfile_content

def main():
    args = parse_arguments()
    packages = read_packages(args.packages)
    nix_config_content = generate_nix_config(args, packages)

    with open('shell.nix', 'w') as f:
        f.write(nix_config_content)
    print('shell.nix has been generated.')

    dockerfile_content = generate_dockerfile()
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    print('Dockerfile has been generated.')

if __name__ == '__main__':
    main()