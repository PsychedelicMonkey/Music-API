from flask import jsonify, request, url_for, current_app
import string

def paginate_query(query, schema, endpoint, **kwargs):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['ITEMS_PER_PAGE'], type=int), current_app.config['MAX_ITEMS_PER_PAGE'])
    order_by = request.args.get('order_by', 'id', type=str)
    resources = query.order_by(order_by).paginate(page, per_page, False)
    return jsonify({
        'items': schema.dump(resources.items),
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': resources.pages,
            'total_items': resources.total,
            'order_by': order_by,
        },
        '_links': {
            'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
            'next': url_for(endpoint, page=resources.next_num, per_page=per_page, **kwargs) if resources.has_next else None,
            'prev': url_for(endpoint, page=resources.prev_num, per_page=per_page, **kwargs) if resources.has_prev else None,
        },
    })