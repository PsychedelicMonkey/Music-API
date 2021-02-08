import os

f = open('.env', 'w')
f.write('FLASK_APP=main.py\n')
f.write('FLASK_DEBUG=1\n')
f.write(f'SECRET_KEY={os.urandom(32).hex()}\n')
f.write(f'JWT_SECRET_KEY={os.urandom(32).hex()}\n')
f.close()

if not os.path.exists('uploads'):
    os.mkdir('uploads')