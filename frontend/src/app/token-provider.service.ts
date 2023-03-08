import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class TokenProviderService {

  private readonly TOKEN_NAME = 'auth_token'

  constructor() { }

  get token(): string{
    // @ts-ignore
    return localStorage.getItem(this.TOKEN_NAME) ? localStorage.getItem(this.TOKEN_NAME) : "";
  }

  set token(value){
    localStorage.setItem(this.TOKEN_NAME, value);
  }

  removeToken(){
    localStorage.setItem(this.TOKEN_NAME, '');
  }
}
