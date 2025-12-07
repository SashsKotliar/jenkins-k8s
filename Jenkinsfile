pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages {  
    stage('Build and Push to Dockerhub') { 
      steps { 
        sh 'kubectl version' 
    } 
    stage('Deploy') { 
      steps { 
        echo 'Deploying...' 
      } 
    } 
  }
}
