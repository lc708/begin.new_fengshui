#!/usr/bin/env python3
"""
后端API服务启动脚本
"""

import sys
import subprocess
import os
import signal

def check_port_available(port):
    """检查端口是否可用"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        return True
    except OSError:
        return False

def kill_existing_services():
    """停止已存在的服务"""
    try:
        subprocess.run(['pkill', '-f', 'backend_api.py'], capture_output=True)
        print("🔄 停止已存在的服务...")
    except:
        pass

def main():
    print("="*50)
    print("🏮 风水命理大师 - 后端API服务")
    print("="*50)
    
    # 停止已存在的服务
    kill_existing_services()
    
    # 使用固定端口
    preferred_ports = [8080, 8081, 8082, 8888, 8000]
    port = None
    
    for p in preferred_ports:
        if check_port_available(p):
            port = p
            break
    
    if port is None:
        print("❌ 所有优选端口都不可用")
        sys.exit(1)
    
    print(f"✅ 选择端口: {port}")
    
    # 设置环境变量
    env = os.environ.copy()
    env['FLASK_PORT'] = str(port)
    
    print(f"🚀 启动后端服务在端口 {port}...")
    print(f"📡 API地址: http://localhost:{port}")
    print(f"📝 前端配置: NEXT_PUBLIC_API_URL=http://localhost:{port}")
    print()
    print("💡 按 Ctrl+C 停止服务")
    print("="*50)
    
    try:
        # 启动服务
        subprocess.run([sys.executable, "backend_api.py"], env=env, check=True)
    except KeyboardInterrupt:
        print("\n⏹️ 服务已停止")
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")

if __name__ == "__main__":
    main()
