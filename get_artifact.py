import subprocess
import json
import sys

def run_gh(args):
    cmd = ['gh'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def main():
    run_id = '30809133231'
    # Get artifact list
    out = run_gh(['run', 'view', run_id, '--repo', 'hipliteidk-glitch/MyPlugin', '--json', 'artifacts'])
    data = json.loads(out)
    artifacts = data.get('artifacts', [])
    print("Artifacts:")
    for art in artifacts:
        print(f"  {art['name']} (ID: {art['id']})")
    # Find the one that might be the plugin zip. The workflow uploads 'plugin-zip' and 'plugin-apk'.
    # But maybe it's named differently. Let's see.
    # We'll download the first one that looks like plugin-zip or the one with 'zip' in name.
    target = None
    for art in artifacts:
        if art['name'] == 'plugin-zip':
            target = art
            break
    if not target:
        # fallback: if any artifact has 'zip' in name
        for art in artifacts:
            if 'zip' in art['name'].lower():
                target = art
                break
    if target:
        print(f"Downloading {target['name']}...")
        # Download with gh run download -n name
        download_cmd = ['run', 'download', run_id, '--repo', 'hipliteidk-glitch/MyPlugin', '-n', target['name'], '-D', '.']
        print(f"Running: {' '.join(download_cmd)}")
        result = subprocess.run(['gh'] + download_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Download failed: {result.stderr}")
            sys.exit(1)
        print("Download completed.")
        # List files
        import os
        for f in os.listdir('.'):
            if target['name'] in f:
                print(f"Found: {f}")
                # If it's a zip, maybe unzip? but we can just report.
    else:
        print("No suitable artifact found.")

if __name__ == '__main__':
    main()
