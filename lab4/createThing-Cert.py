################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string
import os
import shutil
################################################### Parameters for Thing
thingArn = ''
thingId = ''
thingName = ''
defaultPolicyName = 'My_Iot_Policy'
###################################################

def createThing():
  global thingClient
  print('Creating Thing...', thingName)
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  # print(data)
  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
        createCertificate()

def createCertificate():
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
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
	
	if os.path.exists(device_DirPath):
		shutil.rmtree(device_DirPath)
	os.mkdir(device_DirPath)
							
	with open(public_Path, 'w') as outfile:
			outfile.write(PublicKey)
	with open(private_Path, 'w') as outfile:
			outfile.write(PrivateKey)
	with open(cert_path, 'w') as outfile:
			outfile.write(certificatePem)

	response = thingClient.attach_policy(
			policyName = defaultPolicyName,
			target = certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName = thingName,
			principal = certificateArn
	)

thingClient = boto3.client('iot')
DirPath = "./device_list"
if os.path.exists(DirPath):
    shutil.rmtree(DirPath)
os.mkdir(DirPath)

device_num = 5
for i in range(device_num):
    thingName = 'device_' + str(i)

    device_DirPath = os.path.join(DirPath, thingName)
    cert_path = os.path.join(device_DirPath, "{}.cert.pem".format(thingName))
    private_Path = os.path.join(device_DirPath, "{}.private.key".format(thingName))
    public_Path = os.path.join(device_DirPath, "{}.public.key".format(thingName))

    createThing()