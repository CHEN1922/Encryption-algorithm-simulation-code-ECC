import ecdsa
import hashlib

# 椭圆曲线参数
curve = ecdsa.curves.SECP256k1
generator = curve.generator

# 生成私钥和公钥
def generate_keys():
    num = [];
    n = 3500
    i = 2
    for i in range(2, n):
        j = 2
        for j in range(2, i):
            if (i % j == 0):
                break
        else:
            num.append(i)
    private_key = ecdsa.util.randrange(curve.order)
    public_key = private_key * generator
    return private_key, public_key

# 计算中间密钥 KCN 和 KUE
def compute_intermediate_key(private_key, public_key_other, RAND):
    shared_secret = private_key * public_key_other
    return hashlib.sha256(str(shared_secret.x() * RAND).encode()).digest()

# # 生成私钥和公钥对
# SKUE, PKUE = generate_keys()
# SKCN, PKCN = generate_keys()
#
# # 随机数 RAND
# RAND = 5  # 简化的随机数生成
#
# KCN = compute_intermediate_key(SKCN, PKUE, RAND)
# KUE = compute_intermediate_key(SKUE, PKCN, RAND)
#
# print(f"UE's intermediate key (KUE): {KUE.hex()}")
# print(f"CN's intermediate key (KCN): {KCN.hex()}")
#
# # 检查 KCN 和 KUE 是否相同
# assert KCN == KUE, "Intermediate keys do not match!"
#
# print("Intermediate keys match, the authentication can proceed.")
