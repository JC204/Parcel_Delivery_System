import React, { useState } from 'react';
import { Truck, Package, Search } from 'lucide-react';
import { ParcelTracker } from './components/ParcelTracker';
import { ParcelForm } from './components/ParcelForm';

function App() {
  const [activeTab, setActiveTab] = useState<'track' | 'create'>('track');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Truck className="w-8 h-8 text-blue-600" />
              <h1 className="ml-2 text-2xl font-bold text-gray-900">ParcelPro</h1>
            </div>
            <nav className="flex space-x-4">
              <button
                onClick={() => setActiveTab('track')}
                className={`flex items-center px-4 py-2 rounded-lg ${
                  activeTab === 'track'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Search className="w-5 h-5 mr-1" />
                Track
              </button>
              <button
                onClick={() => setActiveTab('create')}
                className={`flex items-center px-4 py-2 rounded-lg ${
                  activeTab === 'create'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Package className="w-5 h-5 mr-1" />
                New Shipment
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'track' ? <ParcelTracker /> : <ParcelForm />}
      </main>
    </div>
  );
}

export default App;