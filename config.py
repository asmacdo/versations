import os
import yaml

def load_config_from_env():
   required_conf = {
      "user_id": "MATRIX_USERNAME",
      "device_id": "MATRIX_DEVICE_ID",
      "password": "MATRIX_PASSWORD",
      "homeserver": "MATRIX_HOST",
      "room_id": "MATRIX_ROOM_ID",
      "store_path": "MATRIX_STORE_PATH",
   }

   config = {}
   for key, env_var in required_conf.items():
      value = os.environ.get(env_var)
      config[key] = value

   return config
