# Installation Guide for KeyHunter Framework

This guide provides step-by-step instructions to set up and install the KeyHunter Framework on your system. It is optimized for Kali Linux and other Debian-based distributions, ensuring a smooth and professional deployment.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: KeyHunter Framework is developed with Python 3.8 and later versions.
*   **Git**: For cloning the repository.
*   **Sudo privileges**: The installer script requires `sudo` to install system-level dependencies.

## Step 1: Clone the Repository

First, clone the KeyHunter Framework repository from GitHub to your local machine:

```bash
git clone https://github.com/Panda1847/keyhunter-framework.git
cd keyhunter-framework
```

## Step 2: Run the Installer Script

The repository includes an `install.sh` script that automates the setup process, including installing system dependencies, creating a Python virtual environment, and installing all necessary Python packages.

```bash
chmod +x hybrid_scraper/install.sh
sudo ./hybrid_scraper/install.sh
```

This script will perform the following actions:

1.  Update system package lists.
2.  Install essential system dependencies (e.g., `python3-pip`, `python3-venv`, `git`, `curl`, and browser rendering libraries).
3.  Create a Python virtual environment named `venv` in the project root.
4.  Activate the virtual environment.
5.  Install all required Python packages (`curl_cffi`, `nodriver`, `aiohttp`, `loguru`, `requests`).

## Step 3: Verify Installation

After the installation script completes, you can verify the setup by activating the virtual environment and checking the installed packages:

```bash
source venv/bin/activate
pip list
```

You should see `curl_cffi`, `nodriver`, `loguru`, `aiohttp`, and `requests` among the installed packages.

## Troubleshooting

*   **Permission Denied**: If you encounter a "Permission denied" error when running `install.sh`, ensure you execute it with `sudo` as shown in Step 2.
*   **Python Version**: If you have multiple Python versions, ensure `python3` points to Python 3.8+.
*   **Network Issues**: Proxy fetching might fail if there are network connectivity issues. Ensure your internet connection is stable.
*   **Missing Libraries**: If you encounter errors related to missing shared libraries (e.g., `libnss3.so`), ensure all system dependencies were installed correctly. You might need to manually install them if your system differs from Kali Linux.

For further assistance, please refer to the [KeyHunter Framework GitHub Issues](https://github.com/Panda1847/keyhunter-framework/issues) page.
