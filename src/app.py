import os
import math
import urllib.parse
import urllib.request
from flask import Flask, render_template, request, abort, Response
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cosmos DB configuration
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "LegoDatabase")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "legoSets")

if not COSMOS_ENDPOINT:
    raise RuntimeError(
        "COSMOS_ENDPOINT is not set. Copy src/.env.sample to src/.env and set "
        "COSMOS_ENDPOINT to your Cosmos DB account endpoint "
        "(e.g. https://<your-cosmos-account>.documents.azure.com:443/)."
    )

ITEMS_PER_PAGE = 24


def get_container():
    client_id = os.environ.get("AZURE_CLIENT_ID")
    if client_id:
        credential = ManagedIdentityCredential(client_id=client_id)
    else:
        credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
    database = client.get_database_client(COSMOS_DATABASE)
    return database.get_container_client(COSMOS_CONTAINER)


def query_cosmos(query, parameters=None, max_count=None):
    container = get_container()
    kwargs = {
        "query": query,
        "enable_cross_partition_query": True,
    }
    if parameters:
        kwargs["parameters"] = parameters
    if max_count:
        kwargs["max_item_count"] = max_count
    return list(container.query_items(**kwargs))


@app.route("/")
def home():
    # Featured sets — large popular sets
    featured = query_cosmos(
        "SELECT TOP 8 * FROM c WHERE c.number_of_parts > 2000 ORDER BY c.number_of_parts DESC"
    )
    # Stats
    stats = query_cosmos("SELECT VALUE COUNT(1) FROM c")
    total_sets = stats[0] if stats else 0
    theme_count = query_cosmos("SELECT VALUE COUNT(1) FROM (SELECT DISTINCT c.theme_name FROM c)")
    total_themes = theme_count[0] if theme_count else 0
    return render_template("home.html", featured=featured, total_sets=total_sets, total_themes=total_themes)


@app.route("/browse")
def browse():
    search = request.args.get("q", "").strip()
    theme = request.args.get("theme", "").strip()
    year = request.args.get("year", "").strip()
    sort = request.args.get("sort", "name")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    # Build query
    conditions = []
    parameters = []

    if search:
        conditions.append("CONTAINS(LOWER(c.name), LOWER(@search))")
        parameters.append({"name": "@search", "value": search})
    if theme:
        conditions.append("c.theme_name = @theme")
        parameters.append({"name": "@theme", "value": theme})
    if year:
        conditions.append("c.year_released = @year")
        parameters.append({"name": "@year", "value": int(year)})

    where_clause = " AND ".join(conditions)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Sort mapping
    sort_map = {
        "name": "c.name ASC",
        "year_desc": "c.year_released DESC",
        "year_asc": "c.year_released ASC",
        "parts_desc": "c.number_of_parts DESC",
        "parts_asc": "c.number_of_parts ASC",
    }
    order_by = sort_map.get(sort, "c.name ASC")

    # Count query
    count_query = f"SELECT VALUE COUNT(1) FROM c {where_clause}"
    count_result = query_cosmos(count_query, parameters or None)
    total_items = count_result[0] if count_result else 0
    total_pages = max(1, math.ceil(total_items / ITEMS_PER_PAGE))
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * ITEMS_PER_PAGE
    data_query = f"SELECT * FROM c {where_clause} ORDER BY {order_by} OFFSET {offset} LIMIT {ITEMS_PER_PAGE}"
    sets = query_cosmos(data_query, parameters or None)

    # Get all themes for the filter dropdown
    themes = query_cosmos("SELECT DISTINCT VALUE c.theme_name FROM c ORDER BY c.theme_name ASC")

    return render_template(
        "browse.html",
        sets=sets,
        themes=themes,
        search=search,
        selected_theme=theme,
        selected_year=year,
        sort=sort,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
    )


@app.route("/set/<set_id>")
def detail(set_id):
    results = query_cosmos(
        "SELECT * FROM c WHERE c.id = @id",
        parameters=[{"name": "@id", "value": set_id}],
    )
    if not results:
        abort(404)
    lego_set = results[0]

    # Get related sets from the same theme
    related = query_cosmos(
        "SELECT TOP 6 * FROM c WHERE c.theme_name = @theme AND c.id != @id ORDER BY c.number_of_parts DESC",
        parameters=[
            {"name": "@theme", "value": lego_set["theme_name"]},
            {"name": "@id", "value": set_id},
        ],
    )
    return render_template("detail.html", set=lego_set, related=related)


@app.route("/image-proxy")
def image_proxy():
    """Proxy remote images (e.g. cdn.rebrickable.com) that are blocked from
    direct browser access in some lab/network environments."""
    url = request.args.get("url", "").strip()
    if not url or not url.startswith(("http://", "https://")):
        abort(400)
    # Only allow proxying from the rebrickable CDN to avoid an open proxy.
    allowed_hosts = ("cdn.rebrickable.com",)
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        abort(400)
    if parsed.hostname not in allowed_hosts:
        abort(403)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lego-vault-proxy/1.0"})
        with urllib.request.urlopen(req, timeout=10) as upstream:
            data = upstream.read()
            content_type = upstream.headers.get("Content-Type", "image/jpeg")
    except Exception:
        abort(502)

    return Response(data, content_type=content_type, headers={"Cache-Control": "public, max-age=86400"})


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
