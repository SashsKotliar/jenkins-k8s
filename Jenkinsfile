pipeline {
  agent {
    kubernetes {
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: sashak9/pod-agent:latest
    workingDir: /home/jenkins
    tty: true
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "1Gi"
        cpu: "1"
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    user: root
    command:
      - cat
    tty: true
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "1Gi"
        cpu: "1"
    workingDir: /home/jenkins
"""
    }
  }
  stages {
    stage ('Build and Push') {
      steps {
        container('kaniko') {
          withCredentials([usernamePassword(
            credentialsId: 'dockerhub-credentials', 
            usernameVariable: 'DOCKER_USER', 
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
              mkdir -p /home/jenkins/.docker
              echo "{\"auths\":{\"https://index.docker.io/v1/\":{\"auth\":\"$(echo -n $DOCKER_USER:$DOCKER_PASS | base64)\"}}}" \
                > /home/jenkins/.docker/config.json

              /kaniko/executor \
                --dockerfile=${WORKSPACE}/Dockerfile \
                --context=${WORKSPACE} \
                --destination="sashak9/webapp:latest" \
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
