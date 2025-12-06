pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'git@github.com:SashsKotliar/jenkins-k8s.git'
            }
        }
    }
}
