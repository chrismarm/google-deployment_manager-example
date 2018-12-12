### Instance deployment on GCE using Deployment Manager

To start the deployment of the instance with Deployment Manager

```sh
$ gcloud deployment-manager deployments create exampledeployment --config python/config.yaml
# Or with jinja instead of Python
$ gcloud deployment-manager deployments create exampledeployment --config jinja/config.yaml
```

To delete the deployment
```sh
$ gcloud deployment-manager deployments delete exampledeployment
```

### Installation of a sample Golang app using Ansible

Firstly, we have to create a service account with enough privileges to manage GCE instances and get an email and json file with key, to complete 'inventory/gce.ini' file with those values.

```sh
# In order to create the user and ssh keys, we can run
$ gcloud compute ssh exampledeployment-simple-instance

# Here we can check if we can build a dynamic inventory with Ansible, polling instances in GCE
$ ansible -i ansible/inventory/ all -m ping
# We can also ping filtering by the specified tag
$ ansible -i ansible/inventory/ tag_ansible -m ping

# Now we are ready to run our playbook that will install our app with all its dependencies (Like a Docker image would do)
$ ansible-playbook -v -i ansible/inventory/ ansible/install_app.yaml &
```

The `Ansible` playbook installs Git and Golang, copies the sample app to the remote instance, downloads and installs app dependencies and finally installs and runs the app.

### Golang app to retrieve instance metadata

The app installed is written in Go and it exposes on "instanceIP:8000/metadata" the information retrieved from the instance itself calling `http://metadata.google.internal/computeMetadata/v1`. An example of output:

`
Connection from 88.17.19.235:41420
Project ID: tonal-justice-216711 ( 854286960949 )
Instance metadata:
{
  "attributes": {},
  "cpuPlatform": "Intel Sandy Bridge",
  "description": "",
  "disks": [
    {
      "deviceName": "boot",
      "index": 0,
      "mode": "READ_WRITE",
      "type": "PERSISTENT"
    }
  ],
  "hostname": "exampledeployment-simple-instance.europe-west1-b.c.tonal-justice-216711.internal",
  ...
 `

### TODOs

* Define other GCP elements like VP, subnets, non-boot disks with size/images, tags for instances, etc

