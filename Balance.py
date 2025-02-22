import requests
import time

# ���������
MAX_REQUESTS = 5  # ������������ ���������� �������� ����� ���������
WAIT_TIME = 60  # ����� �������� (� ��������) ����� ���������� ������������� ���������� ��������

def check_bitcoin_balance(address):
    """Proverka balanca bitcoin-adresa cherez API Blockchain."""
    url = f'https://blockchain.info/q/addressbalance/{address}'  # API ��� ��������� �������
    try:
        response = requests.get(url)
        response.raise_for_status()  # ���������� ���������� ��� ������ HTTP (��������, 404 ��� 500)
        
        balance_satoshi = int(response.text)  # �������� ������ � ������
        balance_btc = balance_satoshi / 100000000  # ������������ � BTC
        return balance_btc
    
    except requests.exceptions.RequestException as e:
        # �������� ������ � ��������
        print(f"Error fetching balance for address {address}: {e}")
        return None

def save_to_file(address, balance):
    """Sohraniaem adresa i balans v fail."""
    with open('Good.txt', 'a') as file:
        file.write(f'{address} {balance:.8f} BTC\n')

def read_addresses_from_file(filename):
    """Chtenie adresov iz faila."""
    try:
        with open(filename, 'r') as file:
            addresses = file.readlines()
        return [address.strip() for address in addresses]  # ������� ������� � ������� ����� ������
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []

def manage_requests_count(request_count):
    """Upravliaet kolichestvom zaprosov i vremenem ozidania."""
    if request_count >= MAX_REQUESTS:
        print(f"Dostignut limit zaprosov ({MAX_REQUESTS}). Wait {WAIT_TIME} sec...")
        time.sleep(WAIT_TIME)  # ������� ����� ������������
        return 0  # ���������� ������� ��������
    return request_count

# ������ ������� �� ����� Address.txt
addresses = read_addresses_from_file('Address.txt')

if not addresses:
    print("No addresses found to check.")
else:
    request_count = 0  # ������� ��������

    # �������� ������� ��� ������� ������
    for address in addresses:
        request_count += 1
        balance = check_bitcoin_balance(address)
        
        if balance is not None and balance > 0:  # ��������� ������ ������ � ������������� ��������
            save_to_file(address, balance)
            print(f"Balance addressa {address}: {balance:.8f} BTC")
        
        # ��������� ����������� ��������
        request_count = manage_requests_count(request_count)
