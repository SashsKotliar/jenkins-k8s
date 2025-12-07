pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages {
    stage('Start Docker') {
      steps {
        sh '''
          dockerd &                   # start Docker daemon in background
          while(! docker info >/dev/null 2>&1); do
            echo "Waiting for Docker daemon..."
            sleep 1
          done
        '''
      }
    } 
    stage('Build and Push to Dockerhub') { 
      steps { 
	script {
	  docker.withRegistry('', 'dockerhub-credentials') {
	    def image = docker.build("sashak9/webapp:latest")
	    image.push()
	  }  
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
