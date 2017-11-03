import hashlib
import uuid
salt = uuid.uuid4().hex
algorithm = 'sha512'
#password = 'bob1pass'

def hashPassword(password):
    m = hashlib.new(algorithm)
    m.update(salt + password)
    password_hash = m.hexdigest()
    
    connectedPassword = "$".join([algorithm, salt, password_hash])

    print connectedPassword
    
    return connectedPassword

def hashPasswordWithSalt(password, salt):
    m = hashlib.new(algorithm)
    m.update(salt + password)
    password_hash = m.hexdigest()
    
    connectedPassword = "$".join([algorithm, salt, password_hash])

    print connectedPassword
    
    return connectedPassword    

def getSalt(hashPassword):
    #if re.match("^[A-Za-z0-9_-]*$", str):
    salt = hashPassword[7:39]
    return salt