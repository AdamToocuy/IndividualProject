from flask import Blueprint, request
from markupsafe import escape
from geo_search import search_address_suggestions

hints_bp = Blueprint('hints', __name__)


@hints_bp.route('/api/hints-streets', methods=['GET'])
def get_street_hints():
    query = request.args.get('q', '').strip()
    region = request.args.get('region', '').strip()
    city = request.args.get('city', '').strip()

    if len(query) < 2:
        return ''

    suggestions = search_address_suggestions(query=query, region=region, city=city)
    if not suggestions:
        return ''

    html_rows = []
    for item in suggestions:
        street = escape(item.get('text') or item.get('label', ''))
        district = escape(item.get('district', 'unknown'))
        lat = escape(item.get('lat', ''))
        lon = escape(item.get('lon', ''))
        district_label = f"Район: {district}" if district != 'unknown' else ''

        row = (
            f'<div style="padding: 8px 12px; cursor: pointer; border-bottom: 1px solid #343a40; '
            f'color: #f8f9fa; background-color: #212529;" '
            f'onmouseover="this.style.backgroundColor=\'#343a40\'" '
            f'onmouseout="this.style.backgroundColor=\'#212529\'" '
            f'onclick="selectStreet(\'{street}\', \'{district}\', \'{lat}\', \'{lon}\', \'{district_label}\')">'
            f'{street}</div>'
        )
        html_rows.append(row)

    return ''.join(html_rows)
