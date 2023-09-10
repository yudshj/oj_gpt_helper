import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils import fetch, gpt

index_html = open("template/index.html", "r").read()
def index(request):
    return HttpResponse(index_html)

@csrf_exempt
def submit(request):
    # read json from request
    payload = json.loads(request.body)
    info = fetch.get_code_and_description(payload['submission_url'])
    resp = {
        'response': gpt.gpt_service(info)
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")