pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages { 
    stage('Build') { 
      steps { 
        echo 'Building..'
	sh 'git -v'
      } 
    } 
    stage('Test') { 
      steps { 
        echo 'Testing..' 
        sh 'docker -v'
      } 
    } 
    stage('Deploy') { 
      steps {
	sh 'kubectl version' 
        echo 'Deploying....' 
      } 
    } 
  }
}
