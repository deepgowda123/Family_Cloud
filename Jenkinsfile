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
                bat """
                if not exist venv (
                    %PYTHON% -m venv venv
                )
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Lint') {
            steps {
                bat """
                call venv\\Scripts\\activate
                pip install flake8
                flake8 .
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                call venv\\Scripts\\activate
                pip install pytest pytest-cov
                pytest --cov=. --cov-branch --cov-report xml
                """
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonar-token') // Make sure Jenkins has this credential
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                    call %SONAR_SCANNER%\\bin\\sonar-scanner.bat ^
                        -Dsonar.projectKey=FamilyCloud ^
                        -Dsonar.sources=. ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_TOKEN% ^
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                docker build -t deepika/familycloud:latest .
                """
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
