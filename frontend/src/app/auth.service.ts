import { Injectable } from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {AuthResponse} from "./models/auth-response";
import {environment} from "../environments/environment";
import {BehaviorSubject, tap} from "rxjs";
import {TokenProviderService} from "./token-provider.service";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this._isLoggedIn$.asObservable();

  loginUrl = environment.apiUrl + "/user/login";
  permissionUrl = environment.apiUrl + "/user/permission";

  constructor(private httpClient: HttpClient, private tokenProvider: TokenProviderService) {

    this.checkPermission().subscribe((data: AuthResponse) => {
      this._isLoggedIn$.next(data.value);
    });
  }

  login(address: string, password: string) {
    return this.httpClient.post<AuthResponse>(this.loginUrl, {
      address: address,
      password: password
    }).pipe(tap((response: any) => {
      this._isLoggedIn$.next(true);
      this.tokenProvider.token = response.token;
    })
    );
  }

  logout(){
    this.tokenProvider.removeToken();
  }

  checkPermission(){
    return this.httpClient.get<AuthResponse>(this.permissionUrl);
  }
}
