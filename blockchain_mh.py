import hashlib, json
from datetime import datetime
import rsa  # Thư viện để mã hóa và ký số

# Class đại diện cho một giao dịch
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = ""

    def sign_transaction(self, private_key):
        data = f"{self.sender}{self.recipient}".encode('utf-8')
        self.signature = rsa.sign(data, private_key, 'SHA-256').hex()

    def verify_transaction(self, public_key):
        data = f"{self.sender}{self.recipient}".encode('utf-8')
        try:
            rsa.verify(data, bytes.fromhex(self.signature), public_key)
            return True
        except:
            return False

# Class Block với các giao dịch
class Block:
    def __init__(self, transactions, index):
        self.index = index
        self.transactions = transactions
        self.prev_hash = ""
        self.nonce = 0
        self.hash = ""
        self.timestamp = str(datetime.now())

# Hàm băm để tính hash cho block
def hash(block):
    data = json.dumps([tx.__dict__ for tx in block.transactions]) + block.prev_hash + str(block.nonce)
    data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

# Class Blockchain để chứa các block
class Blockchain:
    def __init__(self, owner):
        self.owner = owner
        self.chain = []
        self.pending_transactions = []
        block = Block([], 0)  # Genesis block với index 0
        block.hash = hash(block)
        self.chain.append(block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def add_block(self):
        block = Block(self.pending_transactions, len(self.chain))  # Đánh số thứ tự block theo thứ tự trong chain
        block.prev_hash = self.chain[-1].hash
        start = datetime.now()
        while not hash(block).startswith("0000"):  # Tạo một hash với 4 số 0
            block.nonce += 1
            block.hash = hash(block)
        end = datetime.now()
        self.chain.append(block)
        self.pending_transactions = []            

    def get_balance(self, person):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == person:
                    balance -= transaction.amount
                if transaction.recipient == person:
                    balance += transaction.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if current_block.prev_hash != prev_block.hash:
                return False
            if not current_block.hash.startswith("0000"):
                return False
        return True
    


# Khởi tạo cặp khóa RSA cho người dùng
public_key, private_key = rsa.newkeys(512)

# In ra public_key và private_key dưới dạng PEM
print("Public Key:", public_key.save_pkcs1().decode())
print("Private Key:", private_key.save_pkcs1().decode())

# Tạo blockchain và thêm giao dịch
blockchain = Blockchain("Van Nhi")

tx1 = Transaction("Phan Minh Duc", "Van Nhi", 1000)
tx1.sign_transaction(private_key)
if tx1.verify_transaction(public_key):
    blockchain.add_transaction(tx1)

tx2 = Transaction("Van Nhi", "Phan Minh Duc", 500)
tx2.sign_transaction(private_key)
if tx2.verify_transaction(public_key):
    blockchain.add_transaction(tx2)

tx3 = Transaction("Minh Duc", "Van Nhi", 1500)
tx3.sign_transaction(private_key)
if tx3.verify_transaction(public_key):
    blockchain.add_transaction(tx3)

# Thêm block đầu tiên và in thông tin
blockchain.add_block()

# Tạo thêm giao dịch và thêm block thứ hai
tx4 = Transaction("Van Nhi", "Nguyen Van A", 300)
tx4.sign_transaction(private_key)
if tx4.verify_transaction(public_key):
    blockchain.add_transaction(tx4)

tx5 = Transaction("Nguyen Van A", "Van Nhi", 200)
tx5.sign_transaction(private_key)
if tx5.verify_transaction(public_key):
    blockchain.add_transaction(tx5)

blockchain.add_block()

# Tạo thêm giao dịch và thêm block thứ ba
tx6 = Transaction("Van Nhi", "Nguyen Van B", 700)
tx6.sign_transaction(private_key)
if tx6.verify_transaction(public_key):
    blockchain.add_transaction(tx6)

tx7 = Transaction("Nguyen Van B", "Van Nhi", 100)
tx7.sign_transaction(private_key)
if tx7.verify_transaction(public_key):
    blockchain.add_transaction(tx7)

blockchain.add_block()

# Kiểm tra số dư của Van Nhi sau khi thêm các block mới
print("Balance of Van Nhi:", blockchain.get_balance("Van Nhi"))
print("Is blockchain valid?", blockchain.is_chain_valid())

# In chi tiết các block
for i, block in enumerate(blockchain.chain):
    print(f"\nBlock {block.index}:")
    print("Timestamp:", block.timestamp)
    print("Previous Hash:", block.prev_hash)
    print("Hash:", block.hash)
    print("Nonce:", block.nonce)
    print("Transactions:", [tx.__dict__ for tx in block.transactions])


