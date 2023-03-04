import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {environment} from "../../../environments/environment";
import { HttpClient } from '@angular/common/http';
import {AuthResponse} from "../../models/auth-response";



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup = new FormGroup({});

  loginUrl = environment.apiUrl + "/user/login";

  constructor(private formBuilder: FormBuilder, private httpClient: HttpClient) { }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }


  onSubmit() {
    // TODO: Handle login logic here
    this.httpClient.post<AuthResponse>(this.loginUrl, {
      address: this.loginForm.get("email")?.value,
      password: this.loginForm.get("password")?.value
    }).subscribe((data)=>{
      console.log(data);
    });
  }

}
