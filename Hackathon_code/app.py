from flask import Flask, render_template, request
import spacy
import fitz  # PyMuPDF
import io

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'  
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Load your SpaCy model
nlp = spacy.load("/Users/adityalanka/Downloads/Hackathon_code/output2/model-best")

# Define the list of important entity labels
important_labels = ['NAME', 'CONTACT', 'COMPANIES WORKED AT', 'YEARS OF EXPERIENCE', 'ORG', 'DATE', 'LOCATION', 'MONEY', 'PERCENT', 'TIME', 'PERSON']

def entity_sort_key(entity):
    if entity['label'] in important_labels:
        return (0, important_labels.index(entity['label']))
    else:
        return (1, entity['label'])  # Sorting by label if not in important_labels

def get_combined_data(entities):
    companies = []
    experiences = []
    for entity in entities:
        if entity['label'] == 'COMPANIES WORKED AT':
            companies.append(entity['text'])
        elif entity['label'] == 'YEARS OF EXPERIENCE':
            experiences.append(entity['text'])
    combined_data = list(zip(companies, experiences))
    return combined_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    if request.method == 'POST':
        if 'resume_file' not in request.files:
            return render_template('index.html', error="No file part")
        
        resume_file = request.files['resume_file']
        if resume_file.filename == '':
            return render_template('index.html', error="No selected file")

        if resume_file:
            # Read PDF file using PyMuPDF
            pdf_content = resume_file.read()
            pdf_document = fitz.open(stream=pdf_content)
            text = ""
            for page_num in range(len(pdf_document)):
                text += pdf_document[page_num].get_text()

            # Process text with SpaCy
            doc = nlp(text)
            entities = [{'text': ent.text.strip(), 'label': ent.label_} for ent in doc.ents]
            sorted_entities = sorted(entities, key=entity_sort_key)
            combined_data = get_combined_data(sorted_entities)
            return render_template('entities.html', entities=sorted_entities, combined_data=combined_data)

    return render_template('index.html', error="Error occurred")

if __name__ == '__main__':
    app.run(debug=True)
