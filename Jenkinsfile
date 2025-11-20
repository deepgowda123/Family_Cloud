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

                rem Install app dependencies
                pip install -r requirements.txt

                rem Install Flask extensions your app needs
                pip install flask-wtf flask_sqlalchemy sqlalchemy wtforms

                rem Install lint & test tools
                pip install flake8 pytest pytest-cov
                """
            }
        }

        stage('Lint') {
            steps {
                bat """
                call venv\\Scripts\\activate
                flake8 .
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                call venv\\Scripts\\activate

                rem Ensures Python can find app, models, tests
                set PYTHONPATH=%CD%

                rem Run tests with coverage
                pytest --cov=. --cov-branch --cov-report=xml:coverage.xml
                """
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonar-token')
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
                body: "Your Jenkins pipeline completed successfully! 🎉"
            )
        }

        failure {
            emailext(
                to: "${EMAIL_TO}",
                subject: "Jenkins Build FAILED: FamilyCloud",
                body: "Your Jenkins pipeline failed. Please check the Jenkins logs. ❌"
            )
        }
    }
}
