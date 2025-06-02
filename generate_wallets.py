import csv
import secrets
from mnemonic import Mnemonic                                                      # generate seed frase
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def generate_metamask_wallets(file_name: str, count: int = 1):
    mnemo = Mnemonic("english")
    
    with open(file_name, mode = 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Address", "Private_key", "Seed Phrase"])
        
        for _ in range(count):
            entropy = secrets.token_bytes(16)                                       # 128 бит случайных данных - ентропия
            seed_phrase = mnemo.to_mnemonic(entropy)                                # превращаем байты в сеед фразу
            seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()                 # генерируем сид
            bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            account = bip44_wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
            
            address = account.PublicKey().ToAddress()
            private_key = account.PrivateKey().Raw().ToHex()
            
            writer.writerow([address, private_key, seed_phrase])
            
            print(f"Address: {address}")
            
if __name__ == "__main__":
    generate_metamask_wallets("wallets.csv", 10)