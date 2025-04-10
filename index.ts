export interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  address: string;
}

export interface TrackingUpdate {
  id: number;
  status: string;
  location: string;
  description: string;
  timestamp: string;
}

export interface Parcel {
  id: number;
  tracking_number: string;
  status: 'pending' | 'assigned' | 'in_transit' | 'delivered';
  sender: Customer;
  recipient: Customer;
  weight: number;
  description: string;
  created_at: string;
  courier_id?: number;
  courier?: Courier;
  tracking_updates: TrackingUpdate[];
}

export interface Courier {
  id: number;
  name: string;
  phone: string;
  status: 'available' | 'busy';
}