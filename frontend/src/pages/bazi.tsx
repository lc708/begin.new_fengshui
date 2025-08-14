import React, { useState } from 'react';
import Link from 'next/link';
import BirthInfoForm from '../components/BirthInfoForm';

const BaziPage: React.FC = () => {
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [loadingPhase, setLoadingPhase] = useState('');

  const handleFormSubmit = async (formData: any) => {
    setLoading(true);
    setLoadingPhase('basic');
    
    try {
      const { analyzeBaziBasic, analyzeBaziPersonality } = await import('../lib/api');
      
      const userInfo = {
        name: formData.name,
        year: parseInt(formData.year),
        month: parseInt(formData.month),
        day: parseInt(formData.day),
        hour: parseInt(formData.hour),
        gender: formData.gender,
        location: formData.location
      };
      
      // 第一步：快速获取八字基础信息
      console.log('🔄 第一步：获取八字基础信息');
      const basicResult = await analyzeBaziBasic(userInfo);
      
      // 立即显示基础八字信息
      setAnalysisResult({
        user_info: basicResult.user_info,
        bazi_result: basicResult.bazi_result,
        analysis_result: null // 暂时为空
      });
      
      // 第二步：获取LLM命理分析
      setLoadingPhase('analysis');
      console.log('🔄 第二步：获取命理分析');
      const analysisResult = await analyzeBaziPersonality({
        user_info: basicResult.user_info,
        bazi_result: basicResult.bazi_result
      });
      
      // 更新完整结果
      setAnalysisResult({
        user_info: basicResult.user_info,
        bazi_result: basicResult.bazi_result,
        analysis_result: analysisResult.analysis_result
      });
      
    } catch (error: any) {
      console.error('分析失败:', error);
      alert(`分析失败: ${error.message || '请检查后端服务是否已启动'}`);
    } finally {
      setLoading(false);
      setLoadingPhase('');
    }
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
          🎋 八字命理分析
        </h1>

        {!analysisResult && !loading && (
          <BirthInfoForm 
            fields={["year", "month", "day", "hour", "gender", "location"]}
            onSubmit={handleFormSubmit}
          />
        )}

        {loading && (
          <div className="traditional-card p-8 text-center">
            <div className="text-6xl mb-4">
              {loadingPhase === 'basic' ? '🔮' : '✨'}
            </div>
            <h2 className="text-xl font-serif-sc mb-4">
              {loadingPhase === 'basic' ? '正在计算您的八字...' : '正在进行命理分析...'}
            </h2>
            <div className="w-full bg-traditional-gold h-2 rounded overflow-hidden">
              <div className="w-full h-full bg-traditional-red animate-pulse"></div>
            </div>
            <p className="text-traditional-dark-green mt-4 opacity-75">
              {loadingPhase === 'basic' 
                ? '正在推演天干地支，解读宿命密码...' 
                : '深入命理玄机，解析人生奥秘...'}
            </p>
            {loadingPhase === 'analysis' && (
              <p className="text-sm text-traditional-dark-green mt-2 opacity-60">
                💫 八字天机已现，正在参悟命理玄机...
              </p>
            )}
          </div>
        )}

        {analysisResult && (
          <div className="space-y-6">
            {/* 八字信息 */}
            <div className="traditional-card p-6">
              <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                📜 您的八字信息
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div className="bg-traditional-gold p-3 rounded">
                  <div className="font-bold text-traditional-red">年柱</div>
                  <div className="text-lg">{analysisResult.bazi_result?.year_pillar || analysisResult.bazi?.year_pillar}</div>
                </div>
                <div className="bg-traditional-gold p-3 rounded">
                  <div className="font-bold text-traditional-red">月柱</div>
                  <div className="text-lg">{analysisResult.bazi_result?.month_pillar || analysisResult.bazi?.month_pillar}</div>
                </div>
                <div className="bg-traditional-gold p-3 rounded">
                  <div className="font-bold text-traditional-red">日柱</div>
                  <div className="text-lg">{analysisResult.bazi_result?.day_pillar || analysisResult.bazi?.day_pillar}</div>
                </div>
                <div className="bg-traditional-gold p-3 rounded">
                  <div className="font-bold text-traditional-red">时柱</div>
                  <div className="text-lg">{analysisResult.bazi_result?.hour_pillar || analysisResult.bazi?.hour_pillar}</div>
                </div>
              </div>
              <div className="mt-4 text-center">
                <span className="bg-traditional-red text-white px-4 py-2 rounded font-medium">
                  生肖：{analysisResult.bazi_result?.zodiac || analysisResult.zodiac} | 纳音：{analysisResult.bazi_result?.nayin || analysisResult.nayin}
                </span>
              </div>
            </div>

            {/* 五行分析 */}
            <div className="traditional-card p-6">
              <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                🔥 五行分析
              </h2>
              
              {/* 五行强度分布 */}
              <div className="grid grid-cols-5 gap-2 mb-6">
                {Object.entries(analysisResult.bazi_result?.wuxing || {}).map(([element, count]) => {
                  const strengthInfo = analysisResult.analysis_result?.wuxing_analysis?.wuxing_strength?.[element];
                  const getElementColor = (el: string) => {
                    const colors: { [key: string]: string } = {'木': 'text-green-600', '火': 'text-red-600', '土': 'text-yellow-600', '金': 'text-gray-600', '水': 'text-blue-600'};
                    return colors[el] || 'text-gray-600';
                  };
                  return (
                    <div key={element} className="text-center border rounded-lg p-3 bg-traditional-beige">
                      <div className={`font-medium text-lg ${getElementColor(element)}`}>{element}</div>
                      <div className="text-2xl font-bold text-traditional-red">{count as number}</div>
                      {strengthInfo && (
                        <div className="text-xs text-traditional-dark-green mt-1">
                          {strengthInfo.strength} ({strengthInfo.percentage}%)
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* 五行平衡分析 */}
              <div className="bg-gradient-to-r from-traditional-gold to-yellow-100 p-4 rounded-lg mb-4">
                <div className="text-center">
                  <div className="text-lg font-medium mb-2">
                    五行平衡分数：<span className="text-traditional-red text-xl font-bold">{analysisResult.analysis_result?.balance_score || 0}</span>/100
                  </div>
                  <div className="grid md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-green-600">喜用神：</span>
                      <span className="text-traditional-dark-green">
                        {(analysisResult.analysis_result?.wuxing_analysis?.favorable_elements || []).join('、')}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-orange-600">过旺元素：</span>
                      <span className="text-traditional-dark-green">
                        {(analysisResult.analysis_result?.wuxing_analysis?.excessive_elements || []).join('、') || '无'}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium text-blue-600">缺失元素：</span>
                      <span className="text-traditional-dark-green">
                        {(analysisResult.analysis_result?.wuxing_analysis?.missing_elements || []).join('、') || '无'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 性格分析 */}
            <div className="traditional-card p-6">
              <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                🌟 性格特点
              </h2>
              {!analysisResult.analysis_result ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">✨</div>
                  <div className="text-traditional-dark-green opacity-75">
                    {loadingPhase === 'analysis' ? '正在洞察心性品格...' : '等待性格玄机解读'}
                  </div>
                  {loadingPhase === 'analysis' && (
                    <div className="mt-3 w-64 mx-auto bg-traditional-gold h-1 rounded overflow-hidden">
                      <div className="w-full h-full bg-traditional-red animate-pulse"></div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <h3 className="font-medium text-traditional-dark-green mb-2">性格特质</h3>
                    <ul className="space-y-1 text-sm">
                      {(analysisResult.analysis_result?.personality?.traits || []).map((trait: string, index: number) => (
                        <li key={index}>• {trait}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-medium text-traditional-dark-green mb-2">优势特点</h3>
                    <ul className="space-y-1 text-sm">
                      {(analysisResult.analysis_result?.personality?.strengths || []).map((strength: string, index: number) => (
                        <li key={index} className="text-green-600">• {strength}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-medium text-traditional-dark-green mb-2">注意事项</h3>
                    <ul className="space-y-1 text-sm">
                      {(analysisResult.analysis_result?.personality?.weaknesses || []).map((weakness: string, index: number) => (
                        <li key={index} className="text-orange-600">• {weakness}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>

            {/* 幸运元素 */}
            <div className="traditional-card p-6">
              <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                🍀 幸运元素
              </h2>
              {!analysisResult.analysis_result ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">🍀</div>
                  <div className="text-traditional-dark-green opacity-75">
                    {loadingPhase === 'analysis' ? '正在寻找吉祥密码...' : '等待开启幸运之门'}
                  </div>
                  {loadingPhase === 'analysis' && (
                    <div className="mt-3 w-64 mx-auto bg-traditional-gold h-1 rounded overflow-hidden">
                      <div className="w-full h-full bg-traditional-red animate-pulse"></div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-6">
                  {/* 幸运颜色 */}
                  <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg">
                    <h3 className="font-medium text-traditional-red mb-3">🌈 幸运颜色</h3>
                    <div className="flex flex-wrap justify-center gap-2 mb-3">
                      {(analysisResult.analysis_result?.lucky_elements?.lucky_colors || []).map((color: string, index: number) => (
                        <span key={index} className="px-3 py-1 bg-traditional-gold rounded-full text-sm font-medium">
                          {color}
                        </span>
                      ))}
                    </div>
                    {analysisResult.analysis_result?.lucky_elements?.avoid_colors?.length > 0 && (
                      <div className="text-center">
                        <span className="text-sm text-gray-600">忌用颜色：</span>
                        <div className="flex flex-wrap justify-center gap-1 mt-1">
                          {analysisResult.analysis_result.lucky_elements.avoid_colors.map((color: string, index: number) => (
                            <span key={index} className="px-2 py-1 bg-gray-200 rounded text-xs text-gray-700">
                              {color}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* 幸运方位 */}
                  <div className="bg-gradient-to-r from-yellow-50 to-orange-50 p-4 rounded-lg">
                    <h3 className="font-medium text-traditional-red mb-3">🧭 幸运方位</h3>
                    <div className="flex flex-wrap justify-center gap-2 mb-3">
                      {(analysisResult.analysis_result?.lucky_elements?.lucky_directions || []).map((direction: string, index: number) => (
                        <span key={index} className="px-3 py-1 bg-traditional-gold rounded-full text-sm font-medium">
                          {direction}
                        </span>
                      ))}
                    </div>
                    {analysisResult.analysis_result?.lucky_elements?.avoid_directions?.length > 0 && (
                      <div className="text-center">
                        <span className="text-sm text-gray-600">忌用方位：</span>
                        <span className="ml-2 text-sm text-gray-700">
                          {analysisResult.analysis_result.lucky_elements.avoid_directions.join('、')}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* 幸运数字 */}
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg">
                    <h3 className="font-medium text-traditional-red mb-3">🔢 幸运数字</h3>
                    <div className="flex justify-center gap-2">
                      {(analysisResult.analysis_result?.lucky_elements?.lucky_numbers || []).map((number: number, index: number) => (
                        <div key={index} className="w-10 h-10 bg-traditional-red text-white rounded-full flex items-center justify-center font-bold">
                          {number}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* 有益物品 */}
                  {analysisResult.analysis_result?.lucky_elements?.beneficial_items?.length > 0 && (
                    <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-4 rounded-lg">
                      <h3 className="font-medium text-traditional-red mb-3">🎁 有益物品</h3>
                      <div className="flex flex-wrap justify-center gap-2">
                        {analysisResult.analysis_result.lucky_elements.beneficial_items.map((item: string, index: number) => (
                          <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 运势分析 */}
            {analysisResult.analysis_result?.fortune && (
              <div className="traditional-card p-6">
                <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                  🔮 运势分析
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-gradient-to-br from-red-50 to-pink-50 p-4 rounded-lg">
                    <h3 className="font-medium text-red-600 mb-2">💼 事业运</h3>
                    <p className="text-sm text-gray-700">{analysisResult.analysis_result.fortune.career}</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-lg">
                    <h3 className="font-medium text-green-600 mb-2">💰 财运</h3>
                    <p className="text-sm text-gray-700">{analysisResult.analysis_result.fortune.wealth}</p>
                  </div>
                  <div className="bg-gradient-to-br from-pink-50 to-rose-50 p-4 rounded-lg">
                    <h3 className="font-medium text-pink-600 mb-2">💕 感情运</h3>
                    <p className="text-sm text-gray-700">{analysisResult.analysis_result.fortune.relationship}</p>
                  </div>
                  <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-4 rounded-lg">
                    <h3 className="font-medium text-blue-600 mb-2">🏥 健康运</h3>
                    <p className="text-sm text-gray-700">{analysisResult.analysis_result.fortune.health}</p>
                  </div>
                </div>
              </div>
            )}

            {/* 生活建议 */}
            {analysisResult.analysis_result?.life_advice?.length > 0 && (
              <div className="traditional-card p-6">
                <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                  💡 生活建议
                </h2>
                <div className="space-y-3">
                  {analysisResult.analysis_result.life_advice.map((advice: string, index: number) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-lg">
                      <div className="flex-shrink-0 w-6 h-6 bg-traditional-red text-white rounded-full flex items-center justify-center text-sm font-bold">
                        {index + 1}
                      </div>
                      <p className="text-traditional-dark-green text-sm leading-relaxed">{advice}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 风水生活贴士 */}
            {analysisResult.analysis_result?.lucky_elements?.lifestyle_tips?.length > 0 && (
              <div className="traditional-card p-6">
                <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4">
                  🏠 风水生活贴士
                </h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {analysisResult.analysis_result.lucky_elements.lifestyle_tips.map((tip: string, index: number) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg">
                      <div className="flex-shrink-0 text-lg">🌟</div>
                      <p className="text-traditional-dark-green text-sm leading-relaxed">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="text-center">
              <button 
                onClick={() => setAnalysisResult(null)}
                className="traditional-button mr-4"
              >
                🔄 重新分析
              </button>
              <Link href="/fengshui" className="traditional-button inline-block">
                🧭 查看风水建议
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BaziPage;
