from cryptography.fernet import Fernet
import os

DATA_FILE = "wallets.csv"
KEY_FILE = "secret.key"
ENCRYPTED_FILE = "wallets.csv.enc"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_out:
        key_out.write(key)
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError(f"Key file {KEY_FILE} not found.")
    with open(KEY_FILE, "rb") as key_in:
        return key_in.read()


def secure_delete(file_path, passes=3):
    # перезаписываем файл 3жды со случайными данными и удаляем
    if os.path.exists(file_path):
        length = os.path.getsize(file_path)
        with open(file_path, "ba+", buffering=0) as delfile:
            for _ in range(passes):
                delfile.seek(0)
                delfile.write(os.urandom(length))
        os.remove(file_path)


def encrypt_file():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Data file {DATA_FILE} not found.")

    key = generate_key()
    fernet = Fernet(key)

    with open(DATA_FILE, "rb") as file_in:
        original = file_in.read()

    encrypted = fernet.encrypt(original)

    with open(ENCRYPTED_FILE, "wb") as file_out:
        file_out.write(encrypted)

    secure_delete(DATA_FILE)


def decrypt_file():
    if not os.path.exists(ENCRYPTED_FILE):
        raise FileNotFoundError(f"Encrypted file {ENCRYPTED_FILE} not found.")

    key = load_key()
    fernet = Fernet(key)

    with open(ENCRYPTED_FILE, "rb") as file_in:
        encrypted = file_in.read()

    decrypted = fernet.decrypt(encrypted)

    output_file = DATA_FILE.replace(".csv", "_decrypted.csv")

    with open(output_file, "wb") as file_out:
        file_out.write(decrypted)


if __name__ == "__main__":
    action = input("What do you want to do? [e]ncrypt or [d]ecrypt: ").strip().lower()
    if action == "e":
        encrypt_file()
    elif action == "d":
        decrypt_file()
    else:
        print('[-] Invalid command. Use "e" to encrypt or "d" to decrypt.')
