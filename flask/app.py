from flask import Flask, redirect, render_template, request
import os, subprocess
import json

app = Flask(__name__)
app_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_path, "config.json")
sentence_path = "sentence.conllu"
sentence_out = sentence_path.replace('.conllu', '_GREWED.conllu')
rules_path = 'conjunto_regras_porttinari.grs'

def save_config():
    with open(config_path, "w") as f:
        json.dump(config, f)

def increase_access_number(n=1):
    if not 'sentences_tested' in config:
        config['sentences_tested'] = 0
    config['sentences_tested'] += n
    config['access_number'] += 1
    save_config()

# load config
default_config = {'access_number': 0, 'sentences_tested': 0}
if not os.path.isfile(config_path):
    config = default_config
    save_config()
else:
    with open(config_path) as f:
        config = json.load(f)

@app.route('/', methods="POST GET".split())
def home(conllu="", enhancement=""):
    if request.method == "POST":
        # convert new-line to linux style and add empty line in the end
        conllu = request.values.get("inputText").strip().replace("\r\n", "\n") + "\n\n"
        conllu_lines = conllu.split("\n")
        for i, line in enumerate(conllu_lines):
            if "\t" in line:
                columns = line.split("\t")
                if len(columns) == 10:
                    columns[8] = "_"
                    conllu_lines[i] = "\t".join(columns)
        conllu = "\n".join(conllu_lines)
        with open(sentence_path, "w") as f:
            f.write(conllu)
        command = f"grew transform -config iwpt -grs \"{rules_path}\" -strat strat_modificadas -i '{sentence_path}' -o '{sentence_out}'"
        try:
            enhancement = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
            enhancement.wait()
            stdout, stderr = enhancement.communicate()
            if enhancement.returncode != 0:
                raise subprocess.CalledProcessError(enhancement.returncode, command, stderr)                    
            with open(sentence_out) as f:
                enhancement = f.read()
            os.remove(sentence_out)
        except subprocess.CalledProcessError as e:
            enhancement = f"Error executing command: {e.stdout.decode('utf-8')}"
        except Exception as e:
            enhancement = f"An unexpected error occurred: {str(e)}"
        finally:
            os.remove(sentence_path)
            increase_access_number(conllu.count("\n\n"))
    access_number = config.get("access_number")
    sentences_tested = config.get("sentences_tested")

    return render_template(
        'index.html', 
        title="",
        conllu=conllu.strip(),
        enhancement=enhancement,
        access_number=access_number,
        sentences_tested=sentences_tested
        )