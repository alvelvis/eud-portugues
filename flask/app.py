from flask import Flask, render_template, request
import os, subprocess, sys
import json

app = Flask(__name__)
app_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_path, "config.json")
sentence_path = os.path.join(app_path, "sentence.conllu")
sentence_out = sentence_path.replace('.conllu', '_GREWED.conllu')
rules_path = os.path.join(app_path, "conjunto_regras_porttinari.grs")

with open(rules_path) as f:
    rules = f.read()
strategies = [x.split("{")[0].strip() for x in rules.split("strat ")[1:]]

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
def home(conllu="", enhancement="", strategy=""):
    if request.method == "POST":
        # convert new-line to linux style and add empty line in the end
        conllu = request.values.get("inputText").strip().replace("\r\n", "\n") + "\n\n"
        strategy = request.values.get("strat")
        enhancement = annotate(conllu, rules_path, strategy)
        increase_access_number(conllu.count("\n\n"))
    access_number = config.get("access_number")
    sentences_tested = config.get("sentences_tested")

    return render_template(
        'index.html', 
        title="",
        conllu=conllu.strip(),
        enhancement=enhancement,
        selected_strat=strategy,
        access_number=access_number,
        sentences_tested=sentences_tested,
        strategies=strategies
        )

def annotate(conllu, rules_path, strategy):
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
    command = f"grew transform -config iwpt -grs \"{rules_path}\" -strat '{strategy}' -i '{sentence_path}' -o '{sentence_out}'"
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

    return enhancement

if __name__ == "__main__":
    conllu_path = sys.argv[1]
    rules_path = sys.argv[2]
    strategy = sys.argv[3]
    assert all(os.path.exists(x) for x in [conllu_path, rules_path])
    with open(conllu_path) as f:
        conllu = f.read()
    print(annotate(conllu, rules_path, strategy))