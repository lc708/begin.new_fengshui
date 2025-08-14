import React, { useState } from 'react';

interface BirthInfoFormProps {
  fields: string[];
  onSubmit?: (data: any) => void;
}

const BirthInfoForm: React.FC<BirthInfoFormProps> = ({ fields, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    year: '',
    month: '',
    day: '',
    hour: '',
    gender: 'male',
    location: '北京'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit?.(formData);
  };

  return (
    <div className="traditional-card p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-serif-sc font-semibold text-traditional-red mb-6 text-center">
        📝 请输入您的生辰信息
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              姓名
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="traditional-input w-full"
              placeholder="请输入您的姓名"
              required
            />
          </div>
          
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              性别
            </label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="traditional-input w-full"
            >
              <option value="male">男</option>
              <option value="female">女</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              年份
            </label>
            <input
              type="number"
              name="year"
              value={formData.year}
              onChange={handleChange}
              className="traditional-input w-full"
              placeholder="1990"
              min="1900"
              max="2025"
              required
            />
          </div>
          
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              月份
            </label>
            <input
              type="number"
              name="month"
              value={formData.month}
              onChange={handleChange}
              className="traditional-input w-full"
              placeholder="6"
              min="1"
              max="12"
              required
            />
          </div>
          
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              日期
            </label>
            <input
              type="number"
              name="day"
              value={formData.day}
              onChange={handleChange}
              className="traditional-input w-full"
              placeholder="15"
              min="1"
              max="31"
              required
            />
          </div>
          
          <div>
            <label className="block text-traditional-dark-green font-medium mb-2">
              时辰
            </label>
            <input
              type="number"
              name="hour"
              value={formData.hour}
              onChange={handleChange}
              className="traditional-input w-full"
              placeholder="14"
              min="0"
              max="23"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-traditional-dark-green font-medium mb-2">
            出生地
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="traditional-input w-full"
            placeholder="北京"
            required
          />
        </div>

        <div className="text-center">
          <button
            type="submit"
            className="traditional-button"
          >
            🔮 开始分析八字
          </button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-traditional-dark-green opacity-75">
        ⚠️ 本应用仅供娱乐参考，不作为人生决策依据
      </div>
    </div>
  );
};

export default BirthInfoForm;
