**Jenkins pipeline in Kubernetes cluster.**

1. Create repository in github, configure ssh keys for cloning and pushing files, clone it to the local PC.
2. Create vpc with 2 public and 2 private subnets, NAT gateway (regional) and Internet gateway, 2 routing tables.
![private_subnet](images/img.png)
![public_subnet](images/img_1.png)
3. Create EKS cluster: custom configuration, only private subnets to place ENIs in - so cluster's traffic stays in private network within the vpc.
4. Create node group with 2 nodes - one for each private subnet
![node_groups](images/img_2.png)
5. To allow managing the cluster from a terminal run: 
    aws eks update-kubeconfig --name <cluster-name> --region <region> 
6. Create EFS in the cluster's vpc (for persistent storage for jenkins)
7. Deploy EFS storage driver: 
    kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
8. Create efs storage class file (for dynamic provisioning) and apply it: 
    kubectl apply -f efs-storage-class.yaml 9
9. Create Persistent Volume Claim and apply it:
    kubectl apply -f efs-pvc.yaml
10. For creating and mounting volumes, nodes' role must contain this policy: AmazonEFSCSIDriverPolicy
11. Create a namespace devops(for jenkins), build-env (for building image) and prod-env (for python app):
     kubectl create namespace devops
     kubectl create namespace build-env
     kubectl create namespace prod-env
     Check:
![get_namespaces](images/img_3.png)
12. Create Jenkins Deployment and service in devops namespace, apply them and check:
![jenkins_deployment_service](images/img_4.png)
13. Create python app Deployment and service in prov-env namespace, apply them and check as in example above
14. Add tags to subnets so EKS can know where to place load balancers:
    kubernetes.io/cluster/cluster-name = shared - tag private and public subnets
    kubernetes.io/role/elb = 1 - tag public subnets
15. Create ingress rule yaml for each service (Jenkins and Weather app)
16. Apply them:
    kubectl apply -f jenkins-ingress.yaml
    kubectl apply -f weather-ingress.yaml
17. Using aws documentation, install eksctl, helm CLI
    Install role so ingress controller could provision an ALB dynamically
    Create a service account and map it to created role, so it could reach aws CLI.
    Using Helm, install AWS load balancer controller in the particular cluster.

    Docs url: https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html
    Secure ALB with TLS using AWS certificate and domain (I used Cloudflare for domain)
![cloudflare_dns_record](images/img_6.png)
18. In pod logs look for a password for accessing jenkins:
    kubectl logs pod-name -n devops 
19. Sign in to jenkins, set up the controller, install needed plugins (Kubernetes, Docker, Pipeline, Github, Git)
20. Create service account for jenkins, create and bind a role for it. (Jenkins need permissions to create ephemeral agent pods)
    Use Role and RoleBinding - because we give permissions only for specific namespace for agents - build-env, attach this service account to jenkins.
21. Create a Dockerfile that contains the default image that jenkins uses to run agent pods, install there kubectl, push it to dockerhub registry
![dockerhub](images/img_5.png)
22. In jenkins to Clouds, create new cloud Kubernetes. Give it a name
    Kubernetes namespace: where we will run agents (build-env)
    Set jenkins url to: http://jenkins.devops.svc.cluster.local:8080 (service.namespace.svc.cluster.local:8080)
23. Configure pod templates: give an agent a name, set namespace to build-env, give agent a label
    Add container, give it name jnlp - so it will override a default container running in a pod
    Set image to image you created and pushed to dockerhub
    Set home directory to /home/jenkins
    Set it to run in privileged mode
24. In github configure a webhook with url: https://jenkins-k8s.skyb.boo
25. Create a new job pipeline, configure it to get GitHub hook trigger for GITScm polling.
    Define pipeline script from SCM
    Set scm to git, put github repository path, set branch to main
![pipeline_config](images/img_7.png)
26. Make a folder with a python app, make requirements file for it, and a dockerfile that builds image
27. Create credentials for jenkins to push image to dockerhub from a pipeline
28. Write a pipeline in a Jenkinsfile that:
    builds image via sidecar container
    pushes it to dockerhub
    deploys it to prod-env namespace

**Project Flow Diagram:**
![diagram](images/diagram.png)
    


