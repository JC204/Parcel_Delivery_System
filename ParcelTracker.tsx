import React, { useState } from 'react';
import { Package, Search } from 'lucide-react';
import { trackParcel } from '../api';
import { Parcel } from '../types';

export function ParcelTracker() {
  const [trackingNumber, setTrackingNumber] = useState('');
  const [parcel, setParcel] = useState<Parcel | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTrack = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setParcel(null);

    try {
      const data = await trackParcel(trackingNumber);
      setParcel(data);
    } catch (err) {
      setError('Failed to track parcel. Please check the tracking number and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-center mb-6">
        <Package className="w-8 h-8 text-blue-600 mr-2" />
        <h2 className="text-2xl font-bold text-gray-800">Track Your Parcel</h2>
      </div>
      
      <form onSubmit={handleTrack} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={trackingNumber}
            onChange={(e) => setTrackingNumber(e.target.value)}
            placeholder="Enter tracking number"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500 hover:text-blue-600 disabled:opacity-50"
            disabled={loading || !trackingNumber}
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </form>

      {loading && (
        <div className="mt-4 text-center text-gray-600">
          Loading...
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {parcel && (
        <div className="mt-6 space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h3 className="font-semibold text-lg mb-2">Parcel Status: {parcel.status}</h3>
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Tracking Number:</span> {parcel.tracking_number}</p>
              <p><span className="font-medium">Weight:</span> {parcel.weight}kg</p>
              <p><span className="font-medium">Created:</span> {new Date(parcel.created_at).toLocaleDateString()}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium mb-2">Sender</h4>
              <div className="text-sm space-y-1">
                <p>{parcel.sender.name}</p>
                <p>{parcel.sender.email}</p>
                <p>{parcel.sender.phone}</p>
              </div>
            </div>
            <div>
              <h4 className="font-medium mb-2">Recipient</h4>
              <div className="text-sm space-y-1">
                <p>{parcel.recipient.name}</p>
                <p>{parcel.recipient.email}</p>
                <p>{parcel.recipient.phone}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}