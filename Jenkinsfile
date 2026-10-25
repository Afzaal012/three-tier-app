
pipeline {
    agent any

    stages {
        stage('Build Application') {
            steps {
                build job: 'Build-Three-Tier-App',
                      wait: true,
                      propagate: true
            }
        }

        stage('Test Application') {
            steps {
                build job: 'Test-Three-Tier-App',
                      wait: true,
                      propagate: true
            }
        }

        stage('Deploy Application') {
            steps {
                build job: 'Deploy-Three-Tier-App',
                      wait: true,
                      propagate: true
            }
        }
    }

    post {
        success {
            echo 'Build, test, and deployment completed successfully!'
        }
        failure {
            echo 'CI/CD failed. Check the failed downstream job.'
        }
    }
}
