from flask import Flask, request, render_template_string, jsonify
import subprocess

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>WebCMD</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; min-height: 100vh; }
        h1 { color: #58a6ff; margin-bottom: 15px; font-size: 1.4em; }
        form { display: flex; gap: 8px; margin-bottom: 15px; }
        input { flex: 1; background: #161b22; border: 1px solid #30363d; color: #c9d1d9; padding: 10px 14px; border-radius: 6px; font-family: monospace; font-size: 1em; }
        input:focus { outline: none; border-color: #58a6ff; }
        button { background: #238636; color: white; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 1em; }
        button:hover { background: #2ea043; }
        pre { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 14px; overflow-x: auto; white-space: pre-wrap; word-break: break-all; min-height: 40px; max-height: 60vh; overflow-y: auto; }
        .error { color: #f85149; }
        .hint { color: #8b949e; font-size: 0.85em; margin-top: 12px; }
    </style>
</head>
<body>
    <h1>$ webcmd</h1>
    <form method="POST">
        <input type="text" name="cmd" placeholder="Enter shell command..." value="{{ last }}" autofocus>
        <button type="submit">Run</button>
    </form>
    {% if output is not none %}
    <pre class="{{ 'error' if rc != 0 else '' }}">{{ output }}</pre>
    <div class="hint">exit code: {{ rc }}</div>
    {% else %}
    <pre></pre>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    rc = 0
    last = ''
    if request.method == 'POST':
        cmd = request.form.get('cmd', '')
        last = cmd
        if cmd.strip():
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                output = result.stdout
                if result.stderr:
                    output += result.stderr
                rc = result.returncode
                if not output:
                    output = '(no output)'
            except subprocess.TimeoutExpired:
                output = 'ERROR: command timed out (30s)'
                rc = 124
            except Exception as e:
                output = f'ERROR: {e}'
                rc = 1
    return render_template_string(HTML, output=output, rc=rc, last=last)

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json(silent=True)
    if not data or 'cmd' not in data:
        return jsonify({'error': 'send JSON with "cmd" key'}), 400
    cmd = data['cmd']
    if not cmd.strip():
        return jsonify({'error': 'cmd is empty'}), 400
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'command timed out (30s)', 'exit_code': 124}), 504
    except Exception as e:
        return jsonify({'error': str(e), 'exit_code': 1}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
