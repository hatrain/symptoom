export interface User {
    id: number;
    email: string;
    username: string;
    password: string;
  }
  
  export interface Admin extends User {
    adminId: number;
  }