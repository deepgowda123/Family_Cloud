pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\HP\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        EMAIL_TO = "deepikagowda255@gmail.com"
        SONAR_SCANNER = tool 'SonarScanner'
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/deepgowda123/Family_Cloud.git', branch: 'main'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                %PYTHON% -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                venv\\Scripts\\activate && pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                venv\\Scripts\\activate && pip install flake8
                venv\\Scripts\\activate && flake8 .
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                venv\\Scripts\\activate && pip install pytest
                venv\\Scripts\\activate && pytest
                '''
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonar-token')
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                    cd E:\\ancestor-tree
                    %SONAR_SCANNER%\\bin\\sonar-scanner.bat ^
                        -Dsonar.projectKey=FamilyCloud ^
                        -Dsonar.sources=. ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_TOKEN%
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                cd E:\\ancestor-tree
                docker build -t deepika/familycloud:latest .
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: "${EMAIL_TO}",
                subject: "Jenkins Build SUCCESS: FamilyCloud",
                body: "Your Jenkins pipeline completed successfully!"
            )
        }

        failure {
            emailext(
                to: "${EMAIL_TO}",
                subject: "Jenkins Build FAILED: FamilyCloud",
                body: "Your Jenkins pipeline failed. Check Jenkins logs."
            )
        }
    }
}
