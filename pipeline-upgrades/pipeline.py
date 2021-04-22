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
    
    
    train_op_1 = dsl.ContainerOp(
        name='Train_2 Model',
        image='ghcr.io/jaredallencarterjac/train:latest',
        arguments=[
            '--x_train', dsl.InputArgumentPath(preprocess_op.outputs['x_train']),
            '--y_train', dsl.InputArgumentPath(preprocess_op.outputs['y_train'])
        ],
#model trained and packaged to send to test step
        file_outputs={
            'model_1': '/app/model_1.pkl'
        } ,
    )
    
    
    train_op_1.set_image_pull_policy("Always")
    
    train_op_2 = dsl.ContainerOp(
        name='Train_2 Model',
        image='ghcr.io/jaredallencarterjac/train:latest',
        arguments=[
            '--x_train', dsl.InputArgumentPath(preprocess_op.outputs['x_train']),
            '--y_train', dsl.InputArgumentPath(preprocess_op.outputs['y_train'])
        ],
#model trained and packaged to send to test step
        file_outputs={
            'model_2': '/app/model_2.pkl'
        } ,
    )

    train_op_2.set_image_pull_policy("Always")
    
    test_op_1 = dsl.ContainerOp(
        name='Test_1 Model',
        image='ghcr.io/jaredallencarterjac/test:latest',
        arguments=[
            '--x_test', dsl.InputArgumentPath(preprocess_op.outputs['x_test']),
            '--y_test', dsl.InputArgumentPath(preprocess_op.outputs['y_test']),
            '--model_1', dsl.InputArgumentPath(train_op_1.outputs['model_1'])
        ],
        file_outputs={
            'mean_squared_error': '/app/output_1.txt'
        },  
    )
    
    test_op_1.set_image_pull_policy("Always") 
    
    test_op_2 = dsl.ContainerOp(
        name='Test_2 Model',
        image='ghcr.io/jaredallencarterjac/test:latest',
        arguments=[
            '--x_test', dsl.InputArgumentPath(preprocess_op.outputs['x_test']),
            '--y_test', dsl.InputArgumentPath(preprocess_op.outputs['y_test']),
            '--model_2', dsl.InputArgumentPath(train_op_2.outputs['model_2'])
        ],
        file_outputs={
            'mean_squared_error': '/app/output_2.txt'
        },  
    )
    
    test_op_2.set_image_pull_policy("Always") 

#applys to pipeline as whole
#dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="dockersecret")])
   
    
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_demo, __file__ + '.zip')
