# ChatAgent Backend

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env  # add your Google API key
uvicorn chatagent.app:app --host 0.0.0.0 --port 8080
```

## systemd
```bash
sudo cp backend/systemd/chatagent.service /etc/systemd/system/chatagent.service
sudo systemctl daemon-reload
sudo systemctl enable --now chatagent
journalctl -u chatagent -f
```
