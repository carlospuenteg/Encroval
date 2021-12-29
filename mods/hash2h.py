import hashlib

def h2h(hash,iters):
    for x in range(0,iters):
        hash = hashlib.sha512(hash.encode()).hexdigest()
    return hash