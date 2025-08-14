import React, { useState } from 'react';

interface DigitalCompassProps {
  directions: number;
  colors: string[];
  onDirectionSelect?: (direction: string) => void;
}

const DigitalCompass: React.FC<DigitalCompassProps> = ({ directions, colors, onDirectionSelect }) => {
  const [selectedDirection, setSelectedDirection] = useState<string | null>(null);

  const directionNames = ['北', '东北', '东', '东南', '南', '西南', '西', '西北'];
  const directionColors = ['#000080', '#8B4513', '#228B22', '#32CD32', '#FF0000', '#FF8C00', '#FFD700', '#C0C0C0'];

  const handleDirectionClick = (direction: string, index: number) => {
    setSelectedDirection(direction);
    if (onDirectionSelect) {
      onDirectionSelect(direction);
    }
  };

  return (
    <div className="traditional-card p-8 max-w-2xl mx-auto">
      <h2 className="text-2xl font-serif-sc font-semibold text-traditional-red mb-6 text-center">
        🧭 数字风水罗盘
      </h2>
      
      <div className="relative w-64 h-64 mx-auto mb-6 bg-gradient-to-br from-yellow-100 to-amber-200 rounded-full border-4 border-traditional-gold shadow-lg">
        {/* 中心太极图 */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-white rounded-full border-2 border-traditional-gold flex items-center justify-center text-3xl">
          ☯
        </div>
        
        {/* 八个方位 */}
        {directionNames.map((direction, index) => {
          const angle = (index * 45) - 90; // 从北方开始
          const radian = (angle * Math.PI) / 180;
          const radius = 90; // 相对于256px容器中心
          const x = Math.cos(radian) * radius + 128;
          const y = Math.sin(radian) * radius + 128;
          
          return (
            <button
              key={direction}
              onClick={() => handleDirectionClick(direction, index)}
              className={`absolute w-12 h-12 rounded-full border-2 border-traditional-gold 
                         flex items-center justify-center font-bold transition-all cursor-pointer
                         ${selectedDirection === direction 
                           ? 'bg-traditional-red text-white scale-110 shadow-lg' 
                           : 'bg-white text-traditional-red hover:bg-traditional-gold hover:scale-105'}`}
              style={{
                left: `${x - 24}px`,
                top: `${y - 24}px`,
                color: selectedDirection === direction ? 'white' : '#8B0000'
              }}
            >
              {direction}
            </button>
          );
        })}
      </div>

      {selectedDirection && (
        <div className="mt-8 text-center">
          <div className="traditional-card p-4 bg-traditional-gold">
            <h3 className="text-lg font-serif-sc font-semibold mb-2">
              {selectedDirection}方位信息
            </h3>
            <p className="text-traditional-dark-green">
              您选择了{selectedDirection}方位，这个方位的能量特性正在分析中...
            </p>
          </div>
        </div>
      )}

      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">
        <div className="p-2 bg-blue-100 rounded">
          <div className="text-blue-800 font-medium">水</div>
          <div className="text-blue-600">北方</div>
        </div>
        <div className="p-2 bg-green-100 rounded">
          <div className="text-green-800 font-medium">木</div>
          <div className="text-green-600">东方</div>
        </div>
        <div className="p-2 bg-red-100 rounded">
          <div className="text-red-800 font-medium">火</div>
          <div className="text-red-600">南方</div>
        </div>
        <div className="p-2 bg-yellow-100 rounded">
          <div className="text-yellow-800 font-medium">金</div>
          <div className="text-yellow-600">西方</div>
        </div>
      </div>
    </div>
  );
};

export default DigitalCompass;
