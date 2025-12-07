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
              # Wait for Docker daemon to start
              until docker info >/dev/null 2>&1; do
                echo "Waiting for Docker daemon..."
                sleep 1
              done

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
          sh """
	    kubectl patch deployment weather-app -n prod-env \
              -p '{"spec":{"template":{"metadata":{"annotations":{"kubectl.kubernetes.io/restartedAt":"'"\$(date +%Y-%m-%dT%H:%M:%S%Z)"'"}}}}}'
	    
	    kubectl set image deployment/weather-app weather=sashak9/webapp:latest -n prod-env
	    kubectl rollout status deployment/weather-app -n prod-env
	  """
        }
      }
    }
  }
}
