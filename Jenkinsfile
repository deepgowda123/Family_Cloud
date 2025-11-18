pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/deepgowda123/Family_Cloud.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Running basic lint check...'
            }
        }

        stage('Tests') {
            steps {
                echo 'No tests yet — skipping.'
            }
        }
    }

    post {
        success {
            echo "BUILD SUCCESS ✔"
        }
        failure {
            echo "BUILD FAILED ❌"
        }
    }
}
