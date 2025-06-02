from web3 import Web3

wallet_address = "0xE4EF95Ed2748Ceb1F659a51C3ffc013a6D7d57d7"
wallet_address = Web3.to_checksum_address(wallet_address)

with open("rpc.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

for line in lines:
    try:
        chain_name, rpc_url = line.split(",")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            print(f"[!] {chain_name}: RPC недоступен по адресу {rpc_url}")
            continue
        
        balance_wei = w3.eth.get_balance(wallet_address)
        balance_eth = w3.from_wei(balance_wei, 'ether')

        print(f"[] {chain_name}: {balance_eth} ETH")
    except Exception as e:
        print(f"[!] {chain_name}: Ошибка при подключении или запросе баланса: {e}")
        
    