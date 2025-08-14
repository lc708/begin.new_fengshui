/**
 * API客户端库
 * 封装与后端API的通信接口
 */

import axios from 'axios';

// API基础配置  
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90秒超时，适应生产环境LLM调用时间
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🔄 API请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API响应: ${response.config.url}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ API响应错误:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// 类型定义
export interface UserInfo {
  name: string;
  year: number;
  month: number;
  day: number;
  hour: number;
  gender: 'male' | 'female';
  location: string;
}

export interface BaziResult {
  tiangang: string[];
  dizhi: string[];
  wuxing: Record<string, number>;
  zodiac: string;
  nayin: string;
  year_pillar: string;
  month_pillar: string;
  day_pillar: string;
  hour_pillar: string;
}

export interface AnalysisResult {
  wuxing_analysis: any;
  personality: {
    traits: string[];
    strengths: string[];
    weaknesses: string[];
  };
  fortune: {
    career: string;
    wealth: string;
    health: string;
    relationship: string;
  };
  lucky_elements: {
    colors: string[];
    numbers: number[];
    directions: string[];
  };
  life_advice: string[];
  balance_score: number;
}

export interface DailyFortune {
  date: string;
  ganzhi: string;
  year_ganzhi: string;
  month_ganzhi: string;
  suitable: string[];
  unsuitable: string[];
  wealth_direction: string;
  overall_score: number;
  time_fortune: Record<string, string>;
  conflict_zodiac: string;
  zodiac_clash: string;
  
  // 农历信息（cnlunar完整版本）
  lunar_info: {
    year: string;
    month: string;
    day: string;
    description: string;
    is_leap_month: boolean;
    season: string;
    lunar_year_num: number;
    lunar_month_num: number;
    lunar_day_num: number;
    month_long: boolean;
  };
  
  // 兼容性字段
  accurate_lunar: {
    lunar_year: string;
    lunar_month: string;
    lunar_day: string;
    lunar_date_str: string;
    bazi: string;
    wuxing: string;
    rilu: string;
    shenshou: string;
    sigong: string;
  };
  
  // 传统算法特有字段
  good_gods: string[];          // 吉神
  bad_gods: string[];           // 凶煞
  twelve_officer: string;       // 建除十二神
  twelve_god: string;           // 十二值神
  twenty_eight_stars: string;   // 二十八星宿
  east_zodiac: string;          // 东方星座
  today_level: number;          // 今日等级
  level_name: string;           // 等级名称
  thing_level: string;          // 事务等级
  solar_terms: string;          // 节气
  next_solar_term: string;      // 下个节气
  next_solar_date: number[];    // 下个节气日期
  star_zodiac: string;          // 星座
  zodiac_animal: string;        // 生肖
  week_day: string;             // 星期
  season: string;               // 季节
  pengzu_taboo?: string;        // 彭祖百忌
  fetal_god?: string;           // 胎神占方
  algorithm_type: string;       // 算法类型
}

// API接口函数

/**
 * 健康检查
 */
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/api/health');
    return response.data;
  } catch (error) {
    throw new Error('无法连接到后端服务');
  }
};

/**
 * 八字基础信息分析（快速）
 */
export const analyzeBaziBasic = async (userInfo: UserInfo) => {
  try {
    console.log('🔄 开始八字基础分析API调用:', userInfo);
    const response = await apiClient.post('/api/bazi/basic', userInfo);
    console.log('✅ 八字基础分析API响应:', response.data);
    
    if (!response.data.success) {
      throw new Error(response.data.error || '基础分析失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    console.error('❌ 八字基础分析API错误:', error);
    if (error.code === 'ECONNABORTED') {
      throw new Error('请求超时，请稍后重试。');
    }
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    if (error.response?.status) {
      throw new Error(`服务器错误 (${error.response.status}): ${error.response.data?.message || '未知错误'}`);
    }
    throw new Error('八字基础分析失败，请检查网络连接或稍后重试');
  }
};

/**
 * 八字命理分析（LLM）
 */
export const analyzeBaziPersonality = async (data: { user_info: any; bazi_result: any }) => {
  try {
    console.log('🔄 开始八字命理分析API调用');
    const response = await apiClient.post('/api/bazi/analysis', data);
    console.log('✅ 八字命理分析API响应:', response.data);
    
    if (!response.data.success) {
      throw new Error(response.data.error || '命理分析失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    console.error('❌ 八字命理分析API错误:', error);
    if (error.code === 'ECONNABORTED') {
      throw new Error('命理分析超时，请稍后重试。LLM分析可能需要较长时间。');
    }
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    if (error.response?.status) {
      throw new Error(`服务器错误 (${error.response.status}): ${error.response.data?.message || '未知错误'}`);
    }
    throw new Error('八字命理分析失败，请检查网络连接或稍后重试');
  }
};

/**
 * 八字完整分析（兼容性保留）
 */
export const analyzeBazi = async (userInfo: UserInfo) => {
  try {
    console.log('🔄 开始八字分析API调用:', userInfo);
    const response = await apiClient.post('/api/bazi/analyze', userInfo);
    console.log('✅ 八字分析API响应:', response.data);
    
    if (!response.data.success) {
      throw new Error(response.data.error || '分析失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    console.error('❌ 八字分析API错误:', error);
    if (error.code === 'ECONNABORTED') {
      throw new Error('请求超时，请稍后重试。分析过程可能需要较长时间。');
    }
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    if (error.response?.status) {
      throw new Error(`服务器错误 (${error.response.status}): ${error.response.data?.message || '未知错误'}`);
    }
    throw new Error('八字分析失败，请检查网络连接或稍后重试');
  }
};

/**
 * 风水建议
 */
export const getFengshuiAdvice = async (data: {
  user_info?: UserInfo;
  bazi_result?: BaziResult;
  analysis_result?: AnalysisResult;
  query?: {
    type: string;
    direction?: string;
    user_location?: string;
  };
}) => {
  try {
    const response = await apiClient.post('/api/fengshui/advice', data);
    
    if (!response.data.success) {
      throw new Error(response.data.error || '获取建议失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('获取风水建议失败，请检查网络连接');
  }
};

/**
 * 每日运势
 */
export const getDailyFortune = async (date?: string, userBazi?: BaziResult) => {
  try {
    const params: any = {};
    if (date) params.date = date;
    if (userBazi) params.user_bazi = JSON.stringify(userBazi);
    
    const response = await apiClient.get('/api/daily/fortune', { params });
    
    if (!response.data.success) {
      throw new Error(response.data.error || '查询失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('查询每日运势失败，请检查网络连接');
  }
};

/**
 * 吉日查询
 */
export const getAuspiciousDays = async (
  startDate?: string,
  endDate?: string,
  activityType: string = 'general'
) => {
  try {
    const params: any = { activity_type: activityType };
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await apiClient.get('/api/daily/auspicious', { params });
    
    if (!response.data.success) {
      throw new Error(response.data.error || '查询失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('查询吉日失败，请检查网络连接');
  }
};

/**
 * 完整分析
 */
export const completeAnalysis = async (userInfo: UserInfo) => {
  try {
    const response = await apiClient.post('/api/analyze/complete', { user_info: userInfo });
    
    if (!response.data.success) {
      throw new Error(response.data.error || '分析失败');
    }
    
    return response.data.data;
  } catch (error: any) {
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    }
    throw new Error('完整分析失败，请检查网络连接');
  }
};

/**
 * 检查API连接状态
 */
export const checkApiConnection = async (): Promise<boolean> => {
  try {
    await healthCheck();
    return true;
  } catch {
    return false;
  }
};

// 错误处理工具
export const handleApiError = (error: any): string => {
  if (error.response?.data?.error) {
    return error.response.data.error;
  }
  if (error.message) {
    return error.message;
  }
  return '未知错误，请稍后重试';
};
