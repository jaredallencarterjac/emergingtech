#execute this script, then navigate to Kubeflow Central dash->Pipelines->Experiments
from kubernetes import client as k8s_client
import kfp.dsl as dsl
import json
from string import Template

@dsl.pipeline(
   name='Boston Housing Pipeline',
   description='An example pipeline that trains and logs a regression model.'
)


def pipeline_demo(
    
    ):
     
#each component is defined as a function that returns an object of type ContainerOP, which comes from kfp sdk
    preprocess_op = dsl.ContainerOp(
        name='Preprocess Data',
        image='ghcr.io/jaredallencarterjac/preprocess:latest',
        arguments=[],
#/app is coming from where we placed the npy files in the WORKDIR of the Dockerfile
        file_outputs={
            'x_train': '/app/x_train.npy',
            'x_test': '/app/x_test.npy',
            'y_train': '/app/y_train.npy',
            'y_test': '/app/y_test.npy',
        } 
    )
    preprocess_op.set_image_pull_policy("Always")
    
    
    train_op = dsl.ContainerOp(
        name='Train Model',
        image='ghcr.io/jaredallencarterjac/train:latest',
        arguments=[
            '--x_train', dsl.InputArgumentPath(preprocess_op.outputs['x_train']),
            '--y_train', dsl.InputArgumentPath(preprocess_op.outputs['y_train'])
        ],
#model trained and packaged to send to test step
        file_outputs={
            'model': '/app/model.pkl'
        } ,
    )
    
    train_op.set_image_pull_policy("Always")

    
    test_op = dsl.ContainerOp(
        name='Test Model',
        image='ghcr.io/jaredallencarterjac/test:latest',
        arguments=[
            '--x_test', dsl.InputArgumentPath(preprocess_op.outputs['x_test']),
            '--y_test', dsl.InputArgumentPath(preprocess_op.outputs['y_test']),
            '--model', dsl.InputArgumentPath(train_op.outputs['model'])
        ],
        file_outputs={
            'mean_squared_error': '/app/output.txt'
        },  
    )
    
    test_op.set_image_pull_policy("Always") 

#applys to pipeline as whole
#dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="dockersecret")])
   
    
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_demo, __file__ + '.zip')
