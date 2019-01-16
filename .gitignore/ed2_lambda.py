import os
import boto3

def get_ec2_instances(region,project,state):
    ec2_instances = []
    
    ec2 = boto3.resource('ec2',region_name=region)

    filters = [
            {
             'Name': 'tag:project',
            'Values': [project]   
            },
            {'Name': 'instance_state_name',
            'Values': [state]}
        ]

    for instance in ec2_instances.filters(filters=filters):
        ip = instance.private_ip_address
    state_name = instance_.state['Name']
    print("ip:{}, state:{}", format(ip,state_name))
    ec2_instances.append(instance)    
    
    return ec2_instances

def start_ec2_instances(region,project,state):
    instances_to_stop = get_ec2_instances(region,project,'stopped')
    instance_state_changed = 0
    for instance in instances_to_stop:
        instance.start()
    instance_state_changed += 1 
    return instance_state_changed

def stop_ec2_instances(region,project,state):
    instances_to_stop = get_ec2_instances(region,project,'running')
    instance_state_changed = 0
    for instance in instances_to_stop:
        instance.stop()
    instance_state_changed += 1 
    return instance_state_changed

def lambda_handler(event,context):
    region = os.getenv('REGION','US-EAST-1')
    project = os.getenv('PROJECT','DEMO')

    instance_state_changed = 0
    if(event.get('action') =='start'):
        instance_state_changed = start_ec2_instances(region,project)
    elif(event.get('action') == 'stop'):
        instance_state_changed = stop_ec2_instances(region,project)

    return instance_state_changed
