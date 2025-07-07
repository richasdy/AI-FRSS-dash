export interface User {
    id: string;
    email: string;
    name: string | null;
    username: string | null;
    password: string;
    isApproved: boolean;
    created_at: Date;
    updated_at: Date;
  }
  