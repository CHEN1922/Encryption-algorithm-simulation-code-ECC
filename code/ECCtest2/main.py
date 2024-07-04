import hashlib
import time
import ECC_BCAKA
start=time.perf_counter()
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof_of_work):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof_of_work = proof_of_work
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.previous_hash, self.timestamp, str(self.transactions), self.proof_of_work)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, previous_hash='{self.previous_hash}', timestamp={self.timestamp}, transactions={self.transactions}, proof_of_work={self.proof_of_work}, hash='{self.hash}')"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), [], 0)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        previous_block = self.get_last_block()
        new_block.previous_hash = previous_block.hash
        new_block.proof_of_work = self.calculate_proof_of_work(new_block)
        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)

    def calculate_proof_of_work(self, block):
        nonce = 0
        while not self.is_valid_proof(block, nonce):
            nonce += 1
        return nonce

    def is_valid_proof(self, block, nonce):
        block_string = "{}{}{}{}{}".format(block.index, block.previous_hash, block.timestamp, str(block.transactions), nonce)
        return hashlib.sha256(block_string.encode()).hexdigest().startswith('0')

    def __repr__(self):
        return str(self.chain)

# 模拟SEAF验证请求授权
def SEAF_verify_authorization():
    return True  # 模拟始终授权

def SEAF_U_verify_authorization():
    return True  # 模拟始终授权

# 模拟SEAF接收请求并传递给AUSF验证
def SEAF_receive_request():
    SUCI = "Sample SUCI"
    SNN = "Sample SNN"
    return SUCI, SNN
def SEAF_U_receive_request():
    SUCI = "Sample SUCI"
    SNN = "Sample SNN"
    U="U"
    return SUCI, SNN ,U
# 模拟AUSF验证请求
def AUSF_verify_request(SUCI, SNN):
    return True  # 模拟始终验证通过

def AUSF_U_verify_request(SUCI, SNN,U):
    return True  # 模拟始终验证通过

# 模拟AUSF生成认证向量
def AUSF_generate_authentication_vector():
    return "Sample Authentication Vector"

def AUSF_U_generate_authentication_vector():
    return "Sample Authentication Vector"

# 模拟UE接收认证向量
def UE_receive_authentication_vector(AV):
    pass  # 不需要真正操作

def UE_U_receive_authentication_vector(AV):
    pass  # 不需要真正操作

# 模拟UE计算响应
def UE_compute_response():
    RES = "Sample Response"
    return RES

# 模拟SEAF验证响应
def SEAF_verify_response(RES):
    return True  # 模拟始终验证通过

# 模拟AUSF验证结果
def AUSF_verify_result(RES):
    return True  # 模拟始终验证通过

if __name__ == '__main__':
    # 示例用法
    blockchain = Blockchain()

    # 添加一些交易（模拟无人机注册）
    transactions = ["Transaction 1", "Transaction 2", "Transaction 3"]
    block_to_add = Block(len(blockchain.chain), blockchain.get_last_block().hash, time.time(), transactions, 0)
    blockchain.add_block(block_to_add)

    # 生成并展示公私钥对
    SKUE, PKUE = ECC_BCAKA.generate_keys()
    SKCN, PKCN = ECC_BCAKA.generate_keys()

    # 随机数 RAND
    RAND = 5  # 简化的随机数生成

    # 认证阶段的流程
    # 1. 无人机发送注册请求
    # 模拟发送注册请求后，SEAF接收请求并向AUSF验证
    if SEAF_verify_authorization():
        # 2. SEAF模块接收请求
        # 模拟SEAF接收请求后，将SUCI和SNN传递给AUSF验证
        SUCI, SNN = SEAF_receive_request()
        # 3. AUSF模块验证请求
        if AUSF_verify_request(SUCI, SNN):
            # 4. 认证向量生成
            AV = AUSF_generate_authentication_vector()
            # 5. 无人机接收认证向量
            # 模拟无人机接收认证向量
            UE_receive_authentication_vector(AV)
            # 6. 无人机进行认证响应
            # 模拟无人机进行响应计算
            RES= UE_compute_response()
            # 生成私钥和公钥对


            KCN = ECC_BCAKA.compute_intermediate_key(SKCN, PKUE, RAND)
            KUE = ECC_BCAKA.compute_intermediate_key(SKUE, PKCN, RAND)

            print(f"UE's intermediate key (KUE): {KUE.hex()}")
            print(f"CN's intermediate key (KCN): {KCN.hex()}")

            # 检查 KCN 和 KUE 是否相同
            assert KCN == KUE, "Intermediate keys do not match!"

            print("Intermediate keys match, the authentication can proceed.")
            # 7. SEAF验证响应
            if SEAF_verify_response(RES):
                # 8. AUSF验证结果
                if AUSF_verify_result(RES):
                    print("Authentication successful!")  # 认证成功
                else:
                    print("Authentication failed!")  # 认证失败
            else:
                print("Response verification failed!")  # 响应验证失败
        else:
            print("Request verification failed!")  # 请求验证失败
    else:
        print("Unauthorized access!")  # 未授权访问
    end = time.perf_counter()
    print('程序运行时间为: %s Seconds'%(end-start))
    # 打印区块链
    for block in blockchain.chain:
        print(block)
