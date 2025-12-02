import os
from dotenv import load_dotenv

# Load from root .env
load_dotenv('.env')

threshold = float(os.getenv('CONFIDENCE_THRESHOLD', '0.5'))
print(f'Successfully loaded CONFIDENCE_THRESHOLD from root .env: {threshold}')
print(f'Type: {type(threshold).__name__}')
