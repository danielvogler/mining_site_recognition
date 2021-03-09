from sentinelhub import SHConfig

config = SHConfig()

config.instance_id = '{instance_id}'
config.sh_client_id = '{sh_client_id}'
config.sh_client_secret = '{sh_client_secret}'

config.save()
