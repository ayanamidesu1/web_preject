// src/cookies.d.ts

declare module './cookies' {
    // 设置cookies
    export function set_cookie(key: string, value: string): Promise<void>;
  
    // 过期cookie
    export function expireCookie(name: string): void;
  
    // 获取指定cookie的值
    export function get_cookie(name: string): string | null;
  
    // 设置localStorage值
    export function set_storage(key: string, value: string): void;
  
    // 获取localStorage值
    export function get_storage(key: string): string | null;
  
    // 清除所有cookies
    export function clearAllCookies(): void;
  
    // 清除所有localStorage
    export function clearAllLocalStorage(): void;
  
    // 清除所有sessionStorage
    export function clearAllSessionStorage(): void;
  }
  