from web3 import Web3
import json

def get_rpc_url(chain_name, rpc_file='rpc.txt'):
    with open(rpc_file, 'r') as f:
        for line in f:
            if line.strip():
                name, url = line.strip().split(',')
                if name.lower() == chain_name.lower():
                    return url
    raise ValueError(f'RPC URL for "{chain_name}" not found.')

def get_token_balance(rpc_url, token_address_raw, wallet_address_raw, abi_path='erc20.json'):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    token_address = Web3.to_checksum_address(token_address_raw)
    wallet_address = Web3.to_checksum_address(wallet_address_raw)

    with open(abi_path, 'r') as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=token_address, abi=abi)
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    raw_balance = contract.functions.balanceOf(wallet_address).call()
    human_balance = raw_balance / (10 ** decimals)

    return {
        'token_name': name,
        'token_symbol': symbol,
        'decimals': decimals,
        'wallet': wallet_address,
        'raw_balance': raw_balance,
        'human_balance': human_balance
    }

if __name__ == '__main__':
    rpc_url = get_rpc_url('optimism')
    token_address = '0x4200000000000000000000000000000000000042'

    with open('evm.txt', 'r') as f:
        wallets = [line.strip() for line in f if line.strip()]

    for wallet in wallets:
        data = get_token_balance(rpc_url, token_address, wallet)
        print(f"Wallet: {data['wallet']} - Raw: {data['raw_balance']} - Balance: {data['human_balance']} {data['token_symbol']}")