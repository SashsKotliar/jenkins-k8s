pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages { 
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
