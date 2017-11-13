from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import traceback
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .controllers import mongo_controller as db_controller
from . import envs


# ====================>>>>>>>> Utils <<<<<<<<====================
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# ====================>>>>>>>> Templates <<<<<<<<====================

def index(request):
    return render(request, 'web_app/index.html')


def security_policies(request):
    return render(request, 'web_app/security_policies.html')


# ====================>>>>>>>> APIs <<<<<<<<====================

@csrf_exempt
def api_security_policy(request, policy_id=""):
    """
    POST: Add or update a security policy
    GET: Retrieve all policies
    :param request:
    :return:
    """
    try:
        if request.method == 'POST':

            # Get the request json body
            payload = json.loads(request.body)

            # Update the database
            db_controller.insert_policy(payload)

            # Return the full object
            return JSONResponse({"response": "ok"})

        elif request.method == 'GET':

            # Get all the policies in database
            policies = db_controller.get_all_policies()

            return JSONResponse(policies)
        elif request.method == 'DELETE':

            # Get all the policies in database
            db_controller.delete_policy(policy_id)

            return JSONResponse({"response": "ok"})
        else:
            return JSONResponse("Bad request. " + request.method + " is not supported", status=400)
    except Exception as e:
        print(traceback.print_exc())
        # return the error to web client
        return JSONResponse({'error': e.__class__.__name__, 'message': str(e)}, status=500)
