### Instance deployment on GCE using Deployment Manager

To start the deployment of the instance with Deployment Manager

```sh
$ gcloud deployment-manager deployments create exampledeployment --config python/config.yaml
# Or with jinja instead of Python
gcloud deployment-manager deployments create exampledeployment --config jinja/config.yaml
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

# If so, now we can tag our instance and filter by that tag
$ gcloud compute instances add-tags exampledeployment-simple-instance --tags ansible
$ ansible -i ansible/inventory/ tag_ansible -m ping

# Now we are ready to run our playbook that will install our app with all its dependencies (Like a Docker image would do)
$ ansible-playbook -v -i ansible/inventory/ ansible/install_app.yaml &
```

The `Ansible` playbook installs Git and Golang, copies the sample app to the remote instance, downloads and installs app dependencies and finally installs and runs the app.


### TODOs

* Define other GCP elements like VP, subnets, non-boot disks with size/images, tags for instances, etc

