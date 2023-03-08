import { Component, OnInit } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";


@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.less']
})
export class ForgotPasswordComponent implements OnInit {

    forgotPasswordUrl = environment.apiUrl + "/user/forgot_password";
    forgotPasswordForm: FormGroup = new FormGroup({});


  constructor(private formBuilder: FormBuilder, private httpClient: HttpClient) { }

  ngOnInit(): void {

    this.forgotPasswordForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onForgotPassword() {

    this.httpClient.post(this.forgotPasswordUrl, {address: this.forgotPasswordForm.get("email")?.value})
      .subscribe(
        (response) => {
          console.log(response)
        }
      );
}

}
