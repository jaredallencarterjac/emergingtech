import argparse

def deploy_model(model_path):
    print(f'deploy model {model_path}...')
    
if__name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model')
    args = parser.parse_args()
    deploy_model(args.model)