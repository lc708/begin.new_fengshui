import React, { useState } from 'react';
import Link from 'next/link';
import DigitalCompass from '../components/DigitalCompass';

const FengshuiPage: React.FC = () => {
  const [selectedDirection, setSelectedDirection] = useState<string | null>(null);
  const [advice, setAdvice] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const getDirectionAdvice = async (direction: string) => {
    setLoading(true);
    try {
      const { getFengshuiAdvice } = await import('../lib/api');
      
      // 调用真实的风水建议API（方位分析不需要用户信息）
      const result = await getFengshuiAdvice({
        query: {
          type: 'direction_analysis',
          direction: direction
        }
      });
      
      // API客户端已经解析了 response.data.data，所以直接使用 result.fengshui_advice
      if (result.fengshui_advice) {
        setAdvice(result.fengshui_advice);
      } else {
        // 如果没有找到建议数据，使用原始响应作为降级
        setAdvice(result);
      }
    } catch (error: any) {
      console.error('获取风水建议失败:', error);
      // 降级到本地建议
      const adviceMap: Record<string, any> = {
        '北': {
          element: '水',
          color: '黑色、深蓝色',
          beneficial: '事业运、智慧运',
          suggestions: ['摆放水景装饰', '使用蓝黑色调', '放置镜子或玻璃制品']
        },
        '东': {
          element: '木',
          color: '绿色、青色',
          beneficial: '健康运、家庭运',
          suggestions: ['摆放绿色植物', '使用木制家具', '保持空气流通']
        },
        '南': {
          element: '火',
          color: '红色、紫色',
          beneficial: '名声运、桃花运',
          suggestions: ['使用红色装饰', '增加照明亮度', '摆放红色花卉']
        },
        '西': {
          element: '金',
          color: '白色、金色',
          beneficial: '贵人运、财运',
          suggestions: ['摆放金属制品', '使用白色主调', '保持整洁明亮']
        },
        '东南': {
          element: '木',
          color: '绿色、青色',
          beneficial: '财运、学业运',
          suggestions: ['摆放富贵竹', '使用绿色装饰', '保持明亮通风']
        },
        '西南': {
          element: '土',
          color: '黄色、橙色',
          beneficial: '人际运、婚恋运',
          suggestions: ['摆放成双摆件', '使用暖色调', '保持温馨整洁']
        },
        '东北': {
          element: '土',
          color: '黄色、棕色',
          beneficial: '学业运、智慧运',
          suggestions: ['摆放书籍文具', '使用土色调', '保持安静整齐']
        },
        '西北': {
          element: '金',
          color: '白色、银色',
          beneficial: '事业运、权威运',
          suggestions: ['摆放金属饰品', '使用白银色调', '保持威严整洁']
        }
      };
      
      setAdvice(adviceMap[direction] || {
        element: '未知',
        color: '中性色',
        beneficial: '平衡运势',
        suggestions: ['保持空间整洁', '通风透光', '摆放绿色植物']
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDirectionSelect = (direction: string) => {
    setSelectedDirection(direction);
    getDirectionAdvice(direction);
  };

  return (
    <div className="min-h-screen bg-traditional-beige py-8">
      <div className="max-w-4xl mx-auto px-6">
        {/* 导航 */}
        <div className="mb-8">
          <Link href="/" className="text-traditional-red hover:text-red-700 font-medium">
            ← 返回首页
          </Link>
        </div>

        <h1 className="text-3xl font-serif-sc font-bold text-traditional-red text-center mb-8">
          🧭 风水罗盘
        </h1>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* 罗盘 */}
          <div>
            <DigitalCompass 
              directions={8}
              colors={["red", "gold", "black"]}
              onDirectionSelect={handleDirectionSelect}
            />
            
            <div className="mt-6 text-center">
              <p className="text-traditional-dark-green text-sm">
                点击罗盘上的方位来获取风水建议
              </p>
            </div>
          </div>

          {/* 建议面板 */}
          <div>
            {loading ? (
              <div className="traditional-card p-8 text-center">
                <div className="text-6xl mb-4">🧭</div>
                <h2 className="text-xl font-serif-sc mb-4">正在分析方位能量...</h2>
                <div className="w-full bg-traditional-gold h-2 rounded overflow-hidden">
                  <div className="w-full h-full bg-traditional-red animate-pulse"></div>
                </div>
                <p className="text-traditional-dark-green mt-4 opacity-75">
                  您选择了{selectedDirection}方位，这个方位的能量特性正在分析中...
                </p>
              </div>
            ) : !advice ? (
              <div className="traditional-card p-8 text-center">
                <div className="text-6xl mb-4">🔮</div>
                <h2 className="text-xl font-serif-sc mb-4">选择方位</h2>
                <p className="text-traditional-dark-green">
                  请在左侧罗盘上点击任意方位，获取对应的风水建议和指导。
                </p>
              </div>
            ) : (
              <div className="traditional-card p-6">
                <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                  📍 {selectedDirection}方位分析
                </h2>
                
                <div className="space-y-4">
                  <div className="flex items-center">
                    <span className="font-medium w-20">五行：</span>
                    <span className="bg-traditional-gold px-3 py-1 rounded">
                      {advice.element || '未知'}
                    </span>
                  </div>
                  
                  <div className="flex items-center">
                    <span className="font-medium w-20">颜色：</span>
                    <span className="text-traditional-dark-green">
                      {advice.color || '中性色'}
                    </span>
                  </div>
                  
                  <div className="flex items-center">
                    <span className="font-medium w-20">主运：</span>
                    <span className="text-traditional-red">
                      {advice.beneficial || '平衡运势'}
                    </span>
                  </div>
                  
                  <div>
                    <div className="font-medium mb-2">布置建议：</div>
                    <ul className="space-y-1 text-traditional-dark-green">
                      {(advice.suggestions || []).map((suggestion: string, index: number) => (
                        <li key={index}>• {suggestion}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {/* 通用建议 */}
            <div className="traditional-card p-6 mt-6">
              <h3 className="text-lg font-serif-sc font-semibold text-traditional-red mb-3">
                🏠 通用风水建议
              </h3>
              <ul className="space-y-2 text-sm text-traditional-dark-green">
                <li>• 保持居室整洁，避免杂物堆积</li>
                <li>• 确保空气流通，阳光充足</li>
                <li>• 床头靠墙，避免梁压床</li>
                <li>• 镜子不对床，避免反射煞气</li>
                <li>• 厨厕保持干净，避免异味</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="text-center mt-8">
          <Link href="/daily" className="traditional-button">
            📅 查看每日宜忌
          </Link>
        </div>
      </div>
    </div>
  );
};

export default FengshuiPage;
