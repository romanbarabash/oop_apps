import justpy as jp

from dictionary_api_app import api, documentation

jp.Route("/api", api.Api.serve)
jp.Route("/", documentation.Doc.serve)
jp.justpy()
