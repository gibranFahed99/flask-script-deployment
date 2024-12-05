from flask import Flask,request
import requests
import json
import os

app = Flask(__name__)

PORTAINER_URL = os.getenv('PORTAINER_URL')
PORTAINER_USERNAME = os.getenv('PORTAINER_USERNAME')
PORTAINER_PASSWORD = os.getenv('PORTAINER_PASSWORD')

def get_portainer_token():
    login_url = f"{PORTAINER_URL}/auth"
    payload = {"username":PORTAINER_USERNAME,"password":PORTAINER_PASSWORD} 
    response = requests.post(login_url,json=payload)
    return response.json().get("jwt")


def redeploy_stack(jwt_token,stack_id,endpoint_id):
    deploy_url = f"{PORTAINER_URL}/stacks/{stack_id}/git/redeploy?endpointId={endpoint_id}"
    headers = {'Authorization':f"Bearer {jwt_token}",'content-type':'application/json'}
    response = requests.put(deploy_url,headers=headers,json={
        "pullImage": True
    })

    requests.post(f"{PORTAINER_URL}/endpoints/{endpoint_id}/docker/images/prune",headers=headers,json={})

    return response.status_code,response.text

@app.route("/webhook",methods=['post'])
def webhook():
    data  = request.json
    print(f"received webhook {json.dumps(data,indent=4)}")

    if 'push_data' in data and data['push_data']['tag'] == 'latest':
        jwt_token = get_portainer_token()
        status_code,response = redeploy_stack(jwt_token,18,2)
        if status_code == 200:
            return 'Stack redeployed successfully', 200
        else:
            return f"Failed to redeploy stack: {response}", 500
    
    if 'push_data' in data and data['push_data']['tag'] == 'licensePos':
            jwt_token = get_portainer_token()
            status_code,response = redeploy_stack(jwt_token,28,2)
            if status_code == 200:
                return 'Stack redeployed successfully', 200
    
    if 'push_data' in data and data['push_data']['tag'] == 'wasteManagementSaudi':
        jwt_token = get_portainer_token()    
        status_code,response = redeploy_stack(jwt_token,29,2)
        if status_code == 200:
            return 'Stack redeployed successfully', 200

    if 'push_data' in data and data['push_data']['tag'] == 'wasteManagement':
        jwt_token = get_portainer_token()    
        status_code,response = redeploy_stack(jwt_token,30,2)
        if status_code == 200:
            return 'Stack redeployed successfully', 200

    if 'push_data' in data and data['push_data']['tag'] == 'selfComplaince':
        jwt_token = get_portainer_token()    
        status_code,response = redeploy_stack(jwt_token,31,2)
        if status_code == 200:
            return 'Stack redeployed successfully', 200

    if 'push_data' in data and data['push_data']['tag'] == 'selfComplainceMidd':
        jwt_token = get_portainer_token()    
        status_code,response = redeploy_stack(jwt_token,32,2)
        if status_code == 200:
            return 'Stack redeployed successfully', 200
      
    return 'No action taken', 400

if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=5000)
