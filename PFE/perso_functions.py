import yaml

def update_from_yaml(self, config_file, which):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        for group, params in config.items():
            if isinstance(params, dict):
                # Handle grouped parameters
                for key, value in params.items():
                    if group == which:
                        setattr(self, f"{key}", value)
                        print(f'{key}:\t{value}' )
                    elif group == 'all':
                        setattr(self,f'{key}', value)
            else:
                # Handle non-grouped parameters
                setattr(self, group, params)

