#!/usr/bin/env python3
"""
全栈应用启动脚本
同时启动后端API和前端开发服务器
"""

import sys
import subprocess
import threading
import time
import os
import socket
import random

def find_free_port():
    """在8000-9000范围内查找可用端口"""
    # 优选端口列表
    preferred_ports = [8080, 8081, 8082, 8888, 8000, 8001, 8002]
    
    # 首先尝试优选端口
    for port in preferred_ports:
        if 8000 <= port <= 9000:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                continue
    
    # 如果优选端口都不可用，随机选择
    for _ in range(50):
        port = random.randint(8003, 8999)  # 避开常用端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    
    raise RuntimeError("无法在8000-9000范围内找到可用端口")

def start_backend(port):
    """启动后端服务"""
    print(f"🔧 启动后端API服务在端口 {port}...")
    
    # 设置环境变量
    env = os.environ.copy()
    env['FLASK_PORT'] = str(port)
    
    try:
        # 启动后端
        subprocess.run([sys.executable, "backend_api.py"], 
                      env=env, check=True)
    except KeyboardInterrupt:
        print("⏹️ 后端服务已停止")
    except Exception as e:
        print(f"❌ 后端服务错误: {e}")

def start_frontend(backend_port):
    """启动前端服务"""
    print("🎨 启动前端开发服务器...")
    
    try:
        # 切换到前端目录
        os.chdir('frontend')
        
        # 设置环境变量
        env = os.environ.copy()
        env['NEXT_PUBLIC_API_URL'] = f'http://localhost:{backend_port}'
        
        # 安装依赖
        print("📦 安装前端依赖...")
        subprocess.run(['npm', 'install'], check=True, capture_output=True)
        
        # 启动前端
        subprocess.run(['npm', 'run', 'dev'], env=env, check=True)
        
    except KeyboardInterrupt:
        print("⏹️ 前端服务已停止")
    except Exception as e:
        print(f"❌ 前端服务错误: {e}")

def main():
    print("="*60)
    print("🏮 风水命理大师 - 全栈应用启动器")
    print("="*60)
    
    # 检查依赖
    if not os.path.exists('backend_api.py'):
        print("❌ 未找到后端文件 backend_api.py")
        sys.exit(1)
    
    if not os.path.exists('frontend/package.json'):
        print("❌ 未找到前端项目目录")
        sys.exit(1)
    
    # 查找可用端口
    try:
        backend_port = find_free_port()
        print(f"✅ 选择后端端口: {backend_port}")
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # 安装后端依赖
    print("📦 安装后端依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ 后端依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ 后端依赖安装失败")
        sys.exit(1)
    
    print()
    print("🚀 启动服务...")
    print(f"📡 后端API: http://localhost:{backend_port}")
    print("📡 前端界面: http://localhost:3000")
    print()
    print("💡 两个服务将同时启动，按 Ctrl+C 停止所有服务")
    print("="*60)
    
    try:
        # 在后台启动后端
        backend_thread = threading.Thread(target=start_backend, args=(backend_port,))
        backend_thread.daemon = True
        backend_thread.start()
        
        # 等待后端启动
        time.sleep(3)
        
        # 启动前端（主线程）
        start_frontend(backend_port)
        
    except KeyboardInterrupt:
        print("\n⏹️ 正在停止所有服务...")
        print("✅ 服务已停止")

if __name__ == "__main__":
    main()
