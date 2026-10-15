
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    set -eu

                    python --version
                    poetry --version
                    poetry check --lock
                    poetry install --no-root
                    poetry run python -m compileall models repository services terminal
                '''
            }
        }

        stage('Testes - Emprestimo') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/test_emprestimo.py -v --junitxml=reports/emprestimo.xml
                '''
            }
            post {
                always {
                    junit testResults: 'reports/emprestimo.xml', allowEmptyResults: false
                }
            }
        }
    }
}
