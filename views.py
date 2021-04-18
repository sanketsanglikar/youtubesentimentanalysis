from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.http import HttpResponse
from .services import YoutubeSentimentAnalysis
from rest_framework.decorators import api_view, renderer_classes
from zipfile import ZipFile
import time
from .custom_renderers import PNGRenderer
from wsgiref.util import FileWrapper
import base64
from PIL import Image
import io
from io import BytesIO


@api_view(['POST'])
#@renderer_classes((PNGRenderer,))
def send_file(request):
    obj = YoutubeSentimentAnalysis(request.data['api_key'], request.data['video_id'])
    comments = obj.ytScrap()
    words_in_comments = obj.data_cleaning(comments)
    all_words_no_sw = obj.removing_stop_words(words_in_comments)
    obj.saving_figure(all_words_no_sw)
    time.sleep(5)
    response = HttpResponse(content_type='application/zip')
    zipObj = ZipFile(response,'w')
    zipObj.write(r'api/static/{}_{}_sentiment.png'.format(request.data['api_key'], request.data['video_id']))
    zipObj.write(r'api/static/{}_{}_wordcloud.png'.format(request.data['api_key'], request.data['video_id']))
    response['Content-Disposition'] = 'attachment; filename=api/static/{}_{}.zip'.format(request.data['api_key'], request.data['video_id'])
    return response

