# Creating a Self-Hosted GitHub Runner on Proxmox

**Context**  
Proxmox VE in this setup runs on a private network without direct internet exposure.  
To use GitHub Actions, we create a **self-hosted runner** inside the private network.  
This avoids exposing Proxmox ports publicly while allowing workflows to interact directly with the server.

---

## 1. Update packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl unzip -y
```

## 2. Create a dedicated runner user
```bash
sudo useradd -m -d /home/github-runner -s /bin/bash github-runner
```
We use a dedicated user for security, so the runner process does not run as root.

## 3. Log in as github-runner
```bash
sudo su - github-runner
```


## 4. Get installation instructions from GitHub
Go to your repository on GitHub.

Navigate to: Settings → Actions → Runners → New self-hosted runner.

Copy the commands shown — they will include your unique token.

⚠️ Tokens expire quickly (usually 1 hour). Generate a fresh one if needed.


## 5. Download and extract the runner
Example (replace with the current version from GitHub):

```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.327.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.327.1/actions-runner-linux-x64-2.327.1.tar.gz
echo "d68ac1f500b747d1271d9e52661c408d56cffd226974f68b7dc813e30b9e0575  actions-runner-linux-x64-2.327.1.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.327.1.tar.gz
```

## 6. Configure the runner
```bash
./config.sh --url https://github.com/<ORG>/<REPO> --token <TOKEN>
```
Where:

`<ORG>` = your GitHub account or organization name (e.g., fabiengaubert)
`<REPO>` = your repository name (e.g., pryxmox)
`<TOKEN>` = temporary token from GitHub


## 7. Exit back to the admin account
```bash
exit
```

## 8. Install the runner as a service
```bash
cd /home/github-runner/actions-runner
sudo ./svc.sh install github-runner
sudo ./svc.sh start
```
The service will now run automatically on boot as the github-runner user.


## 9. Ensure github-runner has permissions on the folder
```bash
sudo chown -R github-runner:github-runner /home/github-runner/actions-runner
sudo chmod -R u+rwX /home/github-runner/actions-runner
```

## 10. Using the self-hosted runner in a GitHub Action

In your `.github/workflows/*.yaml` file:

```yaml
jobs:
  build:
    runs-on: self-hosted
```

## Tip
If you later remove or rename the runner in GitHub, also stop and uninstall the system service:
```bash
sudo ./svc.sh stop
sudo ./svc.sh uninstall
```
