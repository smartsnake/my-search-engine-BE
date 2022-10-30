import json

from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from django.shortcuts import get_list_or_404
from django.views.generic import ListView
from rest_framework.response import Response

from .models import Index


class WebsiteSerializer(serializers.Serializer):
    URL = serializers.CharField()
    Description = serializers.CharField()
    Title = serializers.CharField()


def get_all(request):
    queue = Index.objects.all()
    websiteList = get_list_or_404(queue)

    return JsonResponse(WebsiteSerializer(websiteList, many=True).data, safe=False)


#TODO: Adjust search to not care about capital letters
def search(request):
    searchQuery = request.GET.get('q')
    if searchQuery:
        # Get words from search input
        # split the search term into a list of words
        list_of_words = searchQuery.split(' ')

        #TODO: Maybe not filter on all websites in database.
        websiteList = get_list_or_404(Index.objects.all())

        # Attach sorting value
        for website in websiteList:
            website.sortedValue = 0

        # Calculate value from Title
        for website in websiteList:
            text_value = 0
            for word in list_of_words:
                if website.Title:
                    text_value += (website.Title.count(word) * 3)
            website.sortedValue += text_value

        # Calculate value from description
        for website in websiteList:
            text_value = 0
            for word in list_of_words:
                if website.Description:
                    text_value += (website.Description.count(word) * 2)
            website.sortedValue += text_value

        # Calculate value from words
        for website in websiteList:
            text_value = 0
            for word in list_of_words:
                if word in website.words:
                    text_value += (website.words[word])
            website.sortedValue += text_value

        sorted_websites = sorted(websiteList, key=lambda x: x.sortedValue, reverse=True)

        return JsonResponse(WebsiteSerializer(sorted_websites, many=True).data, safe=False)

    print('Bad Request!')
    return HttpResponse(status=400)


def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")
