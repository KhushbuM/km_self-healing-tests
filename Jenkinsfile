pipeline {
    agent any
    
    options {
        skipStagesAfterUnstable()
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
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    playwright install chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    sh '''
                        . venv/bin/activate
                        pytest tests/ -v --tb=short
                    '''
                }
            }
        }

        stage('Self Heal') {
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
            echo '❌ Pipeline failed!'
        }
        always {
            echo '📊 Pipeline complete'
        }
    }
}