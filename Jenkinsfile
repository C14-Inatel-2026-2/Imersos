
pipeline {
    agent {
        label 'built-in'
    }
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

        stage('Relatorio de Cobertura') {
            steps {
                sh '''
                    set -eu

                    poetry run python -m pytest tests/ -v \
                        --junitxml=reports/testes-completos.xml \
                        --cov=models \
                        --cov=repository \
                        --cov=services \
                        --cov=terminal \
                        --cov-report=term-missing \
                        --cov-report=html:reports/htmlcov \
                        --cov-report=xml:reports/coverage.xml
                '''
            }

            post {
                always {
                    publishHTML(target: [
                        reportDir: 'reports/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Cobertura de Testes',
                        keepAll: true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: true
                    ])

                    archiveArtifacts artifacts: 'reports/**/*',
                                    allowEmptyArchive: true
                }
            }
        }


        stage('Deploy - Docker Hub') {
            when {
                beforeAgent true
                expression {
                    env.GIT_BRANCH == 'origin/main' ||
                    env.GIT_BRANCH == 'main' ||
                    env.BRANCH_NAME == 'main'
                }
            }

            agent {
                label 'windows-docker'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        $usuario = $env:DOCKERHUB_USER.ToLowerInvariant()
                        $imagem = "$usuario/imersos"
                        $versao = "{0}:{1}" -f $imagem, $env:BUILD_NUMBER
                        $latest = "$imagem`:latest"

                        Write-Host "Construindo imagem Docker..."

                        docker build -t $versao -t $latest .
                        if ($LASTEXITCODE -ne 0) {
                            throw "Falha ao construir a imagem"
                        }

                        Write-Host "Autenticando no Docker Hub..."

                        
                        $utf8SemBom = New-Object System.Text.UTF8Encoding($false)
                        [Console]::InputEncoding = $utf8SemBom
                        $OutputEncoding = $utf8SemBom

                        $usuario = $env:DOCKERHUB_USER.Trim().ToLowerInvariant()
                        $token = $env:DOCKERHUB_TOKEN.Trim()

                        $token | docker login --username $usuario --password-stdin


                        if ($LASTEXITCODE -ne 0) {
                            throw "Falha na autenticacao"
                        }

                        try {
                            Write-Host "Publicando versao $versao"

                            docker push $versao
                            if ($LASTEXITCODE -ne 0) {
                                throw "Falha ao publicar a versao"
                            }

                            Write-Host "Publicando tag latest..."

                            docker push $latest
                            if ($LASTEXITCODE -ne 0) {
                                throw "Falha ao publicar latest"
                            }

                            Write-Host "Imagem publicada com sucesso!"
                        }
                        finally {
                            docker logout | Out-Null
                        }
                    '''
                }
            }
        }
    }
}
