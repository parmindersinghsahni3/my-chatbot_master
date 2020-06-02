from django.shortcuts import render
from django.http import HttpResponse
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from django.conf import settings

PATH = os.path.join(settings.BASE_DIR,"SERVICE_ACCOUNT.json")


# Create your views here.
def home_page(request):
	if request.method == "GET":
		return render(request,"chatbot/popup3.html")
	else:
		chat_msg= request.POST.get('MSG')
		os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH
		DIALOGFLOW_PROJECT_ID = 'YOUR_PROJECT_ID'
		DIALOGFLOW_LANGUAGE_CODE = 'language_code'
		SESSION_ID = 'me'
		session_client = dialogflow.SessionsClient()
		session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
		text_input = dialogflow.types.TextInput(text=chat_msg, language_code=DIALOGFLOW_LANGUAGE_CODE)
		query_input = dialogflow.types.QueryInput(text=text_input)
		try:
			response = session_client.detect_intent(session=session, query_input=query_input)
		except InvalidArgument:
			raise

		print("Query text:", response.query_result.query_text)
		print("Detected intent:", response.query_result.intent.display_name)
		print("Detected intent confidence:", response.query_result.intent_detection_confidence)
		print("Fulfillment text:", response.query_result.fulfillment_text)
		return HttpResponse(response.query_result.fulfillment_text)    
	    
	