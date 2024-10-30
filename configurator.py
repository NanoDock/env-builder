#!/usr/bin/env python3

import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate NixOS configuration files for development environments.')
    parser.add_argument('-language', '--language', required=True, help='Programming language (e.g., python, nodejs, deno, go, rust, swift, java, c++, dart, r)')
    parser.add_argument('-version', '--version', required=True, help='Version of the programming language (e.g., 3.12.2)')
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
    elif language == 'bun':
        content = generate_bun_nix(version, packages)
    elif language == 'go':
        content = generate_go_nix(version)
    elif language == 'rust':
        content = generate_rust_nix(version)
    elif language == 'r':
        content = generate_r_nix(version, packages)
    elif language == 'java':
        content = generate_java_nix(version, packages)
    elif language == 'swift':
        content = generate_swift_nix(version, packages)
    elif language == 'c++' or language == 'cpp':
        content = generate_cpp_nix(version, packages)
    elif language == 'dart':
        content = generate_dart_nix(version, packages)
    else:
        print(f'Language "{language}" is not supported yet.')
        sys.exit(1)
    return content

def generate_python_nix(version, packages):
    python_version_attr = f'python{version.replace(".", "")}'
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

def generate_nodejs_nix(version, packages, framework):
    nodejs_version_attr = f'nodejs-{version}'
    pkgs_import = '<nixpkgs>'

    packages_list = ''
    if packages:
        packages_list = ' '.join([f'ps."{pkg}"' for pkg in packages])
    else:
        packages_list = ''

    framework_dependency = ''
    if framework:
        # For example, Next.js is installed via npm
        if framework.lower() == 'nextjs' or framework.lower() == 'next':
            framework_dependency = 'ps.next'
        else:
            framework_dependency = f'ps.{framework.lower()}'

    if framework_dependency:
        packages_list = f'{packages_list} {framework_dependency}'.strip()

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

let
  nodePackages = pkgs.{nodejs_version_attr}.packages;
in
pkgs.mkShell {{
  buildInputs = [
    pkgs.{nodejs_version_attr}
    (nodePackages.buildNodePackage {{
      name = "my-node-package";
      src = null;
      pkgJson = {{
        dependencies = {{
          {', '.join([f'"{pkg}": "*"' for pkg in packages])}
        }};
      }};
    }})
  ];
}}
'''
    return shell_nix

def generate_deno_nix(version):
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [
    pkgs.deno
  ];

  DENOVER = "{version}";
}}
'''
    return shell_nix

def generate_bun_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    packages_list = ''
    if packages:
        packages_list = ' '.join([f'"{pkg}"' for pkg in packages])

    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [
    pkgs.bun
  ];

  shellHook = ''
    bun install {packages_list}
  '';
}}
'''
    return shell_nix

def generate_go_nix(version):
    go_version_attr = f'go_{version.replace(".", "_")}'
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.{go_version_attr} ];
}}
'''
    return shell_nix

def generate_rust_nix(version):
    rust_channel = f'stable-{version}'
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ (pkgs.rustChannelOf {{ channel = "{rust_channel}"; }}).rust ];
}}
'''
    return shell_nix

def generate_r_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    packages_list = ''
    if packages:
        packages_list = ' '.join([f'ps.{pkg}' for pkg in packages])
    else:
        packages_list = ''
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [
    pkgs.R
  ];
}}
'''
    return shell_nix

def generate_java_nix(version, packages):
    java_version_attr = f'jdk{version.replace(".", "")}'
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.{java_version_attr} ];
}}
'''
    return shell_nix

def generate_swift_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.swift ];
}}
'''
    return shell_nix

def generate_cpp_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.gcc pkgs.make ];
}}
'''
    return shell_nix

def generate_dart_nix(version, packages):
    pkgs_import = '<nixpkgs>'
    shell_nix = f'''
{{ pkgs ? import {pkgs_import} {{}} }}:

pkgs.mkShell {{
  buildInputs = [ pkgs.dart ];
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
