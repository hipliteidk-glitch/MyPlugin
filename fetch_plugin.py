import json, urllib.request, time, sys, os

REPO = "hipliteidk-glitch/MyPlugin"
BRANCH = "main"

def get_latest_run():
    url = f"https://api.github.com/repos/{REPO}/actions/runs?branch={BRANCH}&per_page=1"
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
        runs = data.get('workflow_runs', [])
        if not runs:
            return None
        return runs[0]

def download_artifact(download_url, output_path):
    req = urllib.request.Request(download_url, headers={'Accept': 'application/zip'})
    with urllib.request.urlopen(req) as resp:
        with open(output_path, 'wb') as f:
            f.write(resp.read())

def main():
    print("Waiting for build to complete...")
    while True:
        run = get_latest_run()
        if not run:
            print("No workflow run found.")
            sys.exit(1)
        status = run.get('status')
        conclusion = run.get('conclusion')
        print(f"Status: {status}, Conclusion: {conclusion}")
        if status == 'completed':
            if conclusion == 'success':
                artifacts_url = run['artifacts_url']
                req = urllib.request.Request(artifacts_url, headers={'Accept': 'application/vnd.github.v3+json'})
                with urllib.request.urlopen(req) as resp:
                    arts = json.load(resp)
                    for art in arts.get('artifacts', []):
                        if art['name'] == 'plugin-apk':
                            download_url = art['archive_download_url']
                            print(f"Downloading APK from {download_url}")
                            download_artifact(download_url, 'plugin.apk')
                            print("Downloaded plugin.apk")
                            return
                    print("Artifact 'plugin-apk' not found.")
                    sys.exit(1)
            else:
                print(f"Build failed with conclusion: {conclusion}")
                sys.exit(1)
        else:
            time.sleep(10)

if __name__ == '__main__':
    main()
