import requests
import time

# Параметры
MAX_REQUESTS = 5  # Максимальное количество запросов перед ожиданием
WAIT_TIME = 60  # Время ожидания (в секундах) после достижения максимального количества запросов

def check_bitcoin_balance(address):
    """Proverka balanca bitcoin-adresa cherez API Blockchain."""
    url = f'https://blockchain.info/q/addressbalance/{address}'  # API для получения баланса
    try:
        response = requests.get(url)
        response.raise_for_status()  # Генерирует исключение для ошибок HTTP (например, 404 или 500)
        
        balance_satoshi = int(response.text)  # Получаем баланс в сатоши
        balance_btc = balance_satoshi / 100000000  # Конвертируем в BTC
        return balance_btc
    
    except requests.exceptions.RequestException as e:
        # Логируем ошибку с запросом
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
        return [address.strip() for address in addresses]  # Убираем пробелы и символы новой строки
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []

def manage_requests_count(request_count):
    """Upravliaet kolichestvom zaprosov i vremenem ozidania."""
    if request_count >= MAX_REQUESTS:
        print(f"Dostignut limit zaprosov ({MAX_REQUESTS}). Wait {WAIT_TIME} sec...")
        time.sleep(WAIT_TIME)  # Ожидаем перед продолжением
        return 0  # Сбрасываем счетчик запросов
    return request_count

# Чтение адресов из файла Address.txt
addresses = read_addresses_from_file('Address.txt')

if not addresses:
    print("No addresses found to check.")
else:
    request_count = 0  # Счетчик запросов

    # Проверка баланса для каждого адреса
    for address in addresses:
        request_count += 1
        balance = check_bitcoin_balance(address)
        
        if balance is not None and balance > 0:  # Сохраняем только адреса с положительным балансом
            save_to_file(address, balance)
            print(f"Balance addressa {address}: {balance:.8f} BTC")
        
        # Управляем количеством запросов
        request_count = manage_requests_count(request_count)
