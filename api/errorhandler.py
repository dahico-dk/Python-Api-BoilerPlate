from flask import jsonify
from auth.auth import AuthError


def set_handler(app):
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "error": 404,
            "message": "resource not found",
            "success": False
        })

    @app.errorhandler(405)
    def handle_405(e):
        return jsonify({
            "error": 405,
            "message": "method not allowed",
            "success": False
        })

    @app.errorhandler(408)
    def handle_408(e):
        return jsonify({
            "error": 408,
            "message": "request time out",
            "success": False
        })

    @app.errorhandler(413)
    def handle_413(e):
        return jsonify({
            "error": 413,
            "message": "Payload Too Large",
            "success": False
        })

    @app.errorhandler(429)
    def handle_429(e):
        return jsonify({
            "error": 429,
            "message": "Payload Too Large",
            "success": False
        })

    @app.errorhandler(403)
    def handle_403(e):
        return jsonify({
            "error": 403,
            "message": "403 Forbidden",
            "success": False
        })

    @app.errorhandler(422)
    def handle_422(e):
        return jsonify({
            "error": 422,
            "message": "422 Unprocessable Entity",
            "success": False
        })

    @app.errorhandler(AuthError)
    def autherror(error):
        error_details = error.error
        error_status_code = error.status_code
        return jsonify({
            'success': False,
            'error': error_status_code,
            'message': error_details['description']
        }), error_status_code

    return app
