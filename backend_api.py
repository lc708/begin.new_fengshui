"""
风水命理应用后端API服务
基于Flask提供RESTful API接口，连接MACore业务逻辑与前端界面
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flow import create_fengshui_analysis_flow, create_bazi_only_flow, create_fengshui_consultation_flow, create_quick_daily_flow
from utils.calendar_query import get_daily_fortune, find_auspicious_days
import traceback
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# 配置CORS支持生产环境
CORS(app, 
     origins=['https://app-fengshui.begin.new', 'http://localhost:3000'],
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "message": "风水命理大师API服务运行正常",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bazi/basic', methods=['POST'])
def analyze_bazi_basic():
    """八字基础信息分析（快速响应）"""
    try:
        data = request.get_json()
        logger.info(f"收到八字基础分析请求: {data}")
        
        # 验证输入数据
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'gender', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必要字段: {field}"
                }), 400
        
        # 构造共享存储
        shared = {
            "user_info": {
                "name": data['name'],
                "birth_date": {
                    "year": int(data['year']),
                    "month": int(data['month']),
                    "day": int(data['day']),
                    "hour": int(data['hour'])
                },
                "gender": data['gender'],
                "location": data['location']
            },
            "service_type": "api_bazi_basic"
        }
        
        # 只运行用户信息收集和八字计算，不做LLM分析
        from nodes import UserInfoCollectionNode, BaziCalculationNode
        user_node = UserInfoCollectionNode()
        bazi_node = BaziCalculationNode()
        
        # 手动执行节点，跳过LLM分析
        user_prep = user_node.prep(shared)
        user_exec = user_node.exec(user_prep)
        user_node.post(shared, user_prep, user_exec)
        
        bazi_prep = bazi_node.prep(shared)
        bazi_exec = bazi_node.exec(bazi_prep)
        bazi_node.post(shared, bazi_prep, bazi_exec)
        
        # 提取基础结果
        response_data = {
            "success": True,
            "data": {
                "user_info": shared.get("user_info"),
                "bazi_result": shared.get("bazi_result")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("八字基础分析完成")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"八字基础分析出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"基础分析过程出错: {str(e)}"
        }), 500

@app.route('/api/bazi/analysis', methods=['POST'])
def analyze_bazi_personality():
    """八字命理分析（LLM分析）"""
    try:
        data = request.get_json()
        logger.info(f"收到八字命理分析请求")
        
        # 需要包含基础八字信息
        required_fields = ['user_info', 'bazi_result']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必要字段: {field}"
                }), 400
        
        # 构造共享存储
        shared = {
            "user_info": data['user_info'],
            "bazi_result": data['bazi_result'],
            "service_type": "api_bazi_analysis"
        }
        
        # 只运行LLM命理分析
        from nodes import FortuneAnalysisNode
        analysis_node = FortuneAnalysisNode()
        
        analysis_prep = analysis_node.prep(shared)
        analysis_exec = analysis_node.exec(analysis_prep)
        analysis_node.post(shared, analysis_prep, analysis_exec)
        
        # 提取分析结果
        response_data = {
            "success": True,
            "data": {
                "analysis_result": shared.get("analysis_result")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("八字命理分析完成")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"八字命理分析出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"命理分析过程出错: {str(e)}"
        }), 500

@app.route('/api/bazi/analyze', methods=['POST'])
def analyze_bazi():
    """八字完整分析API接口（兼容性保留）"""
    try:
        data = request.get_json()
        logger.info(f"收到八字分析请求: {data}")
        
        # 验证输入数据
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'gender', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必要字段: {field}"
                }), 400
        
        # 构造共享存储
        shared = {
            "user_info": {
                "name": data['name'],
                "birth_date": {
                    "year": int(data['year']),
                    "month": int(data['month']),
                    "day": int(data['day']),
                    "hour": int(data['hour'])
                },
                "gender": data['gender'],
                "location": data['location']
            },
            "service_type": "api_bazi"
        }
        
        # 运行八字分析流程
        flow = create_bazi_only_flow()
        flow.run(shared)
        
        # 提取结果
        response_data = {
            "success": True,
            "data": {
                "user_info": shared.get("user_info"),
                "bazi_result": shared.get("bazi_result"),
                "analysis_result": shared.get("analysis_result")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("八字分析完成")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"八字分析出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"分析过程出错: {str(e)}"
        }), 500

@app.route('/api/fengshui/advice', methods=['POST'])
def get_fengshui_advice():
    """风水建议API接口"""
    try:
        data = request.get_json()
        logger.info(f"收到风水咨询请求: {data}")
        
        # 处理简单的方位查询，不需要八字计算
        if 'query' in data and data['query'].get('type') == 'direction_analysis':
            direction = data['query'].get('direction', '东')
            
            # 使用简化的方位建议逻辑，不依赖用户八字
            from utils.fengshui_advisor import get_direction_advice
            advice = get_direction_advice(direction)
            
            response_data = {
                "success": True,
                "data": {
                    "fengshui_advice": advice,
                    "user_info": data.get('user_info', {})
                },
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("方位风水建议生成完成")
            return jsonify(response_data)
        
        # 可以接收已有的八字信息，或重新计算（用于完整分析）
        if 'bazi_result' in data:
            # 使用已有八字结果
            shared = {
                "user_info": data.get('user_info', {}),
                "bazi_result": data['bazi_result'],
                "analysis_result": data.get('analysis_result', {}),
                "service_type": "api_fengshui"
            }
        else:
            # 重新计算八字
            shared = {
                "user_info": data.get('user_info', {}),
                "service_type": "api_fengshui"
            }
            # 运行完整流程到风水建议
            flow = create_fengshui_consultation_flow()
            flow.run(shared)
        
        # 如果有完整八字信息，使用完整的风水建议
        if 'bazi_result' in shared and 'analysis_result' in shared:
            from nodes import FengshuiAdviceNode
            fengshui_node = FengshuiAdviceNode()
            
            prep_data = fengshui_node.prep(shared)
            advice = fengshui_node.exec(prep_data)
            shared["fengshui_advice"] = advice
        
        response_data = {
            "success": True,
            "data": {
                "fengshui_advice": shared.get("fengshui_advice"),
                "user_info": shared.get("user_info")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("风水建议生成完成")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"风水咨询出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"咨询过程出错: {str(e)}"
        }), 500

@app.route('/api/daily/fortune', methods=['GET'])
def get_daily_fortune_api():
    """每日运势API接口"""
    try:
        date = request.args.get('date', datetime.now().strftime("%Y-%m-%d"))
        user_bazi = request.args.get('user_bazi')  # 可选的用户八字信息
        
        logger.info(f"查询日期 {date} 的运势")
        
        # 解析用户八字（如果提供）
        parsed_bazi = None
        if user_bazi:
            import json
            try:
                parsed_bazi = json.loads(user_bazi)
            except:
                parsed_bazi = None
        
        # 获取当日运势
        daily_info = get_daily_fortune(date, parsed_bazi)
        
        response_data = {
            "success": True,
            "data": daily_info,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"每日运势查询完成: {date}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"每日运势查询出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"查询过程出错: {str(e)}"
        }), 500

@app.route('/api/daily/auspicious', methods=['GET'])
def get_auspicious_days_api():
    """吉日查询API接口"""
    try:
        start_date = request.args.get('start_date', datetime.now().strftime("%Y-%m-%d"))
        end_date = request.args.get('end_date')
        activity_type = request.args.get('activity_type', 'general')
        
        if not end_date:
            from datetime import timedelta
            end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        logger.info(f"查询 {start_date} 到 {end_date} 的 {activity_type} 吉日")
        
        # 查找吉日
        auspicious_days = find_auspicious_days(start_date, end_date, activity_type)
        
        response_data = {
            "success": True,
            "data": {
                "auspicious_days": auspicious_days,
                "query_params": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "activity_type": activity_type
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"吉日查询完成，找到 {len(auspicious_days)} 个吉日")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"吉日查询出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"查询过程出错: {str(e)}"
        }), 500

@app.route('/api/analyze/complete', methods=['POST'])
def complete_analysis():
    """完整分析API接口"""
    try:
        data = request.get_json()
        logger.info(f"收到完整分析请求: {data.get('user_info', {}).get('name', 'Unknown')}")
        
        # 验证输入数据
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'gender', 'location']
        user_info = data.get('user_info', data)  # 兼容不同的数据格式
        
        for field in required_fields:
            if field not in user_info:
                return jsonify({
                    "success": False,
                    "error": f"缺少必要字段: {field}"
                }), 400
        
        # 构造共享存储
        shared = {
            "user_info": {
                "name": user_info['name'],
                "birth_date": {
                    "year": int(user_info['year']),
                    "month": int(user_info['month']),
                    "day": int(user_info['day']),
                    "hour": int(user_info['hour'])
                },
                "gender": user_info['gender'],
                "location": user_info['location']
            },
            "service_type": "api_complete"
        }
        
        # 运行完整分析流程
        flow = create_fengshui_analysis_flow()
        flow.run(shared)
        
        # 提取完整结果
        response_data = {
            "success": True,
            "data": {
                "user_info": shared.get("user_info"),
                "bazi_result": shared.get("bazi_result"),
                "analysis_result": shared.get("analysis_result"),
                "fengshui_advice": shared.get("fengshui_advice"),
                "daily_info": shared.get("daily_info"),
                "final_report": shared.get("final_report")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("完整分析完成")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"完整分析出错: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"分析过程出错: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        "success": False,
        "error": "API接口不存在",
        "available_endpoints": [
            "/api/health",
            "/api/bazi/analyze",
            "/api/fengshui/advice", 
            "/api/daily/fortune",
            "/api/daily/auspicious",
            "/api/analyze/complete"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        "success": False,
        "error": "服务器内部错误"
    }), 500

def find_free_port():
    """查找可用端口，优先支持生产环境"""
    import socket
    import random
    
    # Railway/生产环境使用PORT环境变量
    railway_port = os.getenv('PORT')
    if railway_port:
        try:
            return int(railway_port)  # Railway会确保端口可用
        except ValueError:
            print(f"⚠️ 无效的PORT环境变量: {railway_port}")
    
    # 首先尝试一些固定的优选端口（开发环境）
    preferred_ports = [8080, 8081, 8082, 8888, 8000, 8001, 8002]
    
    # 检查优选端口
    for port in preferred_ports:
        if 8000 <= port <= 9000:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                continue
    
    # 如果优选端口都不可用，则随机选择
    for _ in range(100):  # 减少尝试次数
        port = random.randint(8000, 9000)
        if port not in preferred_ports:  # 避免重复检查
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                continue
    
    raise RuntimeError("无法在8000-9000范围内找到可用端口")

if __name__ == '__main__':
    print("🌟 启动风水命理大师API服务...")
    print("📡 API接口文档:")
    print("   GET  /api/health              - 健康检查")
    print("   POST /api/bazi/analyze        - 八字分析")
    print("   POST /api/fengshui/advice     - 风水建议")
    print("   GET  /api/daily/fortune       - 每日运势")
    print("   GET  /api/daily/auspicious    - 吉日查询")
    print("   POST /api/analyze/complete    - 完整分析")
    print()
    
    # 获取端口配置
    import os
    port = None
    
    # 1. 优先使用环境变量指定的端口
    if 'FLASK_PORT' in os.environ:
        try:
            port = int(os.environ['FLASK_PORT'])
            print(f"📌 使用环境变量指定端口: {port}")
        except ValueError:
            print("⚠️ 环境变量FLASK_PORT格式错误，将自动选择端口")
    
    # 2. 如果没有指定端口或端口不可用，自动选择
    if port is None:
        try:
            port = find_free_port()
            print(f"🎯 自动选择可用端口: {port}")
        except RuntimeError as e:
            print(f"❌ {e}")
            exit(1)
    
    # 3. 验证选择的端口是否可用
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
    except OSError:
        print(f"❌ 端口 {port} 不可用，重新选择...")
        try:
            port = find_free_port()
            print(f"🔄 重新选择端口: {port}")
        except RuntimeError as e:
            print(f"❌ {e}")
            exit(1)
    
    print(f"🚀 服务将在 http://localhost:{port} 启动")
    print("🔗 CORS已启用，支持前端跨域访问")
    print(f"📝 前端环境变量: NEXT_PUBLIC_API_URL=http://localhost:{port}")
    print()
    print("💡 提示:")
    print(f"   - 要固定端口，请设置环境变量: export FLASK_PORT={port}")
    print("   - 按 Ctrl+C 停止服务")
    print("="*60)
    
    # 启动服务（关闭调试模式中的自动重载）
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=False,  # 关闭调试模式避免自动重启
        use_reloader=False  # 关闭自动重载
    )
