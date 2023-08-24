from subprocess import call
from threading import Thread

def remove_cache():
	call("rm -rf __pycache__", shell=True)
	call("rm -rf database/__pycache__", shell=True)
	call("rm -rf handlers/__pycache__", shell=True)
	call("rm -rf inline/__pycache__", shell=True)
	call("rm -rf middlewares/__pycache__", shell=True)
	print("Кэш успешно очищен!")
	
def delete_cache():
	rm_cache = Thread(target=remove_cache)
	rm_cache.start()