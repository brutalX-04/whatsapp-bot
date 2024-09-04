import os
from dotenv import load_dotenv

load_dotenv()

def get_value(key):
	value = os.getenv(key)

	return value