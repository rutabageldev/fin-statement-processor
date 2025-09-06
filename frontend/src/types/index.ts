// API Response Types
export interface ApiResponse<T> {
  data?: T
  error?: {
    code: string
    message: string
    details?: Record<string, unknown>
    request_id?: string
  }
}

// Statement Types
export interface Statement {
  id: string
  institution_id: string
  account_id: string
  period_start: string
  period_end: string
  uploaded_at: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  files: {
    pdf_url?: string
    csv_url?: string
  }
  summary?: {
    transaction_count: number
    total_credits: number
    total_debits: number
    net_amount: number
  }
}

export interface StatementDetails {
  id: string
  statement_id: string
  previous_balance: number
  new_balance: number
}

export interface CreditCardDetails {
  id: string
  account_id: string
  statement_id: string
  credit_limit: number
  available_credit: number
  points_earned: number
  points_redeemed: number
  cash_advances: number
  fees: number
  purchases: number
  credits: number
}

// Transaction Types
export interface Transaction {
  id: string
  statement_id: string
  account_id: string
  date: string
  amount: number
  description: string
  custom_description?: string
  category?: string
  type: 'debit' | 'credit' | 'payment' | 'refund'
}

// Analytics Types
export interface CategorySpending {
  category: string
  amount: number
  percentage: number
  transaction_count: number
}

export interface MonthlySpending {
  period: {
    year: number
    month?: number
    start_date: string
    end_date: string
  }
  total_spending: number
  total_credits: number
  net_amount: number
  categories: CategorySpending[]
  daily_breakdown: {
    date: string
    amount: number
    transaction_count: number
  }[]
}

// Pagination Types
export interface PaginationInfo {
  page: number
  limit: number
  total: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: PaginationInfo
}
