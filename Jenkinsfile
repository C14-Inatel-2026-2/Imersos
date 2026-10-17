
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

        stage('Testes - Services') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/test_livro_service.py -v \
                        --junitxml=reports/services.xml \
                        --cov=services --cov-report=term
                '''
            }
            post {
                always {
                    junit testResults: 'reports/services.xml', allowEmptyResults: false
                }
            }
        }

        stage('Testes - Livro') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/test_livro.py -v \
                        --junitxml=reports/livro.xml \
                        --cov=models.livro \
                        --cov-report=term-missing \
                        --cov-report=xml:reports/coverage-livro.xml
                '''
            }
            post {
                always {
                    junit testResults: 'reports/livro.xml',
                          allowEmptyResults: false

                    archiveArtifacts artifacts: 'reports/coverage-livro.xml',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Testes - Terminal') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/test_terminal.py -v \
                        --junitxml=reports/terminal.xml \
                        --cov=terminal --cov-report=term
                '''
            }
            post {
                always {
                    junit testResults: 'reports/terminal.xml', allowEmptyResults: false
                }
            }
        }
        stage('Testes - Repository') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/test_repository.py -v \
                        --junitxml=reports/repository.xml \
                        --cov=repository --cov-report=term
                '''
            }
            post {
                always {
                    junit testResults: 'reports/repository.xml', allowEmptyResults: false
                }
            }
        }
    }
}
