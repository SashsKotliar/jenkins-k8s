pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages {  
    stage('Build and Push to Dockerhub') { 
      steps { 
        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
	  sh 'ls -l /kaniko-executor'
          sh '/kaniko-executor --version'
	  sh '''
            mkdir -p /home/jenkins/.docker
            cat <<EOF > /home/jenkins/.docker/config.json 
{
  "auths": {
    "https://index.docker.io/v1/": {
      "username": "$DOCKER_USER",
      "password": "$DOCKER_PASS"
    }
  }
}
EOF
	    /kaniko-executor --dockerfile=Dockerfile --context=\$(pwd) --destination=sashak9/webapp:latest 
       	  '''
	}
      } 
    } 
    stage('Deploy') { 
      steps { 
        echo 'Deploying...' 
      } 
    } 
  }
}
