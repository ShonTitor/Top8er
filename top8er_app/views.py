from top8er_app.cached_functions import read_game_data, read_home_data, read_template_data, read_templates_metadata, read_games_data, slug_to_code
from top8er_app.generar.getsets import sgg_data, challonge_data, tonamel_data, parrygg_data
from .forms import identify_slug
from .utils import graphic_from_request, response_from_json
from .generar.perro2 import generate_graphic
from .validators import validate_options, validate_players

from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.html import escape
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import BlogPost, Category, Author

from io import BytesIO

import base64
import json
import logging
import re

logger = logging.getLogger(__name__)

class salu2(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            img = graphic_from_request(request, request.POST['game'], hasextra=False, icon_sizes=(64, 32), default_bg="bg")
            return Response({
                "base64_img": img
                })
        except Exception:
            logger.exception("salu2 generation failed")
            return Response({"error": "Image generation failed"}, status=500)
        
class api_game_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, game):
        game = slug_to_code(game)
        if game is None:
            return Response({}, status=404)
        game_data = read_game_data(game)
        return Response(game_data)
        
class api_template_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, template):
        if template in settings.GRAPHIC_TEMPLATES:
            template_data = read_template_data(template)
            return Response(template_data)
        else:
            return Response({}, status=404)

class api_games(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(read_games_data())

class api_templates(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(read_templates_metadata())
    
class api_home_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        home_data = read_home_data()
        return Response(home_data)

class api_tournament_data(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        url = request.GET.get("url")
        game = slug_to_code(request.GET.get("game", ""))

        if not url:
            return Response({"error": "Missing 'url' query parameter"}, status=400)

        slug_type, slug = identify_slug(url)

        if slug_type is None:
            return Response({"error": "Unrecognized tournament URL"}, status=400)

        try:
            data_functions = {
                "startgg": lambda s: sgg_data(s, game),
                "challonge": challonge_data,
                "tonamel": tonamel_data,
                "parrygg": parrygg_data,
            }
            data = data_functions[slug_type](slug)
        except Exception:
            logger.exception("Tournament data fetch failed")
            return Response({"error": "Could not retrieve tournament data"}, status=500)

        if data is None or data is False:
            return Response({"error": "Could not retrieve tournament data"}, status=404)

        return Response(data)

class api_generate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, template, game):

        game = slug_to_code(game)
        template_data = read_template_data(template, complete=True)
        game_data = read_game_data(game) if game else None

        if template_data is None or game_data is None:
            return Response({}, status=404)
        
        if type(request.data) is dict:
            request_data = request.data
        else:
            if "data" not in request.data:
                return Response("Content type must either be 'application/json' or include a 'data' key with json content", 
                                status=400)
            try:
                request_data = json.loads(request.data["data"])
            except Exception:
                return Response("Could not parse the value of the key 'data', must be json", status=400)
        
        player_fields = template_data["player_fields"]
        options_schema = template_data["options"]
        player_number = template_data["player_number"]

        missing_keys = [k for k in ("players", "options") if k not in request_data]
        if missing_keys:
            return Response([{"scope": "root", "field": k, "message": "This key is required"} for k in missing_keys], 400)

        if not isinstance(request_data.get("options"), dict):
            return Response([{"scope": "root", "field": "options", "message": "'options' must be a JSON object"}], 400)
        if not isinstance(request_data.get("players"), list):
            return Response([{"scope": "root", "field": "players", "message": "'players' must be a JSON array"}], 400)

        options_data, opt_errors = validate_options(request_data["options"], options_schema, request.FILES)

        players_data = request_data["players"]
        if len(players_data) != player_number:
            return Response([{
                "scope": "root",
                "field": "players",
                "message": f"Number of players doesn't match, must be {player_number}"
            }], 400)

        if opt_errors:
            return Response(opt_errors, 400)

        validated_players, player_errors = validate_players(
            players_data, player_fields, player_number, game_data, request.FILES, game=game
        )

        if player_errors:
            return Response(player_errors, 400)

        data = {
            "game": game,
            "template": template,
            "players": validated_players,
            "options": options_data,
        }

        try:
            img = generate_graphic(data)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            b64_img = base64.b64encode(buffered.getvalue())
        except Exception:
            logger.exception("Graphic generation failed")
            return Response({"error": "Graphic generation failed"}, status=500)
        return Response({"base64_img": b64_img})

def response_from_game_path(game):
    return lambda x: response_from_json(x, game)

def react_view(request):
    response = render(request, 'index.html')

    blog_post_match = re.match(r'^/beta/blog/(?!category/|author/)([^/]+?)/?$', request.path)
    if blog_post_match:
        slug = blog_post_match.group(1)
        try:
            post = BlogPost.objects.get(slug=slug, published=True)
            og_parts = [
                '<meta property="og:type" content="article">',
                f'<meta property="og:title" content="{escape(post.title)}">',
                f'<meta property="og:url" content="{request.build_absolute_uri()}">',
            ]
            if post.excerpt:
                og_parts.append(f'<meta property="og:description" content="{escape(post.excerpt)}">')
            if post.main_image:
                og_parts.append(f'<meta property="og:image" content="{request.build_absolute_uri(post.main_image.url)}">')
            og_html = '\n    '.join(og_parts)
            content = response.content.decode('utf-8')
            response.content = content.replace('</head>', f'    {og_html}\n  </head>', 1).encode()
        except BlogPost.DoesNotExist:
            pass

    return response


def _make_content_urls_absolute(content, request):
    """Rewrite relative src attributes in HTML content to absolute URLs."""
    return re.sub(
        r'src="(/[^"]*)"',
        lambda m: f'src="{request.build_absolute_uri(m.group(1))}"',
        content,
    )

def _abs_url(request, file_field):
    if not file_field:
        return None
    return request.build_absolute_uri(file_field.url)

def _serialize_post_summary(post, request):
    return {
        'title': post.title,
        'slug': post.slug,
        'excerpt': post.excerpt,
        'published_at': post.published_at or post.created_at,
        'main_image': _abs_url(request, post.main_image),
        'categories': list(post.categories.values('name', 'slug')),
        'author': _serialize_author_brief(post.author, request) if post.author else None,
    }

def _serialize_author_brief(author, request):
    if author is None:
        return None
    return {
        'username': author.user.username if author.user else None,
        'display_name': author.display_name,
        'profile_picture': _abs_url(request, author.profile_picture),
    }

def _serialize_author_full(author, request):
    return {
        'username': author.user.username if author.user else None,
        'display_name': author.display_name,
        'profile_picture': _abs_url(request, author.profile_picture),
        'description': author.description,
        'twitter': author.twitter,
        'instagram': author.instagram,
        'twitch': author.twitch,
        'youtube': author.youtube,
        'bluesky': author.bluesky,
        'discord': author.discord,
    }

def _get_published_posts():
    return BlogPost.objects.filter(published=True).select_related('author__user').prefetch_related('categories')


PAGE_SIZE = 10

class api_flags(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(settings.FLAGS)


class api_blog_list(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = _get_published_posts()
        q = request.GET.get('q', '').strip()
        category = request.GET.get('category', '').strip()
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(content__icontains=q) | qs.filter(excerpt__icontains=q)
        if category:
            qs = qs.filter(categories__slug=category)
        qs = qs.distinct()

        paginator = Paginator(qs, PAGE_SIZE)
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        page = max(1, min(page, paginator.num_pages))
        page_obj = paginator.page(page)

        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'page': page,
            'results': [_serialize_post_summary(p, request) for p in page_obj],
        })


class api_blog_categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cats = Category.objects.filter(posts__published=True).distinct()
        return Response(list(cats.values('name', 'slug')))


class api_blog_by_category(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            cat = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        qs = _get_published_posts().filter(categories=cat)
        paginator = Paginator(qs, PAGE_SIZE)
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        page = max(1, min(page, paginator.num_pages or 1))
        page_obj = paginator.page(page)
        return Response({
            'category': {'name': cat.name, 'slug': cat.slug},
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'page': page,
            'results': [_serialize_post_summary(p, request) for p in page_obj],
        })


class api_blog_by_author(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        try:
            author = Author.objects.select_related('user').get(user__username=username)
        except Author.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        qs = _get_published_posts().filter(author=author)
        paginator = Paginator(qs, PAGE_SIZE)
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        page = max(1, min(page, paginator.num_pages or 1))
        page_obj = paginator.page(page)
        return Response({
            'author': _serialize_author_full(author, request),
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'page': page,
            'results': [_serialize_post_summary(p, request) for p in page_obj],
        })


class api_blog_post(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            post = _get_published_posts().get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        data = _serialize_post_summary(post, request)
        data['content'] = _make_content_urls_absolute(post.content, request)
        if post.author:
            data['author'] = _serialize_author_full(post.author, request)
        return Response(data)