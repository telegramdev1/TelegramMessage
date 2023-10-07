from flask import Flask, request
import config
import tgMessage_sender
import asyncio

app = Flask(__name__)


@app.route('/api/query', methods=['GET'])
def query_data():
    try:
        current = int(request.args.get("current"))
        pageSize = int(request.args.get("pageSize"))
        startTime = request.args.get("startTime")
        endTime = request.args.get("endTime")
        data = {"sender_id": request.args.get("sender_id"), "username": request.args.get("username"),
                "group_username": request.args.get("group_username"), "send_flag": request.args.get("send_flag"),
                "message": request.args.get("message")}
        result, total = config.query_message(current, pageSize, data, startTime, endTime)
        data_dict = {"data": result, "page": current, "success": True, "total": total}
        return data_dict
    except Exception as e:
        config.logging.exception(e)
        return {"data": {}, "success": False}


@app.route('/api/resend', methods=['GET'])
def resend_message():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        id = int(request.args.get('id'))
        tgMessage_sender.resend_message(id)
        return {'success': True}
    except Exception as e:
        config.logging.exception(e)
        return {'success': False}


if __name__ == '__main__':
    app.run(port=8686)
