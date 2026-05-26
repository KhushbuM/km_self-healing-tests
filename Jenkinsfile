pipeline {
    agent any

    environment {
        ANTHROPIC_API_KEY = credentials('ANTHROPIC_API_KEY')
        GITHUB_TOKEN      = credentials('GITHUB_TOKEN')
        GITHUB_REPO       = 'KhushbuM/km_self-healing-tests'
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    playwright install chromium
                    playwright install-deps chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
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
                    . venv/bin/activate
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