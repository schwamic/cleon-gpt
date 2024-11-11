"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from ninja import NinjaAPI, Redoc

from conversations.api import router as conversations_router
from users.api import router as users_router


"""
HTTP(s) REST API configuration
"""
rest_api_v1 = NinjaAPI(
    docs=Redoc(),
    version="0.1.1",
    urls_namespace="public_api",
    title="Cleon OpenAPI",
    description="Cleon OpenAPI documentation for REST requests. See http://localhost:8000/api/v1/docs/asyncapi/v3 for Websocket API documentation.",
    docs_url="/docs/openapi/v3/"
)

rest_api_v1.add_router("/conversations/", conversations_router)
rest_api_v1.add_router("/users/", users_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", rest_api_v1.urls),
    path("api/v1/docs/asyncapi/v3/", lambda request: redirect(
        "https://studio.asyncapi.com/?share=4594dc10-eb4a-4c8b-8f38-1f0338c70afe"), name="asyncapi"),
]
