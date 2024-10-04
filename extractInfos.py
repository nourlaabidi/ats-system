import openai
import json
import uuid
from textProcessing import process_file, clean_json_response, none_if_empty, get_embedding
#extractInfos.py will have the file path of the resume as an input and process it using the LLM (gpt 3.5 turbo 16k ) to return the 
#usefull informations of a resume and then store these informations in the index created
def process_and_index_resume(file_path, search_client, existed_resumes):
    if file_path not in existed_resumes:
        try:
            text = process_file(file_path)
        except ValueError as e:
            print(e, file_path)
            return None

        if text:
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo-16K",
                messages=[
                    {
                        "role": "user",
                        "content":  f"You are a very experienced AI assistant with a deep understanding of tech field that generate in JSON format response. For a given text, extract the following information: speaking langages: what are the langage that she/he speaks?. \Answer output them as a comma separated Python list. Skills: what are the technical and non technical skills?.\Answer output them as a comma separated Python list.Work experience: List all positions held, and calculate the duration (in years and months) worked in each position. Output this as a comma-separated Python list, where each field is followed by the duration in the format Position (Duration) e.g., Position (2 years, 3 months). technologies: what are the technologies that he/she worked with in his/her projects and work experiences? \Answer output them as a comma separated Python list. take your time and format the output as JSON with the following keys: Name of the person, Skills, Technologies, Languages, work experience. here is the text: {text}"
                    }
                ],
                temperature=0,
                max_tokens=4096,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )

            try:
                cleaned_response_content = clean_json_response(response['choices'][0]['message']['content'])
                data = json.loads(cleaned_response_content)
                name = data.get("Name", "")
                skills = none_if_empty(data.get("Skills", ""))
                technologies = none_if_empty(data.get("Technologies", ""))
                languages = none_if_empty(data.get("Languages", ""))
                work_experience = none_if_empty(data.get("Work Experience", ""))

                
                document = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "file_path": file_path,
                    "skills": skills.split(",") if skills else [],
                    "skillsEmb": get_embedding(skills),
                    "technologies": technologies.split(",") if technologies else [],
                    "technologiesEmb": get_embedding(technologies),
                    "language": languages.split(",") if isinstance(languages, list) else [],
                    "WorkExperiences": (work_experience.split(",") if isinstance(work_experience, str) else work_experience) or [],
                    "WorkExperiencesEmb": get_embedding(work_experience)
                }
                
                search_client.upload_documents(documents=[document])
                print("information succefully uploaded")
                existed_resumes.append(file_path)

            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
                print("Raw response content where the error occurs:", response['choices'][0]['message']['file_path'])