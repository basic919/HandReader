import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {AuthResponse} from "../../models/auth-response";
import { HttpClient } from '@angular/common/http';
import {environment} from "../../../environments/environment";




@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.less']
})
export class RegisterComponent implements OnInit {
  registrationForm: FormGroup = new FormGroup({});

  registerUrl = environment.apiUrl + "/user/register";


  constructor(private formBuilder: FormBuilder, private httpClient: HttpClient) { }

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    });
  }

  onSubmit() {
    // TODO: Handle registration logic here
    this.httpClient.post<AuthResponse>(this.registerUrl,
      {
      address: this.registrationForm.get("email")?.value,
      password: this.registrationForm.get("password")?.value
    }).subscribe((data)=>{
      //console.log(data);
    });

    // console.log(this.registrationForm.get("email")?.value)
    // console.log(this.registrationForm.get("password")?.value)
  }

}
