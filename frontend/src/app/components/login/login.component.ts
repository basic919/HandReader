import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {environment} from "../../../environments/environment";
import { HttpClient } from '@angular/common/http';
import {AuthResponse} from "../../models/auth-response";
import { Router } from '@angular/router';



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup = new FormGroup({});

  loginUrl = environment.apiUrl + "/user/login";
  permissionUrl = environment.apiUrl + "/user/permission";

  constructor(private formBuilder: FormBuilder, private httpClient: HttpClient, private router: Router) { }

  ngOnInit(): void {

    this.httpClient.get<AuthResponse>(this.permissionUrl, { withCredentials: true }).subscribe((data)=>{
      console.log(data.value)
      if(data.value){
        console.log(this.router.navigate(['/dashboard']));  // TODO: Woops ne radi!
      }
    });


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
    }).subscribe((data: AuthResponse)=>{
      if(data.value){
        console.log(this.router.navigate(['/dashboard']));
      }
    });
  }

}
