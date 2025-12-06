pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages { 
    stage('Build') { 
      steps { 
	sh 'docker build -t sashak9/webapp:latest'
      } 
    } 
    stage('Push to dockerhub') { 
      steps { 
        echo 'Push to docker hub..' 
      } 
    } 
    stage('Deploy') { 
      steps { 
        echo 'Deploying....' 
      } 
    } 
  }
}
