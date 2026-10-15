
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    python --version
                    poetry --version
                    poetry check --lock
                    poetry install --no-root
                    poetry run python -m compileall models repository services terminal
                '''
            }
        }
    }
}
