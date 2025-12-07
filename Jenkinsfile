pipeline {
  agent { label "jenkins-builder" }

  environment {
    IMAGE_NAME = "sashak9/webapp:latest"
  }

  stages {
    stage('Build and Push') {
      steps {
        container('kaniko') {
          // Use Jenkins credentials
          withCredentials([usernamePassword(
            credentialsId: 'dockerhub-cred', 
            usernameVariable: 'DOCKER_USER', 
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
              # create Docker config for Kaniko
              mkdir -p /home/jenkins/.docker
              echo "{\"auths\":{\"https://index.docker.io/v1/\":{\"auth\":\"$(echo -n $DOCKER_USER:$DOCKER_PASS | base64)\"}}}" \
                > /home/jenkins/.docker/config.json

              # run Kaniko
              /kaniko/executor \
                --dockerfile=${WORKSPACE}/Dockerfile \
                --context=${WORKSPACE} \
                --destination=${IMAGE_NAME} \
                --docker-config=/home/jenkins/.docker \
                --verbosity=info
            '''
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        container('jnlp') {
          sh 'kubectl version'
          echo 'Deploying...'
        }
      }
    }
  }
}
