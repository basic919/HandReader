import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";


@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.less']
})
export class ForgotPasswordComponent implements OnInit {

    forgotPasswordUrl = environment.apiUrl + "/user/forgot_password";
    email: string = '';


  constructor(private httpClient: HttpClient) { }

  ngOnInit(): void {
  }

  onForgotPassword() {
    const payload = { email: this.email };

    this.httpClient.post(this.forgotPasswordUrl, payload)
      .subscribe(
        (response) => console.log(response),
        (error) => console.log(error)
      );
}

}
