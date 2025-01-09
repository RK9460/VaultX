# Password Manager

## Overview
This is a secure password manager that allows users to store their passwords safely by creating a master password that is hashed. The application provides features like password encryption, password sharing, strong password generation with AI suggestions, and the ability to recover passwords using security questions.

## Features
- **Master Password**: Users create a master password, which is hashed for security.
- **Password Storage**: Store multiple passwords securely with associated website names and usernames.
- **Password Encryption**: All passwords are encrypted to ensure privacy.
- **Security Questions**: Users can set security questions during the initial setup for password recovery.
- **Password Sharing**: Share passwords with others securely.
- **AI-Based Password Generation**: AI suggests strong passwords for users to enhance security.
- **Password Recovery**: If the master password is forgotten, users can recover it using the security questions.
- **Modern GUI**: The password manager has a clean, user-friendly interface.
- **Password Visibility**: Passwords are shown as asterisks (hidden text) when entered for security.
- **Authentication**: Users must enter the master password before accessing stored passwords.

## Installation

To use this password manager, you can clone this repository and run the code locally:

### Prerequisites
- Python 3.x
- Tkinter (for GUI)
- OpenSSL (for encryption)

### Steps
1. Clone the repository:

   ```bash
   git clone https://github.com/RK9460/VaultX.git
   cd VaultX

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

3. Run the application:

    ```bash
    python password_manager.py

## Usage
**Creating a Master Password**
1. Upon running the application, you'll be prompted to create a master password.
2. After setting the master password, you’ll be asked to input security questions for password recovery.

**Storing passwords**
1. After setting up the master password, you can start storing passwords by entering the website name, username, and password.
2. Each password will be encrypted and saved securely.

**Viewing Stored Passwords**
1. To view stored passwords, you must first authenticate by entering your master password.
2. Passwords will be displayed as asterisks when entered for privacy.

**AI-Based Password Generation**
1. You can generate strong passwords using the AI-based suggestion feature when creating a new password.

## Authors
- Rahul Kala -  Security contributions and development 
- Ravinder Singh - Contributions to AI-based password generation

