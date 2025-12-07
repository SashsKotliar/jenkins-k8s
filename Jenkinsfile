pipeline {
  agent {
    kubernetes {
      defaultContainer 'docker'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24-dind
    securityContext:
      privileged: true
    env:
      - name: DOCKER_TLS_CERTDIR
        value: ""
    command:
      - dockerd-entrypoint.sh
    tty: true
    volumeMounts:
      - name: docker-data
        mountPath: /var/lib/docker
  - name: jnlp
    image: sashak9/pod-agent:latest
    tty: true
    workingDir: /home/jenkins
  volumes:
    - name: docker-data
      emptyDir: {}
"""
    }
  }
  stages {
    stage('Checkout') {
      steps {
        container('jnlp') {
          checkout scm
        }
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        container('docker') {
          withCredentials([usernamePassword(
            credentialsId: 'dockerhub-credentials',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
          )]) {
            sh '''
              echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
              docker build -t sashak9/webapp:latest .
              docker push sashak9/webapp:latest
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

