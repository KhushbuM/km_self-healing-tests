pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '--user root'
        }
    }

    environment {
        ANTHROPIC_API_KEY = credentials('ANTHROPIC_API_KEY')
        GITHUB_TOKEN      = credentials('GITHUB_TOKEN')
        GITHUB_REPO       = 'KhushbuM/km_self-healing-tests'
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    playwright install chromium
                    playwright install-deps chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pytest tests/ -v --tb=short
                '''
            }
        }

        stage('Self Heal') {
            when {
                expression {
                    currentBuild.result == 'FAILURE' || currentBuild.result == null
                }
            }
            steps {
                sh '''
                    python -m healer.runner
                '''
            }
        }
    }

    post {
        success {
            echo '✅ All tests passed — no healing needed!'
        }
        failure {
            echo '❌ Tests failed — self healing triggered!'
        }
        always {
            echo '📊 Pipeline complete'
        }
    }
}