import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import {AuthResponse} from "../../models/auth-response";
import { Router } from '@angular/router';
import {AuthService} from "../../auth.service";



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup = new FormGroup({});

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private router: Router) { }

  ngOnInit(): void {

    this.authService.checkPermission().subscribe((data)=>{
      console.log(data.value)
      if(data.value){
        console.log(data.message);
        this.router.navigate(['/dashboard']);
      }
    });


    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }


  onSubmit() {
    // TODO: Handle login logic here
    this.authService.login(this.loginForm.get("email")?.value,
      this.loginForm.get("password")?.value).subscribe((data: AuthResponse)=>{
      console.log(data);
      if(data.value){
        console.log(data.message);
        this.router.navigate(['/dashboard']);
      }
    });
  }
}
