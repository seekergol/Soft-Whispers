from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
# 允许所有来源的跨域请求，以确保最大的兼容性
CORS(app)

# 解决浏览器缓存问题
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# MySQL数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': '123456', # 如果您的MySQL root用户设置了密码，请务必填写
    'database': 'dreamtales'
}

@app.route('/')
def serve_landing_page():
    """提供前端HTML页面"""
    logger.info("请求首页")
    return send_from_directory('.', 'bedtime_story_landing.html')

@app.route('/privacy.html')
def serve_privacy_page():
    """提供隐私政策页面"""
    logger.info("请求隐私政策页面")
    return send_from_directory('.', 'privacy.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    """处理订阅请求，将邮箱存入数据库。"""
    logger.info("收到订阅请求")
    data = request.get_json()
    if not data or 'email' not in data or not data['email']:
        logger.warning("请求中缺少邮箱地址")
        return jsonify({'success': False, 'message': '邮箱地址不能为空。'}), 400

    email = data['email']
    logger.info(f"处理邮箱: {email}")
    
    conn = None # 初始化 conn
    try:
        logger.info("尝试连接数据库")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 检查表是否存在，如果不存在则创建
        logger.info("检查user_subscriptions表是否存在")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `user_subscriptions` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `email` VARCHAR(255) NOT NULL UNIQUE,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()
        
        # 检查邮箱是否已存在
        logger.info("检查邮箱是否已存在")
        cursor.execute("SELECT email FROM user_subscriptions WHERE email = %s", (email,))
        if cursor.fetchone():
            logger.info(f"邮箱 {email} 已存在")
            return jsonify({'success': False, 'message': '您已预约过啦，请直接在邮箱查看我们的消息！'}), 200

        # 插入新用户
        logger.info(f"插入新邮箱: {email}")
        insert_query = "INSERT INTO user_subscriptions (email) VALUES (%s)"
        cursor.execute(insert_query, (email,))
        conn.commit()
        logger.info("数据库事务已提交。")

        # 立刻验证写入是否成功
        cursor.execute("SELECT id FROM user_subscriptions WHERE email = %s", (email,))
        if not cursor.fetchone():
            logger.critical(f"严重错误：刚刚提交的邮箱 {email} 在数据库中未找到！事务可能已回滚或未生效。")
            return jsonify({'success': False, 'message': '服务器内部错误：无法保存您的订阅信息。'}), 500
        
        logger.info(f"验证成功：邮箱 {email} 已确认写入数据库。")
        
        logger.info("邮箱订阅成功")
        return jsonify({'success': True, 'message': '太棒了！我们已收到您的预约，专属故事将很快通过邮件发送给您。'})

    except mysql.connector.Error as err:
        logger.error(f"数据库错误: {err}")
        if err.errno == 1045: # Access denied
            return jsonify({'success': False, 'message': '数据库认证失败，请检查用户名或密码。'}), 500
        elif err.errno == 1049: # Unknown database
             return jsonify({'success': False, 'message': '数据库不存在，请先创建。'}), 500
        else:
            return jsonify({'success': False, 'message': f'服务器出现未知数据库错误: {err}'}), 500
    except Exception as e:
        logger.error(f"处理订阅时发生未知错误: {e}", exc_info=True)
        return jsonify({'success': False, 'message': '服务器出现了一个未知错误，请联系技术支持。'}), 500
    finally:
        # 确保无论成功或失败，连接都会被关闭
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            logger.info("数据库连接已关闭")

@app.route('/test')
def serve_test_page():
    """提供测试页面"""
    logger.info("请求测试页面")
    return send_from_directory('.', 'button_test.html')

if __name__ == '__main__':
    logger.info("启动Flask应用")
    # 启动Flask应用, debug=True 会让服务器在代码更改后自动重启
    app.run(debug=True,host="0.0.0.0", port=5000) 
