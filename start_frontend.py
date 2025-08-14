#!/usr/bin/env python3
"""
前端开发服务器启动脚本
"""

import sys
import subprocess
import os

def check_dependencies():
    """检查前端依赖"""
    if not os.path.exists('frontend/package.json'):
        print("❌ 未找到前端项目目录")
        return False
    
    if not os.path.exists('frontend/node_modules'):
        print("📦 安装前端依赖...")
        try:
            subprocess.run(['npm', 'install'], cwd='frontend', check=True)
            print("✅ 前端依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 前端依赖安装失败")
            return False
    
    return True

def main():
    print("="*50)
    print("🎨 风水命理大师 - 前端开发服务器")
    print("="*50)
    
    # 检查Node.js
    try:
        subprocess.run(['node', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到Node.js，请先安装Node.js 18+")
        sys.exit(1)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    print("🚀 启动前端开发服务器...")
    print("📡 前端将在 http://localhost:3000 启动")
    print("🔗 请确保后端API服务已启动")
    print("💡 如需修改API地址，请编辑 frontend/.env.local")
    print()
    print("按 Ctrl+C 停止服务")
    print("="*50)
    
    try:
        # 启动前端开发服务器
        subprocess.run(['npm', 'run', 'dev'], cwd='frontend', check=True)
    except KeyboardInterrupt:
        print("\n⏹️ 前端服务已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端服务启动失败: {e}")

if __name__ == "__main__":
    main()
