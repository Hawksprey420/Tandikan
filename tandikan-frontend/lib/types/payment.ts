export interface FeeItem {
  id: number;
  name: string;
  description: string;
  amount: number;
  category: 'tuition' | 'laboratory' | 'miscellaneous' | 'other';
}

export interface Assessment {
  id: number;
  enrollment: number;
  items: FeeItem[];
  totalAmount: number;
  discountAmount: number;
  netAmount: number;
  status: 'pending' | 'approved' | 'paid';
  createdAt: string;
  approvedAt?: string;
}

export interface Payment {
  id: number;
  assessment: number;
  amount: number;
  paymentMethod: 'cash' | 'card' | 'bank_transfer' | 'online';
  referenceNumber?: string;
  receivedBy: string;
  createdAt: string;
  status: 'pending' | 'confirmed' | 'cancelled';
}
