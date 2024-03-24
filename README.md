# tapi-user-service
A user service in python using clean architecture and the asynchronous sanic framework for non-blocking

brew install pyenv
pyenv install 3.11.2
pyenv global 3.11.2

nano ~/.zshrc

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

source ~/.zshrc

python --version  # or python3 --version


git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv

eval "$(pyenv virtualenv-init -)"

source ~/.zshrc

pyenv virtualenv-init -


pip install sanic

pyenv global 3.12.2

Select environment with pyenv from visual studio

modify code runner settings:
"code-runner.executorMap": {
    "python": "\"/Users/nkenchor/.pyenv/versions/3.12.2/bin/python\" -u",
}



Organisation Service
Identity Service
Otp Service
Notification Service
Onboaring Servicee
User Service
Licensing Service
Sales Service
Product Service
Payment Service