# env-builder
Script that builds nix-os config files automatically using arugments to setup a dev environment.

# Development Environment Setup with Nix and Docker

This guide provides instructions on how to use the `configurator.py` script to generate Nix configuration files and a Dockerfile for setting up a development environment tailored to your programming language and package requirements. It also explains how to build and run the Docker container using the generated files.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone or Download the Repository](#1-clone-or-download-the-repository)
  - [2. Prepare the Packages File (Optional)](#2-prepare-the-packages-file-optional)
- [Using `configurator.py`](#using-configuratorpy)
  - [Command-Line Arguments](#command-line-arguments)
  - [Supported Languages](#supported-languages)
  - [Examples](#examples)
    - [Python Example](#python-example)
    - [Node.js Example](#nodejs-example)
    - [Go Example](#go-example)
    - [Rust Example](#rust-example)
- [Building and Running the Docker Container](#building-and-running-the-docker-container)
  - [1. Build the Docker Image](#1-build-the-docker-image)
  - [2. Run the Docker Container](#2-run-the-docker-container)
- [Edge Cases and Troubleshooting](#edge-cases-and-troubleshooting)
- [Additional Notes](#additional-notes)

---

## Introduction

The `configurator.py` script automates the generation of Nix configuration files (`shell.nix`) and a `Dockerfile` for creating a reproducible development environment. By specifying the programming language, version, and packages/frameworks, you can quickly set up a containerized environment tailored to your needs.

## Prerequisites

- **Python 3.x**: To run the `configurator.py` script.
- **Docker**: To build and run the Docker container.
- **Git** (optional): To clone the repository.

## Getting Started

### 1. Clone or Download the Repository

Clone the repository or download the `configurator.py` script to your local machine.

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

*Alternatively, you can directly download the `configurator.py` script and place it in a directory of your choice.*

### 2. Prepare the Packages File (Optional)

If you have specific packages or dependencies to include, create a text file listing them, one per line.

**Example: `packages.txt`**

```
numpy
pandas
scipy
```

## Using `configurator.py`

The `configurator.py` script generates the `shell.nix` and `Dockerfile` based on your specifications.

### Command-Line Arguments

Run the script using the following syntax:

```bash
python configurator.py -language LANGUAGE [-version VERSION] [-packages PACKAGES_FILE] [-framework FRAMEWORK]
```

**Arguments:**

- `-language` or `--language` (required): The programming language for the environment.

- `-version` or `--version` (optional): The version of the programming language. If not specified, the latest version is used.

- `-packages` or `--packages` (optional): Path to a text file listing packages to install.

- `-framework` or `--framework` (optional): A specific framework to include (e.g., `nextjs`).

### Supported Languages

The script currently supports the following languages:

- Python
- Node.js
- Deno
- Go
- Rust

*You can extend the script to support additional languages as needed.*

### Examples

#### Python Example

**Command:**

```bash
python configurator.py -language python -version 3.10 -packages packages.txt
```

- **Language:** Python
- **Version:** 3.10
- **Packages:** Listed in `packages.txt`

**Explanation:**

- Generates a `shell.nix` file that sets up a Python 3.10 environment with the specified packages.
- Creates a `Dockerfile` that uses the `shell.nix` to build the environment.

#### Node.js Example

**Command:**

```bash
python configurator.py -language nodejs -version 14 -framework express -packages packages.txt
```

- **Language:** Node.js
- **Version:** 14
- **Framework:** Express
- **Packages:** Listed in `packages.txt`

**Explanation:**

- Sets up a Node.js environment with version 14, including Express and other packages.
- The `shell.nix` file includes the necessary configurations for Node.js.

#### Go Example

**Command:**

```bash
python configurator.py -language go
```

- **Language:** Go
- **Version:** Latest (since `-version` is not specified)

**Explanation:**

- Generates a `shell.nix` for the latest version of Go.
- Useful when you want the most recent stable release.

#### Rust Example

**Command:**

```bash
python configurator.py -language rust -version 1.72.0
```

- **Language:** Rust
- **Version:** 1.72.0

**Explanation:**

- Sets up Rust with the specified version.
- Uses `rustup` to manage the Rust toolchain.

## Building and Running the Docker Container

After generating the `shell.nix` and `Dockerfile`, you can build and run the Docker container.

### 1. Build the Docker Image

**Command:**

```bash
docker build -t my-environment .
```

- **`-t my-environment`**: Tags the image with the name `my-environment`.
- **`.`**: Specifies the build context is the current directory.

**Explanation:**

- Docker reads the `Dockerfile` and builds the image accordingly.
- The image includes the environment configured in the `shell.nix` file.

### 2. Run the Docker Container

**Command:**

```bash
docker run -it my-environment
```

- **`-it`**: Runs the container in interactive mode with a pseudo-TTY.
- **`my-environment`**: The name of the image to run.

**Explanation:**

- Starts the container and drops you into a shell.
- The environment is set up according to your specifications.

**Optional: Mounting Volumes**

If you want to access files from your host machine within the container, use the `-v` option.

```bash
docker run -it -v "$(pwd)":/app my-environment
```

- Mounts the current directory into the `/app` directory inside the container.

## Edge Cases and Troubleshooting

- **Unsupported Language:**

  - If you specify a language not supported by the script, it will display an error message.
  - **Solution:** Ensure you're using one of the supported languages or extend the script.

- **Version Not Found:**

  - If the specified version is not available in Nixpkgs, the build might fail.
  - **Solution:** Check the available versions in Nixpkgs or omit the version to use the latest.

- **Package Installation Issues:**

  - For some languages, package management may not be handled by Nix.
  - **Solution:** You might need to adjust the `shell.nix` file or manage packages within the container using the language's package manager.

- **Docker Build Fails:**

  - Errors during `docker build` could be due to syntax errors in `shell.nix` or issues with the Dockerfile.
  - **Solution:** Review the error messages, check the generated files for typos or incorrect configurations.

## Additional Notes

- **Customizing the Docker Image Name:**

  - In the `docker build` and `docker run` commands, you can replace `my-environment` with a name of your choice.

- **Extending Language Support:**

  - The `configurator.py` script can be extended by adding functions for additional languages following the existing patterns.

- **Modifying the Dockerfile:**

  - The generated `Dockerfile` uses the Nix image and sets up the environment using `nix-shell`.
  - If you need additional customization (e.g., installing system packages), you can manually edit the Dockerfile.

- **Using the Environment:**

  - Once inside the container, you can verify the installed language and version:

    ```bash
    # For Python
    python --version

    # For Node.js
    node --version

    # For Go
    go version

    # For Rust
    rustc --version
    ```

- **Exiting the Container:**

  - To exit the container shell, type `exit` or press `Ctrl+D`.

---

**Example Workflow:**

1. **Prepare `packages.txt` (optional):**

   ```
   numpy
   pandas
   ```

2. **Run the `configurator.py` script:**

   ```bash
   python configurator.py -language python -version 3.10 -packages packages.txt
   ```

3. **Build the Docker image:**

   ```bash
   docker build -t python-env .
   ```

4. **Run the Docker container:**

   ```bash
   docker run -it python-env
   ```

5. **Inside the container, verify the environment:**

   ```bash
   python --version
   python -c "import numpy; import pandas; print('Packages imported successfully.')"
   ```

6. **Start developing your application within the container.**
