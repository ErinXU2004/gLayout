#!/bin/bash
# Docker启动脚本 - 用于Mac上的IIC-OSIC-TOOLS
# 基于 https://github.com/iic-jku/iic-osic-tools

# 设置默认值
DESIGNS=${DESIGNS:-"/Users/hua/Desktop/gLayout/glayout"}
DOCKER_USERNAME=${DOCKER_USERNAME:-"root"}
DOCKER_TAG=${DOCKER_TAG:-"latest"}
CONTAINER_NAME=${CONTAINER_NAME:-"iic-osic-tools-polyres-test"}

# X11相关设置 (Mac需要XQuartz)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到macOS系统"
    
    # 检查XQuartz是否运行
    if ! pgrep -x "XQuartz" > /dev/null; then
        echo "⚠  XQuartz未运行，请先启动XQuartz:"
        echo "   1. 打开XQuartz应用"
        echo "   2. 在XQuartz偏好设置中启用'Allow connections from network clients'"
        echo "   3. 重启XQuartz"
        echo ""
        echo "继续运行脚本..."
    fi
    
    # 设置DISPLAY
    export DISPLAY=${DISPLAY:-":0"}
    echo "DISPLAY设置为: $DISPLAY"
fi

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "✗ Docker未运行，请启动Docker Desktop"
    exit 1
fi

echo "✓ Docker运行正常"

# 停止并删除现有容器（如果存在）
if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "停止并删除现有容器: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME} > /dev/null 2>&1
    docker rm ${CONTAINER_NAME} > /dev/null 2>&1
fi

echo "启动IIC-OSIC-TOOLS容器..."
echo "设计目录: ${DESIGNS}"
echo "容器名称: ${CONTAINER_NAME}"

# 启动容器
docker run -it --rm \
    --name ${CONTAINER_NAME} \
    --user $(id -u):$(id -g) \
    -e DISPLAY=${DISPLAY} \
    -v "${DESIGNS}:/workspace" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    hpretl/iic-osic-tools:${DOCKER_TAG} \
    --x11 --wait bash -c "
        echo '=== IIC-OSIC-TOOLS容器启动成功 ==='
        echo '工作目录: /workspace'
        echo '当前用户: \$(whoami)'
        echo 'Python版本: \$(python3 --version)'
        echo ''
        echo '可用的EDA工具:'
        echo '- Klayout: \$(klayout --version 2>/dev/null || echo '未找到')'
        echo '- Magic: \$(magic --version 2>/dev/null || echo '未找到')'
        echo '- Netgen: \$(netgen --version 2>/dev/null || echo '未找到')'
        echo ''
        echo '运行测试脚本:'
        echo 'cd /workspace && python3 docker_polyres_test.py'
        echo ''
        bash
    "

echo "容器已退出"
