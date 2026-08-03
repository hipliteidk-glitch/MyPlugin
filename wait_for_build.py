import subprocess
import json
import time
import sys
import os

def run_gh(args):
    cmd = ['gh'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'Error: {result.stderr}', file=sys.stderr)
        sys.exit(1)
    return result.stdout

def main():
    run_id = '30809956483'
    repo = 'hipliteidk-glitch/MyPlugin'
    
    print('Waiting for build to complete...')
    while True:
        out = run_gh(['run', 'view', run_id, '--repo', repo, '--json', 'jobs'])
        data = json.loads(out)
        job = data['jobs'][0]
        status = job['status']
        conclusion = job.get('conclusion')
        
        print(f'Status: {status}, Conclusion: {conclusion or "N/A"}')
        
        if status == 'completed':
            if conclusion == 'success':
                print('Build succeeded! Downloading artifact...')
                # Download the plugin-zip artifact
                download_cmd = ['run', 'download', run_id, '--repo', repo, '-n', 'plugin-zip', '-D', '.']
                result = subprocess.run(['gh'] + download_cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f'Download failed: {result.stderr}')
                    sys.exit(1)
                print('Downloaded plugin-zip artifact.')
                # List files
                for f in os.listdir('.'):
                    if 'plugin-zip' in f or f.endswith('.zip'):
                        print(f'Found: {f}')
                break
            else:
                print(f'Build failed with conclusion: {conclusion}')
                sys.exit(1)
        else:
            time.sleep(10)

if __name__ == '__main__':
    main()
