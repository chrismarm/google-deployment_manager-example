To start the deployment of the instance

```sh
$ gcloud deployment-manager deployments create exampledeployment --config python/config.yaml
```

To delete the deployment
```sh
gcloud deployment-manager deployments delete exampledeployment
```

### TODOs

* `Jinja` to define resources
* Define other GCP elements like VP, subnets, non-boot disks with size/images, tags for instances, etc
* Deploy on this instance a `Go` RESTful service using `Ansible`

