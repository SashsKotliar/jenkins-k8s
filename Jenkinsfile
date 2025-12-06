pipeline { 
  agent { 
    label "jenkins-builder" 
  } 
  stages { \
    stage('Build') { 
      steps { 
        echo 'Building..' 
      } 
    } 
    stage('Test') { 
      steps { 
        echo 'Testing..' 
        sh 'git -v' 
      } 
    } 
    stage('Deploy') { 
      steps { 
        echo 'Deploying....' 
      } 
    } 
  }
}
