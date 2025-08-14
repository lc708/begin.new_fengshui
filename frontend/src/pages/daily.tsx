import React, { useState, useEffect } from 'react';
import Link from 'next/link';

const DailyPage: React.FC = () => {
  const [todayFortune, setTodayFortune] = useState<any>(null);
  const [selectedDate, setSelectedDate] = useState<string>('');

  useEffect(() => {
    // 获取今日运势
    const today = new Date().toISOString().split('T')[0];
    setSelectedDate(today);
    
    // 调用真实API获取今日运势
    const fetchTodayFortune = async () => {
      try {
        const { getDailyFortune } = await import('../lib/api');
        const fortune = await getDailyFortune(today);
        console.log('每日运势API响应:', fortune);
        setTodayFortune(fortune);
      } catch (error) {
        console.error('获取今日运势失败:', error);
        // 如果API失败，使用默认数据
        const mockFortune = {
          date: today,
          ganzhi: "辛酉",
          suitable: ["安床", "牧养", "立卷", "求嗣"],
          unsuitable: ["掘井", "开渠"],
          wealth_direction: "东南",
          overall_score: 75,
          time_fortune: {"09:00-11:00": "吉"},
          conflict_zodiac: "兔",
          lunar_info: {
            month: "七月",
            day: 15,
            description: "七月十五日"
          }
        };
        setTodayFortune(mockFortune);
      }
    };
    
    fetchTodayFortune();
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreText = (score: number) => {
    if (score >= 80) return '大吉';
    if (score >= 60) return '中吉';
    if (score >= 40) return '平';
    return '小凶';
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
          📅 每日宜忌查询
        </h1>

        {todayFortune && (
          <div className="space-y-6">
            {/* 今日概览 */}
            <div className="traditional-card p-6">
              <h2 className="text-xl font-serif-sc font-semibold text-traditional-red mb-4 text-center">
                📆 今日运势概览
              </h2>
              
              <div className="grid md:grid-cols-3 gap-6 text-center">
                <div className="bg-traditional-gold p-4 rounded">
                  <div className="font-bold text-traditional-red mb-2">日期</div>
                  <div className="text-lg">{todayFortune.date}</div>
                  <div className="text-sm text-traditional-dark-green">
                    {todayFortune.accurate_lunar?.lunar_date_str || `农历${todayFortune.lunar_info.description}`}
                  </div>
                  {todayFortune.accurate_lunar && (
                    <div className="text-xs text-traditional-dark-green mt-1">
                      {todayFortune.accurate_lunar.bazi}
                    </div>
                  )}
                </div>
                
                <div className="bg-traditional-gold p-4 rounded">
                  <div className="font-bold text-traditional-red mb-2">天干地支</div>
                  <div className="text-2xl font-serif-sc">{todayFortune.ganzhi}</div>
                </div>
                
                <div className="bg-traditional-gold p-4 rounded">
                  <div className="font-bold text-traditional-red mb-2">运势评分</div>
                  <div className={`text-2xl font-bold ${getScoreColor(todayFortune.overall_score)}`}>
                    {todayFortune.overall_score}
                  </div>
                  <div className="text-sm">
                    {getScoreText(todayFortune.overall_score)}
                  </div>
                </div>
              </div>
            </div>

            {/* 宜忌事项 - 传统算法版本 */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="traditional-card p-6">
                <h3 className="text-lg font-serif-sc font-semibold text-green-600 mb-4 text-center">
                  ✅ 今日宜 ({todayFortune.suitable.length}项)
                </h3>
                <div className="max-h-60 overflow-y-auto">
                  <div className="grid grid-cols-2 gap-2">
                    {todayFortune.suitable.map((item: string, index: number) => (
                      <div key={index} className="bg-green-50 text-green-700 px-2 py-1 rounded text-center text-sm font-serif-sc">
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="traditional-card p-6">
                <h3 className="text-lg font-serif-sc font-semibold text-red-600 mb-4 text-center">
                  ❌ 今日忌 ({todayFortune.unsuitable.length}项)
                </h3>
                <div className="max-h-60 overflow-y-auto">
                  <div className="grid grid-cols-2 gap-2">
                    {todayFortune.unsuitable.map((item: string, index: number) => (
                      <div key={index} className="bg-red-50 text-red-700 px-2 py-1 rounded text-center text-sm font-serif-sc">
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* 详细信息 */}
            <div className="traditional-card p-6">
              <h3 className="text-lg font-serif-sc font-semibold text-traditional-red mb-4">
                🔍 详细信息
              </h3>
              
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-traditional-dark-green font-medium mb-2">💰 财神方位</div>
                  <div className="text-lg bg-traditional-gold px-4 py-2 rounded">
                    {todayFortune.wealth_direction}
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="text-traditional-dark-green font-medium mb-2">⏰ 吉时</div>
                  <div className="text-sm bg-traditional-gold px-4 py-2 rounded">
                    {todayFortune.time_fortune && Object.entries(todayFortune.time_fortune)
                      .filter(([_, fortune]) => String(fortune).includes('吉'))
                      .slice(0, 2)
                      .map(([time, _]) => time.split('(')[0])
                      .join('、') || '无'}
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="text-traditional-dark-green font-medium mb-2">⚠️ 冲煞</div>
                  <div className="text-lg bg-red-100 text-red-700 px-4 py-2 rounded">
                    冲{todayFortune.conflict_zodiac}
                  </div>
                </div>
              </div>
            </div>

            {/* 传统黄历详情 */}
            <div className="traditional-card p-6">
              <h3 className="text-lg font-serif-sc font-semibold text-traditional-red mb-4">
                🏮 传统黄历详情
              </h3>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <div className="text-center bg-traditional-gold p-3 rounded">
                  <div className="text-traditional-dark-green font-medium mb-1">五行</div>
                  <div className="text-lg font-serif-sc">{todayFortune.accurate_lunar.wuxing}</div>
                </div>
                
                <div className="text-center bg-traditional-gold p-3 rounded">
                  <div className="text-traditional-dark-green font-medium mb-1">神兽</div>
                  <div className="text-lg font-serif-sc">{todayFortune.accurate_lunar.shenshou}</div>
                </div>
                
                <div className="text-center bg-traditional-gold p-3 rounded">
                  <div className="text-traditional-dark-green font-medium mb-1">四宫</div>
                  <div className="text-lg font-serif-sc">{todayFortune.accurate_lunar.sigong}</div>
                </div>
                
                <div className="text-center bg-traditional-gold p-3 rounded">
                  <div className="text-traditional-dark-green font-medium mb-1">日禄</div>
                  <div className="text-sm font-serif-sc">{todayFortune.accurate_lunar.rilu}</div>
                </div>
              </div>

              {/* 新增：传统算法特有信息 */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-md font-serif-sc font-medium text-traditional-red mb-3">⭐ 星宿神煞</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-traditional-dark-green">建除十二神:</span>
                      <span className="font-serif-sc">{todayFortune.twelve_officer}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-traditional-dark-green">十二值神:</span>
                      <span className="font-serif-sc">{todayFortune.twelve_god}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-traditional-dark-green">二十八星宿:</span>
                      <span className="font-serif-sc">{todayFortune.twenty_eight_stars}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-traditional-dark-green">东方星座:</span>
                      <span className="font-serif-sc">{todayFortune.east_zodiac}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-md font-serif-sc font-medium text-traditional-red mb-3">🔮 吉凶神煞</h4>
                  <div className="space-y-2">
                    <div>
                      <span className="text-green-600 font-medium">吉神: </span>
                      <span className="text-sm">{todayFortune.good_gods.join('、')}</span>
                    </div>
                    <div>
                      <span className="text-red-600 font-medium">凶煞: </span>
                      <span className="text-sm">{todayFortune.bad_gods.join('、')}</span>
                    </div>
                    <div className="mt-3 p-2 bg-blue-50 rounded text-sm">
                      <span className="font-medium">今日等级: </span>
                      <span className="font-serif-sc">{todayFortune.thing_level}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* 彭祖百忌和胎神（如果有） */}
              {(todayFortune.pengzu_taboo || todayFortune.fetal_god) && (
                <div className="mt-6 grid md:grid-cols-2 gap-4">
                  {todayFortune.pengzu_taboo && (
                    <div className="bg-yellow-50 p-3 rounded">
                      <div className="text-traditional-dark-green font-medium mb-1">📜 彭祖百忌</div>
                      <div className="text-sm font-serif-sc">{todayFortune.pengzu_taboo}</div>
                    </div>
                  )}
                  {todayFortune.fetal_god && (
                    <div className="bg-pink-50 p-3 rounded">
                      <div className="text-traditional-dark-green font-medium mb-1">👶 胎神占方</div>
                      <div className="text-sm font-serif-sc">{todayFortune.fetal_god}</div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 温馨提示 */}
            <div className="traditional-card p-6 bg-blue-50">
              <h3 className="text-lg font-serif-sc font-semibold text-traditional-red mb-3">
                💡 今日温馨提示
              </h3>
              <ul className="space-y-2 text-traditional-dark-green text-sm">
                <li>• 今日总体运势{getScoreText(todayFortune.overall_score)}，适合进行宜事项中的活动</li>
                <li>• 财神在{todayFortune.wealth_direction}方，相关活动可朝此方向</li>
                <li>• 吉时适合进行重要事宜，请参考下方时辰运势详情</li>
                <li>• 属{todayFortune.conflict_zodiac}的朋友今日宜谨慎行事</li>
              </ul>
            </div>

            {/* 时辰运势详情 */}
            {todayFortune.time_fortune && (
              <div className="traditional-card p-6">
                <h3 className="text-lg font-serif-sc font-semibold text-traditional-red mb-4 text-center">
                  ⏰ 十二时辰运势
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                  {Object.entries(todayFortune.time_fortune).map(([time, fortune]) => {
                    const fortuneStr = String(fortune); // 明确转换为字符串
                    const getFortuneColor = (fortune: string) => {
                      if (fortune.includes('大吉')) return 'bg-green-100 text-green-800 border-green-300';
                      if (fortune.includes('吉')) return 'bg-blue-100 text-blue-800 border-blue-300';
                      if (fortune.includes('平')) return 'bg-gray-100 text-gray-800 border-gray-300';
                      if (fortune.includes('大凶')) return 'bg-red-100 text-red-800 border-red-300';
                      if (fortune.includes('凶')) return 'bg-orange-100 text-orange-800 border-orange-300';
                      return 'bg-gray-100 text-gray-800 border-gray-300';
                    };
                    
                    return (
                      <div key={time} className={`p-3 rounded-lg border-2 text-center ${getFortuneColor(fortuneStr)}`}>
                        <div className="font-medium text-sm">{time}</div>
                        <div className="text-lg font-bold mt-1">{fortuneStr}</div>
                      </div>
                    );
                  })}
                </div>
                <div className="mt-4 text-center text-sm text-traditional-dark-green">
                  💡 大吉、吉时适合重要活动；平时可正常安排；凶时宜谨慎行事
                </div>
              </div>
            )}

            {/* 算法说明 */}
            {todayFortune.algorithm_type && (
              <div className="traditional-card p-4 bg-gray-50">
                <div className="text-center text-sm text-gray-600">
                  <span className="font-medium">算法来源: </span>
                  {todayFortune.algorithm_type === 'traditional' ? (
                    <span>cnlunar传统黄历算法 - 基于建除十二神、二十八星宿等传统理论</span>
                  ) : (
                    <span>简化算法</span>
                  )}
                </div>
              </div>
            )}

            {/* 操作按钮 */}
            <div className="text-center space-x-4">
              <button 
                onClick={() => window.location.reload()}
                className="traditional-button"
              >
                🔄 刷新运势
              </button>
              <Link href="/bazi" className="traditional-button inline-block">
                🎋 查看八字分析
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DailyPage;
