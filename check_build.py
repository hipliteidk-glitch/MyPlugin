import json, urllib.request, sys

repo = 'hipliteidk-glitch/MyPlugin'
url = f'https://api.github.com/repos/{repo}/actions/runs?branch=main&status=completed&per_page=1'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
with urllib.request.urlopen(req) as resp:
    data = json.load(resp)
    runs = data.get('workflow_runs', [])
    if not runs:
        print('NO_RUN')
        sys.exit()
    run = runs[0]
    if run['conclusion'] != 'success':
        print(f'FAILED: {run["conclusion"]}')
        sys.exit()
    # Get artifacts
    artifacts_url = run['artifacts_url']
    req2 = urllib.request.Request(artifacts_url, headers={'Accept': 'application/vnd.github.v3+json'})
    with urllib.request.urlopen(req2) as resp2:
        arts = json.load(resp2)
        for art in arts.get('artifacts', []):
            if art['name'] == 'plugin-apk':
                print(f"ARTIFACT_URL={art['archive_download_url']}")
                print(f"ARTIFACT_ID={art['id']}")
                break
        else:
            print('NO_APK_ARTIFACT')
