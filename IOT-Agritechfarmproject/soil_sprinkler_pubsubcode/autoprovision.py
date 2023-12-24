################################################### Connecting to AWS
import boto3
import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
thingName = 'sensor_data'
thingName2 = 'sprinkler'
thingTypeName = 'agritech-sensors'
thingGroupName = 'devices'
thingClient = boto3.client('iot', region_name='us-east-1')
#defaultPolicyName = 'GGTest_Group_Core-policy'


###################################################

def createThing():
    global thingClient
    print("thingName",thingName)
    #z = thingClient.list_things()
    #y = aws_iot_core_get_policies()
    #print(z)
    #y = z['things']


    #print(y)
    #print(x)
    a = thingClient.create_thing_type(thingTypeName = thingTypeName)
    #print(a)
    print(thingTypeName)
    b = thingClient.create_thing_group(thingGroupName = thingGroupName)
    #print(b)
    for item in b:
        if item == 'thingGroupArn':
            thingGroupArn = b['thingGroupArn']

    print(thingGroupName)
    #if thingName not in y:
    thingResponse = thingClient.create_thing(
        thingName=thingName, thingTypeName = thingTypeName
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    print(data)
    for element in data:
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
            c = createCertificate()
            print(c)
            _create_and_attach_policy(thingName,c, region_name="us-east-1")

    response6 = thingClient.add_thing_to_thing_group(
        thingGroupName= thingGroupName,
        thingGroupArn= thingGroupArn,
        thingName= thingName,
        thingArn= thingArn,
        overrideDynamicGroups=True | False
    )

    thingResponse2 = thingClient.create_thing(
        thingName=thingName2, thingTypeName=thingTypeName
    )
    data2 = json.loads(json.dumps(thingResponse2, sort_keys=False, indent=4))
    print(data)
    for element2 in data2:
        if element2 == 'thingArn':
            thingArn2 = data2['thingArn']
        elif element2 == 'thingId':
            thingId = data2['thingId']
            c = createCertificate2()
            print(c)
            _create_and_attach_policy(thingName2, c, region_name="us-east-1")

    response7 = thingClient.add_thing_to_thing_group(
        thingGroupName=thingGroupName,
        thingGroupArn=thingGroupArn,
        thingName=thingName2,
        thingArn=thingArn2,
        overrideDynamicGroups=True | False
    )
def createCertificate():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive=True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']

    with open('soilsensorpublic.key', 'w') as outfile:
        outfile.write(PublicKey)
    with open('soilsensorprivate.key', 'w') as outfile:
        outfile.write(PrivateKey)
    with open('soilsensorcert.pem', 'w') as outfile:
        outfile.write(certificatePem)

    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )

    return certificateArn
def createCertificate2():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive=True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']

    with open('sprinklerpublic.key', 'w') as outfile:
        outfile.write(PublicKey)
    with open('sprinklerprivate.key', 'w') as outfile:
        outfile.write(PrivateKey)
    with open('sprinklercert.pem', 'w') as outfile:
        outfile.write(certificatePem)

    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )

    return certificateArn


def _create_and_attach_policy(thingName, certificateArn, region_name='us-east-1'):
        # Create and attach to the principal/certificate the minimal action
        # privileges Thing policy that allows publish and subscribe
        print("test1")
        tp = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": "iot:*",
                "Resource": [
                    "arn:aws:iot:{0}:*:*".format(region_name)
                ]
            }]
        }

        policy_name = thingName+'policy'.format(thingName)
        print(policy_name)
        policy = json.dumps(tp)
        # log.debug('[_create_and_attach_policy] soilsensorpolicy'.format(policy))
        p = thingClient.create_policy(
            policyName=policy_name,
            policyDocument=policy
        )
        # log.debug("[_create_and_attach_policy] Created Soilsensorpolicy".format(
        # p['policyName']))
        print(p)
        data1 = json.loads(json.dumps(p, sort_keys=False, indent=4))
        print(data1)
        print("test2")
        thingClient.attach_principal_policy(
            policyName=policy_name, principal=certificateArn)
        # log.debug("[_create_and_attach_policy] Attached {0} to {1}".format(
        # policy_name, thing_cert_arn))
        print("test3")
        return p['policyName'], p['policyArn']

    #response = thingClient.attach_policy(
     #   policyName=policy_name,
     #   target=certificateArn
    #)

